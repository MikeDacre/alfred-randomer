# GitHub Actions Workflows

This directory contains GitHub Actions workflows for continuous integration and code quality checks.

## Workflows

### test.yml - Test Suite

**Triggers:**
- Push to `main`, `mine`, or `develop` branches
- Pull requests to `main` or `mine` branches

**What it does:**
1. Runs tests on Python 3.8, 3.9, 3.10, and 3.11
2. Uses Poetry for dependency management
3. Caches virtualenv for faster runs
4. Runs full test suite with verbose output
5. Generates coverage report (Python 3.11 only)
6. Uploads coverage to Codecov (optional)

**Duration:** ~2-3 minutes per Python version (runs in parallel)

**Matrix Strategy:**
- Tests run on macOS (required for `plutil` in release script)
- Tests all supported Python versions from pyproject.toml

**Caching:**
- Virtualenv cached based on `poetry.lock` hash
- Significantly speeds up subsequent runs

### lint.yml - Code Quality

**Triggers:**
- Push to `main`, `mine`, or `develop` branches
- Pull requests to `main` or `mine` branches

**What it does:**
1. Checks code formatting with Black
2. Shows diff if formatting issues found
3. Fails if code isn't properly formatted

**Duration:** ~30 seconds

**How to fix failures:**
```bash
make format
git add .
git commit -m "Fix code formatting"
git push
```

## Viewing Results

### On GitHub
1. Go to your repository
2. Click the "Actions" tab
3. See all workflow runs with status

### In README
Status badges show current build status:
- ✅ Green badge = all tests passing
- ❌ Red badge = tests failing
- 🟡 Yellow badge = tests running

### On Pull Requests
- Workflow status appears directly on PR
- Required checks can block merging if tests fail
- Click "Details" to see full logs

## Local Testing

Before pushing, run locally to catch issues:

```bash
# Run what CI runs
make test              # Run all tests
make format            # Format code with Black
make test-coverage     # Generate coverage report

# Check formatting without changing files
poetry run black --check src/ tests/
```

## Coverage Reports

Coverage reports are generated on Python 3.11 runs and can be:
- Uploaded to Codecov (requires setup)
- Viewed as XML file in workflow artifacts
- Generated locally with `make test-coverage`

### Setting up Codecov (Optional)

1. Go to [codecov.io](https://codecov.io)
2. Sign up with GitHub
3. Add your repository
4. Get upload token
5. Add as repository secret: `CODECOV_TOKEN`
6. Uncomment the token line in `test.yml`

## Branch Protection

Recommended GitHub branch protection rules for `main`:

1. Go to Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Select: `test (3.11)` and `lint`
   - ✅ Require linear history (optional)
   - ✅ Include administrators

This ensures all code is tested before merging.

## Troubleshooting

### Tests pass locally but fail in CI
- Check Python version (CI tests multiple versions)
- Verify all dependencies in `pyproject.toml`
- Check for platform-specific code (macOS vs Linux)

### Cache issues
- Clear cache in GitHub Actions settings
- Or update `poetry.lock` to invalidate cache

### Slow workflow runs
- Cache is working if you see "Cache restored"
- First run is slow, subsequent runs are fast
- Matrix builds run in parallel for speed

## Customization

### Add more Python versions
Edit `test.yml`:
```yaml
python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
```

### Change trigger branches
Edit `on.push.branches` and `on.pull_request.branches`

### Add more checks
Create new workflow files in this directory:
- `security.yml` - Security scanning
- `dependencies.yml` - Dependency updates
- `release.yml` - Automated releases

## CI/CD Best Practices

1. **Keep workflows fast** - Use caching, run in parallel
2. **Test multiple versions** - Ensure compatibility
3. **Fail fast** - Linting before heavy tests
4. **Informative failures** - Verbose output, clear error messages
5. **Required checks** - Block merging if tests fail
6. **Version pinning** - Use specific versions for reproducibility
