import concurrent.futures
import os
import queue
import time
from pathlib import Path
from typing import List, Optional

from orcastrator.calculation import OrcaCalculation
from orcastrator.logger import clear_context, debug, error, info, set_context, warning
from orcastrator.molecule import Molecule
from orcastrator.stats import MoleculeStats, PipelineStats, StepStats


def process_molecule(
    molecule: Molecule, config: dict, cpus: Optional[int] = None
) -> tuple[bool, MoleculeStats]:
    """Process a single molecule with the given configuration.

    Args:
        molecule: The molecule to process
        config: Dictionary containing calculation configuration
        cpus: Optional number of CPUs to use for this calculation. If None,
              will use the default from the config.

    Returns:
        bool: True if all calculation steps completed successfully, False otherwise
    """
    # Set molecule context for logging
    set_context(molecule=molecule.name)
    info(
        f"Processing molecule: {molecule.name} (charge={molecule.charge}, mult={molecule.mult})"
    )

    # Initialize molecule statistics
    molecule_stats = MoleculeStats(name=molecule.name, success=True, elapsed_time=0.0)

    # Start timing the molecule processing
    start_time = time.time()

    # Set up directories
    output_dir = Path(config["main"]["output_dir"]) / molecule.name
    output_dir.mkdir(parents=True, exist_ok=True)
    debug(f"Created output directory: {output_dir}")

    scratch_dir = Path(config["main"]["scratch_dir"])
    if slurm_job_id := os.getenv("SLURM_JOB_ID"):
        scratch_dir = scratch_dir / slurm_job_id
    debug(f"Using scratch directory: {scratch_dir}")

    # Get the CPU count for this calculation
    cpu_count = cpus if cpus is not None else config["main"]["cpus"]
    debug(f"Using {cpu_count} CPUs for calculation")

    # Process each step in the calculation pipeline
    previous_calc = None
    success = True

    try:
        for step in config["step"]:
            # Set step context for logging
            set_context(molecule=molecule.name, step=step["name"])
            info(f"Starting calculation step: {step['name']}")
            step_dir = output_dir / step["name"]
            step_dir.mkdir(exist_ok=True)
            debug(f"Created step directory: {step_dir}")

            # Create calculation for this step (either initial or chained from previous)
            if previous_calc is None:
                debug(f"Creating initial calculation for step {step['name']}")
                calc = OrcaCalculation(
                    directory=step_dir,
                    molecule=molecule,
                    keywords=step["keywords"],
                    blocks=step.get("blocks", []),
                    overwrite=config["main"]["overwrite"],
                    cpus=cpu_count,
                    mem_per_cpu_gb=config["main"]["mem_per_cpu_gb"],
                    scratch_dir=scratch_dir,
                )
            else:
                # Chain from previous calculation
                charge = step.get("charge", molecule.charge)
                mult = step.get("mult", molecule.mult)
                debug(
                    f"Chaining calculation from previous step with charge={charge}, mult={mult}"
                )

                calc = previous_calc.chain(
                    directory=step_dir,
                    keywords=step["keywords"],
                    blocks=step.get("blocks", []),
                    charge=charge,
                    mult=mult,
                )

            debug(f"Running calculation step {step['name']} for {molecule.name}")
            calc_success, step_time = calc.run()

            # Record step statistics
            step_stats = StepStats(
                name=step["name"], success=calc_success, elapsed_time=step_time
            )
            molecule_stats.steps.append(step_stats)

            if not calc_success:
                warning("Calculation failed at current step")
                success = False
                molecule_stats.success = False
                break

            info(f"Step {step['name']} completed successfully")
            previous_calc = calc
    except Exception:
        error("Error processing molecule", exc_info=True)
        success = False

    # Calculate total processing time
    elapsed_time = time.time() - start_time
    molecule_stats.elapsed_time = elapsed_time

    if success:
        info(f"All calculation steps completed successfully (took {elapsed_time:.2f}s)")
    else:
        warning(f"Calculation pipeline failed (took {elapsed_time:.2f}s)")

    return success, molecule_stats


