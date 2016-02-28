from setuptools import setup

setup(name='flaskone',
      version='1.0',
      description='flask on OpenShift App',
      author='fhamami',
      author_email='fuadgoinet@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=
      [
      'flask'
      'flask-login'
      'flask-openid'
      'flask-mail'
      'flask-sqlalchemy'
      'sqlalchemy-migrate'
      'flask-whooshalchemy'
      'flask-wtf'
      'flask-babel'
      'guess_language'
      'flipflop'
      'coverage'
      ],
     )
