#!/bin/bash

set -x

function config_ssh {
    ssh_private_key=$1

    mkdir -p /root/.ssh
    echo "${ssh_private_key}" >/root/.ssh/id_rsa
    chmod 600 /root/.ssh/id_rsa
    echo "StrictHostKeyChecking no" >>/etc/ssh/ssh_config
    mkdir -p ~/.ssh
    cp /root/.ssh/* ~/.ssh/ 2>/dev/null || true
}

function mirror {
    src_repo=$1
    dest_repo=$2
    repo=$(basename ${dest_repo})
    prefix=./.github/mirror/repo

    echo "mirror ${src_repo} => ${dest_repo}"

    mkdir -p ${prefix}
    git clone --mirror ${src_repo} ${prefix}/${repo} && cd ${prefix}/${repo}
    git remote set-url --push origin "${dest_repo}"
    git fetch -p origin

    git for-each-ref --format 'delete %(refname)' refs/pull | git update-ref --stdin

    git push --mirror
}
