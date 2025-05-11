from distutils.core import setup
"""更新 test_python 模块"""

setup(
    name="setup_baizhanMath02",   #模块对外的名字
    version="1.1",                #模块的版本号
    description="测试第一个对外发布模块",   #模块描述
    author="zhoutongtong",        #本模块的作者
    author_email="2311522765@qq.com",  #本模块的邮箱
    py_modules=["baizhanNath2.demo_01","baizhanNath2.demo_02"]   #要发布的模块
)
