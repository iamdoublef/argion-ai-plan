$files = @(
    @{ asin='B0BVG33PWR'; path='D:\work\private\yjsplan\_b0bvg33pwr_snapshot.txt' },
    @{ asin='B07RHQ338J'; path='D:\work\private\yjsplan\_b07rhq338j_snapshot.txt' }
)
foreach ($entry in $files) {
    $asin = $entry.asin
    $content = Get-Content $entry.path -Raw
    Write-Output "=== $asin ==="
    $priceMatches = [regex]::Matches($content, '\$[\d,]+\.\d{2}')
    if ($priceMatches.Count -gt 0) { Write-Output "  Price: $($priceMatches[0].Value)" }
    $ratingMatch = [regex]::Match($content, '(\d+\.\d+) out of 5 stars')
    if ($ratingMatch.Success) { Write-Output "  Rating: $($ratingMatch.Value)" }
    $reviewMatch = [regex]::Match($content, '(\d[\d,]*) (ratings?|global)')
    if ($reviewMatch.Success) { Write-Output "  Reviews: $($reviewMatch.Value)" }
    $stockMatches = [regex]::Matches($content, '(In Stock|Only \d+ left|Currently unavailable|out of stock)', 'IgnoreCase')
    if ($stockMatches.Count -gt 0) { Write-Output "  Stock: $($stockMatches[0].Value)" }
    $boughtMatch = [regex]::Match($content, '(\d+[\d,K+]*) bought in past month')
    if ($boughtMatch.Success) { Write-Output "  Bought: $($boughtMatch.Value)" }
    # Check for variant info (12" vs 16")
    $variantMatch = [regex]::Match($content, 'Vac.*Seal.*12|Vac.*Seal.*16|12.*Wide|16.*Wide')
    if ($variantMatch.Success) { Write-Output "  Variant: $($variantMatch.Value)" }
}
