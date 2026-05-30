# Maintainer Access Runbook

This document describes the intended maintenance access model for this repository.

> Do not commit tokens, private keys, passwords, recovery codes, or 2FA secrets.

## Accounts

| Platform | Account | Purpose |
|---|---|---|
| GitHub | `mildman1848` | Primary repository, Actions, GHCR packages |
| Codeberg | `mildman1848` | Source mirror / fallback forge |

## GitHub

Primary repo:

```text
https://github.com/mildman1848/home-assistant-addons
```

Recommended access methods:

1. `gh` CLI authenticated with a maintainer token.
2. Dedicated SSH key for Git fallback.
3. GitHub Actions `GITHUB_TOKEN` for CI builds and GHCR package pushes.

### Recommended GitHub token permissions

For long-term maintenance, prefer a fine-grained Personal Access Token or GitHub App with only the required permissions.

Recommended fine-grained repository permissions:

| Permission | Level | Purpose |
|---|---|---|
| Contents | Read and write | Push code and manage files |
| Actions | Read and write | Trigger and inspect workflows |
| Administration | Read and write | Repository settings and branch protection |
| Packages | Read and write | GHCR package management |
| Workflows | Read and write | Edit workflow files |
| Issues | Read and write | Issue maintenance |
| Pull requests | Read and write | PR maintenance |
| Secrets | Read and write | Set Actions secrets |
| Metadata | Read-only | Required by GitHub |

If GitHub's fine-grained token does not expose a needed API, use a narrowly scoped classic token temporarily.

Classic fallback scopes:

```text
repo
workflow
read:packages
write:packages
admin:public_key
```

Add `delete_repo` only temporarily when a repository deletion is explicitly required.

### GitHub SSH fallback

Dedicated local key path on the Hermes host:

```text
~/.ssh/hermes_github_mildman1848
```

Public key title:

```text
hermes-github-mildman1848
```

Add the public key in GitHub:

```text
https://github.com/settings/keys
```

## Codeberg

Mirror repo:

```text
https://codeberg.org/mildman1848/home-assistant-addons
```

Recommended access methods:

1. Dedicated SSH key for Git push/pull.
2. Codeberg/Forgejo API token for repository creation and metadata updates.

### Codeberg SSH fallback

Dedicated local key path on the Hermes host:

```text
~/.ssh/hermes_codeberg_mildman1848
```

Public key title:

```text
hermes-codeberg-mildman1848
```

### Recommended Codeberg token permissions

Forgejo/Codeberg may require `write:user` to create repositories through the API.

Recommended token capabilities:

| Scope / Area | Purpose |
|---|---|
| `write:user` | Create user-owned repositories |
| Repository read/write | Edit repository contents and metadata |
| User read | Verify authenticated account |

Do not grant admin/global scopes unless needed for a specific maintenance task.

## Remotes

Expected remotes:

```bash
git remote -v
```

```text
origin    https://github.com/mildman1848/home-assistant-addons.git
codeberg  git@codeberg.org:mildman1848/home-assistant-addons.git
```

## Routine maintenance

### Push to GitHub

```bash
git push origin main
```

### Push mirror to Codeberg

```bash
git push codeberg main
```

### Check GitHub Actions

```bash
gh run list --repo mildman1848/home-assistant-addons --limit 10
```

### Check workflows

```bash
gh workflow list --repo mildman1848/home-assistant-addons
```

## Revocation checklist

If access must be revoked:

1. Revoke the GitHub maintainer token.
2. Remove `hermes-github-mildman1848` from GitHub SSH keys.
3. Revoke the Codeberg API token.
4. Remove `hermes-codeberg-mildman1848` from Codeberg SSH keys.
5. Rotate any repository or Actions secrets that may have been exposed.
