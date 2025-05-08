from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pdmparse',
    version='1.0.2',
    author='fhp',
    author_email='chinafengheping@outlook.com',
    description='解析PowerDesigner的数据库设计pdm文件，用于模板代码生成',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/9kl/pdmparse',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'Jinja2==3.1.6'
    ]
)