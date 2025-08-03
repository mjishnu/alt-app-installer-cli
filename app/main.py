import argparse

from download import download
from install import install

VERSION = "v1.1.0"

parser = argparse.ArgumentParser(description="Alt App Installer CLI Help")
parser.add_argument("url", help="The URL of the app to install")
parser.add_argument(
    "-v", "--version", action="version", version=f"Alt App Installer CLI {VERSION}"
)
parser.add_argument(
    "-d",
    "--download_only",
    help="Download only, do not install",
    action="store_true",
)
parser.add_argument(
    "-deps",
    "--dependencies",
    help="Dependency handling mode (default: required)",
    choices=["all", "required", "ignore_ver", "none"],
    default="required",
)
parser.add_argument(
    "-p",
    "--progress",
    help="Set the progress bar type (default: full)",
    choices=["full", "simple", "none"],
    default="full",
)
parser.add_argument(
    "-o",
    "--output",
    help="Output directory for downloaded files (default: ./downloads)",
    type=str,
)

parser.add_argument(
    "-a",
    "--arch",
    help="Architecture to use for downloading (default: auto-detect)",
    type=str,
    choices=["x64", "arm", "arm64", "x86", "auto"],
    default="auto",
)

args = parser.parse_args()

dep_mapping = {
    "all": {
        "all_dependencies": True,
        "ignore_ver": False,
        "no_dependencies": False,
    },
    "required": {
        "all_dependencies": False,
        "ignore_ver": False,
        "no_dependencies": False,
    },
    "ignore_ver": {
        "all_dependencies": False,
        "ignore_ver": True,
        "no_dependencies": False,
    },
    "none": {
        "all_dependencies": False,
        "ignore_ver": False,
        "no_dependencies": True,
    },
}

dep_config = dep_mapping[args.dependencies]


print("Downloading Packages...")
data = download(args.url, args.progress, args.output, args.arch, **dep_config)
if not args.download_only:
    print("Installing Packages...")
    install(*data)
