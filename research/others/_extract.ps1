$content = Get-Content 'C:\Users\iamdo\.claude\projects\D--work-private-yjsplan\a47e6a1e-622a-4a06-8a80-d80980f90f8a\tool-results\mcp-playwright-browser_snapshot-1771154962148.txt' -Raw
$asins = @('B0BVG33PWR','B0BVG374W9','B0C3VRSVS2','B07GVPTY5B','B0C8JDRLMJ','B0C8JCQW23','B07DRRL2KG','B07RDM2BNL','B07RHQ338J')
foreach ($asin in $asins) {
    $idx = $content.IndexOf($asin)
    if ($idx -ge 0) {
        $start = [Math]::Max(0, $idx - 300)
        $len = [Math]::Min(800, $content.Length - $start)
        $context = $content.Substring($start, $len)
        Write-Output "===ASIN:${asin}==="
        Write-Output $context
        Write-Output ""
    } else {
        Write-Output "===ASIN:${asin}===NOT FOUND"
    }
}
