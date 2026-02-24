$content = Get-Content 'C:\Users\iamdo\.claude\projects\D--work-private-yjsplan\a47e6a1e-622a-4a06-8a80-d80980f90f8a\tool-results\mcp-playwright-browser_snapshot-1771154962148.txt' -Raw
$asins = @('B0BVG33PWR','B0C3VRSVS2','B07GVPTY5B','B0C8JCQW23')
foreach ($asin in $asins) {
    $idx = $content.IndexOf($asin)
    if ($idx -ge 0) {
        $start = $idx
        $len = [Math]::Min(2500, $content.Length - $start)
        $context = $content.Substring($start, $len)
        Write-Output "===ASIN:${asin}==="
        Write-Output $context
        Write-Output ""
    }
}
