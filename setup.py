# -*- coding: utf-8 -*-
import re
import sys
import os
import subprocess

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
    from distutils.util import convert_path

    def _find_packages(where='.', exclude=()):
        """Return a list all Python packages found within directory 'where'

        'where' should be supplied as a "cross-platform" (i.e. URL-style) path; it
        will be converted to the appropriate local path syntax.  'exclude' is a
        sequence of package names to exclude; '*' can be used as a wildcard in the
        names, such that 'foo.*' will exclude all subpackages of 'foo' (but not
        'foo' itself).
        """
        out = []
        stack = [(convert_path(where), '')]
        while stack:
            where, prefix = stack.pop(0)
            for name in os.listdir(where):
                fn = os.path.join(where, name)
                if ('.' not in name and os.path.isdir(fn) and
                        os.path.isfile(os.path.join(fn, '__init__.py'))):
                    out.append(prefix+name)
                    stack.append((fn, prefix + name + '.'))
        for pat in list(exclude)+['ez_setup', 'distribute_setup']:
            from fnmatch import fnmatchcase
            out = [item for item in out if not fnmatchcase(item, pat)]
        return out

    find_packages = _find_packages


def find_version(fname):
    '''Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    '''
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version("webtest_plus/__init__.py")

PUBLISH_CMD = "python setup.py register sdist bdist_wheel upload"
TEST_PUBLISH_CMD = 'python setup.py register -r test sdist bdist_wheel upload -r test'
TEST_CMD = 'nosetests'

if 'publish' in sys.argv:
    try:
        __import__('wheel')
    except ImportError:
        print("wheel required. Run `pip install wheel`.")
        sys.exit(1)
    status = subprocess.call(PUBLISH_CMD, shell=True)
    sys.exit(status)

if 'publish_test' in sys.argv:
    try:
        __import__('wheel')
    except ImportError:
        print("wheel required. Run `pip install wheel`.")
        sys.exit(1)
    status = subprocess.call(TEST_PUBLISH_CMD, shell=True)
    sys.exit()

if 'run_tests' in sys.argv:
    try:
        __import__('nose')
    except ImportError:
        print('nose required. Run `pip install nose`.')
        sys.exit(1)

    status = subprocess.call(TEST_CMD, shell=True)
    sys.exit(status)


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='webtest-plus',
    version=__version__,
    description='An extension of WebTest with useful extras, including requests-style authentication.',
    long_description=(read("README.rst") + '\n\n' +
                        read("HISTORY.rst")),
    author='Steven Loria',
    author_email='sloria1@gmail.com',
    url='https://github.com/sloria/webtest-plus',
    packages=find_packages(exclude=("test*", )),
    package_dir={'webtest_plus': 'webtest_plus'},
    install_requires=[
        'webtest>=2.0.9'
    ],
    license=read("LICENSE"),
    zip_safe=False,
    keywords="wsgi test unit tests web",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
    tests_require=['nose', 'flask'],
)
