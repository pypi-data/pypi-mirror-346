from setuptools import setup, find_packages

setup(
    name='my_package_kirill_panichkin',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Паничкин Кирилл',
    author_email='unbearable.panic@gmail.com',
    description='Описание пакета',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/terriblepanic/my_package.git',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
