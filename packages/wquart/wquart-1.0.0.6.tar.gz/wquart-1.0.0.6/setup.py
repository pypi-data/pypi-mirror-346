#!/usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup#,find_packages
setup(name = 'wquart',      # 包名
      description = 'wuqi chip703X uart message resolve',
      long_description = 'wuqi-chip703X uart message resolve', 
      author = 'wuqi-wanjian',
      author_email = 'wan.jian@wuqi-tech.com',
      url = 'http://www.wuqi-tech.com/',
      license = '',
      install_requires = ["pyserial"],
      classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Utilities'
      ],
      package_dir = {'wquart':'wquart'},
      packages= ['wquart'],
)

## 上传到pypi
#twine upload dist/* 