# Branch Strategy

This repository uses a three-branch strategy for development and upstream tracking.

## Branches

### `master` (Default Branch)
- **Purpose:** Main development branch for this fork
- **Protection:** Should be protected - require PR reviews and passing tests
- **Deployment:** Releases are created from this branch
- **Push:** Only via pull requests from `develop`

### `develop`
- **Purpose:** Active development branch
- **Usage:** Day-to-day development work happens here
- **Testing:** CI runs on every push
- **Merge:** Merge to `master` when ready for release

### `main`
- **Purpose:** Tracks upstream repository (fedecalendino/alfred-randomer)
- **Updates:** Only updated by pulling from upstream
- **PRs:** Pull requests to upstream go from this branch
- **Do NOT:** Push your changes here directly

## Workflow

### Daily Development
```bash
# Work on develop branch
git checkout develop

# Make changes
git add .
git commit -m "Your changes"

# Push to your fork
git push origin develop
```

### Creating a Release
```bash
# Create PR from develop to master on GitHub
# After review and tests pass, merge

# Or locally:
git checkout master
git merge develop
git push origin master

# Create release
make release-patch  # or release-minor, release-major
```

### Syncing with Upstream
```bash
# Update main from upstream
git checkout main
git pull upstream main
git push origin main

# Optionally merge upstream changes to develop
git checkout develop
git merge main
git push origin develop
```

### Contributing Back to Upstream
```bash
# Create feature branch from main
git checkout main
git checkout -b feature-name

# Make changes
git add .
git commit -m "Feature description"

# Push to your fork
git push origin feature-name

# Create PR from your fork's feature-name to upstream's main
```

## GitHub Actions CI/CD

Tests run automatically on:
- ✅ Every push to `master` or `develop`
- ✅ Every pull request to `master` or `main`

## Branch Protection (Recommended)

Set up on GitHub for `master` branch:
1. Settings → Branches → Add rule
2. Branch name pattern: `master`
3. Enable:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass (select `test (3.11)` and `lint`)
   - ✅ Require branches to be up to date
   - ✅ Include administrators

## Remote Configuration

```
origin   → https://github.com/MikeDacre/alfred-randomer.git (your fork)
upstream → https://github.com/fedecalendino/alfred-randomer.git (original)
```

## Current State

After reorganization:
- ✅ `master` - Your main branch (pushed to origin)
- ✅ `develop` - Development branch (pushed to origin)
- ✅ `main` - Tracks upstream (unchanged, tracks origin/main and upstream/main)
- ✅ Old `mine` branch renamed to `develop`
- ✅ GitHub Actions configured for new branch structure
