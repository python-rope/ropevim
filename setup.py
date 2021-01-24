extra_kwargs = {}
try:
    from setuptools import setup
    extra_kwargs['install_requires'] = ['rope >= 0.9.3', 'ropemode']
    extra_kwargs['zip_safe'] = False
except ImportError:
    from distutils.core import setup


classifiers = [
    'Development Status :: 6 - Mature',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Operating System :: OS Independent',
    'Environment :: X11 Applications',
    'Environment :: Win32 (MS Windows)',
    # Have not been tested on MacOS
    'Environment :: MacOS X',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Topic :: Software Development']


def get_long_description():
    lines = open('README.rst').read().splitlines(False)
    end = lines.index('Installation')
    return '\n' + '\n'.join(lines[:end]) + '\n'

setup(name='ropevim',
      version='0.8.1',
      description='A vim plugin for using rope python refactoring library',
      long_description=get_long_description(),
      py_modules=['ropevim', 'rope_omni'],
      maintainer='Matej Cepl',
      maintainer_email='mcepl@cepl.eu',
      author='Ali Gholami Rudi',
      author_email='aligrudi@users.sourceforge.net',
      url='http://rope.sf.net/ropevim.html',
      license='GNU GPL',
      classifiers=classifiers,
      requires=['ropemode'],
      **extra_kwargs
      )
