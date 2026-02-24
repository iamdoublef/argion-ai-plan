$content = Get-Content 'D:\work\private\yjsplan\_sousvide_snapshot.txt' -Raw
$asin = 'B0C8JDRLMJ'
$idx = $content.IndexOf($asin)
Write-Output "Index of B0C8JDRLMJ: $idx"
if ($idx -ge 0) {
    $start = [Math]::Max(0, $idx - 200)
    $len = [Math]::Min(3000, $content.Length - $start)
    $context = $content.Substring($start, $len)
    Write-Output $context
}
