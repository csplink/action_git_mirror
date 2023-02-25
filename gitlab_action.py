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
# @file        gitlab_action.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2023-02-25     xqyjlj       initial version
#

import gitlab


def get_or_create_repository(host, owner, repo, token, is_user=False):
    gl = gitlab.Gitlab(host, private_token=token)
    obj = 0
    if is_user:
        obj = gl.users.list(username=owner)[0]
    else:
        obj = gl.groups.list(search=owner)[0]
    assert obj.name == owner, f"not found owner: {owner}"
    repos = obj.projects.list(search=repo)
    if len(repos) == 0 or repos[0].name != repo:
        gl.projects.create({'name': repo, 'namespace_id': obj.id, 'visibility': 'public'})
