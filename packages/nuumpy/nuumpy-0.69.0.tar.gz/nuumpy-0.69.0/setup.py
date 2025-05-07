from setuptools import setup, find_packages

setup(
    name='nuumpy',                     # Your package name
    version='0.69.0',                   # Initial version
    description='INSANE PACKAGE FOR SANE PEOPLE',  # Short description
    author='Your Name',
    author_email='your@email.com',
    packages=find_packages(),         # Automatically find packages
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
