# Security Policy

Rashinban is a local, dependency-free tool that reads and writes text — its
attack surface is small, but reports are welcome.

## Reporting a vulnerability

**Please do not open a public issue for a vulnerability.** Use GitHub's private
reporting: **Security → Report a vulnerability** on this repo.

Relevant classes:

- a crafted `/goal` file that makes a script crash, hang, or write outside its
  intended paths,
- the plans-store bridge writing anywhere other than the inbox file,
- any path traversal in the scripts.

You can expect an acknowledgement within a few days, and credit for confirmed
issues unless you prefer otherwise.

## Supported versions

Rashinban is pre-1.0; the latest `main` is supported. Pin a tag for
reproducibility.
