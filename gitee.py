#!/usr/bin/env python3

import os
import urllib
import urllib.request
import json


def create_orgs_repository(owner, repo, token):
    url = f'https://gitee.com/api/v5/orgs/{owner}/repos'  # organization
    data = {}
    data["access_token"] = token
    data["name"] = repo
    data["has_issues"] = True
    data["has_wiki"] = True
    data["can_comment"] = True
    data = json.dumps(data)
    data = data.encode('utf-8')
    request = urllib.request.Request(url, data, {'content-type': 'application/json', 'charset': 'utf-8'})
    try:
        response = urllib.request.urlopen(request)
        resp = response.read().decode('utf-8')
    except Exception as e:
        print('create repositories: ' + repo + ' failed')
        print('e.code  : ' + str(e.code))
        print('e.reason: ' + str(e.reason))
    return json.loads(resp)


def create_user_repository(repo, token):
    url = 'https://gitee.com/api/v5/user/repos'  # user
    data = {}
    data["access_token"] = token
    data["name"] = repo
    data["has_issues"] = True
    data["has_wiki"] = True
    data["can_comment"] = True
    data = json.dumps(data)
    data = data.encode('utf-8')
    request = urllib.request.Request(url, data, {'content-type': 'application/json', 'charset': 'utf-8'})
    try:
        response = urllib.request.urlopen(request)
        resp = response.read().decode('utf-8')
    except Exception as e:
        print('create repositories: ' + repo + ' failed')
        print('e.code  : ' + str(e.code))
        print('e.reason: ' + str(e.reason))
    return json.loads(resp)


def get_or_create_repository(owner, repo, token, is_user=False):
    url = f'https://gitee.com/api/v5/repos/{owner}/{repo}?access_token={token}'
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
        resp = response.read().decode('utf-8')
    except Exception as e:
        if e.code == 404 or e.code == 410:
            if is_user:
                return create_user_repository(repo, token)
            else:
                return create_orgs_repository(owner, repo, token)
        else:
            print('get repository: ' + repo + ' failed, and http code not 404 ot 410!')
            print('e.code  : ' + str(e.code))
            print('e.reason: ' + str(e.reason))
    return json.loads(resp)
