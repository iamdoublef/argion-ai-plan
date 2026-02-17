$content = Get-Content 'D:\work\private\yjsplan\_sousvide_snapshot.txt' -Raw
$asins = @('B0C8JDRLMJ','B0C8JCQW23','B07DRRL2KG','B07RDM2BNL','B07RHQ338J','B0BVG374W9')
foreach ($asin in $asins) {
    $idx = $content.IndexOf($asin)
    if ($idx -ge 0) {
        $start = $idx
        $len = [Math]::Min(4000, $content.Length - $start)
        $context = $content.Substring($start, $len)
        # Extract title
        $titleMatch = [regex]::Match($context, 'heading "([^"]+)"')
        $title = if ($titleMatch.Success) { $titleMatch.Groups[1].Value } else { "N/A" }
        # Extract rating
        $ratingMatch = [regex]::Match($context, '(\d+\.\d+) out of 5 stars')
        $rating = if ($ratingMatch.Success) { $ratingMatch.Groups[1].Value } else { "N/A" }
        # Extract reviews
        $reviewMatch = [regex]::Match($context, 'link "(\d[\d,]*) ratings?"')
        $reviews = if ($reviewMatch.Success) { $reviewMatch.Groups[1].Value } else { "N/A" }
        # Extract price
        $priceMatches = [regex]::Matches($context, '\$[\d,]+\.?\d*')
        $price = if ($priceMatches.Count -gt 0) { $priceMatches[0].Value } else { "N/A" }
        
        Write-Output "===ASIN:${asin}==="
        Write-Output "  Title: $title"
        Write-Output "  Rating: $rating"
        Write-Output "  Reviews: $reviews"
        Write-Output "  Price: $price"
        Write-Output ""
    } else {
        Write-Output "===ASIN:${asin}===NOT FOUND"
    }
}
