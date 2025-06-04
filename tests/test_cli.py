import pytest

from episteme.cli.main import get_parser
from unittest import mock


@mock.patch('sys.argv',['add_task', 'construct a self recursive mirror'])
def test_add_task():
    parser = get_parser()
    args = parser.parse_args()

    assert args.task == "construct a self recursive mirror"

def test_missing_task_arg_exits():
    parser = get_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])

def test_help_flag(capsys):
    parser = get_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(['--help'])
    out, err = capsys.readouterr()
    assert 'usage:' in out