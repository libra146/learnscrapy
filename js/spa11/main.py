import subprocess

import requests
import urllib3

urllib3.disable_warnings()


def get_js():
    # 可能是ssl 证书失效了，忽略异常
    r = requests.get('https://spa11.scrape.center/js/main.js', verify=False).text
    return r


def run_js(code):
    js_code = f"""
    String.prototype.print = function() {{
    console.log(this);
    return this;
    }};
    {code.strip()[:-6]}.toString().print();
    """
    process = subprocess.Popen(['node', '-e', js_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stderr.decode('utf-8'))
    print(stdout.decode('utf-8'))
    return stdout.decode('utf-8')


if __name__ == '__main__':
    js = get_js()
    run_js(js)
