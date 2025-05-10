Calculation
-----------

- directory
- scratch_directory
- charge, mult, xyz =  a "molecule"?
- keywords, blocks
- overwrite
- cpus, mem_per_cpu_gb

molecule
--------

- charge, mult, xyz
- from_xyz_file(Optional[charge], Optional[mult])
- consume_xyz_files(directory) -> list[Molecule]

Runner
------

Protocol

- run(input_file)

### OrcaRunner

- orca_executable = shutil.which("orca")

Workflow/Pipeline
-----------------

chain several calculations with different keywords/blocks - propagate the molecule
