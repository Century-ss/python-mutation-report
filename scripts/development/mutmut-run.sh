if [ -e .mutmut-cache ]; then
  echo "Removing .mutmut-cache"
  rm .mutmut-cache
fi

mutmut run --paths-to-mutate pipenv-project/src \
--tests-dir pipenv-project/tests \
--runner 'pytest pipenv-project/tests' > results/run_result.txt
