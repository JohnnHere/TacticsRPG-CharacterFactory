$ErrorActionPreference='Stop'
$skillRoot=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$repoRoot=(Resolve-Path (Join-Path $skillRoot '../../..')).Path
$entry=Get-Content -LiteralPath (Join-Path $skillRoot 'SKILL.md') -Raw -Encoding UTF8
if($entry -notmatch '(?s)^---\r?\nname: character-art-design\r?\ndescription: ([^\r\n]+)\r?\n---\r?\n'){throw 'Expected valid simple YAML frontmatter with name and description'}
if((Split-Path $skillRoot -Leaf) -ne 'character-art-design'){throw 'Folder/name mismatch'}
$links=0
foreach($file in Get-ChildItem -LiteralPath $skillRoot -Recurse -Filter '*.md'){
    $body=Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    foreach($m in [regex]::Matches($body,'\[[^\]]+\]\(([^)]+)\)')){
        $target=$m.Groups[1].Value
        if($target -match '^(https?:|#)'){continue}
        if(-not(Test-Path -LiteralPath (Join-Path $file.DirectoryName ($target.Split('#')[0])))){throw "Broken link $target in $($file.Name)"}
        $links++
    }
}
$contract=Get-Content -LiteralPath (Join-Path $skillRoot 'references/project-contract.md') -Raw -Encoding UTF8
$sources=0
foreach($m in [regex]::Matches($contract,'`((?:Docs|Assets)/[^`]+)`')){
    if(-not(Test-Path -LiteralPath (Join-Path $repoRoot $m.Groups[1].Value))){throw "Missing project source $($m.Groups[1].Value)"}
    $sources++
}
$tokens=@('DESIGN','GENERATE','ADAPT','ANIMATE','VALIDATE','PREPARE_INTEGRATION','INTEGRATE','AUDIT','Gate 1','Gate 2','Gate 3')
foreach($t in $tokens){if(-not $entry.Contains($t)){throw "Missing routing/gate $t"}}
Write-Output "PASS: simple frontmatter, directory name, $links resource links, $sources project sources, 8 modes and 3 gates. Full platform discovery/invocation NOT_RUN."
