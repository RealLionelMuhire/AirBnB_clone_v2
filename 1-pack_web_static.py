#!/usr/bin/python3
"""
This module contains the finction do_pack that generates  a .tgz from the
contents of the web_statoc folder (fabric script).
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """Fabric script to generate a .tgz archive from the contents of the
    web_static folde and store it in the versions directory."""

    local("mkdir -p versions")

    # Get the current date and time for the archive filename
    date = datetime.now().strftime("%Y%m%d%H%M%S")

    # Define the filename with the full path
    filename = "versions/web_static_{}.tgz".format(date)

    # Create the .tgz archive from the 'web_static' directory
    result = local("tar -cvzf {} web_static".format(filename))

    if result.succeeded:
        return filename
    else:
        return None
