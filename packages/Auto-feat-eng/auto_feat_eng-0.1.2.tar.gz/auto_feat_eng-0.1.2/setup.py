from setuptools import find_packages, setup

setup(
    name='Auto_feat_eng',
    packages=find_packages(include=['mypythonlib']),
    version='0.1.2',
    description='My own library',
    author='Khemraj Mangal',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)