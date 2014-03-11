import setuptools
import sys

tests_require = ['nose', 'mock']
if sys.version_info < (2, 7, 0):
    tests_require.append('unittest2')

dnspython = 'dnspython' if sys.version_info < (3, 0, 0) else 'dnspython3'

setuptools.setup(name='srvlookup',
                 version='0.1.0',
                 description='Service lookup using DNS SRV records',
                 long_description=open('README.rst').read(),
                 author='Gavin M. Roy',
                 author_email='gavinr@aweber.com',
                 url='http://github.com/AWeber/srvlookup',
                 py_modules=['srvlookup'],
                 package_data={'': ['LICENSE', 'README.rst']},
                 include_package_data=True,
                 install_requires=[dnspython],
                 tests_require=tests_require,
                 test_suite='nose.collector',
                 license=open('LICENSE').read(),
                 classifiers=['Development Status :: 4 - Beta',
                              'Intended Audience :: Developers',
                              'License :: OSI Approved :: BSD License',
                              'Operating System :: OS Independent',
                              'Programming Language :: Python :: 2',
                              'Programming Language :: Python :: 2.6',
                              'Programming Language :: Python :: 2.7',
                              'Programming Language :: Python :: 3',
                              'Programming Language :: Python :: 3.2',
                              'Programming Language :: Python :: 3.3',
                              'Programming Language :: Python :: Implementation :: CPython',
                              'Programming Language :: Python :: Implementation :: PyPy',
                              'Topic :: Communications',
                              'Topic :: Internet',
                              'Topic :: Software Development :: Libraries'],
                 zip_safe=True)