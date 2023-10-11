#!/usr/bin/python3
"""
this distributes an archive to your web servers, using the function do_deploy
"""

from fabric.api import local, env, put, run
import os

env.hosts = ['<IP web-01>', '<IP web-02>']

def do_deploy(archive_path):
    """
    distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_filename)[0]

        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, "/tmp/")

        # Create the folder to uncompress the archive
        run("sudo mkdir -p /data/web_static/releases/{}".format(archive_no_ext))

        # Uncompress the archive
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(archive_filename, archive_no_ext))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(archive_filename))

        # Delete the old symbolic link
        run("sudo rm /data/web_static/current")

        # Create a new symbolic link linked to the new version
        run("sudo ln -sf /data/web_static/releases/{} /data/web_static/current".format(archive_no_ext))

        return True
    except Exception:
        return False

