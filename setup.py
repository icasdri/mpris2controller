# Copyright 2014 icasdri
#
# This file is part of mpris2controller.
#
# mpris2controller is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mpris2controller is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
__author__ = "icasdri"
from distutils.core import setup
from mpris2controller.controller import VERSION, DESCRIPTION

setup(
    name='mpris2controller',
    version=str(VERSION),
    license='GPL3',
    author='icasdri',
    author_email='icasdri@gmail.com',
    description=DESCRIPTION,
    url='https://github.com/icasdri/mpris2controller',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Media',
        'License :: OSI Approved :: GPL License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
    packages=['mpris2controller'],
    scripts=['distributing/mpris2controller'],
    data_files=[('/etc/xdg/autostart', ['distributing/mpris2controller.desktop'])]
)
