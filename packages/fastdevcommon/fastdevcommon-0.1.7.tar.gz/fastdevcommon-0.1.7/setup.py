from setuptools import setup, find_packages
MAJOR =0
MINOR =1
PATCH =7
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"

def get_install_requires():
    reqs = [
    'aiohappyeyeballs==2.6.1',
    'aiohttp==3.11.16',
    'aioredis==2.0.1',
    'aiosignal==1.3.2',
    'annotated-types==0.7.0',
    'async-timeout==5.0.1',
    'attrs==25.3.0',
    'backports.tarfile==1.2.0',
    'certifi==2025.1.31',
    'charset-normalizer==3.4.1',
    'colorama==0.4.6',
    'docutils==0.21.2',
    'frozenlist==1.5.0',
    'id==1.5.0',
    'idna==3.10',
    'importlib_metadata==8.6.1',
    'jaraco.classes==3.4.0',
    'jaraco.context==6.0.1',
    'jaraco.functools==4.1.0',
    'keyring==25.6.0',
    'loguru==0.7.3',
    'markdown-it-py==3.0.0',
    'mdurl==0.1.2',
    'more-itertools==10.6.0',
    'multidict==6.3.1',
    'nh3==0.2.21',
    'packaging==24.2',
    'propcache==0.3.1',
    'pydantic==2.11.1',
    'pydantic_core==2.33.0',
    'Pygments==2.19.1',
    'pywin32-ctypes==0.2.3',
    'readme_renderer==44.0',
    'redis==5.2.1',
    'requests==2.32.3',
    'requests-toolbelt==1.0.0',
    'rfc3986==2.0.0',
    'rich==14.0.0',
    'typing-inspection==0.4.0',
    'typing_extensions==4.13.0',
    'urllib3==2.3.0',
    'win32_setctime==1.2.0',
    'yarl==1.18.3',
    'zipp==3.21.0',
    'nacos-sdk-python==2.0.3',
    'uvicorn',
    'fastapi'
]
    return reqs


setup(
    name='fastdevcommon',
    version=VERSION,
    packages=find_packages(),
    description='A common development component',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hwzlikewyh/FastDevCommon.git',
    author='hwzlikewyh',
    author_email='hwzlikewyh@163.com',
    license='MIT',
    install_requires=get_install_requires(),
    package_data={'': ['*.csv', '*.txt', '.toml']},  # 这个很重要
    include_package_data=True  # 也选上
)
