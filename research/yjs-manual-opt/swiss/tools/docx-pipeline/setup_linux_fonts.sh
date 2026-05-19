#!/bin/bash
# 在 Linux dev 工位安装 Calibri → Carlito 的 fontconfig 别名。
#
# 背景：母版 OOXML 写的是 `Calibri`（Windows 客户用 MS Word 打开自动拿到真
# Calibri，没问题）。但 Linux 上 fc-match Calibri 默认 fallback 到 DejaVu Sans
# 或其他字体，度量不一致会导致排版偏移。
#
# Carlito 是 Google 出品的 Calibri metrics-equivalent 开源替代品（crosextra-carlito），
# 与 Calibri 度量相同，渲染清晰。
#
# 影响范围：仅影响本机 Linux soffice 渲染 / pdftoppm 预览。不改任何 docx OOXML。
# Windows 客户打开 docx 时仍用真 Calibri。
#
# 用法：
#   bash setup_linux_fonts.sh
set -e

# 1. 安装 Carlito 字体（如未安装）
if ! fc-list "Carlito" | grep -q .; then
  echo "Installing Carlito (Calibri-equivalent)..."
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get install -y fonts-crosextra-carlito || apt-get install -y fonts-crosextra-carlito
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y google-crosextra-carlito-fonts
  elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y google-crosextra-carlito-fonts
  else
    echo "Unknown package manager; install Carlito font manually."
    echo "Download: https://fonts.google.com/specimen/Carlito"
    exit 1
  fi
fi

# 2. 安装 Courier New 替代（Liberation Mono）
if ! fc-list "Liberation Mono" | grep -q .; then
  echo "Installing Liberation Mono (Courier New equivalent)..."
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get install -y fonts-liberation || apt-get install -y fonts-liberation
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y liberation-mono-fonts
  elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y liberation-mono-fonts
  fi
fi

# 3. 写 fontconfig 别名
mkdir -p "$HOME/.config/fontconfig/conf.d"
cat > "$HOME/.config/fontconfig/conf.d/52-calibri-fallback.conf" <<'XML'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <alias binding="strong">
    <family>Calibri</family>
    <prefer><family>Carlito</family></prefer>
  </alias>
  <alias binding="strong">
    <family>Courier New</family>
    <prefer><family>Liberation Mono</family></prefer>
  </alias>
</fontconfig>
XML

# 移除旧的 Arial fallback 配置（如果存在）
rm -f "$HOME/.config/fontconfig/conf.d/52-arial-fallback.conf"

fc-cache -f

echo
echo "fc-match results:"
fc-match "Calibri"
fc-match "Courier New"
echo
echo "OK. Re-render with: soffice --headless --convert-to pdf <docx>"
