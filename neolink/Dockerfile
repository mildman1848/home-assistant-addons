ARG BUILD_FROM
FROM ${BUILD_FROM}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_ARCH
ARG NEOLINK_VERSION

# Install runtime dependencies for Neolink/GStreamer and tools used by init scripts.
RUN apt-get update     && apt-get install -y --no-install-recommends         ca-certificates         curl         unzip         jq         libgstrtspserver-1.0-0         libgstreamer1.0-0         libgstreamer-plugins-bad1.0-0         gstreamer1.0-tools         gstreamer1.0-x         gstreamer1.0-plugins-base         gstreamer1.0-plugins-good         gstreamer1.0-plugins-bad         gstreamer1.0-libav         openssl     && rm -rf /var/lib/apt/lists/*

# Download upstream Neolink release binary matching the Home Assistant build architecture.
RUN set -eux;     case "${BUILD_ARCH}" in       amd64) asset="neolink_linux_x86_64_bullseye.zip" ;;       aarch64) asset="neolink_linux_arm64.zip" ;;       *) echo "Unsupported architecture: ${BUILD_ARCH}" >&2; exit 1 ;;     esac;     url="https://github.com/QuantumEntangledAndy/neolink/releases/download/${NEOLINK_VERSION}/${asset}";     curl -fsSL "${url}" -o /tmp/neolink.zip;     unzip /tmp/neolink.zip -d /tmp/neolink;     install -m 0755 "$(find /tmp/neolink -type f -name neolink | head -n 1)" /usr/local/bin/neolink;     rm -rf /tmp/neolink /tmp/neolink.zip;     neolink --version

COPY rootfs /

RUN find /etc/cont-init.d /etc/services.d -type f -print -exec chmod +x {} \;
