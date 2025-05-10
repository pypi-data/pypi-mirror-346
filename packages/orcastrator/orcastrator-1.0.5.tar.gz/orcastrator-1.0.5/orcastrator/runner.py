import shutil
import subprocess
from pathlib import Path
from typing import Optional

from orcastrator.logger import debug, error, info, warning


class OrcaRunner:
    def __init__(self, orca_executable: Optional[Path] = None) -> None:
        debug("Initializing OrcaRunner")
        if orca_executable:
            debug(f"Using provided ORCA executable: {orca_executable}")
            self.orca_executable = Path(orca_executable).resolve()
            if not self.orca_executable.is_file():
                error(f"ORCA executable not found at {self.orca_executable}")
                raise FileNotFoundError(f"ORCA executable not found at {self.orca_executable}")
        else:
            debug("Searching for ORCA executable in PATH")
            found_path = shutil.which("orca")
            if found_path is None:
                error("ORCA executable not found in PATH")
                raise RuntimeError("ORCA executable not found in PATH. Please ensure it's installed and in your PATH, or specify its path.")
            self.orca_executable = Path(found_path).resolve()
            debug(f"Found ORCA executable: {self.orca_executable}")

    def run(self, input_file: Path, output_file: Path) -> subprocess.CompletedProcess:
        debug(f"Preparing to run ORCA on input file: {input_file}")
        working_dir = input_file.parent
        debug(f"Working directory: {working_dir}")

        if not working_dir.is_dir():
            error(f"Working directory not found: {working_dir}")
            raise FileNotFoundError(f"Working directory not found {working_dir}")

        if not input_file.is_file():
            error(f"Input file not found: {input_file}")
            raise FileNotFoundError(f"Input file not found {input_file}")

        if not input_file.parent == working_dir:
            error(f"Input file {input_file} is not in working directory {working_dir}")
            raise ValueError("Specified input file is not in the working directory")

        cmd = [
            str(self.orca_executable.resolve()),
            input_file.name,
        ]
        debug(f"Executing command: {' '.join(cmd)} > {output_file}")
        
        info(f"Starting ORCA process in {working_dir}")
        with open(output_file, 'w') as output_fd:
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                stdout=output_fd,
                stderr=subprocess.PIPE,
                text=True,
                check=False,  # We handle success/failure based on ORCA's output text
            )
        debug(f"ORCA process completed with return code: {result.returncode}")
        if result.returncode != 0:
            warning(f"ORCA process returned non-zero exit code: {result.returncode}")
            debug(f"ORCA stderr: {result.stderr}")
        else:
            debug("ORCA process completed with exit code 0")

        return result
