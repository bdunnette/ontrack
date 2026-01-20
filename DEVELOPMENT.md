# Development Tools Setup

This document describes the development tools configured for the OnTrack project.

## Dependabot

**Location**: [.github/dependabot.yml](file:///c:/Users/dunn0172/Documents/GitHub/ontrack/.github/dependabot.yml)

Dependabot is configured to automatically check for dependency updates:

### Python Dependencies
- **Schedule**: Weekly on Mondays
- **Package ecosystem**: pip
- **Grouping**: Minor and patch updates are grouped together
- **Pull request limit**: 5 open PRs at a time
- **Labels**: `dependencies`, `python`
- **Commit prefix**: `chore`

### GitHub Actions
- **Schedule**: Weekly on Mondays
- **Pull request limit**: 5 open PRs at a time
- **Labels**: `dependencies`, `github-actions`
- **Commit prefix**: `chore`

## Pre-commit Hooks

**Location**: [.pre-commit-config.yaml](file:///c:/Users/dunn0172/Documents/GitHub/ontrack/.pre-commit-config.yaml)

Pre-commit hooks run automatically before each commit to ensure code quality.

### Configured Hooks

#### General File Checks
- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with a newline
- **check-yaml**: Validates YAML syntax
- **check-json**: Validates JSON syntax
- **check-toml**: Validates TOML syntax
- **check-added-large-files**: Prevents committing large files (>1MB)
- **check-merge-conflict**: Detects merge conflict markers
- **detect-private-key**: Prevents committing private keys
- **mixed-line-ending**: Fixes mixed line endings (converts to LF)

#### Python Code Quality
- **ruff (linter)**: Fast Python linter with auto-fix
- **ruff-format**: Fast Python code formatter (replaces Black)

### Installation

Pre-commit is installed automatically when you run:

```bash
uv sync --all-groups
```

To install the git hooks:

```bash
uv run pre-commit install
```

### Usage

Pre-commit hooks run automatically on `git commit`. To run manually:

```bash
# Run on all files
uv run pre-commit run --all-files

# Run on staged files only
uv run pre-commit run

# Run a specific hook
uv run pre-commit run ruff --all-files
```

### Bypassing Hooks

If you need to bypass pre-commit hooks (not recommended):

```bash
git commit --no-verify
```

## Benefits

### Dependabot
- ✅ Automatic dependency updates
- ✅ Security vulnerability alerts
- ✅ Reduced manual maintenance
- ✅ Grouped updates to reduce PR noise

### Pre-commit
- ✅ Consistent code formatting
- ✅ Catch common errors before commit
- ✅ Automated code quality checks
- ✅ Faster CI/CD pipelines (issues caught locally)
- ✅ Reduced code review time

## Configuration Files

All configuration is stored in version control:

- [.github/dependabot.yml](file:///c:/Users/dunn0172/Documents/GitHub/ontrack/.github/dependabot.yml) - Dependabot configuration
- [.pre-commit-config.yaml](file:///c:/Users/dunn0172/Documents/GitHub/ontrack/.pre-commit-config.yaml) - Pre-commit hooks configuration
- [pyproject.toml](file:///c:/Users/dunn0172/Documents/GitHub/ontrack/pyproject.toml) - Python project configuration with dev dependencies

## Verification

Pre-commit hooks have been tested and all checks pass:

```
✓ trim trailing whitespace
✓ fix end of files
✓ check yaml
✓ check for added large files
✓ check json
✓ check toml
✓ check for merge conflicts
✓ detect private key
✓ mixed line ending
✓ ruff (linter)
✓ ruff-format (formatter)
```
