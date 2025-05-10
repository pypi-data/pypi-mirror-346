import csv
import logging
import os
import shlex
import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

from dayhoff_tools.fasta import subset_fasta

logger = logging.getLogger(__name__)


class Processor(ABC):
    """Processes data locally.  Abstract class for specific calculations.
    Takes in a single file and produces a single file or folder of outputs."""

    @abstractmethod
    def run(self, input_file: str) -> str:
        """Do the calculation, including reading from input_file
        and writing to output_file"""
        output_path = "output_file"

        return output_path


class BoltzPredictor(Processor):
    """Processor for running Boltz docking predictions.

    This class wraps the Boltz docking tool to predict protein structures
    from sequence data.
    """

    def __init__(self, num_workers: int, boltz_options: str | None = None):
        """Initialize the BoltzPredictor.

        Args:
            num_workers: Number of worker threads to use as a default.
                         This can be overridden if --num_workers is present
                         in boltz_options.
            boltz_options: A string containing additional command-line options
                           to pass to the Boltz predictor. Options should be
                           space-separated (e.g., "--option1 value1 --option2").
        """
        self.num_workers = num_workers
        self.boltz_options = boltz_options

    def run(self, input_file: str) -> str:
        """Run Boltz prediction on the input file.

        Constructs the command using the input file, default number of workers,
        and any additional options provided via `boltz_options`. If `--num_workers`
        is specified in `boltz_options`, it overrides the default `num_workers`.

        Args:
            input_file: Path to the input file containing sequences

        Returns:
            Path to the output directory created by Boltz

        Raises:
            subprocess.CalledProcessError: If Boltz prediction fails
        """
        # Determine expected output directory name
        input_base = os.path.splitext(os.path.basename(input_file))[0]
        expected_output_dir = f"boltz_results_{input_base}"
        logger.info(f"Expected output directory: {expected_output_dir}")

        # Start building the command
        cmd = ["boltz", "predict", input_file]

        # Parse additional options if provided
        additional_args = []
        num_workers_in_opts = False
        if self.boltz_options:
            try:
                parsed_opts = shlex.split(self.boltz_options)
                additional_args.extend(parsed_opts)
                if "--num_workers" in parsed_opts:
                    num_workers_in_opts = True
                    logger.info(
                        f"Using --num_workers from BOLTZ_OPTIONS: {self.boltz_options}"
                    )
            except ValueError as e:
                logger.error(f"Error parsing BOLTZ_OPTIONS '{self.boltz_options}': {e}")
                # Decide if we should raise an error or proceed without options
                # For now, proceed without the additional options
                additional_args = []  # Clear potentially partially parsed args

        # Add num_workers if not specified in options
        if not num_workers_in_opts:
            logger.info(f"Using default num_workers: {self.num_workers}")
            cmd.extend(["--num_workers", str(self.num_workers)])

        # Add the parsed additional arguments
        cmd.extend(additional_args)

        # Log the final command
        # Use shlex.join for safer command logging, especially if paths/args have spaces
        try:
            safe_cmd_str = shlex.join(cmd)
            logger.info(f"Running command: {safe_cmd_str}")
        except AttributeError:  # shlex.join is Python 3.8+
            logger.info(f"Running command: {' '.join(cmd)}")

        # Stream output in real-time
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        stdout = process.stdout
        if stdout:
            for line in iter(stdout.readline, ""):
                logger.info(f"BOLTZ: {line.rstrip()}")

        # Wait for process to complete
        return_code = process.wait()
        if return_code != 0:
            logger.error(f"Boltz prediction failed with exit code {return_code}")
            raise subprocess.CalledProcessError(return_code, cmd)

        logger.info(
            f"Boltz prediction completed successfully. Output in {expected_output_dir}"
        )
        return expected_output_dir


