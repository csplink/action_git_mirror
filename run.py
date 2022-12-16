#!/usr/bin/env python3

import gitee
import os

ssh_private_key = os.environ["INPUT_SSH_PRIVATE_KEY"]
token = os.environ["INPUT_DEST_TOKEN"]
dest = os.environ["INPUT_DEST"]
src_repo = os.environ["INPUT_SRC_REPO"]

dest_repo = src_repo.replace("github", dest)


def config_ssh():
    os.system('source ci.sh && config_ssh %s' % ssh_private_key)


def mirror():
    os.system('source ci.sh && mirror %s %s' % src_repo, dest_repo)


def main():
    if dest == "gitee":
        source_dir = src_repo.replace("git@github.com:", "").replace(".git", "")
        list = source_dir.split("/")
        gitee.get_or_create_repository(list[0], list[1], token)
    else:
        raise ("dest not support")

    config_ssh()
    mirror()


if __name__ == "__main__":
    main()
