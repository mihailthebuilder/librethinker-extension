#!/bin/bash
# Build script for LibreThinker LibreOffice Extension

set -e  # Exit on error

echo "Building LibreThinker extension..."

# Create dist directory if it doesn't exist
mkdir -p dist

# Remove old build if it exists
rm -f dist/LibreThinker.oxt

# Create the .oxt file (which is just a ZIP file with specific structure)
cd extension
zip -r ../dist/LibreThinker.oxt \
    META-INF/manifest.xml \
    description.xml \
    description/ \
    empty_dialog.xdl \
    Factory.xcu \
    ProtocolHandler.xcu \
    Sidebar.xcu \
    image/ \
    registration/ \
    src/

cd ..

echo "✓ Extension built successfully: dist/LibreThinker.oxt"
echo ""
echo "To install:"
echo "  1. Open LibreOffice Writer"
echo "  2. Go to Tools > Extension Manager > Add"
echo "  3. Select dist/LibreThinker.oxt"
echo ""
echo "Or double-click the .oxt file to install"
