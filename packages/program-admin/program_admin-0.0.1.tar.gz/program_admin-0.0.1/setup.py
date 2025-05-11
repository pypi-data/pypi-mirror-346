from setuptools import setup, find_packages

setup(
    name='program-admin',
    version='0.0.1',
    description='Program management tools for deployment and CI pipelines',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='Internal Engineering',
    author_email='devops@internal.corp',
    url='https://github.com/internal-tools/program-admin',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
)
