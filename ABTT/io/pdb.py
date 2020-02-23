import logging

from Bio import PDB


def read(pdb_file):
    """
    reads a pdb file into a structure object
    :param pdb_file: pdb format file
    :return: structure
    """
    logging.info(f'reading pdb file: {pdb_file}')
    if not pdb_file.lower().endswith('.cif'):
        structure = PDB.PDBParser().get_structure(pdb_file, pdb_file)
    else:
        logging.info(f'switched to cif modus for file: {pdb_file}')
        structure = PDB.MMCIFParser().get_structure(pdb_file, pdb_file)

    return structure


def get(PDB_id, directory=None, format='pdb'):
    """
    gets a structure from the PDB using its PDB id
    :param PDB_id: PDB id code
    :type PDB_id: str
    :param format:  File format
        * "mmCif" (PDBx/mmCif file),
        * "pdb" (default, format PDB),
        * "xml" (PDBML/XML format),
        * "mmtf" (highly compressed),
        * "bundle" (PDB formatted archive for large structure}
    :param directory: directory in which to save pdb file
    :return: structure
    """
    pdb = PDB.PDBList()
    if directory is not None:
        pdb.retrieve_pdb_file(PDB_id, pdir=directory, file_format=format, overwrite=True)
    else:
        pdb.retrieve_pdb_file(PDB_id, file_format=format, overwrite=True)


def get_atoms(pdb_file):
    structure = read(pdb_file)
    return structure.get_atoms()


def full_ids(pdb_file):
    atoms = get_atoms(pdb_file)
    for atom in atoms:
        yield atom.get_full_id()


def coords(pdb_file):
    atoms = get_atoms(pdb_file)
    for atom in atoms:
        yield atom.get_coord()


def unique_chains(pdb_file):
    structure = read(pdb_file)
    return [chain.id for chain in structure.get_chains()]


def chains_coords(pdb_file):
    for atom in get_atoms(pdb_file):
        coord = atom.get_coord()
        chain_id = atom.get_full_id()[2]
        yield (chain_id, coord)
