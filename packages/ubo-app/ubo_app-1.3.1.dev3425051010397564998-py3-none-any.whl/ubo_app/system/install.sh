#!/usr/bin/env bash

set -o xtrace
set -o errexit
set -o pipefail
set -o nounset

USERNAME=${USERNAME:-"ubo"}
TARGET_VERSION=${TARGET_VERSION:-""}
UPDATE=${UPDATE:-false}
UPDATE_PREPARATION=${UPDATE_PREPARATION:-false}
WAIT_FOR_APP=${WAIT_FOR_APP:-false}
BETA=${BETA:-false}
IN_PACKER=${IN_PACKER:-false}
SOURCE=${SOURCE:-"ubo-app"}
INSTALLATION_PATH=${INSTALLATION_PATH:-"/opt/ubo"}
USERNAME=${USERNAME:-"ubo"}
WITH_DOCKER=${WITH_DOCKER:-true}
WITH_WM8960=${WITH_WM8960:-true}
OFFLINE=${OFFLINE:-false}

export DEBIAN_FRONTEND=noninteractive

# Parse arguments
for arg in "$@"; do
  case $arg in
  --username=*)
    USERNAME="${arg#*=}"
    shift
    ;;
  --target-version=*)
    TARGET_VERSION="${arg#*=}"
    shift
    ;;
  --update)
    UPDATE=true
    shift
    ;;
  --update-preparation)
    UPDATE_PREPARATION=true
    shift
    ;;
  --wait-for-app)
    WAIT_FOR_APP=true
    shift
    ;;
  --beta)
    BETA=true
    shift
    ;;
  --in-packer)
    IN_PACKER=true
    shift
    ;;
  --source=*)
    SOURCE="${arg#*=}"
    shift
    ;;
  --with-docker)
    WITH_DOCKER=true
    shift
    ;;
  --with-wm8960)
    WITH_WM8960=true
    shift
    ;;
  --offline)
    OFFLINE=true
    shift
    ;;
  *)
    echo "Unknown option: $arg"
    exit 1
    ;;
  esac
done

echo "----------------------------------------------"
echo "Parameters:"
echo "USERNAME: \"$USERNAME\""
echo "TARGET_VERSION: \"$TARGET_VERSION\""
echo "UPDATE: \"$UPDATE\""
echo "UPDATE_PREPARATION: \"$UPDATE_PREPARATION\""
echo "WAIT_FOR_APP: \"$WAIT_FOR_APP\""
echo "BETA: \"$BETA\""
echo "WITH_DOCKER: \"$WITH_DOCKER\""
echo "WITH_WM8960: \"$WITH_WM8960\""
echo "IN_PACKER: \"$IN_PACKER\""
echo "SOURCE: \"$SOURCE\""
echo "INSTALLATION_PATH: \"$INSTALLATION_PATH\""
echo "----------------------------------------------"

# Check for root privileges
if [ "$(id -u)" != "0" ] && [ "$UPDATE_PREPARATION" = false ]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

setup_virtualenv() {
  echo "Setting up Python virtual environment..."
  rm -rf "$INSTALLATION_PATH/env"                            # Remove old venv
  virtualenv --system-site-packages "$INSTALLATION_PATH/env" # Create new venv
  echo "Virtual environment created at $INSTALLATION_PATH/env."
}

PIP_FLAGS="ubo_app${TARGET_VERSION:+==$TARGET_VERSION}${BETA:+ --pre}"

# Application installation / update
if [ "$UPDATE_PREPARATION" = true ]; then
  if [ "$OFFLINE" = true ]; then
    echo "Offline mode is not supported for update preparation."
    exit 1
  fi

  # Prepare update: download packages
  echo "Preparing update: Downloading packages..."
  UPDATE_DIR="$INSTALLATION_PATH/_update"
  mkdir -p "$UPDATE_DIR"
  # Download Python package and dependencies
  "$INSTALLATION_PATH/env/bin/python" -m pip download \
    $PIP_FLAGS \
    --no-cache-dir \
    --dest "$UPDATE_DIR/" \
    setuptools wheel | tee >(grep -c '^Collecting ' >"$INSTALLATION_PATH/.packages-count")
  echo "Update preparation complete. Packages downloaded to $UPDATE_DIR."
