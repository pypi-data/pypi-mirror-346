# sleazy - cli+easy
import argparse
import re
import typing as t

D = t.TypeVar("D", bound=dict)


def parse_count_spec(spec: str) -> str | int:
    """Parse a count specification into argparse nargs format"""
    # Exact numeric values
    if spec.isdigit():
        return int(spec)

    # Handle comparison operators
    pattern = r'([<>=]{1,2})\s*(\d+)'
    match = re.match(pattern, spec)
    if match:
        op, num = match.groups()
        num = int(num)

        if op == '==':
            return num  # Exactly N
        elif op == '>' and num == 0:
            return '+'  # More than 0 = 1 or more
        elif op == '>' and num > 0:
            return '+'  # More than N (argparse only has +)
        elif op == '>=' and num == 0:
            return '*'  # 0 or more
        elif op == '>=' and num > 0:
            return '+'  # N or more (argparse only has +)
        elif op == '<' and num > 1:
            return '?'  # Less than N (if N>1, argparse only has ?)
        elif op == '<=' and num > 0:
            return '?'  # At most N (argparse only has ? for optional)

    # Default to optional single argument if no pattern matched
    return '?'


def parse_args_from_typeddict(typeddict_cls: t.Type[D], args: t.Optional[list[str]] = None) -> D:
    parser = argparse.ArgumentParser()
    type_hints = t.get_type_hints(typeddict_cls, include_extras=True)

    # First, add all positional arguments
    positional_fields = []
    for field, hint in type_hints.items():
        # Check if it's a positional argument
        is_positional = False
        arg_type = hint
        nargs_value = '?'  # Default is optional single argument
        is_list_type = False

        if t.get_origin(hint) is t.Annotated:
            arg_type, *annotations = t.get_args(hint)

            # Check if the type is a list
            if t.get_origin(arg_type) is list:
                is_list_type = True
                # Get the element type for the list
                elem_type = t.get_args(arg_type)[0] if t.get_args(arg_type) else str

            for anno in annotations:
                if anno == 'positional':
                    is_positional = True
                # Support for positional counts - now directly parse the count spec
                elif isinstance(anno, str) and (any(c in anno for c in ['>', '<', '=']) or anno.isdigit()):
                    nargs_value = parse_count_spec(anno)

        if is_positional:
            positional_fields.append((field, arg_type, nargs_value, is_list_type))

    # Add positional arguments in their own group
    for field, arg_type, nargs_value, is_list_type in positional_fields:
        # Handle Literal types
        if t.get_origin(arg_type) is t.Literal:
            literal_values = t.get_args(arg_type)
            # Use first value's type as the parser type
            if literal_values:
                first_value = literal_values[0]
                parser_type = type(first_value)
                parser.add_argument(field, type=parser_type, nargs=nargs_value, default=None,
                                    choices=literal_values)
            else:
                parser.add_argument(field, nargs=nargs_value, default=None)
        elif is_list_type:
            # For list types, get the element type
            elem_type = t.get_args(arg_type)[0] if t.get_args(arg_type) else str
            parser.add_argument(field, type=elem_type, nargs=nargs_value, default=None)
        else:
            # For non-list types, ensure single values are not put in a list
            # when nargs is a numeric value
            if isinstance(nargs_value, int) and nargs_value == 1 and not is_list_type:
                # For exactly 1 argument that's not a list type, don't use nargs
                parser.add_argument(field, type=arg_type, default=None)
            else:
                parser.add_argument(field, type=arg_type, nargs=nargs_value, default=None)

    # Then add all optional arguments
    for field, hint in type_hints.items():
        # Skip positional arguments as they've already been added
        if field in [f for f, _, _, _ in positional_fields]:
            continue

        arg_type = hint
        if t.get_origin(hint) is t.Annotated:
            arg_type, *_ = t.get_args(hint)

        # Handle Literal types in optional arguments
        if t.get_origin(arg_type) is t.Literal:
            literal_values = t.get_args(arg_type)
            if literal_values:
                first_value = literal_values[0]
                parser_type = type(first_value)
                parser.add_argument(f"--{field.replace('_', '-')}", type=parser_type, choices=literal_values)
            else:
                parser.add_argument(f"--{field.replace('_', '-')}")
        elif arg_type is bool:
            parser.add_argument(f"--{field.replace('_', '-')}", action="store_true")
        else:
            parser.add_argument(f"--{field.replace('_', '-')}", type=arg_type)

    return vars(parser.parse_args(args))


def typeddict_to_cli_args(data: dict[str, t.Any], typeddict_cls: t.Type[D] = None) -> list[str]:
    """
    Convert a TypedDict instance to a list of command-line arguments.
    Positional arguments come first, followed by optional arguments.
    """
    args = []
    typeddict_cls = typeddict_cls or data.__class__
    type_hints = t.get_type_hints(typeddict_cls, include_extras=True)

    # Process positional arguments first
    positional_fields = []
    for field, hint in type_hints.items():
        is_positional = False
        nargs_value = '?'  # Default

        if t.get_origin(hint) is t.Annotated:
            _, *annotations = t.get_args(hint)
            for anno in annotations:
                if anno == 'positional':
                    is_positional = True
                # Support for positional counts with dynamic parsing
                elif isinstance(anno, str) and (any(c in anno for c in ['>', '<', '=']) or anno.isdigit()):
                    nargs_value = parse_count_spec(anno)

        if is_positional:
            positional_fields.append((field, nargs_value))

    # Add positional arguments
    for field, nargs_value in positional_fields:
        if field in data and data[field] is not None:
            if isinstance(data[field], list) and nargs_value in ['*', '+']:
                for item in data[field]:
                    args.append(str(item))
            else:
                args.append(str(data[field]))

    # Add optional arguments
    for field, value in data.items():
        # Skip positional arguments as they've already been added
        if field in [f for f, _ in positional_fields]:
            continue

        # Skip None values
        if value is None:
            continue

        if isinstance(value, bool):
            if value:  # Only add flag if True
                args.append(f"--{field.replace('_', '-')}")
        else:
            args.append(f"--{field.replace('_', '-')}")
            args.append(str(value))

    return args
