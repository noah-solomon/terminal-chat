from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()


setup(
    name='tchat',
    version='0.1.0',
    author='Noah Solomon',
    author_email='hello@noahsolo.com',
    license='MIT License',
    description='Terminal chat application',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/noah-solomon/terminal-chat',
    py_modules=['tchat', 'app'],
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
