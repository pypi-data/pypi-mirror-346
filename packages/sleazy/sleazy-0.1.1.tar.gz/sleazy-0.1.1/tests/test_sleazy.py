"""
Fixme: these tests were automatically generated and should still be manually confirmed!
"""

import pytest
import typing as t
from src.sleazy import parse_args_from_typeddict, typeddict_to_cli_args, parse_count_spec


def test_parse_count_spec():
    # Test various formats of count specifications
    assert parse_count_spec('0') == 0
    assert parse_count_spec('1') == 1
    assert parse_count_spec('5') == 5

    # Test comparison operators
    assert parse_count_spec('>= 0') == '*'
    assert parse_count_spec('>= 1') == '+'
    assert parse_count_spec('>= 5') == '+'  # Any N >= 1 maps to + in argparse
    assert parse_count_spec('<= 1') == '?'
    assert parse_count_spec('<= 5') == '?'  # Any N <= N maps to ? in argparse
    assert parse_count_spec('== 1') == 1
    assert parse_count_spec('== 3') == 3
    assert parse_count_spec('== 10') == 10
    assert parse_count_spec('> 0') == '+'  # More than 0 is at least 1
    assert parse_count_spec('> 5') == '+'  # More than N is at least N+1
    assert parse_count_spec('< 1') == '?'  # Less than 1 means optional (0)
    assert parse_count_spec('< 5') == '?'  # Less than N means 0 to N-1

    # Test with whitespace variations
    assert parse_count_spec('>=0') == '*'
    assert parse_count_spec('<=  1') == '?'
    assert parse_count_spec('>0') == '+'

    # Test default value
    assert parse_count_spec('invalid') == '?'


def test_basic_type_parsing():
    class BasicTypes(t.TypedDict):
        string_val: str
        int_val: int
        float_val: float
        bool_val: bool

    args = ['--string-val', 'test', '--int-val', '42', '--float-val', '3.14', '--bool-val']
    result = parse_args_from_typeddict(BasicTypes, args)

    assert result['string_val'] == 'test'
    assert result['int_val'] == 42
    assert result['float_val'] == 3.14
    assert result['bool_val'] is True


def test_positional_args():
    class PositionalArgs(t.TypedDict):
        pos1: t.Annotated[str, 'positional']
        pos2: t.Annotated[int, 'positional']
        opt1: str

    args = ['value1', '42', '--opt1', 'option']
    result = parse_args_from_typeddict(PositionalArgs, args)

    assert result['pos1'] == 'value1'
    assert result['pos2'] == 42
    assert result['opt1'] == 'option'


def test_literal_types():
    class LiteralTypes(t.TypedDict):
        mode: t.Literal["auto", "manual", "hybrid"]
        level: t.Literal[1, 2, 3]

    # Test valid literals
    args = ['--mode', 'auto', '--level', '2']
    result = parse_args_from_typeddict(LiteralTypes, args)

    assert result['mode'] == 'auto'
    assert result['level'] == 2

    # Test invalid literals - should raise error
    with pytest.raises(SystemExit):
        parse_args_from_typeddict(LiteralTypes, ['--mode', 'invalid', '--level', '2'])

    with pytest.raises(SystemExit):
        parse_args_from_typeddict(LiteralTypes, ['--mode', 'auto', '--level', '5'])


def test_positional_literal():
    class PosLiteral(t.TypedDict):
        mode: t.Annotated[t.Literal["auto", "manual"], 'positional']

    args = ['auto']
    result = parse_args_from_typeddict(PosLiteral, args)
    assert result['mode'] == 'auto'

    with pytest.raises(SystemExit):
        parse_args_from_typeddict(PosLiteral, ['invalid'])


def test_positional_count_zero_or_more():
    class CountTest(t.TypedDict):
        files: t.Annotated[list[str], 'positional', '>= 0']

    # Test with multiple values
    args = ['file1.txt', 'file2.txt', 'file3.txt']
    result = parse_args_from_typeddict(CountTest, args)
    assert result['files'] == ['file1.txt', 'file2.txt', 'file3.txt']

    # Test with no values
    args = []
    result = parse_args_from_typeddict(CountTest, args)
    assert result['files'] == []


