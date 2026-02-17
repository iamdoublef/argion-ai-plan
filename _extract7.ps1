$content = Get-Content 'D:\work\private\yjsplan\_b0bvg374w9_snapshot.txt' -Raw
# Price
$priceMatches = [regex]::Matches($content, '\$[\d,]+\.\d{2}')
Write-Output "=== FIRST 5 PRICES ==="
$count = 0
foreach ($pm in $priceMatches) {
    if ($count -ge 5) { break }
    $pStart = [Math]::Max(0, $pm.Index - 60)
    $pLen = [Math]::Min(150, $content.Length - $pStart)
    Write-Output "  $($pm.Value) => $($content.Substring($pStart, $pLen))"
    Write-Output "---"
    $count++
}
# Rating
$ratingMatches = [regex]::Matches($content, '(\d+\.\d+) out of 5 stars')
Write-Output "=== FIRST 3 RATINGS ==="
$count = 0
foreach ($rm in $ratingMatches) {
    if ($count -ge 3) { break }
    Write-Output "  $($rm.Value)"
    $count++
}
# Reviews
$reviewMatches = [regex]::Matches($content, '(\d[\d,]*) (ratings?|reviews?|global)')
Write-Output "=== FIRST 3 REVIEWS ==="
$count = 0
foreach ($rvm in $reviewMatches) {
    if ($count -ge 3) { break }
    Write-Output "  $($rvm.Value)"
    $count++
}
# Stock
$stockMatches = [regex]::Matches($content, '(In Stock|Only \d+ left|Currently unavailable|out of stock)', 'IgnoreCase')
Write-Output "=== STOCK ==="
$count = 0
foreach ($sm in $stockMatches) {
    if ($count -ge 3) { break }
    Write-Output "  $($sm.Value)"
    $count++
}
