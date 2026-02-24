$content = Get-Content 'C:\Users\iamdo\.claude\projects\D--work-private-yjsplan\a47e6a1e-622a-4a06-8a80-d80980f90f8a\tool-results\mcp-playwright-browser_snapshot-1771154962148.txt' -Raw
# Search for price patterns near each ASIN
$asins = @('B0BVG33PWR','B0C3VRSVS2','B07GVPTY5B','B0C8JCQW23')
foreach ($asin in $asins) {
    $idx = $content.IndexOf($asin)
    if ($idx -ge 0) {
        $start = $idx
        $len = [Math]::Min(4000, $content.Length - $start)
        $context = $content.Substring($start, $len)
        # Find price patterns
        $priceMatches = [regex]::Matches($context, '\$[\d,]+\.?\d*|\d+\.\d{2}')
        Write-Output "===ASIN:${asin}==="
        foreach ($pm in $priceMatches) {
            $pStart = [Math]::Max(0, $pm.Index - 50)
            $pLen = [Math]::Min(120, $context.Length - $pStart)
            Write-Output "  PRICE: $($pm.Value) context: $($context.Substring($pStart, $pLen))"
        }
        Write-Output ""
    }
}
