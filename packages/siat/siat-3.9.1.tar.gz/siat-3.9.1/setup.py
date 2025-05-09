# -*- coding: utf-8 -*-
"""
@author: WANG Dehong (Peter), IBS BFSU
"""

from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
#description does not support image, text only

setup(
    name="siat",
    version="3.9.1",
    #author="Prof. WANG Dehong, Business School, BFSU (北京外国语大学 国际商学院 王德宏)",
    author="Prof. WANG Dehong, International Business School, Beijing Foreign Studies University",
    author_email="wdehong2000@163.com",
    description="Securities Investment Analysis Tools (siat)",
    url = "https://pypi.org/project/siat/",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="Copyright (C) WANG Dehong, 2024. For educational purpose only!",
    packages = find_packages(),
    install_requires=[
        'pandas_datareader',
        'yfinance',
        #'pandas_alive',
        'tqdm',
        'plotly_express',
        #'akshare==1.3.95',#为与urllib3兼容
        #'akshare==1.4.57',#为其他兼容考虑
        #'akshare==1.10.3',
        'akshare',
        #'urllib3==1.25.11',#为其他兼容考虑
        'urllib3',
        #'urllib3',
        'mplfinance',
        'statsmodels',
        'yahoo_earnings_calendar',
        'pypinyin',
        'seaborn',
        'numpy',
        'scipy',
        #'pandas==1.5.3',#为其他兼容考虑
        'pandas',
        'scikit-learn',
        'baostock',
        'pyproject.toml',
        #'ta-lib',#ta-lib需要单独安装，并与Python版本配套
        'pathlib','ruamel-yaml','prettytable',
        'graphviz',#graphviz可能还需要额外安装程序
        'luddite',
        'pendulum','itables','py_trans','bottleneck',
        'translate','translators',
        #注意：translators 5.9.5要求lxml >=5.3.0，与yahooquery的要求矛盾
        'nbconvert',
        'ipywidgets==8.1.6',#解决Error loading widgets
        'playwright',#安装后还需要执行指令：playwright install
        #'yahooquery==2.2.14',#为其他兼容考虑
        'yahooquery==2.3.7',#解决数据获取失败crump限制
        #注意：临时措施，yahooquery 2.3.7要求lxml 4.9.4

    ],            
    #zip_sage=False,
    include_package_data=True, # 打包包含静态文件标识
) 