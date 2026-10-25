"""Tests for bonus challenge A: tools (command injection).

While the bug is present, test_injection_does_not_run FAILS (a crafted host runs
a second command that creates a sentinel file). After you drop the shell and pass
the host as a single argument, all pass. These tests never touch the network.
"""
import os

from challenges.tools import run_check


def test_legit_host_is_echoed():
    out = run_check("cybersoc.kcl.ac.uk")
    assert "cybersoc.kcl.ac.uk" in out


def test_injection_does_not_run(tmp_path):
    sentinel = tmp_path / "pwned"
    # a host value that, if dropped into a shell, would run a second command
    payload = f"x; touch {sentinel}"
    run_check(payload)
    assert not sentinel.exists(), (
        "the input ran a second shell command -- it must be treated as one "
        "host argument, not pasted into a shell string"
    )
