# Forklister - search for active forks of repository

## Goals

Forklister allows you to find forks of repository that are actively developed and not just someone's stash

### What's different

Unlike services like [GitPop2](https://github.com/AndreMiras/gitpop2) and [active-forks](https://github.com/techgaun/active-forks), forklister is:

- Comparing forks to origin by counts of commits ahead and behind
- Standalone solution, so all your searches are private
- Saving results in report file for you

### Installation

#### Prerequisites

- python3
- pipenv package manager
  - you can find installation instructions [here](https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv) 

#### How to install

- Clone this repository and `cd` into it
- Run `pipenv install`

### Usage

- Run `pipenv shell` to activate project virtual environment
- Run `exit` to deactivate environment after work is done

#### Basic scenario

`
python3 forklister.py username/repository
`

will create file username_repository.csv in working directory

#### Getting help

`
python3 forklister.py --help
`

#### Arguments

- `-o, --output` output file name
- `-f, --format` output file format. Can be `csv` or `json`, default is `csv`
- `-sb, --sort-by` sort forks by property, see help. Default is `default`
- `-so, --sort-order` `asc` or `desc`, default is `desc`
- `-t, --token` Github API key
- `-tv, --token-var` environment variable that stores Github API key
