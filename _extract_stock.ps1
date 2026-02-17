# Check stock for B0C8JDRLMJ
$content = Get-Content 'D:\work\private\yjsplan\_b0c8jdrlmj_snapshot.txt' -Raw
$stockMatches = [regex]::Matches($content, '(In Stock|Only \d+ left|Currently unavailable|out of stock)', 'IgnoreCase')
Write-Output "=== B0C8JDRLMJ STOCK ==="
$count = 0
foreach ($sm in $stockMatches) {
    if ($count -ge 3) { break }
    Write-Output "  $($sm.Value)"
    $count++
}
# Also check title
$titleMatch = [regex]::Match($content, 'Page Title: (.+)')
Write-Output "  Title: $($titleMatch.Groups[1].Value.Substring(0, [Math]::Min(200, $titleMatch.Groups[1].Value.Length)))"
# Check reviews count near the product
$reviewMatch = [regex]::Match($content, '(\d[\d,]*) global')
Write-Output "  Global reviews: $($reviewMatch.Value)"
