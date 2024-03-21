# Contribution guidelines

## Commands
- Run mutation test with `mutmut run --paths-to-mutate {src-directory} --tests-dir {test-directory} --runner "pytest {test-directory}"`
  example:`mutmut run --paths-to-mutate pipenv-project/src --tests-dir pipenv-project/tests --runner "pytest pipenv-project/tests"`

- Show mutation report with `mutmut show all`
- Output mutation test results to a html report. `mutmut html`
- Output mutation test results to a junitxml report. `mutmut junitxml --suspicious-policy=error > temporary/junit.xml`

- Delete .mutmut-cache before run mutation test. `rm .mutmut-cache`
