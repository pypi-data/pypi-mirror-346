from setuptools import setup, find_packages

setup(
    name='gender_predictor_rp',
    version='0.3.1',
    description='Predict gender from Indian names using a trained ML model',
    author='Rahul Patel',
    author_email='your@email.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'scikit-learn',
        'joblib'
    ],
)
