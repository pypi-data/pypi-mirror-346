from typing import Any, List, Union
from ..labware import Well, Column

def flatten_wells(ele: Any):
    """flatten the element list if it is a nested structure

    Args:
        ele (Any): ele list

    Returns:
        ele: flatted ele list
    """
    if not isinstance(ele, list):
        ele = [ele]

    return [item for i in ele for item in (i if isinstance(i, list) else [i])]

def get_behind_slot(slot: int) -> Union[int, None]:
    """Get the slot number behind the given slot.
    +--------+--------+---------+
    | Slot 1 | Slot 5 | Slot 9  |
    +--------+--------+---------+
    | Slot 2 | Slot 6 | Slot 10 |
    +--------+--------+---------+
    | Slot 3 | Slot 7 | Slot 11 |
    +--------+--------+---------+
    | Slot 4 | Slot 8 | Slot 12 |
    +--------+--------+---------+
    """
    return {2:1, 3:2, 4:3, 6:5, 7:6, 8:7, 10:9, 11:10, 12:11}.get(slot)

def get_n_wells(wells: Union[List[Well], List[Column]]) -> int:
    """Get the total number of wells from a list of Wells or Columns.

    Args:
        wells (Union[List['Well'], List['Column']]): List of Well or Column objects

    Returns:
        int: Total number of wells
    """
    
    return sum(len(w) if isinstance(w, Column) else 1 for w in wells)

def is_only_first_row(wells: Union[List[Well], List[Column]]) -> bool:
    """Check if all wells are in the first row.

    Args:
        wells (Union[List[Well], List[Column]]): List of Well or Column objects

    Returns:
        bool: True if all wells are in the first row (Ax), False otherwise
    """
    return all(next(filter(str.isalpha, w.id())) == 'A' for w in wells if isinstance(w, Well))
