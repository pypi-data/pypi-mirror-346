from pathlib import Path

from orcastrator.logger import debug, error, info
from orcastrator.molecule import Molecule
from orcastrator.runner_logic.molecule_runner import (
    process_molecules_parallel,
    process_molecules_sequential,
)
from orcastrator.stats import PipelineStats, Timer


class PipelineRunner:
    """Runs a complete molecular calculation pipeline."""

    def __init__(self, config: dict):
        """Initialize the pipeline runner with a configuration.

        Args:
            config: Dictionary containing pipeline configuration
        """
        info("Initializing pipeline runner")
        debug(f"Pipeline configuration: {config}")
        self.config = config
        self.molecules = []

    def load_molecules(self) -> None:
        """Load molecules from XYZ files based on configuration."""
        info(f"Loading molecules from {self.config['molecules']['xyz_dir']}")
        debug(
            f"Default charge: {self.config['molecules']['default_charge']}, Default multiplicity: {self.config['molecules']['default_mult']}"
        )

        molecules = Molecule.from_xyz_files(
            self.config["molecules"]["xyz_dir"],
            self.config["molecules"]["default_charge"],
            self.config["molecules"]["default_mult"],
        )

        if len(molecules) == 0:
            error(f"No molecules found in {self.config['molecules']['xyz_dir']}")
            raise ValueError(
                f"No molecules found in {self.config['molecules']['xyz_dir']}"
            )

        info(f"Loaded {len(molecules)} molecules")
        for mol in molecules:
            debug(
                f"Loaded molecule: {mol.name} (charge={mol.charge}, mult={mol.mult})"
            )

        self.molecules = molecules

    def run(self) -> PipelineStats:
        """Run the calculation pipeline on all loaded molecules.
        
        Returns:
            PipelineStats: Statistics for the pipeline execution
        """
        info("Starting calculation pipeline")
        
        # Create a timer for the entire pipeline
        with Timer("Pipeline") as pipeline_timer:
            # Make sure molecules are loaded
            if not self.molecules:
                debug("No molecules loaded yet, loading now")
                self.load_molecules()
    
            n_workers = self.config["main"]["workers"]
            cpus = self.config["main"]["cpus"]
            debug(f"Configuration: {n_workers} workers, {cpus} total CPUs")
    
            if cpus < n_workers:
                error(f"Not enough CPU cores ({cpus}) for all workers ({n_workers})")
                raise ValueError(
                    f"Not enough CPU cores ({cpus}) for all workers ({n_workers})"
                )
    
            pipeline_stats = None
            
            if n_workers > 1:
                # Calculate CPUs per worker
                worker_cpus = cpus // n_workers
                info(
                    f"Running in parallel mode with {n_workers} workers, {worker_cpus} CPUs per worker"
                )
                # Process molecules in parallel
                pipeline_stats = process_molecules_parallel(
                    self.molecules, n_workers, worker_cpus, self.config
                )
            else:
                # Process molecules sequentially
                info(f"Running in sequential mode with {cpus} CPUs")
                pipeline_stats = process_molecules_sequential(self.molecules, self.config)
    
        info(f"Pipeline execution completed in {pipeline_timer.elapsed_time:.2f}s")
        return pipeline_stats

    @classmethod
    def from_config_file(cls, config_file: Path) -> "PipelineRunner":
        """Create a pipeline runner from a config file.

        Args:
            config_file: Path to the configuration file

        Returns:
            A configured PipelineRunner instance
        """
        info(f"Creating pipeline runner from config file: {config_file}")
        from orcastrator.config import load_config

        config = load_config(config_file)
        debug(f"Config loaded successfully from {config_file}")
        return cls(config)
