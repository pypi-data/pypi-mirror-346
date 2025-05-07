# setup.py
from setuptools import setup, find_packages

setup(
    name='kali_driver',
    use_scm_version={
        "local_scheme": "no-local-version",
    },
    author='stupidfish001',
    author_email='shovel@hscsec.cn',
    description='A driver of kali for al-1s project.',
    # long_description=open('README.md', encoding='utf-8').read(),
    packages=find_packages(),
    install_requires=[
        'pwntools==4.14.0',
        'docker==7.1.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
