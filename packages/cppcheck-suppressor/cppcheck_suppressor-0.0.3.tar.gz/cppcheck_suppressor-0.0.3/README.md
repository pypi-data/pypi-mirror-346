# cppcheck-suppressor

A tool that creates suppression file from Cppcheck results that can be used as a baseline to run further Cppcheck analysis, highlighting any new errors in the analyzed code.

__Setting a baseline helps to see new issues. However, all the errors reported by Cppcheck before setting a baseline should be reviewed with care.__

## Installation

Install the latest cppcheck-suppressor with

```bash
pipx install cppcheck-suppressor
```

or the python package with

```bash
pip install cppcheck-suppressor
```

## Usage

To use the cppcheck-suppressor together with Cppcheck, first make a throughout analysis of your project with Cppcheck without any suppressions and save the results to a xml file:

```bash
cppcheck --xml src/ 2> cppcheck_errors.xml
```

This assumes your sources are in the `src/` folder. Use the arguments for Cppcheck that you would use otherwise - just no `--suppress` or `--suppress-xml` arguments, and keep the `--xml` argument.

After creating the results with Cppcheck, use the cppcheck-suppressor to create a baseline from the results:

```bash
cppcheck-suppressor --file cppcheck_errors.xml --output baseline.xml
```

or

```bash
python -m cppcheck_suppressor --file cppcheck_errors.xml --output baseline.xml
```

And finally use the baseline in the further Cppcheck analyses:

```bash
cppcheck --suppress-xml=baseline.xml src/
```

Now, Cppcheck reports only new issues from the project. The baseline should be updated - especially when any errors are solved from the project.
