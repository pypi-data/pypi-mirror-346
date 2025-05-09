from setuptools import setup, find_packages

setup(
    name='Raigasada',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Кошелев Е. В.',
    author_email='raygasada@gmail.com',
    description='Пакет с функцией hello world',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ваш-профиль/hello_world_package',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)