def process_molecules_parallel(
    molecules: List[Molecule], n_workers: int, worker_cpus: int, config: dict
) -> PipelineStats:
    """Process molecules in parallel using a thread pool and a shared queue.

    This function distributes molecule processing tasks among multiple worker
    threads. Each worker takes a new molecule from the shared queue when it
    finishes processing its current molecule, ensuring efficient load balancing.

    Args:
        molecules: List of molecules to process
        n_workers: Number of parallel workers to use
        worker_cpus: Number of CPUs to allocate to each worker
        config: Dictionary containing calculation configuration
    """
    # Clear any previous context when starting pipeline
    clear_context()
    info(
        f"Starting parallel processing with {n_workers} workers, {worker_cpus} CPUs per worker"
    )
    debug(f"Processing {len(molecules)} molecules in parallel")

    # Initialize pipeline statistics
    pipeline_stats = PipelineStats()

    # Create a shared queue of molecules
    molecule_queue = queue.Queue()
    for molecule in molecules:
        molecule_queue.put(molecule)
        debug(f"Added {molecule.name} to processing queue")

    # Create a function for worker to process molecules from queue
    def worker():
        debug("Worker thread starting")
        while True:
            try:
                molecule = molecule_queue.get_nowait()
                set_context(molecule=molecule.name)
                debug(f"Worker picked up molecule {molecule.name}")
                success, mol_stats = process_molecule(
                    molecule, config, cpus=worker_cpus
                )
                status = "completed successfully" if success else "failed"
                info(f"Molecule {status}")

                # Add molecule statistics to pipeline stats (thread-safe)
                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=1
                ) as single_executor:
                    single_executor.submit(pipeline_stats.add_molecule_stats, mol_stats)

                molecule_queue.task_done()
                debug("Worker finished processing")
                # Clear context when finished with this molecule
                clear_context()
            except queue.Empty:
                debug("Queue empty, worker thread ending")
                break
            except Exception:
                error("Worker thread encountered an error", exc_info=True)

    # Start worker threads
    debug(f"Starting ThreadPoolExecutor with {n_workers} workers")
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = [executor.submit(worker) for _ in range(n_workers)]
        debug(f"Submitted {len(futures)} worker tasks")
        concurrent.futures.wait(futures)
        debug("All worker threads have completed")

    # Mark the pipeline as complete and record the end time
    pipeline_stats.complete()

    # Print statistics summary
    pipeline_stats.print_summary()

    info("All molecules have been processed")

    return pipeline_stats


def process_molecules_sequential(
    molecules: List[Molecule], config: dict
) -> PipelineStats:
    """Process molecules sequentially.

    This function processes each molecule one after another, using all available
    resources for each calculation.

    Args:
        molecules: List of molecules to process
        config: Dictionary containing calculation configuration
    """
    # Clear any previous context when starting pipeline
    clear_context()
    info(f"Starting sequential processing of {len(molecules)} molecules")

    # Initialize pipeline statistics
    pipeline_stats = PipelineStats()

    for i, molecule in enumerate(molecules):
        set_context(molecule=molecule.name)
        info(f"Processing molecule {i + 1}/{len(molecules)}: {molecule.name}")
        try:
            success, mol_stats = process_molecule(molecule, config)
            status = "completed successfully" if success else "failed"
            info(f"Molecule {status}")
            # Clear context after processing this molecule
            clear_context()
            pipeline_stats.add_molecule_stats(mol_stats)
        except Exception:
            error("Error processing molecule", exc_info=True)
            # Clear context after processing this molecule
            clear_context()
            # Add a failed molecule stat when exception occurs
            pipeline_stats.add_molecule_stats(
                MoleculeStats(name=molecule.name, success=False, elapsed_time=0.0)
            )

    # Mark the pipeline as complete and record end time
    pipeline_stats.complete()

    # Print statistics summary
    pipeline_stats.print_summary()

    return pipeline_stats
