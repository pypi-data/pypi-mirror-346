from setuptools import find_packages, setup

setup(
    name='Auto_feat_eng',
    packages=find_packages(include=['mypythonlib']),
    version='0.1.4',
    description='This library is used to do feature engineering work automatic',
    author='Khemraj Mangal',
    install_requires=["pandas", "numpy", "scikit-learn"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)