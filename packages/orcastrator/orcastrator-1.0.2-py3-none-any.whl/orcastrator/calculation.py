import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional, Tuple
from uuid import uuid4

from orcastrator.logger import debug, error, info, warning
from orcastrator.molecule import Molecule
from orcastrator.runner import OrcaRunner
from orcastrator.stats import Timer


class OrcaCalculation:
    def __init__(
        self,
        directory: Path,
        molecule: Molecule,
        keywords: list[str],
        scratch_dir: Path = Path("/scratch"),
        blocks: list[str] = [],
        overwrite: bool = False,
        cpus: int = 1,
        mem_per_cpu_gb: int = 1,
    ) -> None:
        self.directory = directory
        self.scratch_dir = scratch_dir
        self.molecule = molecule
        self.keywords = keywords
        self.blocks = blocks
        self.overwrite = overwrite
        self.cpus = cpus
        self.mem_per_cpu_gb = mem_per_cpu_gb

        # Log initialization
        debug(
            f"Initialized calculation in {directory} with {cpus} CPUs and {mem_per_cpu_gb}GB per CPU"
        )
        debug(f"Keywords: {', '.join(keywords)}")
        debug(
            f"Molecule: {molecule.name} (charge={molecule.charge}, mult={molecule.mult})"
        )

    @property
    def input_file(self) -> Path:
        return self.directory / (self.directory.name + ".inp")

    @property
    def output_file(self) -> Path:
        return self.input_file.with_suffix(".out")

    def build_input_string(self) -> str:
        # Consistently format keywords for reliable matching between runs
        keywords = f"! {' '.join(sorted(self.keywords))}"
        debug(f"Building input with keywords: {keywords}")

        temp_blocks = self.blocks.copy()
        if self.cpus > 1:
            cpu_block = f"%pal nprocs {self.cpus} end"
            temp_blocks.append(cpu_block)
            debug(f"Added CPU parallel block: {cpu_block}")

        if self.mem_per_cpu_gb:
            # ORCA uses total memory in MB per core for %maxcore
            total_mem_mb = self.mem_per_cpu_gb * 1024
            mem_block = f"%maxcore {total_mem_mb}"
            temp_blocks.append(mem_block)
            debug(f"Added memory block: {mem_block}")

        blocks = "\n".join(temp_blocks)
        debug(f"Final blocks configuration: {len(temp_blocks)} blocks")

        molecule = self.molecule.to_orca()
        debug("Molecule format prepared for ORCA")
        return "\n".join([keywords, blocks, molecule])

    @contextmanager
    def create_scratch_dir(self) -> Iterator[Path]:
        debug(f"Creating scratch directory in {self.scratch_dir}")
        if not self.scratch_dir.exists():
            error(f"Scratch directory {self.scratch_dir.resolve()} does not exist")
            raise NotADirectoryError(
                f"Specified scratch directory {self.scratch_dir.resolve()} does not exist"
            )

        run_uuid = str(uuid4())[:8]
        scratch_dir = self.scratch_dir / f"{self.directory.name}_{run_uuid}"
        debug(f"Generated scratch directory: {scratch_dir}")

        try:
            debug(f"Copying files from {self.directory} to scratch")
            shutil.copytree(self.directory, scratch_dir)
            debug("Scratch directory setup complete")
            yield scratch_dir
        except Exception:
            error("Error setting up scratch directory", exc_info=True)
            raise
        finally:
            if scratch_dir.exists():
                debug(
                    f"Copying results back from scratch directory to {self.directory}"
                )
                shutil.copytree(
                    scratch_dir,
                    self.directory,
                    ignore=shutil.ignore_patterns("*.tmp", "*.tmp.*"),
                    dirs_exist_ok=True,
                )
                debug(f"Removing scratch directory {scratch_dir}")
                shutil.rmtree(scratch_dir)

    def completed_normally(self) -> bool:
        debug("Checking if calculation completed normally")
        if not self.output_file.exists():
            warning(f"Output file {self.output_file} does not exist")
            return False

        output = self.output_file.read_text()
        debug(f"Read output file, size: {len(output)} bytes")

        if "opt" in [kw.lower() for kw in self.keywords]:
            debug("Checking optimization convergence")
            convergence_phrases = [
                "THE OPTIMIZATION HAS CONVERGED",
                "OPTIMIZATION RUN DONE",
                "OPTIMIZATION CONVERGED",
                "HURRAY",
            ]
            if not any(phrase in output for phrase in convergence_phrases):
                warning(f"Optimization did not converge in {self.directory}")
                return False
            else:
                debug("Optimization converged successfully")

        if "****ORCA TERMINATED NORMALLY****" not in output:
            warning("ORCA did not terminate normally")
            debug("Missing 'ORCA TERMINATED NORMALLY' message in output")

            # Get last few lines of output for debugging
            last_lines = "\n".join(output.splitlines()[-20:])
            debug(f"Last lines of output:\n{last_lines}")
            return False

        debug("ORCA terminated normally")
        return True

    def run(self) -> Tuple[bool, float]:
        """Run the calculation and return success status and elapsed time."""
        info(f"Starting ORCA calculation for {self.molecule.name} in {self.directory}")
        debug(f"Calculation parameters: {self.cpus} CPUs, {self.mem_per_cpu_gb}GB per CPU")
        
        # Create timer to measure calculation time
        timer = Timer(f"Calculation {self.directory.name}")
        
        # Start timer and perform calculation
        with timer:
            # Check if we can skip calculation due to previous successful run
            if self.directory.exists() and not self.overwrite:
                info(f"Previous calculation directory detected: {self.directory}")
    
                # Check 1: Does input file exist and match what we would generate?
                input_match = False
                new_input = self.build_input_string()
    
                if self.input_file.exists():
                    old_input = self.input_file.read_text()
                    if old_input == new_input:
                        debug("Calculation inputs match")
                        input_match = True
                    else:
                        debug("Calculation inputs do not match - will recalculate")
                        debug(
                            f"Old input hash: {hash(old_input)}, new input hash: {hash(new_input)}"
                        )
                else:
                    debug("No previous input file found")
    
                # Check 2: Did the previous calculation complete successfully?
                if input_match and self.completed_normally():
                    info(
                        f"Skipping calculation - previous run in {self.directory} completed successfully with same input"
                    )
                    return True, timer.elapsed_time
                elif input_match:
                    debug(
                        "Input matches but previous calculation did not complete normally - will recalculate"
                    )
    
            # Need to (re)run the calculation
            try:
                orca = OrcaRunner()
                debug(f"Initialized ORCA runner: {orca.orca_executable}")
    
                input = self.build_input_string()
                debug(f"Writing input file to {self.input_file}")
                self.directory.mkdir(exist_ok=True, parents=True)
                self.input_file.write_text(input)
    
                info(f"Running ORCA calculation in directory: {self.directory}")
                with self.create_scratch_dir() as scratch_dir:
                    scratch_input = scratch_dir / self.input_file.name
                    debug(f"Using scratch input file: {scratch_input}")
                    result = orca.run(
                        input_file=scratch_input,
                        output_file=self.output_file,
                    )
                    debug(f"ORCA process completed with return code: {result.returncode}")
                    if result.returncode != 0:
                        warning(
                            f"ORCA process returned non-zero exit code: {result.returncode}"
                        )
                        debug(f"ORCA stderr: {result.stderr}")
            except Exception:
                error("Error during calculation execution", exc_info=True)
                return False, timer.elapsed_time
    
            success = self.completed_normally()
            if success:
                info(f"Calculation completed successfully: {self.directory} (took {timer.elapsed_time:.2f}s)")
            else:
                warning(f"Calculation did not complete normally: {self.directory} (took {timer.elapsed_time:.2f}s)")
                if self.output_file.exists():
                    # Get the last few lines of output for easier debugging
                    try:
                        with open(self.output_file, "r") as f:
                            last_lines = "".join(f.readlines()[-10:])
                        debug(f"Last lines of failed calculation:\n{last_lines}")
                    except Exception as e:
                        debug(f"Could not read last lines of output file: {e}")

        return success, timer.elapsed_time

    def chain(
        self,
        directory: Path,
        keywords: list[str],
        blocks: list[str] = [],
        charge: Optional[int] = None,
        mult: Optional[int] = None,
    ) -> "OrcaCalculation":
        info(f"Chaining new calculation from {self.directory} to {directory}")
        debug(f"Chain parameters: keywords={keywords}, blocks={blocks}")

        if charge is None:
            charge = self.molecule.charge
        if mult is None:
            mult = self.molecule.mult

        debug(f"Using charge={charge}, mult={mult} for chained calculation")

        xyz_file = self.output_file.with_suffix(".xyz")
        debug(f"Loading molecule from {xyz_file}")
        if xyz_file.exists():
            molecule = Molecule.from_xyz_file(
                xyz_file=xyz_file, charge=charge, mult=mult
            )
            debug("Successfully loaded molecule from previous calculation output")
        else:
            # Some calculations don't generate this xyz file
            # In that case, the self.molecule is already the optimized geometry, right?
            debug(
                f"File {xyz_file} does not exist - reusing the inital coordinates from previous calculation"
            )
            molecule = Molecule(charge, mult, self.molecule.xyz)

        debug(
            f"Creating new calculation with same resources: {self.cpus} CPUs, {self.mem_per_cpu_gb}GB per CPU"
        )
        new_calculation = OrcaCalculation(
            directory=directory,
            scratch_dir=self.scratch_dir,
            molecule=molecule,
            keywords=keywords,
            blocks=blocks,
            overwrite=self.overwrite,
            cpus=self.cpus,
            mem_per_cpu_gb=self.mem_per_cpu_gb,
        )
        return new_calculation