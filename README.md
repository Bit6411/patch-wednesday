# patch wednesday

## Application Overview and Testing Approach (added by Bit6411)

This project is a lightweight Flask-based members portal. Each security vulnerability is isolated in its own file within the `challenges/` directory.

Each challenge includes two categories of tests:

- **Exploit tests**: Designed to demonstrate the vulnerability by attempting to exploit it. These tests should fail when the vulnerability is present and pass once the appropriate security patch has been implemented.
- **Functional tests**: Verify that the application's intended functionality continues to work correctly after the vulnerability has been addressed.

This testing approach ensures that security fixes address the underlying vulnerability without compromising legitimate application behaviour.

Simply removing or disabling vulnerable functionality is not considered a valid solution. Similarly, implementing character-based blocklists or other superficial input restrictions is insufficient, as exploit tests use multiple variations of the same attack technique.

The objective is to implement robust, security-focused fixes that eliminate the underlying vulnerabilities while preserving the application's intended functionality.

## CVE Vulnerabilities and Patches (added by Bit6411)

| Original File | Related CVE (similar vulnerability) | Vulnerability explained in this context | Patch details |
| --- | --- | --- | --- |
| [challenges/login.py](https://github.com/Bit6411/patch-wednesday/blob/23f58d1e17d2814572ce726246d8b64570a02793/challenges/login.py) | [CVE-2014-3704](https://nvd.nist.gov/vuln/detail/CVE-2014-3704) | Vulnerable to SQL injection, query can return user session when logging in without a valid password if malicious input is provided, such as "`' OR '1'='1' --`". | Used parameterized queries instead of building SQL string manually. Patch deployed in commit [a8cf462](https://github.com/Bit6411/patch-wednesday/commit/a8cf4625e0527cfb7a0eb245a6ab0f61f8e45852). |
| [challenges/notes.py](https://github.com/Bit6411/patch-wednesday/blob/23f58d1e17d2814572ce726246d8b64570a02793/challenges/notes.py) | [CVE-2023-4836](https://nvd.nist.gov/vuln/detail/CVE-2023-4836) | Insecure Direct Object Reference (IDOR) vulnerability. This means a user is able to access another user's notes by manipulating the note ID, when a user should only be able to access their own notes. | Check if owner of the note being access matches the identity of the user requesting it in backend logic. Patch deployed in commit [9c0beca](https://github.com/Bit6411/patch-wednesday/commit/9c0becab34b2a8df53244cdf687007a18e9040c3). |
| [challenges/files.py](https://github.com/Bit6411/patch-wednesday/blob/23f58d1e17d2814572ce726246d8b64570a02793/challenges/files.py) | [CVE-2021-41773](https://nvd.nist.gov/vuln/detail/CVE-2021-41773) | Path traversal. Files outside the directory where all files should be served can be accessed, for example by going up one directory level using "`../`". | Resolve the given path constructed by the `name` query parameter. Check if the resolved file path begins with the file path to the directory where files are being served. Patch deployed in commit [6dfc338](https://github.com/Bit6411/patch-wednesday/commit/6dfc338ba34ea1154c3f52c765b3fd4c5c53656c). |
| [challenges/redirect_after_login.py](https://github.com/Bit6411/patch-wednesday/blob/23f58d1e17d2814572ce726246d8b64570a02793/challenges/redirect_after_login.py) | [CVE-2024-54050](https://nvd.nist.gov/vuln/detail/CVE-2024-54050) | Pending review ❌| Pending review ❌|
| [challenges/tools.py](https://github.com/Bit6411/patch-wednesday/blob/23f58d1e17d2814572ce726246d8b64570a02793/challenges/tools.py) | [CVE-2014-6271](https://nvd.nist.gov/vuln/detail/CVE-2014-6271) | Pending review ❌ | Pending review ❌| 


## Blue team instructions (original README.md)

(Following was already explained at [the beginning of this README](#application-overview-and-testing-approach-added-by-bit6411) for clarity on the purpose of this repo.)

~~last week you broke things. this week you fix them.~~

~~this is a small members-portal web app with five **deliberate security bugs**~~
~~in it. your job is the blue-team side: find each bug, understand why it's a~~
problem, and **patch it properly**, not just block the one input you were shown.~~

~~a fix counts when the tests pass. each bug has two kinds of test:~~

~~- an **exploit test** that fails while the bug is there, and~~
~~- **normal-use tests** that check the feature still works.~~

~~so deleting the feature doesn't count, and neither does a blocklist of "bad~~
~~characters": the exploit tests try several versions of the same trick.~~

---

## what you need

- a **github account**
- **git** ([git-scm.com/downloads](https://git-scm.com/downloads), on windows
  the default installer options are fine)
- an editor. vs code is good, but anything works.

you **don't** need python to take part: github runs the tests for you every time
you push. if you do have python and want to run things on your laptop, see
[running it locally](#running-it-locally-optional) at the bottom.

## 1. get your own copy

1. click the green **use this template** button at the top of this page, then
   **create a new repository**. give it any name and keep it **public**.
2. on your new repo, click the green **code** button and copy the https link.
3. in a terminal (on windows: **git bash**, which came with git):

```
git clone <the link you copied>
cd <your repo name>
```

open the folder in your editor.

## 2. see what's broken

on your repo's page on github, open the **actions** tab. your first run has a
**red cross**: that's normal, because the bugs are still in there. click the
run, then **pytest**, and you'll see five failing tests, one per bug.

no run there yet? click **tests** on the left, then **run workflow**.

## 3. the loop

1. pick a bug from the table below and open its file in `challenges/`. the top
   of each file explains the bug and points at the function to fix.
2. fix that one function.
3. ship it:

```
git add .
git commit -m "fix the notes ownership check"
git push
```

4. go back to the **actions** tab. a new run starts within a few seconds. one
   less failure means that fix worked. **all green = every bug patched.**

if github asks you to log in when you push, sign in through the browser window
that pops up.

> **before you commit**, run `git diff` to read exactly what you changed.
> **broke something?** `git restore <file>` puts a file back to your last commit.

## the bugs

top is easiest.

| file | what's wrong |
|---|---|
| `challenges/login.py` | the login query is built from what you type (we fix this one together) |
| `challenges/notes.py` | you can read other people's notes by changing the number in the url |
| `challenges/files.py` | the download can be tricked into reading files outside its folder |
| `challenges/tools.py` | *(bonus)* the host box can run extra commands |
| `challenges/redirect_after_login.py` | *(bonus)* the `?next=` redirect can send you to another site |

## running it locally (optional)

needs **python 3.10+** ([python.org](https://www.python.org/downloads/); on
windows, tick **add python to path** in the installer).

**windows (powershell):**

```
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest
python app.py
```

if powershell says running scripts is disabled, run
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again.

**mac / linux:**

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
python app.py
```

`python app.py` serves the app at http://127.0.0.1:5000 (users: `alice` /
`alpaca`, `bob` / `bonobo`). on windows, one bonus test is skipped locally because
`cmd.exe` uses different shell syntax. github actions still grades it, so trust
the tick there.

## what you'll pick up

- the git loop: clone, change, diff, commit, push
- how automated tests decide whether a change is good enough to ship
- why a real fix beats a blocklist, and five kinds of web bug you'll see
  everywhere: sql injection, idor, path traversal, command injection and open
  redirects

made for kcl cyber security society · [kclcybersoc.org.uk](https://kclcybersoc.org.uk)
