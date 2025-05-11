# coding: utf-8

import logging
import os
from typing import AnyStr, Optional

from . import utils


def install_chromedriver(is_current_working_dir: bool = False, install_path: Optional[AnyStr] = None, disable_ssl: bool = False):
    """
    Appends the directory of the chromedriver binary file to PATH.

    :param is_current_working_dir: Flag indicating whether to download to current working directory. If `is_current_working_dir` is True, then `install_path` argument will be ignored.
    :param install_path: Specify the path where the Chrome driver will be installed. If `is_current_working_dir` value is True, this value is ignored.
    :param disable_ssl: Determines whether or not to use the encryption protocol when downloading the chrome driver.
    :return: The file path of chromedriver
    """
    if is_current_working_dir:
        install_path = os.getcwd()
    chromedriver_filepath = utils.download_chromedriver(install_path, disable_ssl)
    if not chromedriver_filepath:
        logging.debug("Cannot download chromedriver.")
        return
    chromedriver_dir = os.path.dirname(chromedriver_filepath)
    if "PATH" not in os.environ:
        os.environ["PATH"] = chromedriver_dir
    elif chromedriver_dir not in os.environ["PATH"]:
        os.environ["PATH"] = (
            chromedriver_dir + utils.get_env_variable_separator() + os.environ["PATH"]
        )
    return chromedriver_filepath


def fetch_chrome_version():
    """
    Get installed version of chrome on client.

    :return: The version of chrome
    """
    return utils.fetch_chrome_version()
