# Contributing

Thanks for contributing to `mildman1848/home-assistant-addons`.

## Principles

- Keep add-ons Home Assistant native.
- Prefer explicit `build.yaml` base images.
- Keep privileges minimal.
- Do not commit secrets, tokens, camera credentials, private keys, or recovery codes.
- Update docs and changelog for user-facing changes.
- Use clear, small commits.

## Local validation

From the repository root:

```bash
yamllint .
find . -type f \
  \( -name '*.sh' -o -path '*/rootfs/etc/services.d/*/run' -o -path '*/rootfs/etc/cont-init.d/*' \) \
  -print0 | xargs -0 -r shellcheck
```

## Add-on security expectations

- No `full_access` unless absolutely unavoidable.
- No `privileged` unless documented and justified.
- Do not expose services to the internet by default.
- Prefer Home Assistant `schema` validation for all user inputs.
- Use `password` schema for credentials.
