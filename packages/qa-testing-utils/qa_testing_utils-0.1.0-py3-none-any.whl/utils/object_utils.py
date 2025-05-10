# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

import threading
from dataclasses import asdict, fields, is_dataclass, replace
from enum import Enum
from typing import (Any, Callable, Dict, Protocol, Type, final)

# TODO: move to stream_utils module
type Supplier[T] = Callable[[], T]
type Predicate[T] = Callable[[T], bool]


class Valid(Protocol):
    """
    Specifies a method for validating objects.
    """

    def is_valid(self) -> bool:
        """
        Should be implemented by objects that need validation.

        Returns:
            bool: true, if the object is valid
        """
        ...


class ImmutableMixin:
    """
    Enforces immutability by overriding __setattr__ to raise AttributeError.

    This implementation does not work with the WithMixin if the attributes are
    initialized with default values.

    It also does not work when applied to a super type for which the __init__
    is overridden.

    Use it with non-dataclasses.
    """

    def __setattr__(self, key: str, value: Any) -> None:
        if hasattr(self, key):
            raise AttributeError(f"Can't modify attribute '{
                                 key}' after initialization")
        super().__setattr__(key, value)  # Properly sets the attribute


class WithMixin:
    '''
    Supports immutability by copying on change.

    For example, instead of mutating like this::

        obj.field = a_new_value

    use::

        dup_object_with_changes = obj.with_(field=a_new_value)

    This will ensure that the changes are applied on a duplicate of `obj`.

    Can be applied on plain Python classes, and on `dataclases` too.
    '''
    @final
    def with_[T:WithMixin](self: T, **changes: Any) -> T:
        if is_dataclass(self):
            # Directly use replace for dataclasses; it will raise an error for invalid fields
            return replace(self, **changes)

        duplicated_object = self.__class__(**self.__dict__)
        for key, value in changes.items():
            # Get the current attribute to determine its type
            current_attr = getattr(self, key, None)
            if isinstance(current_attr, Enum):
                # If the current attribute is an enum,
                # convert the value to the corresponding enum
                value = current_attr.__class__(value)
            setattr(duplicated_object, key, value)
        return duplicated_object


class ToDictMixin:

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts a dataclass instance (with nested dataclasses) to a dictionary.
        """
        def convert(value):
            if isinstance(value, ToDictMixin):
                return value.to_dict()
            elif isinstance(value, list):
                return [convert(v) for v in value]
            elif isinstance(value, dict):
                return {k: convert(v) for k, v in value.items()}
            return value

        if not is_dataclass(self):
            raise TypeError("not a dataclass instance")

        return {key: convert(value) for key, value in asdict(self).items()}

    def flatten(self, prefix: str = "") -> Dict[str, Any]:
        """
        Flattens the nested structure into a flat dictionary for CSV serialization.
        """
        flat_dict = {}

        def flatten_value(key: str, value: Any):
            if isinstance(value, ToDictMixin):
                # Flatten nested ToDictMixin dataclasses
                nested_flat = value.flatten(prefix=f"{key}_")
                flat_dict.update(nested_flat)
            elif isinstance(value, list):
                # Serialize lists as JSON strings or expand into multiple columns
                for idx, item in enumerate(value):
                    flat_dict[f"{key}[{idx}]"] = item
            elif isinstance(value, dict):
                # Serialize dicts as JSON strings or expand into multiple columns
                for sub_key, sub_val in value.items():
                    flat_dict[f"{key}_{sub_key}"] = sub_val
            else:
                # Directly add non-nested fields
                flat_dict[key] = value

        if not is_dataclass(self):
            raise TypeError("not a dataclass instance")

        for field in fields(self):
            value = getattr(self, field.name)
            flatten_value(f"{prefix}{field.name}", value)

        return flat_dict


class SingletonMeta(type):
    """
    A thread-safe implementation of a Singleton metaclass.
    """
    _instances: Dict[Type['SingletonBase'], 'SingletonBase'] = {}
    _lock: threading.Lock = threading.Lock()  # Ensure thread-safety

    def __call__(cls, *args: Any, **kwargs: Any) -> 'SingletonBase':
        with SingletonMeta._lock:
            if cls not in SingletonMeta._instances:
                instance = super().__call__(*args, **kwargs)
                SingletonMeta._instances[cls] = instance
        return SingletonMeta._instances[cls]


class SingletonBase(metaclass=SingletonMeta):
    """
    Base class for singletons using SingletonMeta.
    """
    pass


class InvalidValueException(ValueError):
    pass


def valid[T:Valid](value: T) -> T:
    """
    Validates specified object, assuming that it supports the Valid protocol.

    Args:
        value (T:Valid): the object

    Raises:
        TypeError: if the object does not support the Valid protocol
        InvalidValueException: if the object is invalid

    Returns:
        T:Valid: the validated object
    """
    if not (hasattr(value, 'is_valid') and callable(
            getattr(value, 'is_valid'))):
        raise TypeError(
            f"{value.__class__.__name__} does not conform to the Valid protocol")

    if value.is_valid():
        return value
    else:
        raise InvalidValueException(value)
