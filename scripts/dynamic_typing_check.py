from functools import wraps
from inspect import signature
from typing import get_type_hints, Any, List, Dict, Tuple, Union, Type, Callable
import collections.abc

def is_instance_of(value: Any, expected_type: Type) -> bool:
    """
    Check if the value matches the expected type, including parameterized generics.

    Args:
        value (Any): The value to check.
        expected_type (Type): The expected type (possibly parameterized).

    Returns:
        bool: True if value matches the type; False otherwise.
    """
    origin = getattr(expected_type, "__origin__", None)
    args = getattr(expected_type, "__args__", None)

    if origin is None:
        # Handle simple types
        return isinstance(value, expected_type)

    if origin in {list, List}:
        return isinstance(value, list) and all(
            is_instance_of(item, args[0]) for item in value
        )
    if origin in {dict, Dict}:
        return isinstance(value, dict) and all(
            is_instance_of(k, args[0]) and is_instance_of(v, args[1])
            for k, v in value.items()
        )
    if origin in {tuple, Tuple}:
        return isinstance(value, tuple) and len(value) == len(args) and all(
            is_instance_of(item, arg) for item, arg in zip(value, args)
        )
    if origin in {collections.abc.Iterable}:
        return isinstance(value, collections.abc.Iterable) and all(
            is_instance_of(item, args[0]) for item in value
        )
    if origin in {Union}:
        return any(is_instance_of(value, arg) for arg in args)

    # Fallback to strict isinstance check
    return isinstance(value, expected_type)


def enforce_types(func: Callable[..., Any]):
    """
    A decorator to enforce type hints for a function's arguments and return value.

    Args:
        func (callable): The function to wrap.

    Returns:
        callable: The wrapped function with type enforcement.
    """
    type_hints = get_type_hints(func)
    sig = signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # Validate argument types
        for name, value in bound_args.arguments.items():
            if name in type_hints:
                expected_type = type_hints[name]
                if not is_instance_of(value, expected_type):
                    raise TypeError(
                        f"Argument '{name}' must be of type {expected_type}, "
                        f"but got value {value!r} of type {type(value).__name__}."
                    )

        result = func(*args, **kwargs)

        # Validate return type
        if "return" in type_hints:
            expected_return_type = type_hints["return"]
            if not is_instance_of(result, expected_return_type):
                raise TypeError(
                    f"Return value must be of type {expected_return_type}, "
                    f"but got value {result!r} of type {type(result).__name__}."
                )

        return result

    return wrapper


# Example usage
@enforce_types
def greet(name: str) -> str:
    return f"Hello, {name}"


@enforce_types
def add(a: int, b: int) -> int:
    return a + b


@enforce_types
def process_items(items: List[int]) -> None:
    for item in items:
        print(item)


@enforce_types
def complex_func(data: Dict[str, List[int]]) -> Tuple[str, int]:
    return list(data.keys())[0], sum(sum(data.values(), []))


# Testing
if __name__ == "__main__":
    print(greet("Alice"))  # Works fine
    print(add(3, 5))       # Gives error
    process_items([1, 2, 3])  # Works fine
    print(complex_func({"key1": [1, 2], "key2": [3, 4]}))  # Works fine
    complex_func({"key1": [1, "two"]})  # Raises TypeError
