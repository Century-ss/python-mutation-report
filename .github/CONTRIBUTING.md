# Contribution guidelines

## Commands
- Run mutation test with `mutmut run --paths-to-mutate {src-directory} --tests-dir {test-directory} --runner "pytest {test-directory}"`
  example:`mutmut run --paths-to-mutate pipenv-project/src --tests-dir pipenv-project/tests --runner "pytest pipenv-project/tests"`

- Show mutation report with `mutmut show all`

- Output mutation test results to a text file. `mutmut show all > result.txt`

- Output mutation test results to a html file. `mutmut html`

## TODO
- reshape output of mutation reort text file
- change repository name python to pytest
- support multiple src or test directories
