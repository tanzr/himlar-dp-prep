import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'funcsigs==1.0.0',
    'pyramid',
    'pyramid_mako',
#    'pyramid_debugtoolbar',
    'authomatic',
    'python-keystoneclient',
    'waitress',
    'grampg',
    'pika==0.11.2',
    ]

setup(name='himlar_dp_prep',
      version='0.0',
      description='himlar_dp_prep',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Jon K Hellan',
      author_email='jon.kare.hellan@uninett.no',
      url='https://github.com/norcams/himlar-dp-prep',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      dependency_links = [
          'http://github.com/jhellan/authomatic/tarball/master#egg=authomatic-0.1.0.uninett2'
      ],
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="",
      entry_points="""\
      [paste.app_factory]
      main = himlar_dp_prep:main
      """,
      )
