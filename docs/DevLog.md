# 开发笔记

1. 上传至pypi的命令: `python setup.py sdist bdist_wheel upload`, 其中:
    - sdist 打包成 *.tar.gz
    - bdist_wheel 打包成 wheel, *-py3-none-any.whl
    - upload 用于上传至 pypi

2. 让打包工具录入非python package文件:
    - include_package_data:  [Doc](https://setuptools.readthedocs.io/en/latest/setuptools.html#new-and-changed-setup-keywords)
        If set to True, this tells setuptools to automatically include any data files it finds inside your package directories that are specified by your MANIFEST.in file. For more information, see the section below on Including Data Files.
        ```
        setup(
            ...,
            include_package_data=True
        )
        ```
    - 如果不加这个命令, 仅写`MANIFEST.in`, 会导致实际安装时json,js等文件不进入package文件夹.

3. 用 twine 先上传到`test.pypi.org` [Doc](https://pypi.org/project/twine/)
```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

4. 如何生成进入bin目录的scripts
    - bin/...py方法 ×
    - entry_points ✔ [Doc](https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins)


5. click的基础用法
    - Boolean Flags [Doc](https://click.palletsprojects.com/en/7.x/options/#boolean-flags)
    - Prameters [Doc](https://click.palletsprojects.com/en/7.x/parameters/#parameters)
    

6. TODO:
    - Testsuits
    - FlaskReact功能设计
    