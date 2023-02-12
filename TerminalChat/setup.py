from setuptools import setup, find_packages

setup(
    name='tchat',
    version='0.1.0',
    py_modules=['tchat'],
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'tchat = tchat:cli',
        ],
    },
)
