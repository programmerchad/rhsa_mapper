from setuptools import setup, find_packages

__version__ = None
# We load version this way otherwise we get an exception about requests not being installed if we try to do
# from rhsa_mapper.__version__ import __version__
with open('rhsa_mapper/__version__.py', 'r') as fh:
    exec(fh.read())

# Load app and test requirements
requirements = []
test_requirements = []
with open('requirements.txt', 'r') as rh:
    for requirement in rh.read().splitlines():
        requirement = requirement.strip()
        if not requirement or requirement.startswith('#'):
            continue
        else:
            requirements.append(requirement)

setup(
    name='rhsa_mapper',
    version=__version__,
    packages=find_packages(),
    author='Chad Dombrowski',
    author_email='cdombrowski85@gmail.com',
    description='CLI interface to retrieve CPE/repository information for Red Hat Security Advisories (RHSA)',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'rhsam=rhsa_mapper:rhsam'
        ]
    }
)
