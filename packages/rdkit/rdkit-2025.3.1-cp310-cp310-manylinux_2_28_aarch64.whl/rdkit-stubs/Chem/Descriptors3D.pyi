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
descList: list  # value = [('PMI1', <function <lambda> at 0xffffbe2cc310>), ('PMI2', <function <lambda> at 0xffffb0fa5900>), ('PMI3', <function <lambda> at 0xffffb0fa5990>), ('NPR1', <function <lambda> at 0xffffb0fa5a20>), ('NPR2', <function <lambda> at 0xffffb0fa5ab0>), ('RadiusOfGyration', <function <lambda> at 0xffffb0fa5b40>), ('InertialShapeFactor', <function <lambda> at 0xffffb0fa5bd0>), ('Eccentricity', <function <lambda> at 0xffffb0fa5c60>), ('Asphericity', <function <lambda> at 0xffffb0fa5cf0>), ('SpherocityIndex', <function <lambda> at 0xffffb0fa5d80>), ('PBF', <function <lambda> at 0xffffb0fa5e10>)]