else
  if id -u "$USERNAME" >/dev/null 2>&1; then
    echo "User $USERNAME already exists."
  else
    echo "Creating user $USERNAME..."
    adduser --disabled-password --gecos "" "$USERNAME"
    echo "User $USERNAME created successfully."
  fi

  if [ "$WAIT_FOR_APP" = true ]; then
    echo "Waiting for application signal at $INSTALLATION_PATH/app_ready..."
    count=0
    while [ ! -f "$INSTALLATION_PATH/app_ready" ] && [ $count -lt 300 ]; do
      sleep 1
      count=$((count + 1))
    done
    echo "Application signal received."
  fi

  echo "Adding user $USERNAME to required groups..."
  usermod -aG adm,audio,video,gpio,i2c,spi,kmem,render "$USERNAME"

  if grep -q "XDG_RUNTIME_DIR" "/home/$USERNAME/.bashrc"; then
    echo "XDG_RUNTIME_DIR already set in .bashrc"
  else
    echo "Setting XDG_RUNTIME_DIR in /home/$USERNAME/.bashrc..."
    echo "export XDG_RUNTIME_DIR=/run/user/$(id -u "$USERNAME")" >>"/home/$USERNAME/.bashrc"
  fi

  # Create the installation path
  mkdir -p "$INSTALLATION_PATH"
  chown -R "$USERNAME:$USERNAME" "$INSTALLATION_PATH"
  cd "$INSTALLATION_PATH"

  PIP_INSTALL_CMD="$INSTALLATION_PATH/env/bin/python -m pip install"
  PIP_FLAGS="$PIP_FLAGS --force-reinstall"

  if [ "$UPDATE" = true ]; then
    setup_virtualenv

    echo "Applying update from $INSTALLATION_PATH/_update/ ..." # Apply update from pre-downloaded packages
    $PIP_INSTALL_CMD $PIP_FLAGS --no-cache-dir --upgrade --no-index --find-links $INSTALLATION_PATH/_update/
  else
    if [ "$OFFLINE" = true ]; then
      echo "Offline mode is not supported for fresh installation."
      exit 1
    fi

    # Install required packages
    apt-get -fy install
    apt-get -y update
    apt-get -y install \
      accountsservice \
      dhcpcd \
      dnsmasq \
      git \
      hostapd \
      i2c-tools \
      ir-keytable \
      libasound2-dev \
      libcap-dev \
      libegl1 \
      libgl1 \
      libmtdev1 \
      libzbar0 \
      python3-alsaaudio \
      python3-apt \
      python3-dev \
      python3-gpiozero \
      python3-libcamera \
      python3-picamera2 \
      python3-pip \
      python3-virtualenv \
      --no-install-recommends --no-install-suggests
    apt-get -y clean
    apt-get -y autoremove

    setup_virtualenv

    # Fresh installation
    echo "Performing fresh installation of $SOURCE..."
    $PIP_INSTALL_CMD $PIP_FLAGS | tee >(grep -c '^Collecting ' >"$INSTALLATION_PATH/.packages-count")
  fi
  echo "Application $SOURCE installed/updated successfully."

  # Enable I2C and SPI
  raspi-config nonint do_i2c 0 || true
  raspi-config nonint do_spi 0 || true

  # Remove the Raspberry Pi's SSH daemon banner warning about setting a valid user
  sed -i '/^Banner /d' /etc/ssh/sshd_config.d/rename_user.conf || true

  # Set the ownership of the installation path
  chown -R "$USERNAME:$USERNAME" "$INSTALLATION_PATH"
  chmod -R 700 "$INSTALLATION_PATH"

  # Bootstrap the application
  UBO_LOG_LEVEL=INFO "$INSTALLATION_PATH/env/bin/ubo-bootstrap"${IN_PACKER:+ --in-packer}${WITH_WM8960:+ --with-wm8960}${WITH_DOCKER:+ --with-docker}
  echo "Bootstrapping completed"
fi

if [ "$UPDATE" = true ]; then
  # Remove the update directory
  rm -rf "$INSTALLATION_PATH/_update"
fi

if [ "$IN_PACKER" = true ] || [ "$UPDATE_PREPARATION" = true ]; then
  exit 0
else
  # The audio driver needs a reboot to work
  reboot
fi
