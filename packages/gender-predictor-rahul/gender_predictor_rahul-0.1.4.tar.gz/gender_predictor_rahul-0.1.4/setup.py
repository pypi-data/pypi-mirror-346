from setuptools import setup, find_packages

setup(
    name='gender_predictor_rahul',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'gender_predictor_module': [
            'gender_predictor_module/tokenizer.pkl',
            'gender_predictor_module/gender_predictor.pkl',
        ],
    },
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
    python_requires='>=3.6',  # Optional: specify the required Python version
)
