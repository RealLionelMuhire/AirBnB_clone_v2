#!/usr/bin/python3
from fabric.api import env, run, put, local
from datetime import datetime
from os.path import exists
from os.path import isfile

env.hosts = ['3.84.161.50', '100.25.131.191']

def do_pack():
    """Creates a tar archive of the web_static directory."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static".format(timestamp))
        return "versions/web_static_{}.tgz".format(timestamp)
    except Exception:
        return None

def do_deploy(archive_path):
    """Deploys a web static package to the servers"""
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        archive_name_no_ext = archive_name.split(".")[0]
        remote_path = "/tmp/" + archive_name
        remote_folder = "/data/web_static/releases/" + archive_name_no_ext

        put(archive_path, remote_path)
        run("mkdir -p {}".format(remote_folder))
        run("tar -xzf {} -C {}".format(remote_path, remote_folder))
        run("rm -f {}".format(remote_path))
        run("mv {}/web_static/* {}/".format(remote_folder, remote_folder))
        run("rm -rf {}/web_static".format(remote_folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(remote_folder))

        return True
    except Exception:
        return False

def deploy():
    """Creates and distributes an archive to web servers and deploys it."""
    archive_path = do_pack()
    if not archive_path:
        return False

    deploy_result = do_deploy(archive_path)
    return deploy_result

if __name__ == "__main__":
    deploy()

