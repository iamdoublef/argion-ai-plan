#!/bin/bash
# 在 Linux dev 工位安装 Arial → Liberation Sans 的 fontconfig 别名。
#
# 背景：W50 母版 OOXML 写的是 `Arial` / `Arial Black`（Windows 客户用 MS Word
# 打开自动拿到真 Arial，没问题）。但 Linux 上 fc-match Arial 默认 fallback 到
# FreeSans，渲染的预览 PDF 字形偏窄、笔画不匀，看起来很丑。
#
# 这个脚本配置一个用户级 fontconfig，让 Linux 上 fc-match Arial → Liberation Sans
# （Liberation Sans 是 Arial 的 metrics-equivalent free 替代品，与 Arial 度量
# 相同，渲染清晰）。
#
# 影响范围：仅影响本机 Linux soffice 渲染 / pdftoppm 预览。不改任何 docx OOXML。
# Windows 客户打开 docx 时仍用真 Arial。
#
# 用法：
#   bash setup_linux_fonts.sh
# 或：
#   ./setup_linux_fonts.sh
set -e

# 1. 安装字体（如未安装）
if ! fc-list "Liberation Sans" | grep -q .; then
  echo "Installing fonts-liberation..."
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get install -y fonts-liberation fonts-liberation2 || apt-get install -y fonts-liberation fonts-liberation2
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y liberation-fonts
  elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y liberation-fonts
  else
    echo "Unknown package manager; install Liberation Sans manually."
    exit 1
  fi
fi

# 2. 写 fontconfig 别名
mkdir -p "$HOME/.config/fontconfig/conf.d"
cat > "$HOME/.config/fontconfig/conf.d/52-arial-fallback.conf" <<'XML'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <alias binding="strong">
    <family>Arial</family>
    <prefer><family>Liberation Sans</family></prefer>
  </alias>
  <alias binding="strong">
    <family>Arial Black</family>
    <prefer><family>Liberation Sans</family></prefer>
  </alias>
  <alias binding="strong">
    <family>Helvetica</family>
    <prefer><family>Liberation Sans</family></prefer>
  </alias>
</fontconfig>
XML

fc-cache -f

echo
echo "fc-match results (should resolve to Liberation Sans on Linux):"
fc-match "Arial"
fc-match "Arial Black"
fc-match "Helvetica"
echo
echo "OK. Re-render with: soffice --headless --convert-to pdf <docx>"
