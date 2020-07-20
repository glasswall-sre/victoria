# V.I.C.T.O.R.I.A.

![Victoria demo](https://raw.githubusercontent.com/glasswall-sre/victoria/master/img/victoria.gif)

**V**ery **I**mportant **C**ommands for **T**oil **O**ptimization: **R**educing **I**nessential **A**ctivities.

Victoria is the SRE toolbelt—a single CLI with multiple pluggable
subcommands for automating any number of 'toil' tasks that inhibit SRE
productivity.

[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/4111/badge)](https://bestpractices.coreinfrastructure.org/projects/4111)
![Quality gate status](https://sonarcloud.io/api/project_badges/measure?project=victoria&metric=alert_status)
![Maintainability rating](https://sonarcloud.io/api/project_badges/measure?project=victoria&metric=sqale_rating)
![Reliability rating](https://sonarcloud.io/api/project_badges/measure?project=victoria&metric=reliability_rating)
![Code coverage](https://codecov.io/gh/glasswall-sre/victoria/branch/master/graph/badge.svg)
![License](https://img.shields.io/github/license/glasswall-sre/victoria)
![Build status](https://img.shields.io/github/workflow/status/glasswall-sre/victoria/CD)
![Python versions](https://img.shields.io/pypi/pyversions/victoria)
![PyPI version](https://img.shields.io/pypi/v/victoria)


![Best practices badge](https://raw.githubusercontent.com/glasswall-sre/victoria/master/img/cii-badge.png)

## Features
- Plugin architecture for easy extension
- Store config for plugins in cloud storage
  - Azure Blob Storage
- Encrypt secret config data at rest using cloud encruption provider
  - Azure Key Vault

## Prerequisites
- Python 3.6+
- Pip

## Installation
```terminal
pip install -U victoria
```

## Documentation
The documentation [can be found here](https://sre.glasswallsolutions.com/victoria/index.html).

## License
[Victoria is licensed under the MIT license.](https://github.com/glasswall-sre/victoria/blob/master/LICENSE)

## Contribution

### Bug reports
[You can submit a bug report here.](https://github.com/glasswall-sre/victoria/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D+%7BDescription+of+issue%7D)

### Feature requests
[You can request a new feature here.](https://github.com/glasswall-sre/victoria/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=%5BREQUEST%5D)

### Vulnerability reports
We prefer vulnerabilities to be reported in private so as to minimise their
impact (so we can fix them before they are exploited!). To this end, please
email any security vulnerability reports to '[sre@glasswallsolutions.com](mailto://sre@glasswallsolutions.com)'.
We would appreciate it if you use the issue template in the link below.
All vulnerabilities will be acknowledged within one business day.

[You can publicly report a security vulnerability here.](https://github.com/glasswall-sre/victoria/issues/new?assignees=&labels=Incident%2C+bug&template=vulnerability-report.md&title=%5BVULNERABILITY%5D)

### Pull requests
We accept pull requests! To contribute: 

1. Pick up an unassigned issue from [our issue board](https://github.com/glasswall-sre/victoria/issues).
   Assign yourself to the issue so other people know you're working on it.
2. Work on your code in a feature branch that's got a descriptive name (like `rework-fancy-integrator`).
3. Follow the [Google style guide for Python](http://google.github.io/styleguide/pyguide.html).
   Every piece of code needs to be documented with [Google-style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
   We use [pylint](https://pypi.org/project/pylint/) to lint our code.
   We run pylint without the 'convention' and 'refactor' message classes.
   You can lint your code with: `poetry run pylint victoria --disable="C,R"`.
   We use [yapf](https://github.com/google/yapf) to automatically format our code. We recommend having it
   format the code whenever you save.
4. Make commits for each part of your pull request. Try not to make too many (if it's a small issue you may only need one).
   We try to use [the imperative mood](https://chris.beams.io/posts/git-commit/#imperative)
   in commit message subjects.
5. We expect all new code to have at least 80% test coverage. This is enforced by [Codecov](https://codecov.io/gh/glasswall-sre/victoria).
6. To run tests locally and check coverage, use: `poetry run pytest tests/ --cov=victoria`.
7. When ready to merge, create a pull request from your branch into master.
8. Make sure you link your pull request to the issue(s) it addresses.
9. The [CI build](https://github.com/glasswall-sre/victoria/actions?query=workflow%3ACI) will run 
   for your pull request. If it fails then it cannot be merged. Inspect the output, figure
   out why it failed, and fix the problem.
   The CI build will lint your code, run tests, and send coverage/code to Codecov
   and [SonarCloud](https://sonarcloud.io/dashboard?id=victoria). 
11. Someone will review your pull request and suggest changes if necessary.
12. When everything is signed off, your pull request will be merged! Congrats.

## Development guide

### Prerequisites
- Python 3.6+
- Poetry

### Quick start
1. Clone the repo.
2. Run `poetry install`.
3. You're good to go.
