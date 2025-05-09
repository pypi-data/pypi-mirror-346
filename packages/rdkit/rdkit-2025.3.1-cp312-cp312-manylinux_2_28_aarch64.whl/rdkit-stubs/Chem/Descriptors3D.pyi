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
descList: list  # value = [('PMI1', <function <lambda> at 0xffff870a7600>), ('PMI2', <function <lambda> at 0xffff870a7ce0>), ('PMI3', <function <lambda> at 0xffff870a7d80>), ('NPR1', <function <lambda> at 0xffff870a7e20>), ('NPR2', <function <lambda> at 0xffff870a7ec0>), ('RadiusOfGyration', <function <lambda> at 0xffff870a7f60>), ('InertialShapeFactor', <function <lambda> at 0xffff85c00040>), ('Eccentricity', <function <lambda> at 0xffff85c000e0>), ('Asphericity', <function <lambda> at 0xffff85c00180>), ('SpherocityIndex', <function <lambda> at 0xffff85c00220>), ('PBF', <function <lambda> at 0xffff85c002c0>)]
