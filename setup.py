# -*- coding: utf-8 -*-
# gpodder.net API Client
# Copyright (C) 2009-2010 Thomas Perl
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup

import glob

setup(name='mygpoclient',
      version='1.3',
      description='Library for accessing gpodder.net web services.',
      author='Thomas Perl',
      author_email='thp@gpodder.org',
      url='http://thpinfo.com/2010/mygpoclient/',
      packages=['mygpoclient'],
      scripts=glob.glob('scripts/*'))

