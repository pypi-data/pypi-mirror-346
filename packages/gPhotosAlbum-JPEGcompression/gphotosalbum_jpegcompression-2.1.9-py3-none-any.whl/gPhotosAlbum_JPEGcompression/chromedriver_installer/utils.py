# coding: utf-8
"""
Helper functions for filename and URL generation.
"""

import json
import logging
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as elemTree
import zipfile
from io import BytesIO
import platform as pf
from packaging import version

__author__ = "Yeongbin Jo <iam.yeongbin.jo@gmail.com>"

from typing import AnyStr, Optional


def get_chromedriver_filename():
    """
    Returns the filename of the binary for the current platform.
    :return: Binary filename
    """
    if sys.platform.startswith("win"):
        return "chromedriver.exe"
    return "chromedriver"


def get_env_variable_separator():
    """
    Returns the environment variable separator for the current platform.
    :return: Environment variable separator
    """
    if sys.platform.startswith("win"):
        return ";"
    return ":"


def determine_platform_architecture(chrome_version=None):
    if sys.platform.startswith("linux") and sys.maxsize > 2**32:
        platform = "linux"
        architecture = "64"
    elif sys.platform == "darwin":
        platform = "mac"
        if pf.processor() == "arm":
            if chrome_version is not None and get_major_version(chrome_version) >= "115":
                print("CHROME >= 115, using mac-arm64 as architecture identifier")
                architecture = "-arm64"
            elif chrome_version is not None and version.parse(chrome_version) <= version.parse("106.0.5249.21"):
                print("CHROME <= 106.0.5249.21, using mac64_m1 as architecture identifier")
                architecture = "64_m1"
            else:
                architecture = "_arm64"
        elif pf.processor() == "i386":
            if chrome_version is not None and get_major_version(chrome_version) >= "115":
                print("CHROME >= 115, using mac-x64 as architecture identifier")
                architecture = "-x64"
            else:
                architecture = "64"
        else:
            raise RuntimeError("Could not determine Mac processor architecture.")
    elif sys.platform.startswith("win"):
        platform = "win"
        architecture = "32"
    else:
        raise RuntimeError(
            "Could not determine chromedriver download URL for this platform."
        )
    return platform, architecture


def construct_chromedriver_url(chromedriver_version, download_options, disable_ssl=False):
    """
    Generates the download URL for the current platform, architecture, and the given version.
    Supports Linux, MacOS, and Windows.

    :param chromedriver_version: ChromeDriver version string
    :param disable_ssl:         Whether to use the encryption protocol when downloading the chrome driver
    :return:                   String. Download URL for chromedriver
    """
    platform, architecture = determine_platform_architecture(chromedriver_version)
    if get_major_version(chromedriver_version) >= "115":
        for option in download_options:
            if option["platform"] == platform + architecture:
                return option['url']
    else:
        base_url = "chromedriver.storage.googleapis.com/"
        base_url = "http://" + base_url if disable_ssl else "https://" + base_url
        return base_url + chromedriver_version + "/chromedriver_" + platform + architecture + ".zip"


def search_binary_in_path(filename):
    """
    Searches for a binary named `filename` in the current PATH. If an executable is found, its absolute path is returned
    else None.
    :param filename: Filename of the binary
    :return: Absolute path or None
    """
    if "PATH" not in os.environ:
        return None
    for directory in os.environ["PATH"].split(get_env_variable_separator()):
        binary = os.path.abspath(os.path.join(directory, filename))
        if os.path.isfile(binary) and os.access(binary, os.X_OK):
            return binary
    return None


def verify_version(binary, required_version):
    try:
        version = subprocess.check_output([binary, "-v"])
        version = re.match(r".*?([\d.]+).*?", version.decode("utf-8"))[1]
        if version == required_version:
            return True
    except Exception:
        return False
    return False


def fetch_chrome_version():
    """
    :return: the version of chrome installed on the client
    """
    platform, _ = determine_platform_architecture()
    if platform == "linux":
        path = get_linux_executable_path()
        with subprocess.Popen([path, "--version"], stdout=subprocess.PIPE) as proc:
            version = (
                proc.stdout.read()
                .decode("utf-8")
                .replace("Chromium", "")
                .replace("Google Chrome", "")
                .strip()
            )
    elif platform == "mac":
        process = subprocess.Popen(
            [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "--version",
            ],
            stdout=subprocess.PIPE,
        )
        version = (
            process.communicate()[0]
            .decode("UTF-8")
            .replace("Google Chrome", "")
            .strip()
        )
    elif platform == "win":
        PROGRAMFILES = f"{os.environ.get('PROGRAMW6432') or os.environ.get('PROGRAMFILES')}\\Google\\Chrome\\Application"
        PROGRAMFILESX86 = f"{os.environ.get('PROGRAMFILES(X86)')}\\Google\\Chrome\\Application"
        
        path = PROGRAMFILES if os.path.exists(PROGRAMFILES) else PROGRAMFILESX86 if os.path.exists(PROGRAMFILESX86) else None

        dirs = [f.name for f in os.scandir(path) if f.is_dir() and re.match("^[0-9.]+$", f.name)] if path else None

        version = max(dirs) if dirs else None
    else:
        return
    return version


