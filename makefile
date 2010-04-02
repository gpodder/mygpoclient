
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

test:
	nosetests --cover-erase --with-coverage --with-doctest \
	    --cover-package=mygpoclient

docs:
	epydoc -n 'gpodder.net API Client Library' -o docs/ mygpoclient -v --exclude='.*_test'

upload-docs: clean docs
	rsync -rpav --delete-after docs/ dev.gpodder.org:/var/www/mygpoclient-apidocs/

clean:
	find -name '*.pyc' -exec rm '{}' \;
	rm -f .coverage
	rm -rf docs/ build/

distclean: clean
	rm -f MANIFEST
	rm -rf dist/

.PHONY: test docs clean distclean

