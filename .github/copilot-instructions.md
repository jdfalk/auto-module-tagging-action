<!-- file: .github/copilot-instructions.md -->
<!-- version: 2.4.0 -->
<!-- guid: 4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a -->
<!-- last-edited: 2026-06-13 -->

# gha-auto-module-tagging — Additional Context

Org-wide coding standards (file headers, language rules, commit format) are at
**<https://github.com/falkcorp/.github>** and apply automatically to this repo.

For full project context: **CLAUDE.md** at the repo root.

## Project overview

GHA composite action: automatic Go module tagging. Language: Python/YAML.
Detects changed Go modules in a monorepo and automatically creates version tags.

## Critical constraints

- This is a GitHub Actions composite action — `action.yml` is the primary entry point.
- Tag format follows Go module versioning conventions (`module/path/vX.Y.Z`).
- Python scripts are used for module detection and tag calculation logic.
