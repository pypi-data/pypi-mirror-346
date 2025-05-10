from setuptools import setup, find_packages

setup(
    name='when-keyword',
    version='0.1.0',
    packages=find_packages(),
    description='A custom Python "when" class simulating a keyword with do and during',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/when-keyword',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)