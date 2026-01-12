rm -rf ./dist
mkdir -p ./dist

echo "Copy dependencies"
SITE_PACKAGES=$(find -L .venv -type d -name "site-packages" | head -1)
if [ -z "$SITE_PACKAGES" ]; then
  echo "Error: site-packages not found in .venv"
  exit 1
fi
cp -r "$SITE_PACKAGES"/* ./dist

echo "Clean up dist folder"
cd ./dist

find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*info" -exec rm -rf {} + 2>/dev/null || true
find . -maxdepth 1 -name "_*" -exec rm -rf {} + 2>/dev/null || true

rm -rf *.so black blackd blib2to3 distutils* pkg_resources pip* setuptools* wheel*

cd ..

echo "Copy source code"
cp -r ./src/* ./dist

echo "Finished"
echo
