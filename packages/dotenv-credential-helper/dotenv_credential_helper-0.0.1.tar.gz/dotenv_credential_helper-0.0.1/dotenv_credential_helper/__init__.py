"""Keeping credentials secure through file permissions"""

__version__ = "0.0.1"

import os
import pathlib
import stat

from dotenv import load_dotenv


def get_credentials(file="~/.credentials"):
    """Read .env formatted file in only if permissions are rw----- by user"""
    if file != "~/.credentials":
        cred_file = pathlib.Path(file).resolve()
    else:
        home = pathlib.Path(os.environ["HOME"])
        cred_file = home / ".credentials"

    stat_info = cred_file.stat()
    if stat.filemode(stat_info.st_mode) != "-rw-------":
        print(f"Bad permissions on credentials file, {cred_file}. It cant be trusted")
        print("File should only be readable by the user")
        print("Current:", stat.filemode(stat_info.st_mode), "Required:", "-rw-------")
        raise (
            PermissionError(f"The file permissions on {file} need to be '-rw-------'")
        )

    # Order of precedence
    # 1. environment variables
    # 2. loaded .evn file variables
    load_dotenv(str(cred_file))
    """ Get credentials from environment variables """
    user = os.environ.get("USER", os.environ.get("USERNAME"))
    passwd = os.environ.get("PASSWD", os.environ.get("PASSWORD"))

    if user is None:
        print("The USER environment variable is not set")
        exit(1)
    if passwd is None:
        print("The PASSWD environment variable is not set")
        exit(1)

    return user, passwd
