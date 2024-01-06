#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#
# Licensed under the GNU General Public License v. 3 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2023-2023 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        mirror.sh
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2023-01-07     xqyjlj       initial version
# 2024-01-06     xqyjlj       only mirror
#

import os, re
import subprocess

repo = os.environ["INPUT_REPO"]


def main():
    match = re.search(r".*/(.+)\.git", repo)
    if match:
        name = match.group(1)
        gitee_repo = f"git@gitee.com:csplink/{name}.git"
        coding_repo = f"git@e.coding.net:csplink/csplink/{name}.git"
        gitlab_repo = f"git@gitlab.com:csplink/{name}.git"
        subprocess.run(["/bin/bash", "/mirror.sh", repo, gitee_repo], check=True)
        subprocess.run(["/bin/bash", "/mirror.sh", repo, coding_repo], check=True)
        subprocess.run(["/bin/bash", "/mirror.sh", repo, gitlab_repo], check=True)


if __name__ == "__main__":
    main()
