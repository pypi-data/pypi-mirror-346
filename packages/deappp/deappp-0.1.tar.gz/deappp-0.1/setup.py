from setuptools import setup, find_packages

setup(
    name='deappp',  # Your package name
    version='0.1',
    author='Aniket Chavan',
    author_email='caniket975@gmail.com',
    description='Educational package for simple BI code examples.',
    long_description='A package containing examples for Linear Regression and CNN classification.',  # Optional
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_package_name',  # Optional, fix when ready
    packages=find_packages(),  # Will find DL_p automatically
    install_requires=[
        "numpy",
        "pandas",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
