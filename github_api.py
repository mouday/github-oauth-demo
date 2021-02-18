# -*- coding: utf-8 -*-

import requests


def get_github_auth_url(client_id, redirect_uri):
    """

    :param client_id: 告诉 GitHub 谁在请求
    :param redirect_uri: 跳转回来的网址
    :return:
    """
    authorize_uri = 'https://github.com/login/oauth/authorize'

    return f'{authorize_uri}?client_id={client_id}&redirect_uri={redirect_uri}'


def get_access_token(client_id, client_secret, code):
    """获取 access_token 此操作在后台完成"""
    url = 'https://github.com/login/oauth/access_token'

    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code
    }

    headers = {
        'accept': 'application/json'
    }

    res = requests.post(url=url, params=params, headers=headers)

    return res.json()


def user(access_token):
    """获取用户信息"""
    url = 'https://api.github.com/user'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    res = requests.get(url=url, headers=headers)

    return res.json()
