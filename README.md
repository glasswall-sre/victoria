<div align="center" style="text-align:center">

# V.I.C.T.O.R.I.A.

![Victoria demo](https://raw.githubusercontent.com/glasswall-sre/victoria/master/img/victoria.gif)

**V**ery **I**mportant **C**ommands for **T**oil **O**ptimization: **R**educing **I**nessential **A**ctivities.

Victoria is the SRE toolbelt—a single CLI with multiple pluggable
subcommands for automating any number of 'toil' tasks that inhibit SRE
productivity.

<img align="center" src="https://sonarcloud.io/api/project_badges/measure?project=victoria&metric=alert_status">
<img align="center" src="https://sonarcloud.io/api/project_badges/measure?project=victoria&metric=sqale_rating">
<img align="center" src="https://sonarcloud.io/api/project_badges/measure?project=victoria&metric=reliability_rating">
<img align="center" src="https://codecov.io/gh/glasswall-sre/victoria/branch/master/graph/badge.svg">
<img align="center" src="https://img.shields.io/github/license/glasswall-sre/victoria">
<img align="center" src="https://img.shields.io/github/workflow/status/glasswall-sre/victoria/CD">
<img align="center" src="https://img.shields.io/pypi/pyversions/victoria">
<img align="center" src="https://img.shields.io/pypi/v/victoria">
</div>

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

## Development guide

### Prerequisites
- Python
- Pipenv

### Quick start
1. Clone the repo.
2. Run `pipenv sync --dev`.
3. You're good to go.
