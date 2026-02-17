$files = @(
    @{ asin='B0C3VRSVS2'; path='D:\work\private\yjsplan\_b0c3vrsvs2_snapshot.txt' },
    @{ asin='B07DRRL2KG'; path='D:\work\private\yjsplan\_b07drrl2kg_snapshot.txt' },
    @{ asin='B07RDM2BNL'; path='D:\work\private\yjsplan\_b07rdm2bnl_snapshot.txt' }
)
foreach ($entry in $files) {
    $asin = $entry.asin
    $content = Get-Content $entry.path -Raw
    Write-Output "=== $asin ==="
    $priceMatches = [regex]::Matches($content, '\$[\d,]+\.\d{2}')
    if ($priceMatches.Count -gt 0) { Write-Output "  Price: $($priceMatches[0].Value)" }
    else { Write-Output "  Price: N/A" }
    $ratingMatch = [regex]::Match($content, '(\d+\.\d+) out of 5 stars')
    if ($ratingMatch.Success) { Write-Output "  Rating: $($ratingMatch.Value)" }
    else { Write-Output "  Rating: N/A" }
    $reviewMatch = [regex]::Match($content, '(\d[\d,]*) (ratings?|global)')
    if ($reviewMatch.Success) { Write-Output "  Reviews: $($reviewMatch.Value)" }
    else { Write-Output "  Reviews: N/A" }
    $stockMatches = [regex]::Matches($content, '(In Stock|Only \d+ left|Currently unavailable|out of stock)', 'IgnoreCase')
    if ($stockMatches.Count -gt 0) { Write-Output "  Stock: $($stockMatches[0].Value)" }
    else { Write-Output "  Stock: Unknown" }
    $boughtMatch = [regex]::Match($content, '(\d+[\d,K+]*) bought in past month')
    if ($boughtMatch.Success) { Write-Output "  Bought: $($boughtMatch.Value)" }
}
