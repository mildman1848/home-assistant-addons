# Neolink Add-on Documentation

## Example configuration

```yaml
log_level: info
bind: 0.0.0.0
bind_port: 8554
rtsp_users: []
cameras:
  - name: reolink_e1
    username: admin
    password: "YOUR_REOLINK_PASSWORD"
    address: 192.168.200.90:9000
    stream: both
```

## Options

### `log_level`

Controls Neolink logging. Use `debug` only during troubleshooting.

### `bind`

Address the RTSP server binds to. Default:

```text
0.0.0.0
```

### `bind_port`

RTSP server port. Default:

```text
8554
```

### `rtsp_users`

Optional RTSP users for Neolink's served streams.

```yaml
rtsp_users:
  - name: viewer
    password: "LONG_RANDOM_PASSWORD"
```

If users are configured, all cameras are restricted to authenticated users.

### `cameras`

List of Reolink cameras.

```yaml
cameras:
  - name: reolink_e1
    username: admin
    password: "YOUR_REOLINK_PASSWORD"
    address: 192.168.200.90:9000
    stream: both
```

`stream` can be:

- `both`
- `mainStream`
- `subStream`

If the camera has connection limits or behaves unreliably, use `subStream` first.

## Frigate example

Use the official Frigate add-on and add streams like:

```yaml
go2rtc:
  streams:
    reolink_e1_main:
      - rtsp://HOME_ASSISTANT_IP:8554/reolink_e1/mainStream
    reolink_e1_sub:
      - rtsp://HOME_ASSISTANT_IP:8554/reolink_e1/subStream

cameras:
  reolink_e1:
    ffmpeg:
      inputs:
        - path: rtsp://127.0.0.1:8554/reolink_e1_sub
          input_args: preset-rtsp-restream
          roles:
            - detect
    detect:
      width: 640
      height: 360
      fps: 5
```

## Security notes

- Do not expose RTSP to the internet.
- Prefer VPN for remote access.
- Use `rtsp_users` if other LAN clients can access port `8554`.
- Keep Reolink camera credentials unique.
