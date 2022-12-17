#!/bin/bash

set -x

ssh_private_key=${INPUT_SSH_PRIVATE_KEY}
src_repo=$2
dest_repo=$3

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

mkdir -p ${prefix}
git clone --mirror ${src_repo} ${prefix}/${repo} && cd ${prefix}/${repo}
git remote set-url --push origin "${dest_repo}"
git fetch -p origin

git for-each-ref --format 'delete %(refname)' refs/pull | git update-ref --stdin

git push --mirror
