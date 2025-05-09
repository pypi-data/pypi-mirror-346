from typing import Literal
from .context import Context
from .handler.gripper import Gripper
from .handler.pipette import Pipette
from .liquid import Liquid
from .labware import Labware
from .module import Module

def init(robot_type: str = 'alphatool', 
         deck_type: Literal['standard', 'ext1'] = 'standard',
         auto_revise: bool = True) -> Context:
    """Initialize the protocol context. This function sets up the protocol context based on the alphatool.

    Args:
        robot_type (str): Type of robot to use (e.g. 'alphatool')
        deck_type (Literal['standard', 'ext1']): Type of deck to use (e.g. 'standard' or 'ext1')
        auto_revise (bool): If True, automatically corrects name errors for pipette, module, and labware if possible. Defaults to True.

    Returns:
        Context: The initialized protocol context.
    """
    if robot_type != 'alphatool':
        raise ValueError(f"Unsupported robot type: {robot_type}. Must be 'alphatool'.")
    if deck_type not in ['standard', 'ext1']:
        raise ValueError(f"Unsupported deck type: {deck_type}. Must be 'standard' or 'ext1'.")
    if not isinstance(auto_revise, bool):
        raise TypeError(f"auto_revise must be a boolean, got {type(auto_revise)}")

    return Context(robot_type=robot_type, deck_type=deck_type, auto_revise=auto_revise)