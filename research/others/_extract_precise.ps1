$files = @(
    @{ asin='B0C3VRSVS2'; path='D:\work\private\yjsplan\_b0c3vrsvs2_snapshot.txt' },
    @{ asin='B07DRRL2KG'; path='D:\work\private\yjsplan\_b07drrl2kg_snapshot.txt' },
    @{ asin='B07RDM2BNL'; path='D:\work\private\yjsplan\_b07rdm2bnl_snapshot.txt' },
    @{ asin='B0BVG33PWR'; path='D:\work\private\yjsplan\_b0bvg33pwr_snapshot.txt' },
    @{ asin='B0BVG374W9'; path='D:\work\private\yjsplan\_b0bvg374w9_snapshot.txt' },
    @{ asin='B07RHQ338J'; path='D:\work\private\yjsplan\_b07rhq338j_snapshot.txt' }
)
foreach ($entry in $files) {
    $asin = $entry.asin
    $content = Get-Content $entry.path -Raw
    Write-Output "=== $asin ==="
    # Look for "X ratings" near "customerReviews" or the product rating section
    $globalMatch = [regex]::Match($content, '(\d[\d,]*) global (ratings?|reviews?)')
    if ($globalMatch.Success) { 
        Write-Output "  Global Reviews: $($globalMatch.Value)" 
    }
    # Also look for the first "X ratings" link which is usually the product's own
    $allRatings = [regex]::Matches($content, '"(\d[\d,]*) ratings?"')
    Write-Output "  All rating counts found:"
    $count = 0
    foreach ($r in $allRatings) {
        if ($count -ge 5) { break }
        Write-Output "    $($r.Value)"
        $count++
    }
}
