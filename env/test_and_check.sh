#!/bin/sh


# pytest
pytest $MAIN
if [ $? -ne 0 ]; then
  echo Pytest error
  exit 1
fi

# Mypy
mypy $MAIN
if [ $? -ne 0 ]; then
  echo MyPy checks error
  exit 1
fi


# bandit
bandit --configfile $MAIN/env/bandit.yaml -r $MAIN/app
if [ $? -ne 0 ]; then
  echo Bandit checks error
  exit 1
fi

