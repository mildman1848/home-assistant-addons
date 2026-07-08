import json
import os
import stat
import subprocess
import tempfile
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "neolink/rootfs/etc/cont-init.d/00-generate-config"


def run_generator(options: dict) -> tuple[dict, str, os.stat_result]:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        options_path = tmp / "options.json"
        output_path = tmp / "neolink.toml"
        redacted_path = tmp / "neolink.redacted.toml"
        options_path.write_text(json.dumps(options), encoding="utf-8")

        env = os.environ.copy()
        env.update(
            {
                "CONFIG_PATH": str(options_path),
                "NEOLINK_CONFIG": str(output_path),
                "REDACTED_CONFIG": str(redacted_path),
            }
        )

        subprocess.run(
            [
                "bash",
                "-c",
                (
                    "function bashio::log.info(){ :; }; "
                    "function bashio::log.debug(){ :; }; "
                    f"source {SCRIPT}"
                ),
            ],
            check=True,
            env=env,
            cwd=REPO_ROOT,
        )

        generated = tomllib.loads(output_path.read_text(encoding="utf-8"))
        redacted = redacted_path.read_text(encoding="utf-8")
        mode = output_path.stat()
        return generated, redacted, mode


def test_generate_config_escapes_toml_and_redacts_secrets() -> None:
    generated, redacted, mode = run_generator(
        {
            "log_level": "debug",
            "bind": "0.0.0.0",
            "bind_port": 8554,
            "rtsp_users": [
                {"name": "viewer_1", "password": "pa\\ss\"word"},
                {"name": "jacky", "password": "secret"},
            ],
            "cameras": [
                {
                    "name": "reolink_e1",
                    "username": "admin",
                    "password": "camera\"secret",
                    "address": "192.168.200.90:9000",
                    "stream": "mainStream",
                }
            ],
        }
    )

    assert generated["bind"] == "0.0.0.0"
    assert generated["bind_port"] == 8554
    assert generated["users"] == [
        {"name": "viewer_1", "pass": 'pa\\ss"word'},
        {"name": "jacky", "pass": "secret"},
    ]
    assert generated["cameras"][0]["stream"] == "mainStream"
    assert generated["cameras"][0]["permitted_users"] == ["viewer_1", "jacky"]
    assert stat.S_IMODE(mode.st_mode) == 0o600

    assert "camera\"secret" not in redacted
    assert 'pa\\ss"word' not in redacted
    assert redacted.count('password = "REDACTED"') == 1
    assert redacted.count('pass = "REDACTED"') == 2


def test_generate_config_omits_auth_when_no_rtsp_users() -> None:
    generated, redacted, _mode = run_generator(
        {
            "log_level": "info",
            "bind": "127.0.0.1",
            "bind_port": 8554,
            "rtsp_users": [],
            "cameras": [
                {
                    "name": "frontdoor",
                    "username": "admin",
                    "password": "camera-password",
                    "address": "frontdoor.local:9000",
                    "stream": "both",
                }
            ],
        }
    )

    assert "users" not in generated
    assert "permitted_users" not in generated["cameras"][0]
    assert "stream" not in generated["cameras"][0]
    assert "camera-password" not in redacted
