from setuptools import setup

setup(name='bigpython',
    version='0.1',
    description='Make things easier for data analysis and automation',
    author='Lee Seongjoo',
    author_email='seongjoo@codebasic.co',
    py_modules=['mail'],
    packages=['bigpython', 'bigpython.webscrap', 'bigpython.office'],
    package_dir={'bigpython':'bigpython'},
    install_requires=[
        'pandas',
        'beautifulsoup4',
        'selenium',
        'requests',
        'imapclient',
        'python-docx'
    ])
