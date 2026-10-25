"""Bonus challenge A: the network tools page.

A little "reachability check": you type a host and it runs a shell command to
look it up. The host you type is pasted into a shell command string, so shell
metacharacters in the input let you tack on a SECOND command of your choice --
this is command (OS) injection.

YOUR JOB: `run_check` must treat the whole input as a single host argument, so
no extra command can ever run, whatever punctuation is in it. Validating the
host and NOT using a shell is the fix.

HINT: subprocess.run(["echo", "resolving", host]) with shell=False. Pass the
arguments as a list, never as one formatted string with shell=True.
"""
import subprocess


def run_check(host):
    """Return the tool output as text. THIS IS THE VULNERABLE PART."""
    cmd = f"echo resolving {host}"
    try:
        out = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=5
        )
        return out.stdout + out.stderr
    except subprocess.SubprocessError:
        return "lookup failed"


def handle(request, session):
    if not session.get("user"):
        return ("please log in first", 401)
    output = ""
    if request.method == "POST":
        output = f"<pre>{run_check(request.form.get('host', ''))}</pre>"
    return (
        "<h1>reachability check</h1>"
        '<form method="post"><input name="host" placeholder="hostname">'
        "<button>check</button></form>" + output
    )
