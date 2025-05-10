from typing import Union, List


def is_none(obj: any) -> bool:
    return obj is None


def is_not_none(obj: any) -> bool:
    return obj is not None


def is_empty(value: Union[List, str, dict, object]) -> bool:
    if isinstance(value, list) or isinstance(value, dict):
        return value is None or len(value) == 0
    if isinstance(value, str):
        return value is None or value.strip() == ""
    return is_none(value)


def is_not_empty(value: Union[List, str, dict, object]) -> bool:
    return not is_empty(value)


def get(obj: object | dict, attr_name: str, default=None):
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(attr_name, default)
    else:
        return getattr(obj, attr_name, default)


def assign_default(target_dict, default_dict):
    if isinstance(target_dict, dict) and isinstance(default_dict, dict):
        for key, default_value in default_dict.items():
            if key in target_dict:
                target_dict[key] = assign_default(target_dict[key], default_value)
            else:
                target_dict[key] = default_value
    return target_dict
