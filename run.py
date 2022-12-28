#!/usr/bin/env python3

import gitee
import os
import subprocess

token = os.environ["INPUT_DEST_TOKEN"]
dest = os.environ["INPUT_DEST"]
src_repo = os.environ["INPUT_SRC_REPO"]
is_user = os.environ["INPUT_IS_USER"] == str(True)

if os.environ["INPUT_DEST_REPO"].strip() == '':
    dest_repo = src_repo.replace("github", dest, 1)
else:
    dest_repo = os.environ["INPUT_DEST_REPO"]


def main():
    try:
        subprocess.run(["/bin/bash", "/ci.sh", src_repo, dest_repo], check=True)
        # if fail, create repo and retry
    except:
        if dest == "gitee":
            source_dir = dest_repo.replace("git@gitee.com:", "").rstrip(".git")
            list = source_dir.split("/")
            gitee.get_or_create_repository(list[0], list[1], token, is_user)
        else:
            raise ("dest not support")
        subprocess.run(["/bin/bash", "/ci.sh", src_repo, dest_repo], check=True)


if __name__ == "__main__":
    main()
