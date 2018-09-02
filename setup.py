from setuptools import setup

setup(
    name='ga-auth-microservice',
    version='1.0.0',
    packages=['servers', 'servers.oauth2', 'website'],
    url='https://github.com/geraldoandradee/auth-microservice',
    license='MIT',
    author='Geraldo Andrade',
    author_email='geraldo@geraldoandrade.com',
    description='This is a simple microservice.', install_requires=['werkzeug', 'flask']
)
