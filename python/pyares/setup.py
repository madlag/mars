from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pyares',
      version='0.1',
      description='pyares is a python package for ...',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.0',
        'Topic :: Text Processing',
      ],
      keywords='',
      url='',
      author='',
      author_email='',
      license='MIT',
      packages=['pyares'],
      install_requires=['click'],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['pyares_run=pyares.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)