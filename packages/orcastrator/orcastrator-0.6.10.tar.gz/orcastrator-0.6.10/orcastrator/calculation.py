import logging
import shutil
import subprocess
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional, Self
from uuid import uuid4

from morca import OrcaOutput

# Get logger for this module
logger = logging.getLogger("orcastrator.calculation")


@dataclass
class Calculation:
    name: str
    parent_dir: Path

    # Geometry
    charge: int
    mult: int
    atoms: list[tuple[str, float, float, float]]

    # Level of theory
    keywords: str | list[str] | set[str]
    blocks: list[str] = field(default_factory=list)

    # Technical
    cpus: int = 1
    mem_per_cpu_gb: Optional[int] = None
    scratch_base_dir: Optional[Path] = None

    # Behaviour
    overwrite: bool = False
    keep_scratch: bool = False

    def __post_init__(self):
        """Ensure keywords and blocks are always lowercase."""
        logger.debug(f"Initializing calculation: {self.name} in {self.parent_dir}")

        # Handle different input types for keywords
        if isinstance(self.keywords, str):
            # Split space-separated string into individual keywords
            self.keywords = set(self.keywords.split())
        elif isinstance(self.keywords, list):
            # Convert list to set
            self.keywords = set(self.keywords)
        # If it's already a set, no conversion needed

        # Convert keywords to lowercase
        self.keywords = {kw.lower() for kw in self.keywords}
        logger.debug(f"Keywords: {self.keywords}")

        # Convert blocks to lowercase
        self.blocks = [block.lower() for block in self.blocks]
        logger.debug(f"Blocks: {self.blocks}")

    @property
    def directory(self) -> Path:
        return self.parent_dir / self.name

    @property
    def input_file(self) -> Path:
        return self.directory / f"{self.name}.inp"

    @property
    def output_file(self) -> Path:
        return self.input_file.with_suffix(".out")

    @property
    def xyz_file(self) -> Path:
        return self.input_file.with_suffix(".xyz")

    @property
    def data(self) -> OrcaOutput:
        return OrcaOutput(self.output_file)

    def set_atoms_from_xyz_file(self, xyz_file: Path) -> Self:
        logger.info(f"Reading geometry from XYZ file: {xyz_file}")
        lines = Path(xyz_file).read_text().splitlines()
        new_atoms = []
        for line in lines[2:]:
            symbol, x, y, z = line.split()
            new_atoms.append((symbol, float(x), float(y), float(z)))
        self.atoms = new_atoms
        logger.debug(f"Read {len(new_atoms)} atoms from XYZ file")
        return self

    def _format_geometry_input_string(self) -> str:
        """Formats the atoms into the ORCA * xyz block."""
        logger.debug(f"Formatting geometry input for {len(self.atoms)} atoms")
        atom_lines = [
            f" {s:4}    {x:>12.8f}    {y:>12.8f}    {z:>12.8f}"
            for s, x, y, z in self.atoms
        ]
        return f"* xyz {self.charge} {self.mult}\n" + "\n".join(atom_lines) + "\n*"

    def _generate_input_string(self) -> str:
        """Constructs the full ORCA input file content."""
        logger.debug(f"Generating input file content for {self.name}")

        # Start with keywords
        input_lines = [f"! {' '.join(sorted(self.keywords))}"]
        logger.debug(f"Keywords line: {input_lines[0]}")

        # Add resource blocks (don't permanently store them in self.blocks)
        temp_blocks = self.blocks.copy()
        if self.cpus > 1:
            cpu_block = f"%pal nprocs {self.cpus} end"
            temp_blocks.append(cpu_block)
            logger.debug(f"Added CPU block: {cpu_block}")

        if self.mem_per_cpu_gb:
            # ORCA uses total memory in MB per core for %maxcore
            total_mem_mb = self.mem_per_cpu_gb * 1000  # Approximate GB to MB
            mem_block = f"%maxcore {total_mem_mb}"
            temp_blocks.append(mem_block)
            logger.debug(f"Added memory block: {mem_block}")

        # Add other defined blocks
        input_lines.extend(temp_blocks)

        # Add geometry
        input_lines.append(self._format_geometry_input_string())

        return "\n".join(input_lines)  # ORCA often prefers lowercase

    def write_input_file(self) -> Path:
        """
        Generates and writes the ORCA input file, with restart logic:
        - If the directory exists and overwrite=False
            * If the existing .inp matches the newly generated one
            and the existing .out terminated normally → skip
            * Otherwise → remove old directory and re-run
        """
        logger.info(f"Preparing input for {self.name}")

        # Basic validation
        if not self.keywords:
            logger.error("Cannot write input file: No keywords defined")
            raise ValueError("Cannot write input file: No keywords defined.")
        if not self.atoms:
            logger.error("Cannot write input file: No atoms defined")
            raise ValueError("Cannot write input file: No atoms defined.")

        # Generate the new content (but don’t write it yet)
        new_input = self._generate_input_string()

        # Check for restart conditions
        if self.directory.exists() and not self.overwrite:
            old_inp = self.input_file
            old_out = self.output_file

            # 1) Does the old input exist and match?
            if old_inp.exists() and old_inp.read_text() == new_input:
                # 2) Does the old output exist and terminate normally?
                if old_out.exists():
                    out_txt = old_out.read_text()
                    if "****ORCA TERMINATED NORMALLY****" in out_txt:
                        logger.info(
                            f"Skipping '{self.name}' (already completed and input unchanged)"
                        )
                        self._skip_marker = True
                        return old_inp
                    else:
                        logger.info(
                            f"Previous run for '{self.name}' incomplete or failed → re-running"
                        )
                else:
                    logger.info(f"No existing output for '{self.name}' → re-running")
            else:
                logger.info(
                    f"Input changed or fresh run for '{self.name}' → re-running"
                )

            # Clean up old directory before a fresh run
            logger.debug(f"Removing existing directory for re-run: {self.directory}")
            shutil.rmtree(self.directory)

        # Either directory didn’t exist, or we deleted it, or overwrite=True
        logger.info(f"Writing input file for {self.name}")
        self.directory.mkdir(parents=True, exist_ok=True)
        self.input_file.write_text(new_input)
        logger.info(f"Input file written to {self.input_file}")

        return self.input_file

    def setup_directory(self) -> None:
        """Creates the source directory, handling overwrites."""
        logger.debug(f"Setting up directory: {self.directory}")
        if self.directory.exists():
            if self.overwrite:
                logger.warning(f"Removing existing directory: {self.directory}")
                shutil.rmtree(self.directory)
            else:
                logger.error(
                    f"Directory {self.directory} already exists and overwrite=False"
                )
                raise IsADirectoryError(
                    f"Directory {self.directory} already exists and overwrite=False"
                )
        self.directory.mkdir(parents=True)
        logger.debug(f"Directory created: {self.directory}")

    @contextmanager
    def _scratch_directory(self) -> Iterator[Path]:
        """
        Context manager for handling the scratch directory lifecycle.
        Creates a scratch directory, yields it, and cleans it up afterwards.
        """
        run_id = str(uuid4())[:8]

        # Check if global scratch exists
        if self.scratch_base_dir:
            base_dir = self.scratch_base_dir
        elif Path("/scratch").exists():
            base_dir = Path("/scratch")
        else:
            base_dir = Path("/tmp")
        scratch_run_dir = (base_dir / f"{self.name}_{run_id}").resolve()

        logger.info(f"Using scratch directory: {scratch_run_dir}")

        try:
            # Setup scratch directory
            if scratch_run_dir.exists():
                logger.warning(
                    f"Removing existing scratch directory: {scratch_run_dir}"
                )
                shutil.rmtree(scratch_run_dir)

            scratch_run_dir.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created scratch directory: {scratch_run_dir}")

            # Copy input file to scratch
            shutil.copy(self.input_file, scratch_run_dir)
            logger.debug(f"Copied input file to scratch: {self.input_file}")

            # Yield the scratch directory for use in the run method
            yield scratch_run_dir

        finally:
            # Clean up scratch directory
            if not self.keep_scratch and scratch_run_dir.exists():
                try:
                    logger.debug(f"Cleaning up scratch directory: {scratch_run_dir}")
                    shutil.rmtree(scratch_run_dir)
                except OSError as e:
                    logger.error(f"Error removing scratch directory: {e}")
                    print(e)

    def run(self) -> bool:
        logger.info(f"Running calculation: {self.name}")
        start_time = time.time()  # Start timing

        orca_bin = shutil.which("orca")
        if orca_bin is None:
            logger.error("ORCA executable not found in PATH")
            raise RuntimeError("ORCA executable not found")
        orca_bin = Path(orca_bin).resolve()
        logger.debug(f"Using ORCA executable: {orca_bin}")

        self.write_input_file()

        if self._skip_marker:
            logger.info(
                f"Calculation {self.name} skipped (elapsed time: {time.time() - start_time:.1f} seconds)"
            )
            return True

        with self._scratch_directory() as scratch_dir:
            cmd = [str(orca_bin), self.input_file.name]  # Run relative to scratch dir
            logger.debug(f"Command: {cmd}")
            logger.debug(f"Working directory: {scratch_dir}")

            logger.info(f"Starting ORCA calculation for {self.name}")
            result = subprocess.run(
                cmd,
                cwd=scratch_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,  # Don't raise exception on non-zero exit code
            )

            logger.debug(
                f"ORCA process completed with return code: {result.returncode}"
            )

            # Save output
            self.output_file.write_text(result.stdout)
            logger.info(f"Output written to {self.output_file}")

            # Copy files back from scratch to result directory
            logger.debug("Copying files from scratch to result directory")
            shutil.copytree(
                scratch_dir,
                self.directory,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("*.tmp", "*.tmp.*"),
            )

        # Check if the calculation terminated normally
        output_text = self.output_file.read_text()
        is_normal = "****ORCA TERMINATED NORMALLY****" in output_text

        elapsed_time = time.time() - start_time  # Calculate elapsed time

        if is_normal:
            logger.info(
                f"Calculation {self.name} terminated normally (elapsed time: {elapsed_time:.1f} seconds)"
            )
        else:
            logger.error(
                f"Calculation {self.name} did not terminate normally (elapsed time: {elapsed_time:.2f} seconds)"
            )
            # Extract error message if present
            if "ERROR MESSAGE" in output_text:
                for line in output_text.splitlines():
                    if "ERROR MESSAGE" in line:
                        logger.error(f"ORCA ERROR: {line}")

        return is_normal

    def set_keywords(self, kws: list[str] | set[str]) -> Self:
        logger.debug(f"Setting keywords: {kws}")
        self.keywords = set(kws)
        return self

    def add_keyword(self, kw: str) -> Self:
        logger.debug(f"Adding keyword: {kw}")
        self.keywords = set(self.keywords)
        self.keywords.add(kw.lower())
        return self

    def add_block(self, block: str) -> Self:
        logger.debug(f"Adding block: {block}")
        self.blocks.append(block.lower())
        return self

    def remove_keyword(self, kw: str) -> Self:
        logger.debug(f"Removing keyword: {kw}")
        self.keywords = set(self.keywords)
        self.keywords.remove(kw.lower())
        return self

    def remove_block(self, block_kw: str) -> Self:
        logger.debug(f"Removing blocks starting with: {block_kw}")
        self.blocks = [b for b in self.blocks if not b.startswith(block_kw.lower())]
        return self

    def set_blocks(self, blocks: list[str]) -> Self:
        logger.debug(f"Setting blocks from: {self.blocks} to {blocks}")
        self.blocks = blocks
        return self

    def create_follow_up(
        self,
        name: str,
        set_all_keywords: Optional[list[str] | set[str]] = None,
        additional_keywords: Optional[list[str] | set[str]] = None,
        remove_keywords: Optional[list[str] | set[str]] = None,
        set_blocks: Optional[list[str]] = None,
        new_charge: Optional[int] = None,
        new_mult: Optional[int] = None,
    ) -> "Calculation":
        """
        Create a follow-up calculation.
        Uses optimized geometry from this one if available, otherwise original.
        Allows overriding keywords, blocks, charge, and multiplicity.
        """
        logger.info(f"Creating follow-up calculation: {name} from {self.name}")

        if not self.output_file.exists() and not self.xyz_file.exists():
            logger.warning(
                f"Neither output file ({self.output_file}) nor explicit XYZ ({self.xyz_file}) found for parent {self.name}. "
                f"Follow-up {name} will use parent's initial geometry if available, or fail if atoms not set."
            )

        # Determine charge and multiplicity for the new calculation
        charge_for_new = new_charge if new_charge is not None else self.charge
        mult_for_new = new_mult if new_mult is not None else self.mult

        new_calc = Calculation(
            name=name,
            parent_dir=self.parent_dir,  # Follow-up calc in the same parent molecule directory
            charge=charge_for_new,
            mult=mult_for_new,
            atoms=self.atoms.copy(),  # Start with parent's atoms (might be updated from XYZ)
            keywords=set(self.keywords).copy()
            if set_all_keywords is None
            else set(),  # Start with parent's kws or empty
            blocks=self.blocks.copy()
            if set_blocks is None
            else [],  # Start with parent's blocks or empty
            cpus=self.cpus,
            mem_per_cpu_gb=self.mem_per_cpu_gb,
            scratch_base_dir=self.scratch_base_dir,
            overwrite=self.overwrite,
            keep_scratch=self.keep_scratch,
        )
        logger.debug(
            f"Created base follow-up calculation '{name}' with charge={charge_for_new}, mult={mult_for_new}"
        )

        # Try to use optimized geometry if available from parent's .xyz file
        # This .xyz file is typically created by ORCA after an optimization.
        if self.xyz_file.exists():
            try:
                logger.debug(
                    f"Attempting to use optimized geometry from {self.xyz_file} for {name}"
                )
                new_calc.set_atoms_from_xyz_file(self.xyz_file)
            except (
                FileNotFoundError
            ):  # Should not happen due to exists() check, but good practice
                logger.warning(
                    f"Optimized geometry file {self.xyz_file} disappeared, using parent's original geometry for {name}"
                )
            except ValueError as e:  # Handles parsing errors
                logger.warning(
                    f"Error parsing optimized geometry from {self.xyz_file} for {name}: {e}. Using parent's original geometry."
                )
        else:
            logger.info(
                f"No specific .xyz output file ({self.xyz_file}) found for parent {self.name}. "
                f"Follow-up {name} will use parent's current atom list."
            )
            if (
                not new_calc.atoms
            ):  # If parent also had no atoms (e.g. error in its setup)
                logger.error(
                    f"Parent calculation {self.name} has no atoms, and no XYZ file. Cannot create follow-up {name}."
                )
                raise ValueError(
                    f"Cannot create follow-up {name}: Parent {self.name} has no geometry."
                )

        # Apply keyword/block modifications
        if set_all_keywords is not None:
            logger.debug(
                f"Setting all keywords in follow-up '{name}': {set_all_keywords}"
            )
            new_calc.set_keywords(set_all_keywords)

        if additional_keywords:
            for kw in additional_keywords:
                logger.debug(f"Adding keyword to follow-up '{name}': {kw}")
                new_calc.add_keyword(kw)

        if remove_keywords:
            for kw in remove_keywords:
                logger.debug(f"Removing keyword from follow-up '{name}': {kw}")
                new_calc.remove_keyword(kw)

        if set_blocks is not None:
            logger.debug(f"Setting all blocks in follow-up '{name}': {set_blocks}")
            new_calc.set_blocks(set_blocks)

        # Re-run post_init to ensure keywords/blocks are correctly formatted (e.g. lowercase)
        # This is now handled by set_keywords and set_blocks.
        # new_calc.__post_init__()

        return new_calc
