import logging
import os
import shlex
import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

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
            "memory_limit_gb": "30",
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

        Args:
            input_file: Path to the input target FASTA file.

        Returns:
            Path to the output directory containing results.m8 and results.fasta.

        Raises:
            subprocess.CalledProcessError: If any MMseqs2 command fails.
            FileNotFoundError: If the input_file is not found.
        """
        if not Path(input_file).is_file():
            raise FileNotFoundError(f"Input target FASTA file not found: {input_file}")

        input_file_path = Path(input_file).resolve()  # Ensure absolute path
        target_fasta_filename = input_file_path.name

        # Create a unique base directory for this run's outputs and temp files
        # This directory will be returned and subsequently uploaded by the Operator
        run_base_dir_name = f"mmseqs_run_{Path(target_fasta_filename).stem}"
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

        # Define output file paths directly within run_base_dir
        local_results_m8_file = run_base_dir / "results.m8"
        local_hits_fasta_file = run_base_dir / "results.fasta"

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
        hits_db = mmseqs_temp_dir / "hitsDB"

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

            # 8. Convert results to tabular format (M8)
            self._run_mmseqs_command(
                [
                    "mmseqs",
                    "convertalis",
                    str(profile_db),  # Query DB used for search (profileDB)
                    str(target_db),
                    str(result_db),
                    str(local_results_m8_file),  # Output M8 file
                    "--threads",
                    self.num_threads,
                ],
                "Convert results to M8",
                run_base_dir,
            )

            # 9. Create subdatabase of hits from original target_db
            self._run_mmseqs_command(
                ["mmseqs", "createsubdb", str(result_db), str(target_db), str(hits_db)],
                "Create hits subDB from target_db",
                run_base_dir,
            )

            # 10. Convert hit sequences to FASTA
            self._run_mmseqs_command(
                ["mmseqs", "convert2fasta", str(hits_db), str(local_hits_fasta_file)],
                "Convert hits to FASTA",
                run_base_dir,
            )

            logger.info(
                f"MMseqs2 workflow completed successfully. Outputs in {run_base_dir}"
            )

        finally:
            # Clean up the MMseqs2 temporary directory
            if mmseqs_temp_dir.exists():
                shutil.rmtree(mmseqs_temp_dir)
                logger.info(
                    f"Cleaned up MMseqs2 temporary directory: {mmseqs_temp_dir}"
                )
            # The input_file (original target) is managed by the Operator
            # The local_target_file (copy inside run_base_dir) will be cleaned up
            # by the Operator when run_base_dir is deleted after upload.

        return str(run_base_dir)  # Return the path to the directory containing results
