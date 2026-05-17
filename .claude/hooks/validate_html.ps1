# PostToolUse Write hook — validates trend_letter HTML
$raw = [Console]::In.ReadToEnd()
if (-not $raw) { exit 0 }
$json = $raw | ConvertFrom-Json

$file_path = $json.tool_input.file_path
if (-not $file_path) { exit 0 }
if ($file_path -notmatch 'trend_letter.*\.html$') { exit 0 }

$content = Get-Content $file_path -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
if (-not $content) { exit 0 }

$errors = @()

if ($content -notmatch '<!doctype html>') {
    $errors += "missing <!doctype html>"
}

$cardCount = ([regex]::Matches($content, 'class="trend-card"')).Count
if ($cardCount -lt 4) {
    $errors += "trend-card blocks: $cardCount (need >= 4)"
}

$imgCount = ([regex]::Matches($content, '<img ')).Count
if ($imgCount -lt 8) {
    $errors += "img tags: $imgCount (need >= 8)"
}

if ($content -match 'placeholder|PLACEHOLDER|YOUR_URL|example\.com/image') {
    $errors += "unverified placeholder URL detected"
}

if ($errors.Count -gt 0) {
    $errStr = $errors -join "; "
    $out = [ordered]@{
        decision = "block"
        reason = "HTML validation failed: $errStr"
        hookSpecificOutput = [ordered]@{
            hookEventName = "PostToolUse"
            additionalContext = "HTML validation failed: $errStr -- fix and re-run Write."
        }
    }
    Write-Output ($out | ConvertTo-Json -Compress)
    exit 0
}

$ok = [ordered]@{ systemMessage = "HTML ok (cards:$cardCount imgs:$imgCount)" }
Write-Output ($ok | ConvertTo-Json -Compress)
