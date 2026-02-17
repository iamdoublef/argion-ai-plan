$files = @{
    'B07GVPTY5B' = 'D:\work\private\yjsplan\_b07gvpty5b_snapshot.txt'
}
foreach ($entry in $files.GetEnumerator()) {
    $asin = $entry.Key
    $content = Get-Content $entry.Value -Raw
    Write-Output "=== $asin ==="
    # Price
    $priceMatches = [regex]::Matches($content, '\$[\d,]+\.\d{2}')
    if ($priceMatches.Count -gt 0) { Write-Output "  Price: $($priceMatches[0].Value)" }
    # Rating
    $ratingMatch = [regex]::Match($content, '(\d+\.\d+) out of 5 stars')
    if ($ratingMatch.Success) { Write-Output "  Rating: $($ratingMatch.Value)" }
    # Reviews
    $reviewMatch = [regex]::Match($content, '(\d[\d,]*) (ratings?|global)')
    if ($reviewMatch.Success) { Write-Output "  Reviews: $($reviewMatch.Value)" }
    # Stock
    $stockMatches = [regex]::Matches($content, '(In Stock|Only \d+ left|Currently unavailable|out of stock)', 'IgnoreCase')
    if ($stockMatches.Count -gt 0) { Write-Output "  Stock: $($stockMatches[0].Value)" }
    else {
        $unavailMatches = [regex]::Matches($content, '(unavailable|not available|see all buying options)', 'IgnoreCase')
        if ($unavailMatches.Count -gt 0) { Write-Output "  Stock: $($unavailMatches[0].Value)" }
        else { Write-Output "  Stock: Unknown" }
    }
    # Bought in past month
    $boughtMatch = [regex]::Match($content, '(\d+[\d,K+]*) bought in past month')
    if ($boughtMatch.Success) { Write-Output "  Bought: $($boughtMatch.Value)" }
}
