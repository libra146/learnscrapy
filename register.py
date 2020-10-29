"""
注册多个账号备用，将多个请求分散到多个账号中。
"""
import requests


def register():
    url = 'https://antispider7.scrape.center/api/register'
    # 简单设置账号密码邮箱为同一个值
    for a in range(10):
        d = f'12345678{a}'
        data = {
            'username': d,
            'password': d,
        }
        r = requests.post(url=url, json=data)
        print(f'12345678{a}-{r.status_code}')


if __name__ == '__main__':
    register()
