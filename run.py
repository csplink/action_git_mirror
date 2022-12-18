#!/usr/bin/env python3

import gitee
import os
import subprocess

token = os.environ["INPUT_DEST_TOKEN"]
dest = os.environ["INPUT_DEST"]
src_repo = os.environ["INPUT_SRC_REPO"]

dest_repo = src_repo.replace("github", dest, 1)


def main():
    if dest == "gitee":
        source_dir = src_repo.replace("git@github.com:", "").rstrip(".git")
        list = source_dir.split("/")
        gitee.get_or_create_repository(list[0], list[1], token)
    else:
        raise ("dest not support")

    subprocess.run(['/ci.sh', {src_repo}, {dest_repo}], check=True)


if __name__ == "__main__":
    main()
