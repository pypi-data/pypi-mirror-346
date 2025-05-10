from setuptools import setup, find_packages

setup(
    name='meroty_utils',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Vasilya',
    author_email='lara_nabieva@bk.ru',
    description='Краткое описание пакета',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/VasilyaNab/my_package',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)