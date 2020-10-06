# Github Release Notes Builder

Small python script to build Release Notes based on Github Milestone.
Script get all PRs attached to a given milestone and leverage J2 template to render release notes.

## Installation

```shell
$ pip install git+https://github.com/titom73/gh-release-notes-builder.git
```

## Usage

### Generic use

```shell
$ release-notes-github -r <YOUR REPOSITORY> -m <YOUR MILESTONE>
```

`YOUR REPOSITORY` should be like `username/repo` and `YOUR MILESTONE` is what you configured in your project.

By default, script uses a generic template provided [here](inetsix_release_notes_builder/templates/default.j2)

### Save Release Notes to a file

```
$ release-notes-github -r <YOUR REPOSITORY> -m <YOUR MILESTONE> -o release-note.md
```

### Use a specific template

```shell
$ release-notes-github -r <YOUR REPOSITORY> -m <YOUR MILESTONE> -t {avd|cvp}.j2
```

### Display help message

```shell
$ release-notes-github -h
usage: release-notes-github [-h] [-r REPOSITORY] [-m MILESTONE] [-t TEMPLATE]
                     [-o OUTPUT] [-v VERBOSITY]

Cloudvision Authentication stress script

optional arguments:
  -h, --help            show this help message and exit
  -r REPOSITORY, --repository REPOSITORY
                        GH Repository like org/repo
  -m MILESTONE, --milestone MILESTONE
                        Milestone
  -t TEMPLATE, --template TEMPLATE
                        Path to template
  -o OUTPUT, --output OUTPUT
                        File to save release-notes
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbose level (debug / info / warning / error /
                        critical)
```

## LICENSE

Project is published under [GNU GPLv3 License](LICENSE)
