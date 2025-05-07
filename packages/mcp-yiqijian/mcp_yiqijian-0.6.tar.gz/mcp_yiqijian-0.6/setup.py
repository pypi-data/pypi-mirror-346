from setuptools import setup, find_packages

setup(
    name='mcp_yiqijian',
    version='0.6',
    packages=find_packages(),
    description='Yiqijian mcp plugin',
    long_description=open('README.md').read(),
    # python3，readme文件中文报错
    # long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    # url='',
    author='Yiqijian',
    author_email='',
    license='MIT',
    install_requires=[
        "fastmcp>=2.2.10",
        "httpx>=0.28.1",
    ],
    entry_points={
        "console_scripts": [
            "mcp_yiqijian=mcp_yiqijian.server:main",
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',  # 目标用户群体
        'License :: OSI Approved :: MIT License',  # 许可证类型
        'Programming Language :: Python :: 3',  # 支持的 Python 版本
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ]
)