#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VERSION="$(python -c 'import binlab; print(binlab.__version__)')"
ARCH="$(uname -m)"
if [[ "$ARCH" != "x86_64" ]]; then
  echo "Esta primeira linha de pacotes suporta x86_64; arquitetura detectada: $ARCH" >&2
  exit 2
fi

rm -rf build/pyinstaller package-root
mkdir -p dist package-root/usr/bin package-root/usr/share/applications \
  package-root/usr/share/icons/hicolor/scalable/apps package-root/usr/share/doc/binlab

pyinstaller --clean --noconfirm --onefile --name binlab \
  --paths src packaging/entrypoints/binlab_cli.py
pyinstaller --clean --noconfirm --onefile --name binlab-gui \
  --paths src packaging/entrypoints/binlab_gui.py

install -m 0755 dist/binlab package-root/usr/bin/binlab
install -m 0755 dist/binlab-gui package-root/usr/bin/binlab-gui
install -m 0644 packaging/linux/binlab.desktop package-root/usr/share/applications/binlab.desktop
install -m 0644 branding/logo.svg package-root/usr/share/icons/hicolor/scalable/apps/binlab.svg
install -m 0644 README.md LICENSE package-root/usr/share/doc/binlab/

fpm -s dir -t deb -n binlab -v "$VERSION" -a amd64 \
  --license MIT --url https://github.com/mnl-nox/BinLab \
  --description "Local-first computational engineering laboratory" \
  --depends libc6 --depends libx11-6 --depends libxext6 --depends libxrender1 \
  --depends libxtst6 --depends libxi6 --depends libfontconfig1 --depends libxft2 \
  --package "dist/binlab_${VERSION}_amd64.deb" -C package-root .

fpm -s dir -t rpm -n binlab -v "$VERSION" -a x86_64 \
  --license MIT --url https://github.com/mnl-nox/BinLab \
  --description "Local-first computational engineering laboratory" \
  --depends glibc --depends libX11 --depends libXext --depends libXrender \
  --depends libXtst --depends libXi --depends fontconfig --depends libXft \
  --package "dist/binlab-${VERSION}-1.x86_64.rpm" -C package-root .

tar -czf "dist/binlab-${VERSION}-linux-x86_64.tar.gz" -C package-root .
(
  cd dist
  sha256sum "binlab_${VERSION}_amd64.deb" "binlab-${VERSION}-1.x86_64.rpm" \
    "binlab-${VERSION}-linux-x86_64.tar.gz" > SHA256SUMS
)
printf 'Linux packages generated for BinLab %s (%s).\n' "$VERSION" "$ARCH"
