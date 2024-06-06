from setuptools import setup, find_packages

setup(
    name='Mast',
    version='0.9',
    packages=find_packages(),
    install_requires=[
        'mast',
        'PySide6'
    ],
    entry_points={
        'console_scripts': [
            # 如果有需要的话，配置命令行脚本入口
        ],
    },
)