class MMSeqsProfileProcessor(Processor):
    """Processor for running MMseqs2 profile searches.

    This class wraps the MMseqs2 workflow to perform a profile-based search
    against a target database using a query FASTA.
    """

    def __init__(
        self,
        query_fasta_path_in_image: str,
        num_threads: int = 8,
        mmseqs_args: dict | None = None,
    ):
        """Initialize the MMSeqsProfileProcessor.

        Args:
            query_fasta_path_in_image: Path to the query FASTA file. This path is expected
                                       to be accessible within the execution environment (e.g.,
                                       packaged in a Docker image).
            num_threads: Number of threads to use for MMseqs2 commands.
            mmseqs_args: A dictionary of additional MMseqs2 parameters.
                         Expected keys: "memory_limit_gb", "evalue", "sensitivity",
                         "max_seqs_search", "min_seq_id_cluster", "max_seqs_profile_msa".
                         Defaults are used if not provided.
        """
        if not Path(query_fasta_path_in_image).is_file():
            raise FileNotFoundError(
                f"Query FASTA file not found at: {query_fasta_path_in_image}"
            )
        self.query_fasta_path = query_fasta_path_in_image
        self.num_threads = str(num_threads)  # MMseqs2 expects string for threads

        default_mmseqs_args = {
            "memory_limit_gb": "25",
            "evalue": "10",
            "sensitivity": "7.5",
            "max_seqs_search": "300",
            "min_seq_id_cluster": "0.8",
            "max_seqs_profile_msa": "1000",
        }
        if mmseqs_args:
            self.mmseqs_args = {**default_mmseqs_args, **mmseqs_args}
        else:
            self.mmseqs_args = default_mmseqs_args

        # Log dayhoff-tools version
        from dayhoff_tools import __version__

        logger.info(f"dayhoff-tools version: {__version__}")
        logger.info(
            f"MMSeqsProfileProcessor initialized with query: {self.query_fasta_path}"
        )
        logger.info(f"MMSeqs args: {self.mmseqs_args}")
        logger.info(f"Num threads: {self.num_threads}")

    def _run_mmseqs_command(
        self, command_parts: list[str], step_description: str, work_dir: Path
    ):
        """Runs an MMseqs2 command and logs its execution.

        Args:
            command_parts: A list of strings representing the command and its arguments.
            step_description: A human-readable description of the MMseqs2 step.
            work_dir: The working directory for the command.

        Raises:
            subprocess.CalledProcessError: If the MMseqs2 command returns a non-zero exit code.
        """
        full_command = " ".join(command_parts)
        logger.info(f"Running MMseqs2 step in {work_dir}: {step_description}")
        logger.info(f"Command: {full_command}")
        try:
            process = subprocess.run(
                command_parts,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=work_dir,  # Run command in the specified working directory
            )
            if process.stdout:
                logger.info(f"MMseqs2 stdout: {process.stdout.strip()}")
            if process.stderr:  # MMseqs often outputs informational messages to stderr
                logger.info(f"MMseqs2 stderr: {process.stderr.strip()}")
            logger.info(f"MMseqs2 step '{step_description}' completed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"MMseqs2 step '{step_description}' failed in {work_dir}.")
            if e.stdout:
                logger.error(f"MMseqs2 stdout: {e.stdout.strip()}")
            if e.stderr:
                logger.error(f"MMseqs2 stderr: {e.stderr.strip()}")
            raise

    def run(self, input_file: str) -> str:
        """Run MMseqs2 profile search.

        The input_file is the target FASTA. The query FASTA is provided
        during initialization.
        The method creates an output directory (e.g., {target_stem})
        which contains the result files, now named meaningfully using the target stem
        (e.g., {target_stem}_results.m8 and {target_stem}_hits.fasta).

        Args:
            input_file: Path to the input target FASTA file.

        Returns:
            Path to the output directory (e.g., {target_stem}) containing
            the meaningfully named result files.

        Raises:
            subprocess.CalledProcessError: If any MMseqs2 command fails.
            FileNotFoundError: If the input_file is not found.
        """
        if not Path(input_file).is_file():
            raise FileNotFoundError(f"Input target FASTA file not found: {input_file}")

        input_file_path = Path(input_file).resolve()  # Ensure absolute path
        target_fasta_filename = input_file_path.name
        target_fasta_stem = input_file_path.stem  # Get stem for naming

        # Create a unique base directory for this run's outputs and temp files
        # This directory will be returned and subsequently uploaded by the Operator
        run_base_dir_name = f"{target_fasta_stem}"  # Use stem as the dir name
        run_base_dir = Path(run_base_dir_name).resolve()
        run_base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created run base directory: {run_base_dir}")

        # Define local paths within the run_base_dir
        local_target_file = run_base_dir / target_fasta_filename
        # Copy the target file into the run directory to keep inputs and outputs together
        shutil.copy(input_file_path, local_target_file)
        logger.info(f"Copied target file {input_file_path} to {local_target_file}")

        # Query file is already specified by self.query_fasta_path (path in image)
        local_query_file = Path(self.query_fasta_path).resolve()

        # Temporary directory for MMseqs2 intermediate files, created inside run_base_dir
        mmseqs_temp_dir = run_base_dir / "mmseqs_tmp"
        mmseqs_temp_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created MMseqs2 temporary directory: {mmseqs_temp_dir}")

        # Define INTERMEDIATE output file paths within mmseqs_temp_dir
        intermediate_results_m8_file = mmseqs_temp_dir / "results.m8"
        intermediate_hits_fasta_file = mmseqs_temp_dir / "results.fasta"
        intermediate_results_as_csv_file = mmseqs_temp_dir / "results_as.csv"

        # Define FINAL output file paths within run_base_dir, using target stem
        final_results_csv_file = run_base_dir / f"{target_fasta_stem}.csv"
        final_hits_fasta_file = run_base_dir / f"{target_fasta_stem}.fasta"
        final_hits_txt_file = run_base_dir / f"{target_fasta_stem}.txt"

        # --- MMseqs2 Workflow Paths (intermediate files in mmseqs_temp_dir) ---
        query_db = mmseqs_temp_dir / "queryDB"
        target_db = mmseqs_temp_dir / "targetDB"
        # Ensure local_target_file is used for creating targetDB
        target_db_input_file = local_target_file

        query_db_cluster = mmseqs_temp_dir / "queryDB_cluster"
        query_db_rep = mmseqs_temp_dir / "queryDB_rep"
        aln_db = mmseqs_temp_dir / "alnDB"
        profile_db = mmseqs_temp_dir / "profileDB"
        result_db = mmseqs_temp_dir / "resultDB"

        try:
            # 1. Create query database
            self._run_mmseqs_command(
                ["mmseqs", "createdb", str(local_query_file), str(query_db)],
                "Create query DB",
                run_base_dir,  # Working directory for the command
            )

            # 2. Create target database
            self._run_mmseqs_command(
                ["mmseqs", "createdb", str(target_db_input_file), str(target_db)],
                "Create target DB",
                run_base_dir,
            )

            # 3. Cluster query sequences
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "cluster",
                    str(query_db),
                    str(query_db_cluster),
                    str(
                        mmseqs_temp_dir / "tmp_cluster"
                    ),  # MMseqs needs a temp dir for cluster
                    "--min-seq-id",
                    self.mmseqs_args["min_seq_id_cluster"],
                    "--threads",
                    self.num_threads,
                ],
                "Cluster query sequences",
                run_base_dir,
            )

            # 4. Create representative set from query clusters
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "createsubdb",
                    str(query_db_cluster),
                    str(query_db),
                    str(query_db_rep),
                ],
                "Create representative query set",
                run_base_dir,
            )

            # 5. Create MSA for profile generation
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "search",
                    str(query_db_rep),
                    str(query_db),  # Search representative against full query DB
                    str(aln_db),
                    str(mmseqs_temp_dir / "tmp_search_msa"),  # Temp for this search
                    "--max-seqs",
                    self.mmseqs_args["max_seqs_profile_msa"],
                    "--threads",
                    self.num_threads,
                ],
                "Create MSA for profile",
                run_base_dir,
            )

            # 6. Create profile database
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "result2profile",
                    str(query_db_rep),  # Use query_db_rep as input for profile
                    str(query_db),  # Full query DB as second arg
                    str(aln_db),
                    str(profile_db),
                    "--threads",  # Added threads option
                    self.num_threads,
                ],
                "Create profile DB",
                run_base_dir,
            )

            # 7. Perform profile search
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "search",
                    str(profile_db),
                    str(target_db),
                    str(result_db),
                    str(mmseqs_temp_dir / "tmp_search_profile"),  # Temp for this search
                    "--split-memory-limit",
                    f"{self.mmseqs_args['memory_limit_gb']}G",
                    "-e",
                    self.mmseqs_args["evalue"],
                    "--max-seqs",
                    self.mmseqs_args["max_seqs_search"],
                    "--threads",
                    self.num_threads,
                    "-s",
                    self.mmseqs_args["sensitivity"],
                ],
                "Perform profile search",
                run_base_dir,
            )

            # 8. Convert results to tabular format (M8) -> to intermediate file
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "convertalis",
                    str(profile_db),  # Query DB used for search (profileDB)
                    str(target_db),
                    str(result_db),
                    str(intermediate_results_m8_file),  # Output M8 file to temp dir
                    "--threads",
                    self.num_threads,
                ],
                "Convert results to M8",
                run_base_dir,
            )

            # 8.5 Convert M8 to CSV with headers
            logger.info(
                f"Converting M8 results {intermediate_results_m8_file} to CSV {intermediate_results_as_csv_file}"
            )
            csv_headers = [
                "query_id",
                "target_id",
                "percent_identity",
                "alignment_length",
                "mismatches",
                "gap_openings",
                "query_start",
                "query_end",
                "target_start",
                "target_end",
                "e_value",
                "bit_score",
            ]
            try:
                if intermediate_results_m8_file.exists():
                    with open(intermediate_results_m8_file, "r") as m8_in, open(
                        intermediate_results_as_csv_file, "w", newline=""
                    ) as csv_out:
                        writer = csv.writer(csv_out)
                        writer.writerow(csv_headers)
                        for line in m8_in:
                            if line.strip():  # Ensure line is not empty
                                columns = line.strip().split("\t")
                                writer.writerow(columns)
                    logger.info(
                        f"Successfully converted M8 to CSV: {intermediate_results_as_csv_file}"
                    )
                else:
                    logger.warning(
                        f"Intermediate M8 file {intermediate_results_m8_file} not found for CSV conversion. CSV will be empty or not created."
                    )
                    # Ensure the CSV file is touched if M8 was missing, so downstream move doesn't fail
                    intermediate_results_as_csv_file.touch()
            except Exception as e:
                logger.error(f"Failed to convert M8 to CSV: {e}")
                # Touch the CSV file in case of error to prevent downstream errors if it's expected
                if not intermediate_results_as_csv_file.exists():
                    intermediate_results_as_csv_file.touch()
                # We might still want to raise e here, depending on desired error handling for CSV conversion failure

            # 9. Extract hit sequences from M8 results using subset_fasta
            logger.info(
                f"PROCESSOR: Parsing M8 results from: {intermediate_results_m8_file}"
            )
            hit_sequence_ids = set()
            try:
                if not intermediate_results_m8_file.exists():
                    logger.warning(
                        f"PROCESSOR: M8 results file {intermediate_results_m8_file} not found. Hits FASTA will be empty.",
                        exc_info=True,
                    )
                    intermediate_hits_fasta_file.touch()  # Create empty hits file
                else:
                    with open(intermediate_results_m8_file, "r") as m8_file:
                        for line in m8_file:
                            if line.strip():
                                columns = line.strip().split("\t")
                                if len(columns) >= 2:
                                    hit_sequence_ids.add(columns[1])
                    logger.info(
                        f"PROCESSOR: Found {len(hit_sequence_ids)} unique target IDs in M8 results."
                    )

                    if not hit_sequence_ids:
                        logger.warning(
                            f"PROCESSOR: No target IDs found in {intermediate_results_m8_file} after parsing. Output hits FASTA will be empty.",
                            exc_info=True,
                        )
                        intermediate_hits_fasta_file.touch()
                    else:
                        logger.info(f"PROCESSOR: === CALLING subset_fasta ===")
                        logger.info(
                            f"PROCESSOR: Input FASTA for subset_fasta: {local_target_file}"
                        )
                        logger.info(
                            f"PROCESSOR: Output FASTA for subset_fasta: {intermediate_hits_fasta_file}"
                        )
                        logger.info(
                            f"PROCESSOR: Number of target IDs for subset_fasta: {len(hit_sequence_ids)}"
                        )
                        try:
                            subset_fasta(
                                fasta_file=str(local_target_file),
                                output_path=str(intermediate_hits_fasta_file),
                                target_ids=hit_sequence_ids,
                                exclude=False,
                                return_written_ids=False,
                            )
                            logger.info(
                                f"PROCESSOR: === RETURNED from subset_fasta ==="
                            )
                            logger.info(
                                f"PROCESSOR: Successfully created hits FASTA: {intermediate_hits_fasta_file} using subset_fasta."
                            )
                        # More specific error catching can be added if subset_fasta raises custom exceptions
                        except FileNotFoundError as e_fnf:
                            logger.error(
                                f"PROCESSOR: subset_fasta FileNotFoundError: {e_fnf}. Ensuring {intermediate_hits_fasta_file} exists as empty.",
                                exc_info=True,
                            )
                            if not intermediate_hits_fasta_file.exists():
                                intermediate_hits_fasta_file.touch()
                            raise
                        except (
                            Exception
                        ) as e_sub:  # Catch any other exception from subset_fasta
                            logger.error(
                                f"PROCESSOR: subset_fasta failed to create {intermediate_hits_fasta_file}: {e_sub}",
                                exc_info=True,
                            )
                            if not intermediate_hits_fasta_file.exists():
                                intermediate_hits_fasta_file.touch()
                            raise
            except Exception as e_m8_proc:
                logger.error(
                    f"PROCESSOR: Error processing M8 file {intermediate_results_m8_file} or its hits extraction: {e_m8_proc}",
                    exc_info=True,
                )
                if not intermediate_hits_fasta_file.exists():
                    intermediate_hits_fasta_file.touch()
                raise

            # 10. Write the set of hit sequence IDs to a .txt file
            logger.info(
                f"PROCESSOR: Writing {len(hit_sequence_ids)} hit sequence IDs to {final_hits_txt_file}"
            )
            try:
                with open(final_hits_txt_file, "w") as txt_out:
                    for seq_id in sorted(
                        list(hit_sequence_ids)
                    ):  # Sort for consistent output
                        txt_out.write(f"{seq_id}\n")
                logger.info(
                    f"PROCESSOR: Successfully wrote hit IDs to {final_hits_txt_file}"
                )
            except Exception as e:
                logger.error(f"Failed to write hit IDs to {final_hits_txt_file}: {e}")
                # The main workflow should still proceed even if this supplementary file fails

            logger.info(
                f"PROCESSOR: MMseqs2 workflow and FASTA/TXT generation completed successfully. Intermediate outputs in {mmseqs_temp_dir}"
            )

            # Move and rename final output files from mmseqs_temp_dir to run_base_dir
            if intermediate_results_as_csv_file.exists():
                shutil.move(
                    str(intermediate_results_as_csv_file), str(final_results_csv_file)
                )
                logger.info(
                    f"Moved and renamed M8 results to CSV: {final_results_csv_file}"
                )
            else:
                logger.warning(
                    f"Intermediate CSV file {intermediate_results_as_csv_file} not found. Creating empty target CSV file."
                )
                final_results_csv_file.touch()  # Create empty file in run_base_dir if not found

            if intermediate_hits_fasta_file.exists():
                shutil.move(
                    str(intermediate_hits_fasta_file), str(final_hits_fasta_file)
                )
                logger.info(f"Moved and renamed hits FASTA to {final_hits_fasta_file}")
            else:
                logger.warning(
                    f"Intermediate hits FASTA {intermediate_hits_fasta_file} not found. Creating empty target file."
                )
                final_hits_fasta_file.touch()  # Create empty file in run_base_dir if not found

        finally:
            # Clean up the MMseqs2 temporary directory (mmseqs_tmp) which contains intermediate DBs etc.
            if mmseqs_temp_dir.exists():
                shutil.rmtree(mmseqs_temp_dir)
                logger.info(
                    f"Cleaned up MMseqs2 temporary directory: {mmseqs_temp_dir}"
                )

            # Clean up the copied input file (local_target_file) from the run_base_dir
            # so it does not get uploaded with the results.
            if local_target_file.exists():
                try:
                    local_target_file.unlink()
                    logger.info(
                        f"Cleaned up copied input file from run directory: {local_target_file}"
                    )
                except OSError as e:
                    logger.error(
                        f"Error deleting copied input file {local_target_file}: {e}"
                    )

            # The run_base_dir (containing only the final, meaningfully named output files)
            # will be cleaned up by the Operator after its contents are uploaded.

        return str(
            run_base_dir
        )  # Return the path to the directory containing meaningfully named results
