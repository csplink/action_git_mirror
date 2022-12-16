#!/usr/bin/env python3

import gitee
import os

ssh_private_key = os.environ["INPUT_SSH_PRIVATE_KEY"]
token = os.environ["INPUT_DEST_TOKEN"]
dest = os.environ["INPUT_DEST"]
src_repo = os.environ["INPUT_SRC_REPO"]

dest_repo = src_repo.replace("github", dest)


def main():
    if dest == "gitee":
        source_dir = src_repo.replace("git@github.com:", "").replace(".git", "")
        list = source_dir.split("/")
        gitee.get_or_create_repository(list[0], list[1], token)
    else:
        raise ("dest not support")

    os.system(f'./ci.sh {ssh_private_key} {src_repo} {dest_repo}')


if __name__ == "__main__":
    main()
