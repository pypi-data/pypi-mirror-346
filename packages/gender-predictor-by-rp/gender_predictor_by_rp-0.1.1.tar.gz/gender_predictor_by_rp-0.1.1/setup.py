from setuptools import setup, find_packages

setup(
    name='gender_predictor_by_rp',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={'gender_predictor': ['assets/*']},
    install_requires=[
        'keras',
        'tensorflow',
    ],
    author='Rahul Patel',
    description='Gender prediction from names using a trained ML model',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
