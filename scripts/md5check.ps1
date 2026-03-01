Get-ChildItem 'D:\work\private\yjsplan\research\yjs-manual-opt\output\images_v23' -File | ForEach-Object {
  $h = (Get-FileHash $_.FullName -Algorithm MD5).Hash
  "$h $($_.Length) $($_.Name)"
} | Sort-Object
