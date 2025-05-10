import json
import os
import platform
import subprocess
import tarfile
import urllib.request
import urllib.request

from setuptools import setup, Command
from setuptools.command.install import install

RELEASES_URL = "https://api.github.com/repos/sass/dart-sass/releases"


def is_musl() -> bool:
    """Detects musl vs glibc."""
    try:
        ldd_output = subprocess.check_output(['ldd', '--version'],
                                             stderr=subprocess.STDOUT,
                                             text=True,
                                             universal_newlines=True)
        return 'musl' in ldd_output.lower()
    except Exception:
        return None


def get_platform_tag():
    system = platform.system().lower()
    machine = platform.machine().lower()

    arch = {
        'x86_64': 'x64',
        'amd64': 'x64',
        'aarch64': 'arm64',
        'armv7l': 'arm',
        'armv6l': 'arm',
        'i386': 'ia32',
        'i686': 'ia32',
        'riscv64': 'riscv64'
    }.get(machine, machine)

    tag = f"{system}-{arch}"
    if system == 'linux':
        if is_musl():
            tag += "-musl"
    return tag


def fetch_latest_url(platform_tag: str):
    req = urllib.request.Request(RELEASES_URL, headers={'User-Agent': 'Python urllib'})
    with urllib.request.urlopen(req) as response:
        data = json.load(response)

    assets = data[0]['assets']
    target = f"{platform_tag}.tar.gz"

    for asset in assets:
        name = asset['name']
        if target in name:
            return asset['browser_download_url']
    return None


class DownloadDependencyCommand(install):
    def run(self):
        # First run the standard install
        install.run(self)

        # Then download and install the custom dependency
        package_dir = os.path.join(self.install_lib, "sassquatch")
        dependency_dir = os.path.join(package_dir, "vendor")
        os.makedirs(dependency_dir, exist_ok=True)

        platform_tag = get_platform_tag()
        if not (url := fetch_latest_url(platform_tag)):
            raise ValueError(f"Unexpected platform: {platform_tag}")
        download_path = os.path.join(dependency_dir, "dart-sass.tar.gz")

        print(f"Downloading dependency from {url}")
        urllib.request.urlretrieve(url, download_path)

        with tarfile.open(download_path, "r:gz") as tar:
            tar.extractall(path=dependency_dir)

        os.remove(download_path)
        print(f"Successfully installed dependency to {dependency_dir}")


# Update the setup call
setup(
    cmdclass={
        'install': DownloadDependencyCommand,
    },
)
