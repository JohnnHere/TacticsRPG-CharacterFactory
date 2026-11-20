$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$qaRoot = (Get-Location).Path
$bodyDir = 'experiments/main-orc-combat-rescue-v5/body-specialist'
$gripDir = 'experiments/main-orc-combat-rescue-v5/grip-specialist/F02-F08'
$bodyRep = Get-Content -LiteralPath "$bodyDir/representative.json" -Raw | ConvertFrom-Json
$inputPaths = [System.Collections.Generic.List[string]]::new()
$expected = @{}
foreach ($name in @('report.md','checkpoint.json','representative.json','canonical-input.png','technical-verification.json','import-keys.lua','diagnostic-zoom-1.png','diagnostic-zoom-2.png','diagnostic-zoom-3.png')) { $inputPaths.Add("$bodyDir/$name") }
foreach ($key in $bodyRep.keys) {
  foreach ($kind in @('nativeMaster','compositeMaster','nativeExport','compositeExport')) {
    $file = $key.$kind; $inputPaths.Add($file.path); $expected[$file.path] = $file.sha256
  }
}
$expected[$bodyRep.sourceInput.path] = $bodyRep.sourceInput.sha256
foreach ($name in @('checkpoint.json','report.md','checks.json','anatomy.json')) { $inputPaths.Add("$gripDir/$name") }
$gripChecks = @()
foreach ($frameName in @('F02','F08')) {
  $repPath = "characters/orc-v1/source/combat-rescue-v5/grip-specialist/$frameName/representative.json"
  $inputPaths.Add($repPath)
  $rep = Get-Content -LiteralPath $repPath -Raw | ConvertFrom-Json
  foreach ($kind in @('master','bodyMaster','nativeMaster')) { $inputPaths.Add($rep.$kind); $expected[$rep.$kind] = $rep.($kind+'Sha256') }
  foreach ($frame in $rep.frames) {
    foreach ($kind in @('png','nativePng')) { $inputPaths.Add($frame.$kind) }
    $expected[$frame.png] = $frame.sha256; $expected[$frame.nativePng] = $frame.nativeSha256
    foreach ($layer in $frame.layers.PSObject.Properties) { $inputPaths.Add($layer.Value.png); $expected[$layer.Value.png] = $layer.Value.sha256 }
  }
  foreach ($file in @($rep.sourceBodyFrame.png,$rep.sourceParentClip,$rep.weapon.sprite,$rep.weapon.master,$rep.weaponDefinition)) { $inputPaths.Add($file) }
  $expected[$rep.sourceBodyFrame.png] = $rep.sourceBodyFrame.sha256
  $expected[$rep.sourceParentClip] = $rep.sourceParentClipSha256
  $expected[$rep.weapon.sprite] = $rep.weapon.spriteSha256
  $expected[$rep.weapon.master] = $rep.weapon.masterSha256
  $newBody = [System.Drawing.Bitmap]::FromFile((Join-Path $qaRoot $rep.frames[0].layers.body.png))
  $oldBody = [System.Drawing.Bitmap]::FromFile((Join-Path $qaRoot $rep.sourceBodyFrame.png))
  $delta = 0
  for ($y=0; $y -lt $newBody.Height; $y++) { for ($x=0; $x -lt $newBody.Width; $x++) { if ($newBody.GetPixel($x,$y).ToArgb() -ne $oldBody.GetPixel($x,$y).ToArgb()) { $delta++ } } }
  $newBody.Dispose(); $oldBody.Dispose()
  $masterBytes = [System.IO.File]::ReadAllBytes((Join-Path $qaRoot $rep.master))
  $duration = [BitConverter]::ToUInt16($masterBytes,136)
  $gripChecks += [ordered]@{frame=$frameName; bodyArgbDelta=$delta; savedMasterFrameDurationMs=$duration; declaredDurationMs=$rep.durationsMs[0]; durationMatches=($duration -eq $rep.durationsMs[0])}
}
$evidence = @($inputPaths | Sort-Object -Unique | ForEach-Object {
  $hash = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant()
  [ordered]@{path=$_;sha256=$hash;declaredSha256=$expected[$_];declaredMatches=if($expected.ContainsKey($_)){$hash -eq $expected[$_]}else{$null}}
})
$result = [ordered]@{recordedUtc=[DateTime]::UtcNow.ToString('o');scope='Exact inspected body keys and F02/F08 grip inputs only; no global preservation claim'; evidenceFiles=$evidence; declaredHashMismatches=@($evidence | Where-Object {$_.declaredMatches -eq $false}).Count; gripIndependentChecks=$gripChecks}
$out = Join-Path $qaRoot 'experiments/main-orc-combat-rescue-v5/qa-sol/input-freeze.json'
$result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $out -Encoding UTF8
[pscustomobject]@{recordedUtc=$result.recordedUtc;declaredHashMismatches=$result.declaredHashMismatches;gripIndependentChecks=$result.gripIndependentChecks} | ConvertTo-Json -Depth 5
