from setuptools import setup, find_packages

def read(fpath):
    with open(fpath, 'r') as f:
        return f.read()

def requirements(fpath):
    return list(filter(bool, read(fpath).split('\n')))

def version(fpath):
    return read(fpath).strip()

setup(
    name = 'dockerman',
    version = version('version.txt'),
    author = 'Matt Bodenhamer',
    author_email = 'mbodenhamer@mbodenhamer.com',
    description = 'Manage docker images and docker containers used for local/desktop applications',
    long_description = read('README.rst'),
    url = 'https://github.com/mbodenhamer/dockerman',
    packages = find_packages(),
    install_requires = requirements('requirements.in'),
    entry_points = {
        'console_scripts': [
            'dockerman = dockerman.main:main',
        ]
    },
    license = 'MIT',
    keywords = ['docker', 'application'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ]
)