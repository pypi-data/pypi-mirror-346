from glob import glob
from setuptools import setup
from itertools import chain
import io
import os
from os.path import join as pjoin

#from stupbase
def get_version(file, name='__version__'):
    """Get the version of the package from the given file by
    executing it and extracting the given `name`.
    """
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]

pkgname = 'nanohubthemes'
version = get_version(pjoin(pkgname, '_version.py'))
url = 'https://github.com/denphi/nanohubthemes'


# get readme content after screenshots for pypi site
README = os.path.join(os.path.dirname(__file__), 'README.md')

longdescr = ''
with open(README) as read_me:
    for line in read_me:
        if "Monospace Fonts" in line:
            break
        longdescr += line

# add layout, .less styles, and compiled .css files to pkg data
layout = os.path.join(pkgname, 'layout')
styles = os.path.join(pkgname, 'styles')
stylesCompiled = os.path.join(styles, 'compiled')

datafiles = {pkgname: []}
for subdir in ['defaults', 'layout', 'styles', 'styles/compiled']:
    filetypes = '*.*ss'
    if subdir=='defaults':
        filetypes = '*.*s'
    files = glob(os.path.join(pkgname, subdir, filetypes))
    filesLocalPath = [os.sep.join(f.split(os.sep)[1:]) for f in files]
    datafiles[pkgname].extend(filesLocalPath)

# recursively point to all included font directories
fontfams = ['monospace', 'sans-serif', 'serif']
fsubdirs = [os.path.join(pkgname, 'fonts', subdir) for subdir in fontfams]
fontsdata = chain.from_iterable([[os.sep.join(f.split(os.sep)[1:])
                                  for f in glob(os.path.join(fsub, '*', '*'))]
                                 for fsub in fsubdirs])
datafiles[pkgname].extend(list(fontsdata))

install_requires = [
    'lesscpy>=0.11.2',
    'jupyter-contrib-nbextensions>=0.5.1',
    'autopep8',
    'yapf'
]

setup(
    name='nanohubthemes',
    version=version,
    packages=['nanohubthemes'],
    include_package_data=True,
    package_data=datafiles,
    description='Select and install a Jupyter notebook theme',
    long_description=open(README).read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url=url,
    author='denphi,dunovank',
    author_email='denphi@denphi.com, dunovank@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=install_requires,
    keywords=['jupyter', 'python', 'ipython', 'notebook', 'theme', 'less', 'css'],
    entry_points={
        'console_scripts': [
            'start_nanohubthemes = nanohubthemes:main'
        ],
    })
