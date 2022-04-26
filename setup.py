import setuptools

setuptools.setup(
    name='srvlookup',
    version='3.0.0',
    description='Service lookup using DNS SRV records',
    long_description=open('README.rst').read(),
    author='Gavin M. Roy',
    author_email='gavinr@aweber.com',
    url='https://github.com/gmr/srvlookup',
    py_modules=['srvlookup'],
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
    install_requires=['dnspython>=2.0.0'],
    tests_require=['nose', 'mock', 'coverage'],
    test_suite='nose.collector',
    license='BSD',
    classifiers=[

    ],
    zip_safe=True)
