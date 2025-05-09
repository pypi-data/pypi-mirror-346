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
descList: list  # value = [('PMI1', <function <lambda> at 0x000001BA37219B20>), ('PMI2', <function <lambda> at 0x000001BA3721A200>), ('PMI3', <function <lambda> at 0x000001BA3721A2A0>), ('NPR1', <function <lambda> at 0x000001BA3721A340>), ('NPR2', <function <lambda> at 0x000001BA3721A3E0>), ('RadiusOfGyration', <function <lambda> at 0x000001BA3721A480>), ('InertialShapeFactor', <function <lambda> at 0x000001BA3721A520>), ('Eccentricity', <function <lambda> at 0x000001BA3721A5C0>), ('Asphericity', <function <lambda> at 0x000001BA3721A660>), ('SpherocityIndex', <function <lambda> at 0x000001BA3721A700>), ('PBF', <function <lambda> at 0x000001BA3721A7A0>)]
