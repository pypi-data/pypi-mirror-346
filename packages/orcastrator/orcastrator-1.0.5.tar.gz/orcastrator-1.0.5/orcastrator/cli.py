import logging
import shutil
import subprocess
import sys
from pathlib import Path

import click

from orcastrator.config import load_config
from orcastrator.logger import (
    clear_context, configure_from_config, debug, error, info, setup_file_logging, warning
)
from orcastrator.runner_logic import PipelineRunner
from orcastrator.slurm import SlurmConfig


@click.group()
def cli():
    """Orcastrator CLI - orchestrate ORCA calculations."""
    pass


@cli.command()
@click.argument(
    "config_file", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
def run(config_file: Path) -> None:
    """Run a calculation pipeline defined in a TOML config file."""
    # Reset any previous logger context
    clear_context()
    
    # Load config first to determine debug level
    config = load_config(config_file)
    
    # Set up log directory
    log_dir = config_file.parent / "logs"
    try:
        log_dir.mkdir(exist_ok=True, parents=True)
        setup_file_logging(log_dir=log_dir, log_level=logging.DEBUG)
    except Exception as e:
        error(f"Failed to create logs directory {log_dir}: {e}")
        # Try to set up logging in the current directory as fallback
        setup_file_logging(log_dir=None, log_level=logging.DEBUG)

    # Configure logging based on debug flag from config
    configure_from_config(config)
    
    info(f"Starting orcastrator run with config: {config_file}")
    try:
        # Create and run the pipeline using the PipelineRunner (with config already loaded)
        pipeline = PipelineRunner(config)
        stats = pipeline.run()
        info("Calculation pipeline completed successfully")
        
        # Log summary statistics
        total_molecules = len(stats.molecules)
        successful = len(stats.successful_molecules)
        failed = len(stats.failed_molecules)
        minutes = stats.elapsed_time / 60
        
        info(f"Summary: Processed {total_molecules} molecules in {minutes:.2f} minutes")
        info(f"         {successful} successful, {failed} failed")
    except Exception:
        error("Error running pipeline", exc_info=True)
        info("Calculation pipeline failed")
        sys.exit(1)


@cli.command()
@click.argument(
    "config_file", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.option(
    "--no-submit",
    is_flag=True,
    help="Generate the SLURM script but don't submit it with sbatch",
)
def slurm(config_file: Path, no_submit: bool) -> None:
    """Generate a SLURM batch script and optionally submit it with sbatch."""
    # Reset any previous logger context
    clear_context()
    
    info(f"Generating SLURM script for config file: {config_file}")
    try:
        config = load_config(config_file)
        debug(f"Loaded configuration: {config['main']}")

        slurm_config = SlurmConfig(
            job_name=config_file.stem,
            ntasks=config["main"]["cpus"],
            mem_per_cpu_gb=config["main"]["mem_per_cpu_gb"],
            orcastrator_command=f"uvx orcastrator run {config_file.resolve()}",
            config_file=config_file.resolve(),
        )
        debug(f"Created SLURM config: {slurm_config}")

        slurm_script_file = config_file.with_suffix(".slurm")
        slurm_config.write_to(slurm_script_file)
        info(f"SLURM script written to {slurm_script_file}")

        if not no_submit and shutil.which("sbatch"):
            debug("Submitting SLURM job with sbatch")
            result = subprocess.run(
                ["sbatch", str(slurm_script_file)], capture_output=True, text=True
            )
            if result.returncode == 0:
                slurm_job_id = result.stdout.strip().split()[-1]
                info(f"Submitted {config_file.name} with ID: {slurm_job_id}")
            else:
                error(f"Failed to submit job: {result.stderr}")
                sys.exit(1)
        elif no_submit:
            info("Script generated but not submitted (--no-submit flag used)")
        else:
            warning("sbatch not found in PATH, cannot submit job")
    except Exception:
        error("Error generating SLURM script", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
