import pytest

from main import main
import sys


@pytest.mark.asyncio
async def test_run_script_without_args(monkeypatch, capsys):
    mock_argv = []
    monkeypatch.setattr(sys, "argv", mock_argv)

    with pytest.raises(SystemExit):
        await main()

    captured = capsys.readouterr()
    assert captured.err == "Please enter urls."


@pytest.mark.asyncio
async def test_run_script_with_correct_args(monkeypatch, capsys):
    mock_argv = [None, "https://www.google.com/"]
    monkeypatch.setattr(sys, "argv", mock_argv)

    await main()

    captured = capsys.readouterr()
    assert captured.out == "{'https://www.google.com/': {'GET': 200, 'HEAD': 200}}\n"


@pytest.mark.asyncio
async def test_run_script_with_correct_single_arg(monkeypatch, capsys):
    mock_argv = [None, "https://www.google.com/"]
    monkeypatch.setattr(sys, "argv", mock_argv)

    await main()

    captured = capsys.readouterr()
    assert captured.out == "{'https://www.google.com/': {'GET': 200, 'HEAD': 200}}\n"


@pytest.mark.asyncio
async def test_run_script_with_diff_args(monkeypatch, capsys):
    mock_argv = [
        None,
        "https://www.google.com/",
        "some string",
        "https://www.linkedin.com/feed/",
    ]
    monkeypatch.setattr(sys, "argv", mock_argv)

    await main()

    captured = capsys.readouterr()
    assert len(captured.out.split("\n")) == 10
