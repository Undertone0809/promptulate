# Contributing to Promptulate

Hi there! Thank you for even being interested in contributing to Promptulate. As an open-source project in a rapidly developing field, we are extremely open to contributions, whether they involve new features, improved infrastructure, better documentation, or bug fixes.

## Guidelines

### GitHub Actions

We use GitHub Actions to automate the testing and building process. If you encounter any issues with the GitHub Actions setup or need troubleshooting steps, please follow the instructions below.
- If the GitHub Actions run fails, please analyze the error logs and follow the troubleshooting steps provided below.

### Troubleshooting GitHub Actions

To troubleshoot GitHub Actions run failures, follow the steps below:
1. Analyze the error logs to identify the root cause of the failure.
2. Common issues that can cause GitHub Actions to fail include:
   - Invalid configuration files
   - Incorrect workflow setup
   - Dependency installation errors
   - Network connectivity issues
3. If you encounter a GitHub Actions run failure, please refer to the [GitHub Actions documentation](https://docs.github.com/en/actions) for troubleshooting tips and best practices.

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

**GitHub Actions Setup and Troubleshooting**

To set up GitHub Actions and troubleshoot run failures, follow the steps below:
1. Create a `.github/workflows` directory in the root of the repository.
2. Inside the directory, create a YAML file to define the GitHub Actions workflow.
3. Add the necessary jobs, steps, and triggers to the workflow file.
4. Commit and push the workflow file to your repository.

### Analyzing Error Logs and Common Issues

When analyzing the error logs from a failed GitHub Actions run, consider the following common issues:
- **Invalid configuration files:** Check if the workflow file or related configuration files have errors.
- **Incorrect workflow setup:** Ensure that the workflow is correctly configured with appropriate triggers and steps.
- **Dependency installation errors:** Look for errors related to package installations or dependencies.
- **Network connectivity issues:** Verify network access for package installations and other external resources.

If you need assistance with troubleshooting GitHub Actions run failures, please reach out to the maintainers for support. If you want to submit a PR, you need to run `make formatting` for code specification formatting before committing, and run `make lint` to pass syntax and unit testing checks.
