from distutils.core import setup
requires = ['dbus-python', 'pygobject']

setup(
    name='mpris2controller',
    version='0.3',
    packages=[''],
    url='https://github.com/icasdri/mpris2controller',
    license='GPL3',
    author='icasdri',
    author_email='icasdri@gmail.com',
    description='A small user daemon for GNU/Linux that intelligently controls MPRIS2-compatible media players'
)
