#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2022-2023 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        run.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2023-01-07     xqyjlj       initial version
#

import coding
import gitee
import gitlab_action
import os, re
import subprocess

token = os.environ["INPUT_DEST_TOKEN"]
dest = os.environ["INPUT_DEST"]
src_repo = os.environ["INPUT_SRC_REPO"]
is_user = os.environ["INPUT_IS_USER"] == str(True)

if os.environ["INPUT_DEST_REPO"].strip() == '':
    if dest == "gitee":
        dest_repo = src_repo.replace("git@github.com:", "git@gitee.com:", 1)
    elif dest == "coding" or dest == "gitlab":
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
        elif dest == "gitlab":
            host = "https://" + re.search(r"(?<=git@).*?(?=:)", dest_repo).group()
            owner = re.search(r"(?<=:).*?(?=[^/]+$)", dest_repo).group().strip("/")
            repo = re.search(r"(?=[^/]+(?!.*/)).*?(?=\.git)", dest_repo).group()
            gitlab_action.get_or_create_repository(host, owner, repo, token, is_user)
        else:
            raise ("dest not support")
        print("*******************************************************************************************************")
        print("try mirror again")
        subprocess.run(["/bin/bash", "/ci.sh", src_repo, dest_repo], check=True)


if __name__ == "__main__":
    main()
