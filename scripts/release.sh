#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Help text
show_help() {
    cat << EOF
Usage: ./scripts/release.sh [VERSION_BUMP] [FLAGS]

VERSION_BUMP options:
  major          Bump major version (1.0.0 -> 2.0.0)
  minor          Bump minor version (1.0.0 -> 1.1.0)
  patch          Bump patch version (1.0.0 -> 1.0.1)
  premajor       Bump to next major prerelease (1.0.0 -> 2.0.0-alpha.0)
  preminor       Bump to next minor prerelease (1.0.0 -> 1.1.0-alpha.0)
  prepatch       Bump to next patch prerelease (1.0.0 -> 1.0.1-alpha.0)
  prerelease     Bump prerelease version (1.0.0-alpha.0 -> 1.0.0-alpha.1)
  X.Y.Z          Set specific version (e.g., 1.2.3)

FLAGS:
  --no-git       Skip git commit and tag
  --skip-tests   Skip running tests
  --help, -h     Show this help message

Examples:
  ./scripts/release.sh patch              # Bump patch version
  ./scripts/release.sh minor              # Bump minor version
  ./scripts/release.sh prerelease         # Bump prerelease
  ./scripts/release.sh 2.0.0              # Set to specific version
  ./scripts/release.sh patch --no-git     # Bump without git commit

If no VERSION_BUMP is provided, uses current version from pyproject.toml
EOF
    exit 0
}

# Parse arguments
VERSION_BUMP=""
NO_GIT=false
SKIP_TESTS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            show_help
            ;;
        --no-git)
            NO_GIT=true
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        major|minor|patch|premajor|preminor|prepatch|prerelease)
            VERSION_BUMP="$1"
            shift
            ;;
        *)
            # Assume it's a version number
            VERSION_BUMP="$1"
            shift
            ;;
    esac
done

# Get bundle info
BUNDLEID=$(plutil -extract bundleid raw -o - ./info.plist)
NAME=${BUNDLEID##*.}

# Get current version
CURRENT_VERSION=$(poetry version --short)
echo -e "${BLUE}Current version: ${NC}v${CURRENT_VERSION}"

# Bump version if requested
if [ -n "$VERSION_BUMP" ]; then
    echo -e "${BLUE}Bumping version: ${NC}${VERSION_BUMP}"
    poetry version "$VERSION_BUMP" > /dev/null
    NEW_VERSION=$(poetry version --short)

    # Update info.plist
    plutil -replace version -string "$NEW_VERSION" info.plist

    echo -e "${GREEN}Version updated: ${NC}v${CURRENT_VERSION} → v${NEW_VERSION}"
else
    NEW_VERSION="$CURRENT_VERSION"
    echo -e "${YELLOW}No version bump specified, using current version${NC}"
fi

VERSION="$NEW_VERSION"
FILENAME="${NAME}.v${VERSION}.alfredworkflow"

echo ""
echo -e "${BLUE}NAME:${NC} $NAME"
echo -e "${BLUE}BUNDLE ID:${NC} $BUNDLEID"
echo -e "${BLUE}VERSION:${NC} v$VERSION"
echo ""

# Check if in git repo
IN_GIT_REPO=false
if git rev-parse --git-dir > /dev/null 2>&1; then
    IN_GIT_REPO=true

    # Check for uncommitted changes (excluding version files we just changed)
    if ! $NO_GIT; then
        CHANGED_FILES=$(git diff --name-only | grep -v "pyproject.toml\|info.plist" || true)
        if [ -n "$CHANGED_FILES" ]; then
            echo -e "${RED}⚠️  Warning: You have uncommitted changes:${NC}"
            echo "$CHANGED_FILES"
            echo ""
            read -p "Continue anyway? (y/N) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    fi
fi

# Run tests
if ! $SKIP_TESTS; then
    echo -e "${BLUE}Running tests...${NC}"
    echo ""

    if PYTHONPATH=src poetry run python3 -m unittest discover -s tests; then
        echo ""
        echo -e "${GREEN}✓ Tests passed${NC}"
    else
        echo ""
        echo -e "${RED}⚠️  TESTS FAILED${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  Skipping tests${NC}"
fi

echo ""

# Build
echo -e "${BLUE}Building workflow...${NC}"
./scripts/build.sh > /dev/null
echo -e "${GREEN}✓ Build complete${NC}"
echo ""

# Create release
echo -e "${BLUE}Creating release package...${NC}"
mkdir -p releases
rm -f "releases/$FILENAME"

if zip -q "releases/$FILENAME" -r dist img *.png info.plist 2>/dev/null; then
    echo -e "${GREEN}✓ Created releases/$FILENAME${NC}"
else
    echo -e "${RED}⚠️  Failed to create release package${NC}"
    exit 1
fi

echo ""

# Git commit and tag
if $IN_GIT_REPO && ! $NO_GIT && [ -n "$VERSION_BUMP" ]; then
    echo -e "${BLUE}Committing to git...${NC}"

    # Stage version files
    git add pyproject.toml info.plist

    # Create commit
    git commit -m "Release v${VERSION}"

    # Create tag
    git tag -a "v${VERSION}" -m "Release version ${VERSION}"

    echo -e "${GREEN}✓ Committed and tagged as v${VERSION}${NC}"
    echo -e "${YELLOW}Don't forget to push: ${NC}git push && git push --tags"
    echo ""
elif $NO_GIT; then
    echo -e "${YELLOW}⚠️  Skipping git commit (--no-git flag)${NC}"
    echo ""
elif ! $IN_GIT_REPO; then
    echo -e "${YELLOW}⚠️  Not in a git repository, skipping commit${NC}"
    echo ""
fi

# Summary
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Released $NAME v$VERSION${NC}"
echo -e "${BLUE}Location:${NC} releases/$FILENAME"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Open release
echo "Opening release in Alfred..."
open "./releases/$FILENAME"
