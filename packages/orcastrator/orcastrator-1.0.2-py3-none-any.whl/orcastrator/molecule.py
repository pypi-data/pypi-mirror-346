from pathlib import Path
from typing import Optional, Self

from orcastrator.logger import debug, error, info, warning


class Molecule:
    def __init__(
        self, charge: int, mult: int, xyz: str, name: str = "molecule"
    ) -> None:
        self.charge = charge
        self.mult = mult
        self.xyz = xyz
        self.name = name
        debug(f"Initialized molecule: {name}, charge={charge}, mult={mult}")

    def __str__(self) -> str:
        atoms = self.xyz.splitlines()
        atoms_str = "\n".join(atoms)
        debug(
            f"Converting molecule {self.name} to string format with {len(atoms)} atoms"
        )
        return f"{len(atoms)}\ncharge={self.charge} mult={self.mult}\n{atoms_str}"

    def to_orca(self) -> str:
        debug(f"Converting molecule {self.name} to ORCA format")
        return f"* XYZ {self.charge} {self.mult}\n{self.xyz}*"

    @staticmethod
    def _parse_charge_mult_from_comment(
        comment: str,
    ) -> tuple[Optional[int], Optional[int]]:
        """Read charge/mult like 'charge=1 mult=1'"""
        debug(f"Parsing charge/mult from comment: '{comment}'")
        charge, mult = None, None
        tokens = comment.strip().split()
        for token in tokens:
            if token.startswith("charge") and "=" in token:
                charge = int(token.split("=")[-1])
                debug(f"Found charge: {charge}")
            if token.startswith("mult") and "=" in token:
                mult = int(token.split("=")[-1])
                debug(f"Found mult: {mult}")
        debug(f"Parse result: charge={charge}, mult={mult}")
        return charge, mult

    @classmethod
    def from_xyz_file(
        cls,
        xyz_file: Path,
        charge: Optional[int] = None,
        mult: Optional[int] = None,
    ) -> Self:
        info(f"Creating molecule from XYZ file: {xyz_file}")
        debug(f"Input charge={charge}, mult={mult}")

        xyz_content = xyz_file.read_text()
        debug(f"Read XYZ file, length: {len(xyz_content)} bytes")

        lines = xyz_content.splitlines()
        n_atoms, comment, *atoms = lines

        debug(f"XYZ file contains {n_atoms} atoms according to header")
        debug(f"Comment line: '{comment}'")

        if int(n_atoms) != len(atoms):
            error(
                f"Invalid XYZ file {xyz_file}: expected {n_atoms} atoms but found {len(atoms)}"
            )
            raise ValueError("Invalid XYZ file, mismatch of n_atoms and actual atoms")

        xyz_charge, xyz_mult = cls._parse_charge_mult_from_comment(comment)

        if charge is None:
            charge = xyz_charge
            debug(f"Using charge from XYZ file: {charge}")

        if mult is None:
            mult = xyz_mult
            debug(f"Using mult from XYZ file: {mult}")

        if charge is None or mult is None:
            error(f"Failed to determine charge/mult for {xyz_file}")
            raise ValueError("Missing charge and/or multiplicity")

        debug(f"Final molecule parameters: charge={charge}, mult={mult}")

        xyz = ""
        for atom in atoms:
            s, x, y, z = atom.split()
            x, y, z = float(x), float(y), float(z)
            xyz += f"{s:4}    {x:>12.8f}    {y:>12.8f}    {z:>12.8f}\n"

        info(f"Successfully created molecule from {xyz_file}")
        return cls(charge, mult, xyz, name=xyz_file.stem)

    @classmethod
    def from_xyz_files(
        cls,
        xyz_files_dir: Path,
        default_charge: Optional[int],
        default_mult: Optional[int],
    ) -> list[Self]:
        # here i want to provide defaults if there are now charge/mults in the xyz files.
        # so it is different than the from_xyz_file
        info(f"Loading molecules from directory: {xyz_files_dir}")
        debug(f"Default charge={default_charge}, default mult={default_mult}")

        xyz_files = list(Path(xyz_files_dir).glob("*.xyz"))
        info(f"Found {len(xyz_files)} XYZ files in directory")

        if not xyz_files:
            warning(f"No XYZ files found in {xyz_files_dir}")

        molecules = []
        for f in xyz_files:
            debug(f"Processing XYZ file: {f}")
            file_content = f.read_text()
            lines = file_content.splitlines()

            if len(lines) < 2:
                error(f"Invalid XYZ file format for {f}: insufficient lines")
                continue

            charge, mult = cls._parse_charge_mult_from_comment(lines[1])

            if charge is None:
                debug(f"No charge specified in {f}, using default: {default_charge}")
                charge = default_charge

            if mult is None:
                debug(f"No mult specified in {f}, using default: {default_mult}")
                mult = default_mult

            if charge is None or mult is None:
                error(f"Failed to determine charge/mult from xyz file {f}")
                raise ValueError(
                    f"Failed to determine charge/mult from xyz file {f} and no defaults provided"
                )

            debug(f"Creating molecule from {f} with charge={charge}, mult={mult}")
            molecules.append(cls.from_xyz_file(f, charge, mult))

        info(f"Successfully loaded {len(molecules)} molecules")
        return molecules
