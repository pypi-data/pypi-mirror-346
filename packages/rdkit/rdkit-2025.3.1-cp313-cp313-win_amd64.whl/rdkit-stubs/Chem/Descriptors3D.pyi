"""
Descriptors derived from a molecule's 3D structure

"""
from __future__ import annotations
from rdkit.Chem.Descriptors import _isCallable
from rdkit.Chem import rdMolDescriptors
__all__ = ['CalcMolDescriptors3D', 'descList', 'rdMolDescriptors']
def CalcMolDescriptors3D(mol, confId = None):
    """
    
    Compute all 3D descriptors of a molecule
    
    Arguments:
    - mol: the molecule to work with
    - confId: conformer ID to work with. If not specified the default (-1) is used
    
    Return:
    
    dict
        A dictionary with decriptor names as keys and the descriptor values as values
    
    raises a ValueError 
        If the molecule does not have conformers
    """
def _setupDescriptors(namespace):
    ...
descList: list  # value = [('PMI1', <function <lambda> at 0x0000021A379F5D00>), ('PMI2', <function <lambda> at 0x0000021A379F6480>), ('PMI3', <function <lambda> at 0x0000021A379F6520>), ('NPR1', <function <lambda> at 0x0000021A379F65C0>), ('NPR2', <function <lambda> at 0x0000021A379F6660>), ('RadiusOfGyration', <function <lambda> at 0x0000021A379F6700>), ('InertialShapeFactor', <function <lambda> at 0x0000021A379F67A0>), ('Eccentricity', <function <lambda> at 0x0000021A379F6840>), ('Asphericity', <function <lambda> at 0x0000021A379F68E0>), ('SpherocityIndex', <function <lambda> at 0x0000021A379F6980>), ('PBF', <function <lambda> at 0x0000021A379F6A20>)]
