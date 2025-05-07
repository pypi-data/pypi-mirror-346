from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='PMteam',
    version='0.2',
    packages=find_packages(),
    author='NASR',
    author_email='nasr2python@gmail.com',
    description='Powerful encryption library for securing Python data by Team PM',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://t.me/NexiaHelpers',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Security :: Cryptography'
    ],
    python_requires='>=3.6',
)