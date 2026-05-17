# Stop hook — checks whether today's trend_letter output file was created
$today = Get-Date -Format "MMdd"
$projectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$expected = Join-Path $projectRoot "output\trend_letter_${today}.html"

if (Test-Path $expected) {
    $size = (Get-Item $expected).Length
    $out = [ordered]@{ systemMessage = "output/trend_letter_${today}.html created ($size bytes)" }
} else {
    $out = [ordered]@{ systemMessage = "WARNING: output/trend_letter_${today}.html not found -- letter may not have been generated today." }
}
Write-Output ($out | ConvertTo-Json -Compress)
