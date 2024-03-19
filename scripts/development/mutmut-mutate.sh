if [ -e .mutmut-cache ]; then
  echo "Removing .mutmut-cache"
  rm .mutmut-cache
fi

python3 scripts/make_command_of_run.py

bash temporary/mutmut-run.sh
