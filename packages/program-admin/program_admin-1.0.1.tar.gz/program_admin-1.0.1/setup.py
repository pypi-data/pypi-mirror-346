from setuptools import setup, find_packages

setup(
    name='program-admin',
    version='1.0.1',  # <-- bump version
    description='Program administration tools used by Python Agent Org CI/CD systems',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='Python Agent Org',
    author_email='ci-team@pyagent.org',
    url='https://github.com/pyagent/program-admin',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
)
