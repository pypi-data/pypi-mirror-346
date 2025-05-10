from setuptools import setup, find_packages

setup(
    name='alphavibe',
    version='1.0.0',
    description='Gen Alpha programming language: Vibe-based Python for Zoomers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Louis the Sigma',
    author_email='developerlouis7923@gmail.com',
    url='https://github.com/PotatoInfinity/genalpha-lang',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Education',
        'Topic :: Software Development :: Interpreters'
    ],
    python_requires='>=3.6',
)
