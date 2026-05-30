# Codeberg Mirror

Maintainer for Codeberg:

```text
mildman1848 <mildman1848@noreply.codeberg.org>
```

Recommended setup after the GitHub repository exists:

```bash
git remote add codeberg git@codeberg.org:mildman1848/home-assistant-addons.git
git push codeberg main
```

For the first release, GitHub Actions should remain the primary build pipeline. Codeberg can start as a source mirror. Add Woodpecker CI later if we want fully independent Codeberg builds.
