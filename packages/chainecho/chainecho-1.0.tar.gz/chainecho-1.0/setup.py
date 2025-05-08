from setuptools import setup, find_packages

setup(
    name='chainecho',
    version='1.0',
    description="Python API Client for https://chainecho.me",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Douglas Vincente',
    author_email='d.vincente@aol.com',
    url='https://github.com/dvincente/pychainecho-api',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'requests>=2.32.1',
        'jsondump>=0.1'
        # Add dependencies here.
    ],
    extra_requires={
        'dev': [
            'twine'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='chainecho news business information',
    python_requires='>=3.6',
)