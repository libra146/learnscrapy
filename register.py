"""
注册多个账号备用，将多个请求分散到多个账号中。
"""
import requests


def register():
    url = 'https://antispider6.scrape.center/register'
    # 简单设置账号密码邮箱为同一个值
    for a in range(10):
        d = f'12345-{a}@qq.com'
        data = {
            'username': d,
            'email': d,
            'password1': d,
            'password2': d
        }
        r = requests.post(url=url, data=data)
        print(f'12345-{a}@qq.com-{r.status_code}')


if __name__ == '__main__':
    register()
