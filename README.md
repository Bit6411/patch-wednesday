# patch wednesday

Last week you broke things. This week you fix them.

This is a small members-portal web app with a few **deliberate security bugs**
baked in. Your job is the blue-team side: find each bug, understand the exploit,
and **patch it properly** — not just block the one payload you were shown.

A patch counts when the tests pass. Each bug has two kinds of test:

- an **exploit test** that fails while the bug is there, and
- **normal-use tests** that check the feature still works.

So you can't "fix" it by deleting the feature, and you can't fix it with a
blocklist of bad characters — the exploit tests try several shapes of the same
trick.

---

## Setup (about two minutes)

You need **Python 3.10+** and **git**.

```bash
git clone <your copy of this repo>
cd patch-wednesday
python -m venv .venv
source .venv/bin/activate      # windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run the app and click around:

```bash
python app.py                  # http://127.0.0.1:5000
```

Run the tests:

```bash
pytest -q
```

You'll see some tests fail. Each failure is a bug to fix. **Fixing a bug makes
its test go green.**

## The loop

1. `pytest` — see what's failing.
2. Open the challenge file it names (under `challenges/`). The top of each file
   explains the bug and what a proper fix looks like.
3. Fix the one function it points at.
4. `pytest` again. Green? Commit and push:
   ```bash
   git add -A
   git commit -m "fix the login query"
   git push
   ```
5. Your push runs the tests on GitHub too (the **Actions** tab). A green tick on
   your commit means it's really fixed.

> Read your change before you ship it: `git diff` shows what you're about to
> commit. If a fix breaks a feature, `git restore <file>` puts it back.

## The bugs

Fix them in roughly this order — top is easiest.

| file | what's wrong |
|---|---|
| `challenges/login.py` | the login query is built from your input (we fix this one together) |
| `challenges/notes.py` | you can read other people's notes by changing the URL |
| `challenges/files.py` | the download can be tricked into reading files outside its folder |
| `challenges/tools.py` | *(bonus)* the host box can run extra shell commands |
| `challenges/redirect_after_login.py` | *(bonus)* the `?next=` redirect can point off-site |

## What you'll pick up

- the git loop: clone → change → `diff` → commit → push
- how automated tests decide whether a change is good enough to ship
- why a real fix beats a blocklist — and five classes of web bug you'll meet
  everywhere: SQL injection, IDOR, path traversal, command injection, open
  redirect

Built for KCL Cyber Security Society.
