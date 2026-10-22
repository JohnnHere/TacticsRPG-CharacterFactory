$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$taskRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $taskRoot
try {
    New-Item -ItemType Directory -Path tmp/tools -Force | Out-Null
    if (!(Test-Path -LiteralPath tmp/tools/uv/uv.exe)) {
        Invoke-WebRequest -Uri 'https://github.com/astral-sh/uv/releases/download/0.13.1/uv-x86_64-pc-windows-msvc.zip' -OutFile tmp/tools/uv.zip
        Expand-Archive -LiteralPath tmp/tools/uv.zip -DestinationPath tmp/tools/uv -Force
    }
    if (!(Test-Path -LiteralPath tmp/tools/pixel-art-fixer/.git)) {
        git clone --depth 1 --no-checkout https://github.com/Retro-Diffusion/pixel-art-fixer.git tmp/tools/pixel-art-fixer
        if ($LASTEXITCODE) { throw 'Pixel Art Fixer clone failed' }
        git -C tmp/tools/pixel-art-fixer fetch --depth 1 origin ef376e57e1c272633ca2dbf5f29ec3fcf6596465
        if ($LASTEXITCODE) { throw 'Pinned commit fetch failed' }
        git -C tmp/tools/pixel-art-fixer checkout --detach ef376e57e1c272633ca2dbf5f29ec3fcf6596465
        if ($LASTEXITCODE) { throw 'Pinned commit checkout failed' }
    }
    $taskRevision = git -C tmp/tools/pixel-art-fixer rev-parse HEAD
    if ($taskRevision -ne 'ef376e57e1c272633ca2dbf5f29ec3fcf6596465') {
        throw 'Existing Pixel Art Fixer checkout has a different revision; preserved without modification.'
    }
    if (!(Test-Path -LiteralPath tmp/pixel-venv/Scripts/python.exe)) {
        & ./tmp/tools/uv/uv.exe venv --python 3.12.15 tmp/pixel-venv
        if ($LASTEXITCODE) { throw 'Python environment creation failed' }
    }
    & ./tmp/tools/uv/uv.exe pip install --python tmp/pixel-venv/Scripts/python.exe -r tools/pixel-production-requirements.txt
    if ($LASTEXITCODE) { throw 'Pixel dependencies installation failed' }
    & ./tmp/tools/uv/uv.exe pip install --python tmp/pixel-venv/Scripts/python.exe --no-deps -e tmp/tools/pixel-art-fixer/python
    if ($LASTEXITCODE) { throw 'Pixel Art Fixer installation failed' }
    if (!(Test-Path -LiteralPath tmp/tools/libresprite/libresprite.exe)) {
        Invoke-WebRequest -Uri 'https://github.com/LibreSprite/LibreSprite/releases/download/v1.3/libresprite-v1.3-windows-x86_64.zip' -OutFile tmp/tools/libresprite.zip
        Expand-Archive -LiteralPath tmp/tools/libresprite.zip -DestinationPath tmp/tools/libresprite -Force
    }
    Write-Output 'Pixel tools ready in tmp/: uv 0.13.1, CPython 3.12.15, pinned Pixel Art Fixer, LibreSprite 1.3 portable.'
}
finally { Pop-Location }
