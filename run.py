# -*- coding: utf-8 -*-
from urllib.parse import urljoin

from flask import Flask, request, url_for

from github_api import get_github_auth_url, user, get_access_token
from mo_cache import FileCache
from environs import Env

# 注册应用获取的参数
env = Env()
env.read_env()

clientID = env.str('clientID')
clientSecret = env.str('clientSecret')

# 使用文件缓存 access_token
cache = FileCache()

ACCESS_TOKEN_KEY = 'access_token_key'

app = Flask(__name__)


def full_url_for(endpoint, **values):
    """获取完整路径"""
    return urljoin(request.host_url, url_for(endpoint, **values))


@app.route('/')
def hello_world():
    """首页暴露接口地址"""
    return {
        'auth_url': full_url_for('get_auth_url'),
        'get_user': full_url_for('get_user')
    }


@app.route('/auth_url')
def get_auth_url():
    """获取由后端拼接的Github第三方登录授权地址"""
    redirect_uri = full_url_for('oauth_redirect')

    auth_url = get_github_auth_url(client_id=clientID, redirect_uri=redirect_uri)

    return {'auth_url': auth_url}


@app.route('/oauth/redirect')
def oauth_redirect():
    """github验证回调地址，从请求参数中获取code"""
    code = request.args.get('code')

    # 拿到code后继续请求获取access_token
    res = get_access_token(client_id=clientID, client_secret=clientSecret, code=code)

    # 存储用户的access_token
    access_token = res.get('access_token')
    cache.set(ACCESS_TOKEN_KEY, access_token)
    return res


@app.route('/user')
def get_user():
    """通过access_token 获取用户信息"""
    # 从缓存中取出
    access_token = cache.get(ACCESS_TOKEN_KEY)

    res = user(access_token=access_token)

    return res


if __name__ == '__main__':
    print(app.url_map)
    # 服务地址需要和应用配置一致
    app.run(port=8080, debug=True)
