# auto-module-tagging-action

GitHub Action for automatic Go module tagging with optional dockerized
execution.

## Features

- ✅ Detects changed Go modules and increments tags (major/minor/patch)
- ✅ Supports explicit module lists or auto-detection
- ✅ Dry-run mode for safe previews
- ✅ Optional docker execution via GHCR image

## Usage

```yaml
jobs:
  tag:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - uses: jdfalk/auto-module-tagging-action@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          version-increment: minor
          dry-run: false
```

### Specify Modules Manually

```yaml
- uses: jdfalk/auto-module-tagging-action@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    module-paths: module-a,module-b
    detect-modules: false
```

### Force Docker Execution

```yaml
- uses: jdfalk/auto-module-tagging-action@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    use-docker: true
    docker-image: ghcr.io/jdfalk/auto-module-tagging-action:main
```

## Inputs

| Input               | Description                                                      | Required | Default                                          |
| ------------------- | ---------------------------------------------------------------- | -------- | ------------------------------------------------ |
| `github-token`      | GitHub token for creating tags                                   | Yes      | (none)                                           |
| `detect-modules`    | Auto-detect changed Go modules                                   | No       | `true`                                           |
| `module-paths`      | Explicit module paths (comma-separated)                          | No       | `''`                                             |
| `version-increment` | Version increment type (`major`, `minor`, `patch`)               | No       | `patch`                                          |
| `dry-run`           | Perform dry run without creating tags                            | No       | `false`                                          |
| `tag-prefix`        | Prefix for module tags                                           | No       | `''`                                             |
| `commit-pattern`    | Regex pattern to match commit messages for versioning            | No       | `''`                                             |
| `use-docker`        | Run the action inside the published container image              | No       | `false`                                          |
| `docker-image`      | Docker image reference (tag or digest) when `use-docker` is true | No       | `ghcr.io/jdfalk/auto-module-tagging-action:main` |

## Outputs

| Output            | Description                          |
| ----------------- | ------------------------------------ |
| `tags-created`    | JSON array of tags that were created |
| `modules-updated` | Number of modules updated/tagged     |

## Notes

- Docker path requires the action to have push access via `github-token`.
- When `detect-modules` is true, modules are inferred from
  `git diff HEAD~1 HEAD`.
