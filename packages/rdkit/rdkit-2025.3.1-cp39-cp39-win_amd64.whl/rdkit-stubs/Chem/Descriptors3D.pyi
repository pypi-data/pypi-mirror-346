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
descList: list  # value = [('PMI1', <function <lambda> at 0x0000021A2B937B80>), ('PMI2', <function <lambda> at 0x0000021A33BD9700>), ('PMI3', <function <lambda> at 0x0000021A33BD9790>), ('NPR1', <function <lambda> at 0x0000021A33BD9820>), ('NPR2', <function <lambda> at 0x0000021A33BD98B0>), ('RadiusOfGyration', <function <lambda> at 0x0000021A33BD9940>), ('InertialShapeFactor', <function <lambda> at 0x0000021A33BD99D0>), ('Eccentricity', <function <lambda> at 0x0000021A33BD9A60>), ('Asphericity', <function <lambda> at 0x0000021A33BD9AF0>), ('SpherocityIndex', <function <lambda> at 0x0000021A33BD9B80>), ('PBF', <function <lambda> at 0x0000021A33BD9C10>)]
