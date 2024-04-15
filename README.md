# python-mutation-report

![Python Version](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![GitHub Release](https://img.shields.io/github/v/release/Century-ss/python-mutation-report)
![GitHub Release Date](https://img.shields.io/github/release-date/Century-ss/python-mutation-report)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Century-ss/python-mutation-report/ubuntu-and-macos-test.yml?label=acceptance%20test)
![GitHub License](https://img.shields.io/github/license/Century-ss/python-mutation-report?color=blue)

This python-mutation-report performs a mutation test on the changed lines in the pull request with `mutmut` of the pip package, and comments the mutation test summary as shown in the [example](docs/sample_summary_comment.md) below.

<img src="docs/sample_summary_comment.png" width="700">

## Example usage in workflow
- If the directory structure is as follows.
  ```
  .
  ├── README.md
  └── python-project
      ├── Pipfile
      ├── Pipfile.lock
      ├── src
      │   ├── __init__.py
      │   ├── src_1.py
      │   └──  src_2.py
      └── tests
          ├── __init__.py
          ├── test_src_1.py
          └──  test_src_2.py
  ```

```yml
on:
  pull_request:
    paths:
      - "python-project/src/**"
      - "python-project/tests/**"

jobs:
  mutation-testing-report:
    runs-on: ubuntu-latest
    name: Mutation testing report
    timeout-minutes: 15
    permissions:
      pull-requests: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      - uses: Century-ss/python-mutation-report@v1
        with:
          lock-file-path: "python-project/Pipfile.lock"
          src-directory: "python-project/src"
          test-directory: "python-project/tests"
          where-to-run-test: "python-project"
          python-version: "3.11"
```

## Notes
- Only `pull_request` events are supported.
- Perform mutation test only on `pull_request` changed lines in files under `src-directory`.
- Only `ubuntu` and `mac os` runners are supported.
- Only `pytest` is supported as a test module.
- `Write permission for pull_request` and `read permission for contents` is required.
- If there are many changed files in the pull_request, it may take longer, so it is recommended to set a `timeout-minutes`.

## How to find a combination of test and src files
- If the change diff has a `hoge.py` in the src file, trying to find `test_hoge.py` in the test directory
  - If `test_hoge.py` is found, include `hoge.py` and `test_hoge.py` in the mutation test.
  - If `test_hoge.py` is not found, not include `hoge.py` in the mutation test.
  - If multiple `test_hoge.py` is found, include them all in the mutation test.

## Inputs
- Required parameters
  - `lock-file-path`: Lock file path for installing python dependencies. The following lock files are supported.
    - `requirements.txt` of pip.
    - `Pipfile.lock` of pipenv
    - `requirements-dev.lock` or `requirements.lock` of rye.
  - `src-directory`: Directory path of the source to plant the mutant.
  - `test-directory`: Directory path of the test to evaluate the mutant.
- Optional parameters.
  - `where-to-run-test`: Path to the location where　test is run. Default is `"."`, it runs in the repository root directory.
  - `python-version`: Version of python used. Default is `"3.11"`

## Outputs
No outputs.
