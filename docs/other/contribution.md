# Contributing to Promptulate

Hi there! Thank you for even being interested in contributing to Promptulate. As an open-source project in a rapidly developing field, we are extremely open to contributions, whether they involve new features, improved infrastructure, better documentation, or bug fixes.

## Guidelines

### 👩‍💻 Contributing Code

To contribute to this project, please follow the ["fork and pull request"](https://docs.github.com/en/get-started/quickstart/contributing-to-projects) workflow.
Please do not try to push directly to this repo unless you are a maintainer.

Please follow the checked-in pull request template when opening pull requests. Note related issues and tag relevant
maintainers.

Pull requests cannot land without passing the formatting, linting, and testing checks first. See [Testing](#testing) and
[Formatting and Linting](#formatting-and-linting) for how to run these checks locally.

It's essential that we maintain great documentation and testing. If you:
- Fix a bug
  - Add a relevant unit or integration test when possible. These live in `tests`.
- Make an improvement
  - Update any affected example notebooks and documentation. These live in `docs`.
  - Update unit and integration tests when relevant.
- Add a feature
  - Add a demo notebook in `docs/`.
  - Add unit and integration tests.

We are a small, progress-oriented team. If there's something you'd like to add or change, opening a pull request is the
best way to get our attention.

### 🚩GitHub Issues

Our [issues](https://github.com/Undertone0809/promptulate/issues) page is kept up to date with bugs, improvements, and feature requests.

There is a taxonomy of labels to help with sorting and discovery of issues of interest. Please use these to help organize issues.

If you start working on an issue, please assign it to yourself.

If you are adding an issue, please try to keep it focused on a single, modular bug/improvement/feature.
If two issues are related, or blocking, please link them rather than combining them.

We will try to keep these issues as up-to-date as possible, though
with the rapid rate of development in this field some may get out of date.
If you notice this happening, please let us know.

### 🙋Getting Help

Our goal is to have the simplest developer setup possible. Should you experience any difficulty getting setup, please
contact a maintainer! Not only do we want to help get you unblocked, but we also want to make sure that the process is
smooth for future contributors.

In a similar vein, we do enforce certain linting, formatting, and documentation standards in the codebase.
If you are finding these difficult (or even just annoying) to work with, feel free to contact a maintainer for help -
we do not want these to get in the way of getting good code into the codebase.

## 🚀 Quick Start

This quick start guide explains how to run the repository locally.

### Dependency Management: Poetry and other env/dependency managers

This project utilizes [Poetry](https://python-poetry.org/) v1.6.1+ as a dependency manager.

❗Note: *Before installing Poetry*, if you use `Conda`, create and activate a new Conda env (e.g. `conda create -n langchain python=3.9`)

Install Poetry: **[documentation on how to install it](https://python-poetry.org/docs/#installation)**.

❗Note: If you use `Conda` or `Pyenv` as your environment/package manager, after installing Poetry,
tell Poetry to use the virtualenv python environment (`poetry config virtualenvs.prefer-active-python true`)

**Environment**
- Python >= 3.8
- make

> This project uses make to build supporting facilities for the project. With the ability of makefiles, it is easy to integrate and run modules such as test and lint. Please ensure that make is installed on your computer.
> 
> [how to install and use make in windows?](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows)

Run the following code:

```shell
git clone https://github.com/Undertone0809/promptulate 
```

Install third-party packages:

```shell
pip install poetry
make install
```

This project uses a code syntax checking tool. If you want to submit a PR, you need to run `make formatting` for code specification formatting before committing, and run `make lint` to pass syntax and unit testing checks.
