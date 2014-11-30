from setuptools import setup, find_packages

setup(
    name='mpris2controller',
    version='0.3',
    license='GPL3',
    author='icasdri',
    author_email='icasdri@gmail.com',
    description='A small user daemon for GNU/Linux that intelligently controls MPRIS2-compatible media players',
    url='https://github.com/icasdri/mpris2controller',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Media',
        'License :: OSI Approved :: GPL License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['mpris2controller = mpris2controller:main']
    }
)
