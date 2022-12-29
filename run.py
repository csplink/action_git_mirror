#!/usr/bin/env python3

import coding
import gitee
import os
import subprocess

token = os.environ["INPUT_DEST_TOKEN"]
dest = os.environ["INPUT_DEST"]
src_repo = os.environ["INPUT_SRC_REPO"]
is_user = os.environ["INPUT_IS_USER"] == str(True)

if os.environ["INPUT_DEST_REPO"].strip() == '':
    if dest == "gitee":
        dest_repo = src_repo.replace("git@github.com:", "git@gitee.com:", 1)
    elif dest == "coding":
        raise ("coding not support empty dest_repo, please set dest_repo")
else:
    dest_repo = os.environ["INPUT_DEST_REPO"]


def main():
    try:
        subprocess.run(["/bin/bash", "/ci.sh", src_repo, dest_repo], check=True)
        # if fail, create repo and retry
    except:
        print("*******************************************************************************************************")
        print("mirror fail, try create repo")
        if dest == "gitee":
            source_dir = dest_repo.replace("git@gitee.com:", "").rstrip(".git")
            list = source_dir.split("/")
            gitee.get_or_create_repository(list[0], list[1], token, is_user)
        elif dest == "coding":
            source_dir = dest_repo.replace("git@e.coding.net:", "").rstrip(".git")
            list = source_dir.split("/")
            coding.get_or_create_repository(list[0], list[1], list[2], token)
        else:
            raise ("dest not support")
        print("*******************************************************************************************************")
        print("try mirror again")
        subprocess.run(["/bin/bash", "/ci.sh", src_repo, dest_repo], check=True)


if __name__ == "__main__":
    main()
