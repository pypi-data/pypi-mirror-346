from setuptools import setup, find_packages

setup(
    name='badgerdoc-storage',
    version='0.0.1',
    description='Internal storage adapter used by the BadgerDoc platform (EPAM)',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='EPAM AI Ops',
    author_email='aiops@epam.com',
    url='https://github.com/epam/badgerdoc-storage',
    license='Apache 2.0',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
)