def get_linux_executable_path():
    """
    Look through a list of candidates for Google Chrome executables that might
    exist, and return the full path to the first one that does. Raise a ValueError
    if none do.

    :return: the full path to a Chrome executable on the system
    """
    for executable in (
        "google-chrome",
        "google-chrome-stable",
        "google-chrome-beta",
        "google-chrome-dev",
        "chromium-browser",
        "chromium",
    ):
        path = shutil.which(executable)
        if path is not None:
            return path
    raise ValueError("No chrome executable found on PATH")


def get_major_version(version):
    """
    :param version: the version of chrome
    :return: the major version of chrome
    """
    return version.split(".")[0]


def find_matching_chromedriver_version(chrome_version, disable_ssl=False):
    """
    Try to find a specific version of ChromeDriver to match a version of Chrome.

    :param chrome_version: the version of Chrome to match against
    :param disable_ssl:    get version list using unsecured HTTP get
    :return:              String. The version of chromedriver that matches the Chrome version
                          None.   if no matching version of chromedriver was discovered
    """
    
    if get_major_version(chrome_version) >= "115":
        browser_major_version = get_major_version(chrome_version)
        version_url = "googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json"
        version_url = f"http://{version_url}" if disable_ssl else f"https://{version_url}"
        latest_version_per_milestone = json.load(urllib.request.urlopen(version_url))
        
        milestone = latest_version_per_milestone['milestones'].get(browser_major_version)
        if milestone:
            try:
                download_options = milestone['downloads']['chromedriver']
                return milestone['version'], download_options
            except KeyError:
                return None, None
                    
    else:
        version_url = "chromedriver.storage.googleapis.com"
        version_url = "http://" + version_url if disable_ssl else "https://" + version_url
        doc = urllib.request.urlopen(version_url).read()
        root = elemTree.fromstring(doc)
        for k in root.iter("{http://doc.s3.amazonaws.com/2006-03-01}Key"):
            if k.text.find(get_major_version(chrome_version) + ".") == 0:
                return k.text.split("/")[0], None
    return None, None


def get_chromedriver_path():
    """
    :return: path of the chromedriver binary
    """
    return os.path.abspath(os.path.dirname(__file__))


def display_chromedriver_path():
    """
    Print the path of the chromedriver binary.
    """
    print(get_chromedriver_path())


def download_chromedriver(install_path: Optional[AnyStr] = None, disable_ssl: bool = False):
    """
    Downloads, unzips and installs chromedriver.
    If a chromedriver binary is found in PATH it will be copied; otherwise downloaded.

    :param install_path: Path of the directory where to save the downloaded chromedriver to.
    :param disable_ssl: Determines whether or not to use the encryption protocol when downloading the chrome driver.
    :return: The file path of chromedriver
    """
    chrome_version = fetch_chrome_version()
    if not chrome_version:
        logging.debug("Chrome is not installed.")
        return
    chromedriver_version, download_options = find_matching_chromedriver_version(chrome_version, disable_ssl)
    
    major_version = get_major_version(chromedriver_version)

    if not chromedriver_version or (major_version >= "115" and not download_options):
        logging.warning(
            "Cannot find chromedriver for currently installed chrome version."
        )
        return

    if install_path:
        if not os.path.isdir(install_path):
            raise ValueError(f"Invalid path: {install_path}")
        chromedriver_directory = os.path.join(os.path.abspath(install_path), major_version)
    else:
        chromedriver_directory = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), major_version
        )
    chromedriver_filename = get_chromedriver_filename()
    chromedriver_filepath = os.path.join(chromedriver_directory, chromedriver_filename)
    if not os.path.isfile(chromedriver_filepath) or not verify_version(
        chromedriver_filepath, chromedriver_version
    ):
        logging.info(f"Downloading chromedriver ({chromedriver_version})...")
        if not os.path.isdir(chromedriver_directory):
            os.makedirs(chromedriver_directory)
            
        url = construct_chromedriver_url(chromedriver_version=chromedriver_version, download_options=download_options, disable_ssl=disable_ssl)
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() != 200:
                raise urllib.error.URLError("Not Found")
        except urllib.error.URLError:
            raise RuntimeError(f"Failed to download chromedriver archive: {url}")
        archive = BytesIO(response.read())
        with zipfile.ZipFile(archive) as zip_file:
            for zip_info in zip_file.infolist():
                if os.path.basename(zip_info.filename) == chromedriver_filename:
                    zip_info.filename = chromedriver_filename
                    zip_file.extract(zip_info, chromedriver_directory)
                    break
    else:
        logging.info("Chromedriver is already installed.")
    if not os.access(chromedriver_filepath, os.X_OK):
        os.chmod(chromedriver_filepath, 0o744)
    return chromedriver_filepath


if __name__ == "__main__":
    print(fetch_chrome_version())
    print(download_chromedriver(disable_ssl=False))