def test_positional_count_one_or_more():
    class CountTest(t.TypedDict):
        files: t.Annotated[list[str], 'positional', '>= 1']

    # Test with multiple values
    args = ['file1.txt', 'file2.txt']
    result = parse_args_from_typeddict(CountTest, args)
    assert result['files'] == ['file1.txt', 'file2.txt']

    # Test with no values - should fail
    with pytest.raises(SystemExit):
        parse_args_from_typeddict(CountTest, [])


def test_positional_count_greater_than():
    class CountTest(t.TypedDict):
        files: t.Annotated[list[str], 'positional', '> 0']

    # Test with values
    args = ['file1.txt', 'file2.txt']
    result = parse_args_from_typeddict(CountTest, args)
    assert result['files'] == ['file1.txt', 'file2.txt']

    # Test with no values - should fail
    with pytest.raises(SystemExit):
        parse_args_from_typeddict(CountTest, [])


def test_positional_count_at_most_one():
    class CountTest(t.TypedDict):
        file: t.Annotated[str, 'positional', '<= 1']

    # Test with one value
    args = ['file1.txt']
    result = parse_args_from_typeddict(CountTest, args)
    assert result['file'] == 'file1.txt'

    # Test with no values
    args = []
    result = parse_args_from_typeddict(CountTest, args)
    assert result['file'] is None

    # Test with multiple values - should fail
    with pytest.raises(SystemExit):
        parse_args_from_typeddict(CountTest, ['file1.txt', 'file2.txt'])


def test_positional_count_less_than():
    class CountTest(t.TypedDict):
        file: t.Annotated[str, 'positional', '< 2']

    # Test with one value
    args = ['file1.txt']
    result = parse_args_from_typeddict(CountTest, args)
    assert result['file'] == 'file1.txt'

    # Test with no values
    args = []
    result = parse_args_from_typeddict(CountTest, args)
    assert result['file'] is None

    # Test with multiple values - should fail
    with pytest.raises(SystemExit):
        parse_args_from_typeddict(CountTest, ['file1.txt', 'file2.txt'])


