from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf-8") as fh:
      long_description = fh.read()

setup(name='uptime_kuma_api_v2_0_1',
      version='2.0.0-beta.2',
      description='this sdk upload with 2025-05-09, uptime_kuma_api_v2, support uptime kuma 2.0.0-beta.2, 支持 Uptime kuma 2.0.0-beta.2 版本的sdk',
      author='zhifubao',
      author_email='zhifubao@alipay.com',
      packages=find_packages(), # 系统自动从当前目录开始找包
      long_description=long_description,
      long_description_content_type="text/markdown",
      # 如果有的包不用打包，则只能指定需要打包的文件
      #packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀
      license='MIT')


