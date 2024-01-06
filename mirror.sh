#!/bin/bash

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
# 2023-04-17     xqyjlj       initial version
#

ssh_private_key=${INPUT_SSH_PRIVATE_KEY}
src_repo=$1
dest_repo=$2

### config ssh
mkdir -p /root/.ssh
echo "${ssh_private_key}" >/root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa
echo "StrictHostKeyChecking no" >>/etc/ssh/ssh_config
mkdir -p ~/.ssh
cp /root/.ssh/* ~/.ssh/ 2>/dev/null || true

# mirror
repo=$(basename ${dest_repo})
prefix=./.github/mirror/repo

echo "mirror ${src_repo} => ${dest_repo}"

rm -rf ${prefix}/${repo} # cache
mkdir -p ${prefix}
git clone --mirror ${src_repo} ${prefix}/${repo} && cd ${prefix}/${repo}
git remote set-url --push origin "${dest_repo}"
git fetch -p origin

git for-each-ref --format 'delete %(refname)' refs/pull | git update-ref --stdin

git push --mirror
