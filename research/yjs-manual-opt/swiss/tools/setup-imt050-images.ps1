# IMT050 图片整理脚本
# 功能：复制原始图片到产品目录 + 生成图片识别HTML

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$rawDir = Join-Path $root "source\images_imt050_raw"
$targetDir = Join-Path $root "swiss\products\imt050\images"

# 1. 复制图片
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

$files = Get-ChildItem $rawDir -Filter "*.png" | Sort-Object { [int]($_.BaseName -replace '\D','') }
Write-Host "Found $($files.Count) images in $rawDir"

foreach ($f in $files) {
    Copy-Item $f.FullName (Join-Path $targetDir $f.Name) -Force
    Write-Host "  Copied: $($f.Name)"
}
Write-Host "`nAll images copied to $targetDir"

# 2. 生成图片识别 gallery HTML
$galleryPath = Join-Path $root "swiss\products\imt050\_image-gallery.html"
$html = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>IMT050 Image Gallery — 图片识别</title>
<style>
body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; max-width: 1200px; margin: 0 auto; }
h1 { border-bottom: 3px solid #E30613; padding-bottom: 8px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.card { background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 12px; text-align: center; }
.card img { max-width: 100%; max-height: 200px; object-fit: contain; border: 1px solid #eee; }
.card .filename { font-weight: bold; font-size: 16px; margin: 8px 0 4px; color: #E30613; }
.card .role { font-size: 13px; color: #666; }
.card select { margin-top: 8px; padding: 4px 8px; font-size: 13px; }
.actions { margin: 20px 0; padding: 16px; background: #fff; border: 1px solid #ddd; border-radius: 8px; }
.actions button { padding: 8px 16px; background: #E30613; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
.actions button:hover { background: #c00; }
pre { background: #1a1a1a; color: #0f0; padding: 12px; border-radius: 4px; white-space: pre-wrap; font-size: 12px; }
table { border-collapse: collapse; width: 100%; margin-top: 12px; }
th, td { border: 1px solid #ddd; padding: 6px 10px; text-align: left; font-size: 13px; }
th { background: #f0f0f0; }
</style>
</head>
<body>
<h1>IMT050 图片识别 Gallery</h1>
<p>请为每张图片选择其角色，然后点击"生成映射表"获取模板引用。</p>

<div class="grid">
"@

foreach ($f in $files) {
    $html += @"

<div class="card">
  <img src="images/$($f.Name)" alt="$($f.Name)">
  <div class="filename">$($f.Name)</div>
  <div class="role">
    <select data-file="$($f.Name)">
      <option value="">— 选择角色 —</option>
      <option value="cover">封面产品图 (Cover)</option>
      <option value="structure">产品结构图 (Structure)</option>
      <option value="panel">控制面板图 (Control Panel)</option>
      <option value="step">操作步骤图 (Operation Step)</option>
      <option value="icon">图标/警告标志 (Icon)</option>
      <option value="cleaning">清洁维护图 (Cleaning)</option>
      <option value="troubleshoot">故障排除图 (Troubleshoot)</option>
      <option value="specs_label">铭牌/参数标签 (Specs Label)</option>
      <option value="other">其他 (Other)</option>
      <option value="unused">不使用 (Unused)</option>
    </select>
  </div>
</div>
"@
}

$html += @"
</div>

<div class="actions">
  <button onclick="generateMapping()">生成映射表</button>
  <div id="output"></div>
</div>

<script>
function generateMapping() {
  const selects = document.querySelectorAll('select[data-file]');
  const mapping = {};
  selects.forEach(s => {
    if (s.value) mapping[s.dataset.file] = s.value;
  });
  
  let table = '<h3>图片映射表</h3><table><tr><th>文件名</th><th>角色</th><th>模板引用</th></tr>';
  const roleLabels = {cover:'封面',structure:'结构图',panel:'控制面板',step:'操作步骤',icon:'图标',cleaning:'清洁',troubleshoot:'故障排除',specs_label:'铭牌',other:'其他',unused:'不使用'};
  
  for (const [file, role] of Object.entries(mapping)) {
    const ref = role === 'unused' ? '—' : './{{images_dir}}/' + file;
    table += '<tr><td>' + file + '</td><td>' + (roleLabels[role]||role) + '</td><td><code>' + ref + '</code></td></tr>';
  }
  table += '</table>';
  
  // Generate template update hints
  const cover = Object.entries(mapping).find(([,r]) => r === 'cover');
  const structure = Object.entries(mapping).find(([,r]) => r === 'structure');
  const panel = Object.entries(mapping).find(([,r]) => r === 'panel');
  
  let hints = '<h3>模板更新提示</h3><pre>';
  if (cover) hints += 'Cover: imt050_cover_01.png → ' + cover[0] + '\\n';
  if (structure) hints += 'Structure: imt050_structure_01.png → ' + structure[0] + '\\n';
  if (panel) hints += 'Panel: imt050_panel_01.png → ' + panel[0] + '\\n';
  hints += '</pre>';
  
  document.getElementById('output').innerHTML = table + hints;
}
</script>
</body>
</html>
"@

$html | Out-File -Encoding UTF8 $galleryPath
Write-Host "`nGallery HTML generated: $galleryPath"
Write-Host "Open it in browser to identify images and generate mapping."
