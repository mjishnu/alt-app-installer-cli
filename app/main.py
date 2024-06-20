import argparse

from download import download
from install import install

parser = argparse.ArgumentParser(description="Alt App Installer CLI Help")
parser.add_argument("url", help="The URL of the app to install")
parser.add_argument(
    "-d",
    "--download_only",
    help="Download only, do not install",
    action="store_true",
)
parser.add_argument(
    "-i",
    "--ignore_ver",
    help="Ignore version of dependencies",
    action="store_true",
)
parser.add_argument(
    "-a",
    "--all_dependencies",
    help="Include all dependencies",
    action="store_true",
)

args = parser.parse_args()
print("Downloading Packages...")
data = download(args.url, args.ignore_ver, args.all_dependencies)
if not args.download_only:
    print("Installing Packages...")
    install(*data)
