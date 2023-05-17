from setuptools import setup

setup(
    name="uploader",
    version='0.1',
    py_modules=['uploader'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        uploadvid=uploader:uploadvid
    ''',
)