def test_positional_count_exactly():
    class CountTest(t.TypedDict):
        files: t.Annotated[list[str], 'positional', '== 3']

    # Test with exact number of values
    args = ['file1.txt', 'file2.txt', 'file3.txt']
    result = parse_args_from_typeddict(CountTest, args)
    assert result['files'] == ['file1.txt', 'file2.txt', 'file3.txt']

    # Test with too few values - should fail
    with pytest.raises(SystemExit):
        parse_args_from_typeddict(CountTest, ['file1.txt', 'file2.txt'])

    # Test with too many values - should fail
    with pytest.raises(SystemExit):
        parse_args_from_typeddict(CountTest, ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt'])


def test_positional_count_exactly_one():
    class CountTest(t.TypedDict):
        command: t.Annotated[str, 'positional', '== 1']

    # Test with single value
    args = ['build']
    result = parse_args_from_typeddict(CountTest, args)
    assert result['command'] == 'build'  # Should be a string, not a list
    assert not isinstance(result['command'], list)

    # Test with multiple values - should fail
    with pytest.raises(SystemExit):
        parse_args_from_typeddict(CountTest, ['build', 'extra'])


def test_multiple_positional_args_with_fixed_counts():
    class FixedCounts(t.TypedDict):
        command: t.Annotated[str, 'positional', '== 1']
        subcommand: t.Annotated[str, 'positional', '== 1']
        target: t.Annotated[str, 'positional', '== 1']
        option: t.Annotated[str, 'positional', '<= 1']

    # Test with all arguments
    args = ['build', 'web', 'app.py', 'debug']
    result = parse_args_from_typeddict(FixedCounts, args)
    assert result['command'] == 'build'
    assert result['subcommand'] == 'web'
    assert result['target'] == 'app.py'
    assert result['option'] == 'debug'

    # Test with minimum required
    args = ['build', 'web', 'app.py']
    result = parse_args_from_typeddict(FixedCounts, args)
    assert result['command'] == 'build'
    assert result['subcommand'] == 'web'
    assert result['target'] == 'app.py'
    assert result['option'] is None


def test_positional_with_count_constraints():
    class PositionalWithConstraints(t.TypedDict):
        command: t.Annotated[str, 'positional', '== 1']
        files: t.Annotated[list[str], 'positional', '== 2']

    # Test with exact file count
    args = ['compress', 'input.txt', 'output.gz']
    result = parse_args_from_typeddict(PositionalWithConstraints, args)
    assert result['command'] == 'compress'
    assert result['files'] == ['input.txt', 'output.gz']

    # Test with wrong file count - should fail
    with pytest.raises(SystemExit):
        print(parse_args_from_typeddict(PositionalWithConstraints, ['compress', 'input.txt']))


def test_exact_numeric_count():
    class CountTest(t.TypedDict):
        files: t.Annotated[list[str], 'positional', '2']

    # Test with exact number
    args = ['file1.txt', 'file2.txt']
    result = parse_args_from_typeddict(CountTest, args)
    assert result['files'] == ['file1.txt', 'file2.txt']

    # Test with wrong number - should fail
    with pytest.raises(SystemExit):
        parse_args_from_typeddict(CountTest, ['file1.txt'])


def test_larger_exact_count():
    class CountTest(t.TypedDict):
        files: t.Annotated[list[str], 'positional', '5']

    # Test with exact number
    args = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt', 'file5.txt']
    result = parse_args_from_typeddict(CountTest, args)
    assert result['files'] == ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt', 'file5.txt']


def test_typeddict_to_cli_args_basic():
    class TestDict(t.TypedDict):
        name: str
        count: int
        verbose: bool

    # Create a dictionary that would be an instance of TestDict
    data = {
        'name': 'test',
        'count': 42,
        'verbose': True
    }

    args = typeddict_to_cli_args(data, TestDict)
    # The order might vary, so we'll check for inclusion
    assert '--name' in args
    assert 'test' in args
    assert '--count' in args
    assert '42' in args
    assert '--verbose' in args


def test_typeddict_to_cli_args_with_positionals():
    class TestDict(t.TypedDict):
        pos1: t.Annotated[str, 'positional']
        pos_multi: t.Annotated[list[str], 'positional', '>= 0']
        flag: bool
        option: str

    # Create a dictionary that would be an instance of TestDict
    data: TestDict = {
        'pos1': 'value1',
        'pos_multi': ['a', 'b', 'c'],
        'flag': True,
        'option': 'opt_val'
    }

    args = typeddict_to_cli_args(data, TestDict)

    # The positionals should come first in order
    assert args[0] == 'value1'
    assert args[1:4] == ['a', 'b', 'c']

    # Check for inclusion of optional arguments
    assert '--flag' in args
    assert '--option' in args
    assert 'opt_val' in args


def test_typeddict_to_cli_args_with_literal():
    class TestDict(t.TypedDict):
        mode: t.Literal["fast", "slow"]
        level: t.Annotated[t.Literal[1, 2, 3], 'positional']

    data = {
        'mode': 'fast',
        'level': 2
    }

    args = typeddict_to_cli_args(data, TestDict)

    assert args[0] == '2'  # Positional comes first
    assert '--mode' in args
    assert 'fast' in args


## hooman:

def test_list_repeat():
    class MyConfigDict(t.TypedDict):
        repeatme: list[str]

    a = parse_args_from_typeddict(MyConfigDict, ["--repeatme", "once"])
    b = parse_args_from_typeddict(MyConfigDict, ["--repeatme", "once", "--repeatme", "twice"])

    assert a["repeatme"] == ["once"]
    assert b["repeatme"] == ["once", "twice"]

    assert typeddict_to_cli_args(a) == ['--repeatme', 'once']
    assert typeddict_to_cli_args(b) == ['--repeatme', 'once', '--repeatme', 'twice']
