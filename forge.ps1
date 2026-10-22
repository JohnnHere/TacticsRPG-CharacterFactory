$ErrorActionPreference = 'Stop'
& node (Join-Path $PSScriptRoot 'src/cli.mjs') @args
exit $LASTEXITCODE
