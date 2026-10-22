param(
    [Parameter(Mandatory=$true)][string]$AssetRoot,
    [string]$ProfilePath,
    [string]$OutputPath
)
# Read-only validator. System.Drawing is supported here on Windows; other hosts need an equivalent decoder.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$profile = @{ width=128; height=128; groundY=126; groundTolerance=0; minHeight=90; maxHeight=105; ppu=100; prefix='warrior_pilot'; requireMeta=$true; requireComplete=$true; counts=@{Idle=4;Walk=6;Attack=5;Hit=3;Defeat=5}; exceptions=@{} }
if ($ProfilePath) {
    $custom = Get-Content -LiteralPath $ProfilePath -Raw | ConvertFrom-Json
    foreach ($p in $custom.PSObject.Properties) {
        if ($p.Name -in @('counts','exceptions')) {
            $map=@{}; foreach ($q in $p.Value.PSObject.Properties) { $map[$q.Name]=$q.Value }; $profile[$p.Name]=$map
        } else { $profile[$p.Name]=$p.Value }
    }
}
$root = (Resolve-Path -LiteralPath $AssetRoot).Path
$results = [System.Collections.Generic.List[object]]::new()
$measurements = [System.Collections.Generic.List[object]]::new()
function Add-Check([string]$file,[string]$check,[string]$status,[string]$detail) {
    $key="$file|$check"
    if ($status -eq 'FAIL' -and $profile.exceptions.ContainsKey($key)) {
        $reason=[string]$profile.exceptions[$key]
        if ([string]::IsNullOrWhiteSpace($reason)) { throw "Exception without reason: $key" }
        $status='WARNING'; $detail += "; documented exception: $reason"
    }
    $results.Add([pscustomobject]@{file=$file;check=$check;status=$status;detail=$detail})
}
function Assert-Check($file,$check,$condition,$detail) {
    $status=if($condition){'PASS'}else{'FAIL'}; Add-Check $file $check $status $detail
}
$files=@(Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.png' | Sort-Object FullName)
Assert-Check '.' 'inventory' ($files.Count -gt 0) "$($files.Count) PNGs"
$pixelHashes=@{}; $guids=@{}
foreach ($file in $files) {
    $rel=$file.FullName.Substring($root.Length+1).Replace('\','/')
    $bitmap=$null
    try {
        $bitmap=[System.Drawing.Bitmap]::new($file.FullName)
        Assert-Check $rel 'dimensions' ($bitmap.Width -eq $profile.width -and $bitmap.Height -eq $profile.height) "$($bitmap.Width)x$($bitmap.Height)"
        $raw=[IO.File]::ReadAllBytes($file.FullName)
        $pngSignature=@(137,80,78,71,13,10,26,10)
        $signatureOK=$raw.Length -ge 33
        for($i=0;$signatureOK -and $i -lt 8;$i++){ $signatureOK=$raw[$i] -eq $pngSignature[$i] }
        if(-not $signatureOK){throw 'Not a PNG signature'}
        $nativeAlpha=$raw[25] -in @(4,6)
        Assert-Check $rel 'alpha-channel' $nativeAlpha "PNG color type $($raw[25]); explicit alpha required (palette tRNS is not RGBA)"
        $left=$bitmap.Width; $top=$bitmap.Height; $right=-1; $bottom=-1; $clear=0; $partial=0
        $pixels=[System.Collections.Generic.List[byte]]::new()
        for($y=0;$y -lt $bitmap.Height;$y++) { for($x=0;$x -lt $bitmap.Width;$x++) {
            $c=$bitmap.GetPixel($x,$y)
            $pixels.Add($c.A); $pixels.Add($c.R); $pixels.Add($c.G); $pixels.Add($c.B)
            if($c.A -eq 0){$clear++} else {
                $left=[Math]::Min($left,$x); $top=[Math]::Min($top,$y); $right=[Math]::Max($right,$x); $bottom=[Math]::Max($bottom,$y)
                if($c.A -lt 255){$partial++}
            }
        } }
        Assert-Check $rel 'transparency' ($clear -gt 0 -and $bottom -ge 0) "clear=$clear partial=$partial"
        if($partial -gt 0){Add-Check $rel 'halo' 'WARNING' 'Partial alpha present; inspect edges. Not proof of a halo.'}else{Add-Check $rel 'halo' 'REQUIRES_HUMAN_REVIEW' 'Binary alpha; edge color/cluster quality still requires review.'}
        if($bottom -ge 0) {
            if($null -ne $profile.groundY){Assert-Check $rel 'ground' ([Math]::Abs($bottom-$profile.groundY) -le $profile.groundTolerance) "bottom=$bottom top-origin"}else{Add-Check $rel 'ground' 'NOT_RUN' 'Profile has no ground target'}
            $contentHeight=$bottom-$top+1
            if($null -ne $profile.minHeight -and $null -ne $profile.maxHeight){Assert-Check $rel 'content-height' ($contentHeight -ge $profile.minHeight -and $contentHeight -le $profile.maxHeight) "height=$contentHeight"}else{Add-Check $rel 'content-height' 'NOT_RUN' 'Profile has no height range'}
            $measurements.Add([pscustomobject]@{file=$rel;left=$left;top=$top;right=$right;bottom=$bottom;height=$contentHeight})
            if($left -eq 0 -or $right -eq $bitmap.Width-1 -or $top -eq 0 -or $bottom -eq $bitmap.Height-1){Add-Check $rel 'canvas-edge' 'WARNING' 'Visible pixels touch canvas edge; inspect clipping'}
        }
        $sha=[Security.Cryptography.SHA256]::Create()
        try{$hash=[BitConverter]::ToString($sha.ComputeHash($pixels.ToArray()))}finally{$sha.Dispose()}
        if($pixelHashes.ContainsKey($hash)){Add-Check $rel 'duplicate' 'WARNING' "Identical decoded pixels to $($pixelHashes[$hash]); may be intentional"}else{$pixelHashes[$hash]=$rel}
    } catch { Add-Check $rel 'decode' 'FAIL' $_.Exception.Message } finally { if($null -ne $bitmap){$bitmap.Dispose()} }
    $metaPath=$file.FullName+'.meta'
    if(Test-Path -LiteralPath $metaPath) {
        $meta=Get-Content -LiteralPath $metaPath -Raw
        $settings=@{textureType=8;spriteMode=1;spritePixelsToUnits=$profile.ppu;filterMode=0;enableMipMap=0;alphaIsTransparency=1}
        foreach($key in $settings.Keys){
            $m=[regex]::Match($meta,"(?m)^\s*${key}:\s*([0-9.]+)\s*$")
            Assert-Check $rel "meta-$key" ($m.Success -and [double]$m.Groups[1].Value -eq $settings[$key]) "expected=$($settings[$key]); actual=$($m.Groups[1].Value)"
        }
        $blocks=[regex]::Split($meta,'(?m)^\s*- serializedVersion:')
        $default=@($blocks | Where-Object {$_ -match 'buildTarget: DefaultTexturePlatform'})
        Assert-Check $rel 'meta-compression' ($default.Count -eq 1 -and $default[0] -match '(?m)^\s*textureCompression:\s*0\s*$') 'DefaultTexturePlatform must have compression 0'
        $gm=[regex]::Match($meta,'(?m)^guid:\s*([a-f0-9]{32})\s*$')
        Assert-Check $rel 'meta-guid' $gm.Success '32 lowercase hex GUID'
        if($gm.Success){$g=$gm.Groups[1].Value; if($guids.ContainsKey($g)){Add-Check $rel 'duplicate-guid' 'FAIL' "Also used by $($guids[$g])"}else{$guids[$g]=$rel}}
    } elseif($profile.requireMeta){Add-Check $rel 'meta' 'FAIL' 'Missing .png.meta'}else{Add-Check $rel 'meta' 'NOT_RUN' 'Meta optional for staging'}
}
$directions=@('back_l','back_r','front_r','front_l')
$expected=[System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
[void]$expected.Add("$($profile.prefix)_mvp1_static_128.png")
foreach($dir in $directions){[void]$expected.Add("Directions/$($profile.prefix)_dir_$dir.png")}
foreach($state in $profile.counts.Keys){
    $count=[int]$profile.counts[$state]
    if($count -lt 1 -or $count -gt 16){throw "Frame count outside current loader range 1..16: $state=$count"}
    foreach($dir in $directions){for($i=0;$i -lt $count;$i++){[void]$expected.Add(('Animations/{0}/{1}_{2}_{3:00}.png' -f $state,$state.ToLowerInvariant(),$dir,$i))}}
}
if($profile.requireComplete){foreach($rel in ($expected | Sort-Object)){Assert-Check $rel 'required-file' (Test-Path -LiteralPath (Join-Path $root $rel)) 'Expected by selected profile'}}
foreach($file in $files){
    $rel=$file.FullName.Substring($root.Length+1).Replace('\','/')
    Assert-Check $rel 'naming' ($expected.Contains($rel)) 'Name/path must match profile inventory; extra or out-of-range frames need profile/runtime review'
}
foreach($state in $profile.counts.Keys){foreach($dir in $directions){
    $stem="Animations/$state/$($state.ToLowerInvariant())_${dir}_"
    $group=@($measurements | Where-Object {$_.file.StartsWith($stem)})
    if($group.Count -gt 1){
        $range=($group | Measure-Object height -Maximum -Minimum)
        if($range.Maximum-$range.Minimum -gt 8){Add-Check "$state/$dir" 'proportions' 'WARNING' 'Height spread >8px; poses may justify it'}
        if($state -eq 'Idle'){$tops=$group | Measure-Object top -Minimum -Maximum; Assert-Check "$state/$dir" 'idle-bob' ($tops.Maximum-$tops.Minimum -le 2) 'Top spread <=2px for pilot baseline'}
    }
}}
Add-Check '.' 'cross-direction-identity' 'REQUIRES_HUMAN_REVIEW' 'Review anatomy, palette, dominant hand, silhouette and animation contacts; dimensions are not artistic proof'
Add-Check '.' 'unity-runtime' 'NOT_RUN' 'Static file scan does not run Unity import, Resources.Load, EditMode or PlayMode'
$summary=@{}; foreach($s in @('PASS','FAIL','WARNING','NOT_RUN','REQUIRES_HUMAN_REVIEW')){$summary[$s]=@($results | Where-Object status -eq $s).Count}
$report=[pscustomobject]@{root=$root;profile=$profile;summary=$summary;measurements=@($measurements.ToArray());checks=@($results.ToArray())}
$json=$report | ConvertTo-Json -Depth 12
if($OutputPath){$json | Set-Content -LiteralPath $OutputPath -Encoding UTF8}else{$json}
if($summary.FAIL -gt 0){exit 1}else{exit 0}
