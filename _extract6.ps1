$content = Get-Content 'D:\work\private\yjsplan\_b0c8jdrlmj_snapshot.txt' -Raw
# Search for price
$priceMatches = [regex]::Matches($content, '\$[\d,]+\.\d{2}')
Write-Output "=== PRICES ==="
foreach ($pm in $priceMatches) {
    $pStart = [Math]::Max(0, $pm.Index - 80)
    $pLen = [Math]::Min(200, $content.Length - $pStart)
    Write-Output "  $($pm.Value) => $($content.Substring($pStart, $pLen))"
    Write-Output "---"
}
# Search for rating
$ratingMatches = [regex]::Matches($content, '(\d+\.\d+) out of 5 stars')
Write-Output "=== RATINGS ==="
foreach ($rm in $ratingMatches) {
    Write-Output "  $($rm.Value)"
}
# Search for reviews count
$reviewMatches = [regex]::Matches($content, '(\d[\d,]*) (ratings?|reviews?|global)')
Write-Output "=== REVIEWS ==="
foreach ($rvm in $reviewMatches) {
    Write-Output "  $($rvm.Value)"
}
