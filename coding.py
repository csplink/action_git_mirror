#!/usr/bin/env python3

import urllib
import urllib.request
import json


def create_project(team,
                   name,
                   token,
                   display_name="",
                   readme_enabled=False,
                   vcs_type="git",
                   create_svn_layout=False,
                   shared=1,
                   project_template="DEV_OPS"):
    if display_name == "":
        display_name = name

    url = f'https://{team}.coding.net/open-api?Action=CreateCodingProject'  # https://coding.net/help/openapi#3a2e078215fb8749e58c8e4d36803aba
    data = {}
    data["Action"] = "CreateCodingProject"
    data["Name"] = name
    data["DisplayName"] = display_name
    data["GitReadmeEnabled"] = readme_enabled
    data["VcsType"] = vcs_type
    data["CreateSvnLayout"] = create_svn_layout
    data["Shared"] = shared
    data["ProjectTemplate"] = project_template
    data = json.dumps(data)
    data = data.encode('utf-8')
    request = urllib.request.Request(url, data, {
        'content-type': 'application/json',
        'charset': 'utf-8',
        'Authorization': f'token {token}'
    })
    try:
        response = urllib.request.urlopen(request)
        resp = response.read().decode('utf-8')
    except Exception as e:
        print('create project: ' + name + ' failed')
        print('e.code  : ' + str(e.code))
        print('e.reason: ' + str(e.reason))
    return json.loads(resp)


def create_repository(team, id, name, token, description="", shared=True):
    url = f'https://{team}.coding.net/open-api?Action=CreateGitDepot'  # https://coding.net/help/openapi#f40ea33719a0a932a54bf4cf7adf9855
    data = {}
    data["Action"] = "CreateGitDepot"
    data["ProjectId"] = id
    data["DepotName"] = name
    data["Description"] = description
    data["Shared"] = shared
    data = json.dumps(data)
    data = data.encode('utf-8')
    request = urllib.request.Request(url, data, {
        'content-type': 'application/json',
        'charset': 'utf-8',
        'Authorization': f'token {token}'
    })
    try:
        response = urllib.request.urlopen(request)
        resp = response.read().decode('utf-8')
    except Exception as e:
        print('create repository: ' + name + ' failed')
        print('e.code  : ' + str(e.code))
        print('e.reason: ' + str(e.reason))
    return json.loads(resp)


def get_projects(team, token, page_number=1, page_size=100, name=""):
    url = f'https://{team}.coding.net/open-api?Action=DescribeCodingProjects'  # https://coding.net/help/openapi#add1b386a4ce6a8ddc07fb10fff254e8
    data = {}
    data["Action"] = "DescribeCodingProjects"
    data["PageNumber"] = page_number
    data["PageSize"] = page_size
    if name != "":
        data["Name"] = name
    data = json.dumps(data)
    data = data.encode('utf-8')
    request = urllib.request.Request(url, data, {
        'content-type': 'application/json',
        'charset': 'utf-8',
        'Authorization': f'token {token}'
    })
    try:
        response = urllib.request.urlopen(request)
        resp = response.read().decode('utf-8')
    except Exception as e:
        print(f'get {team} projects failed')
        print('e.code  : ' + str(e.code))
        print('e.reason: ' + str(e.reason))
    return json.loads(resp)


def get_project_repositories(team, id, token):
    url = f'https://{team}.coding.net/open-api?Action=DescribeProjectDepotInfoList'  # https://coding.net/help/openapi#04f0f34041e112aabd648c8381f31ca5
    data = {}
    data["Action"] = "DescribeProjectDepotInfoList"
    data["ProjectId"] = id
    data = json.dumps(data)
    data = data.encode('utf-8')
    request = urllib.request.Request(url, data, {
        'content-type': 'application/json',
        'charset': 'utf-8',
        'Authorization': f'token {token}'
    })
    try:
        response = urllib.request.urlopen(request)
        resp = response.read().decode('utf-8')
    except Exception as e:
        print(f'get {team} projects failed')
        print('e.code  : ' + str(e.code))
        print('e.reason: ' + str(e.reason))
    return json.loads(resp)


def get_or_create_repository(team, proj_name, repo_name, token):
    resp = get_projects(team, token)
    project_id = 0
    for project in resp["Response"]["Data"]["ProjectList"]:
        if project["Name"] == proj_name:
            project_id = project["Id"]

    if project_id == 0:
        # can not find mirror project, try to create mirror project
        resp = create_project(team, proj_name, token)
        project_id = resp["Response"]["ProjectId"]
    repo_id = 0
    resp = get_project_repositories(team, project_id, token)
    for repository in resp["Response"]["DepotData"]["Depots"]:
        if repository["Name"] == repo_name:
            repo_id = repository["Id"]
    if repo_id == 0:
        # can not find mirror repository, try to create mirror repository
        resp = create_repository(team, project_id, repo_name, token)
        repo_id = resp["Response"]["DepotId"]
    return project_id, repo_id
