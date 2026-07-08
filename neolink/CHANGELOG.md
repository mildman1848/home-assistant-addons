# Changelog

## 0.1.2

- Fix redacted Neolink support config generation so `password` and `pass` keys stay readable while values are hidden.
- Escape generated TOML strings safely for camera credentials and RTSP users.
- Restrict cameras to the configured RTSP user names instead of writing a placeholder `anyone` user.
- Add regression tests for Neolink config generation.

## 0.1.1

- Fix Home Assistant Supervisor store visibility by removing invalid empty `webui` field.
- Add `armv7` support for 32-bit Raspberry Pi OS installations using upstream `armhf` Neolink binary.
- Add Home Assistant Store presentation assets (`icon.png`, `logo.png`).

## 0.1.0

- Initial Home Assistant add-on repository release.
- Add Neolink bridge add-on skeleton.
- Generate `neolink.toml` from Home Assistant add-on options.
