#!/usr/bin/env python3

import gitee
import os

token = os.environ["INPUT_DEST_TOKEN"]
dest = os.environ["INPUT_DEST"]
src_repo = os.environ["INPUT_SRC_REPO"]

dest_repo = src_repo.replace("github", dest, 1)


def main():
    if dest == "gitee":
        source_dir = src_repo.replace("git@github.com:", "").replace(".git", "")
        list = source_dir.split("/")
        gitee.get_or_create_repository(list[0], list[1], token)
    else:
        raise ("dest not support")

    status = os.system(f'sh /ci.sh {src_repo} {dest_repo}')
    if status != 0:
        raise ("mirror fail")


if __name__ == "__main__":
    main()
