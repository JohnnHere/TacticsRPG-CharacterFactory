$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$script=Join-Path $PSScriptRoot '../scripts/validate_character_assets.ps1'
$temp=Join-Path ([IO.Path]::GetTempPath()) ('character-art-tests-'+[guid]::NewGuid().ToString('N'))
[void](New-Item -ItemType Directory -Path $temp)
$passed=0
function Assert($condition,$message){if(-not $condition){throw $message}; $script:passed++}
function Make-Png($path,$ground=126,$alpha=255,$width=128,$rgb=$false){
    $format=if($rgb){[Drawing.Imaging.PixelFormat]::Format24bppRgb}else{[Drawing.Imaging.PixelFormat]::Format32bppArgb}
    $bmp=[Drawing.Bitmap]::new($width,128,$format)
    try {for($y=27;$y -le $ground;$y++){for($x=50;$x -lt 70;$x++){$bmp.SetPixel($x,$y,[Drawing.Color]::FromArgb($alpha,120,60,30))}}; $bmp.Save($path,[Drawing.Imaging.ImageFormat]::Png)}finally{$bmp.Dispose()}
}
function Run-Scan($dir,$profile){
    $pp=Join-Path $temp 'profile.json'; $op=Join-Path $temp 'report.json'
    $profile | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $pp -Encoding UTF8
    & powershell -NoProfile -ExecutionPolicy Bypass -File $script -AssetRoot $dir -ProfilePath $pp -OutputPath $op
    $script:lastExit=$LASTEXITCODE
    if(-not (Test-Path $op)){throw 'Validator produced no report'}
    Get-Content -LiteralPath $op -Raw | ConvertFrom-Json
}
function Has($r,$check,$status){@($r.checks | Where-Object {$_.check -eq $check -and $_.status -eq $status}).Count -gt 0}
try {
    $dir=Join-Path $temp 'assets'; [void](New-Item -ItemType Directory -Path $dir)
    $file=Join-Path $dir 'fixture_mvp1_static_128.png'
    $profile=@{prefix='fixture';requireMeta=$false;requireComplete=$false;counts=@{Idle=4}}
    Make-Png $file
    $r=Run-Scan $dir $profile
    Assert ($lastExit -eq 0 -and $r.summary.FAIL -eq 0) 'Valid RGBA fixture should pass'
    Assert (Has $r 'ground' 'PASS') 'Ground 126 must pass'
    Make-Png $file 125
    $r=Run-Scan $dir $profile
    Assert (Has $r 'ground' 'FAIL') 'Misalignment must fail'
    Assert ($lastExit -eq 1) 'FAIL must produce exit 1'
    $profile.exceptions=@{'fixture_mvp1_static_128.png|ground'='Test approved alternate contact'}
    $r=Run-Scan $dir $profile
    Assert (Has $r 'ground' 'WARNING') 'Documented exception must remain visible'
    $profile.Remove('exceptions')
    Make-Png $file 126 128
    $r=Run-Scan $dir $profile
    Assert (Has $r 'halo' 'WARNING') 'Partial alpha should warn'
    Make-Png $file 126 255 128 $true
    $r=Run-Scan $dir $profile
    Assert (Has $r 'alpha-channel' 'FAIL') 'RGB without alpha must fail'
    Make-Png $file 126 255 96
    $r=Run-Scan $dir $profile
    Assert (Has $r 'dimensions' 'FAIL') 'Wrong dimensions must fail'
    Make-Png $file
    $dirs=Join-Path $dir 'Directions'; [void](New-Item -ItemType Directory -Path $dirs)
    Copy-Item -LiteralPath $file -Destination (Join-Path $dirs 'fixture_dir_front_r.png')
    $r=Run-Scan $dir $profile
    Assert (Has $r 'duplicate' 'WARNING') 'Duplicate decoded pixels must warn'
    $profile.requireComplete=$true
    $r=Run-Scan $dir $profile
    Assert (Has $r 'required-file' 'FAIL') 'Missing directions/frames must fail'
    $anim=Join-Path $dir 'Animations/Idle'; [void](New-Item -ItemType Directory -Path $anim -Force)
    Copy-Item -LiteralPath $file -Destination (Join-Path $anim 'idle_front_r_01.png')
    $r=Run-Scan $dir $profile
    Assert (@($r.checks | Where-Object {$_.file -eq 'Animations/Idle/idle_front_r_00.png' -and $_.status -eq 'FAIL'}).Count -gt 0) 'Sequence starting at 01 must report missing 00'
    Copy-Item -LiteralPath $file -Destination (Join-Path $anim 'idle_front_r_16.png')
    $r=Run-Scan $dir $profile
    Assert (Has $r 'naming' 'FAIL') 'Frame 16 exceeds loader range'
    $profile.requireMeta=$true
    $r=Run-Scan $dir $profile
    Assert (Has $r 'meta' 'FAIL') 'Missing metadata must fail when required'
    $meta=@"
guid: 0123456789abcdef0123456789abcdef
TextureImporter:
  textureType: 8
  spriteMode: 1
  spritePixelsToUnits: 100
  filterMode: 0
  enableMipMap: 0
  alphaIsTransparency: 1
  platformSettings:
  - serializedVersion: 4
    buildTarget: DefaultTexturePlatform
    textureCompression: 1
  - serializedVersion: 4
    buildTarget: Standalone
    textureCompression: 0
"@
    $meta | Set-Content -LiteralPath ($file+'.meta') -Encoding UTF8
    $meta | Set-Content -LiteralPath ((Join-Path $dirs 'fixture_dir_front_r.png')+'.meta') -Encoding UTF8
    $r=Run-Scan $dir $profile
    Assert (Has $r 'meta-compression' 'FAIL') 'Standalone compression 0 must not mask Default compression 1'
    Assert (Has $r 'duplicate-guid' 'FAIL') 'Cloned GUID must fail'
    $profile.groundY=$null; $profile.minHeight=$null; $profile.maxHeight=$null
    $r=Run-Scan $dir $profile
    Assert (Has $r 'ground' 'NOT_RUN') 'Exceptional profile must disable humanoid contact check explicitly'
    Set-Content -LiteralPath $file -Value 'not a PNG' -Encoding ASCII
    $r=Run-Scan $dir $profile
    Assert (Has $r 'decode' 'FAIL') 'Corrupt PNG must fail'
    Write-Output "PASS: $passed assertions; synthetic fixtures only; production assets untouched"
} finally {
    $resolved=[IO.Path]::GetFullPath($temp)
    $tempRoot=[IO.Path]::GetFullPath([IO.Path]::GetTempPath())
    if(-not $resolved.StartsWith($tempRoot,[StringComparison]::OrdinalIgnoreCase) -or (Split-Path $resolved -Leaf) -notlike 'character-art-tests-*'){throw 'Unsafe cleanup target'}
    Remove-Item -LiteralPath $resolved -Recurse -Force
}
