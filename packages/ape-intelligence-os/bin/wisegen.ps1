$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir
node "$RootDir\src\cli.mjs" @args
exit $LASTEXITCODE
