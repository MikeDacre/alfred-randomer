## SETUP

This documentation is for those who want to setup this workflow locally to do some work on it.


### poetry

This workflow uses a tool called [poetry](https://python-poetry.org) for depencency management. 
To install poetry in your local enviroment follow [these instructions](https://python-poetry.org/docs/#installation).


### dependencies

Once you have poetry installed, the next thing is to fetch all of this project's dependencies using the command `poetry install` or `make install`.
This command will use the `pyproject.toml` file to create a virtual env and install all the necesary libraries from pypi.


### development

A Makefile is provided for convenience. Run `make help` to see all available commands:

- `make build` - Build the workflow
- `make test` - Run tests
- `make format` - Format code with Black
- `make clean` - Clean build artifacts


### releasing

To create a release and import it into Alfred:

**Simple releases:**
- `make release-patch` - Bump patch version (bug fixes)
- `make release-minor` - Bump minor version (new features)
- `make release-major` - Bump major version (breaking changes)

**Advanced options:**
```bash
# Prerelease versions
./scripts/release.sh prerelease   # 1.0.0 → 1.0.0-alpha.1

# Specific version
./scripts/release.sh 2.0.0

# Skip git commit
./scripts/release.sh patch --no-git

# Skip tests
./scripts/release.sh minor --skip-tests
```

Run `./scripts/release.sh --help` for full details.

The release process:
1. Updates version in `pyproject.toml` and `info.plist`
2. Runs tests
3. Builds the workflow
4. Creates `.alfredworkflow` file in `releases/`
5. Commits to git and creates version tag
6. Opens the workflow in Alfred for import

> You can find the generated `.alfredworkflow` files in the `releases/` folder.