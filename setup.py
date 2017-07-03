import setuptools

setuptools.setup(
    name="dotapairs",
    version="0.1.0",
    url="https://github.com/kokosoida/dotapairs",

    author="Georgy Gritsenko",
    author_email="kokosoida@gmail.com",

    description="An opinionated, minimal cookiecutter template for Python packages",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'dota2api==1.3.3',
        'tqdm==4.14.0',
        'pymongo==3.4.0',
        'logzero==1.1.1',
        'tenacity==4.2.0',
        'click==6.7',
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    entry_points='''
        [console_scripts]
        pairs=dotapairs.cli:get_matches
    ''',
)
