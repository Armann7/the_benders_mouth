env/check_pylint.cmd

@IF ERRORLEVEL 0 (
   env/check_mypy.cmd
)

@IF ERRORLEVEL 0 (
   env/check_bandit.cmd
)