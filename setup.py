# -*- coding:utf-8 -*-
#
# Copyright (C) 2012, Maximilian Köhl <linuxmaxi@googlemail.com>
# Copyright (C) 2012, Carlos Jenkins <carlos@jenkins.co.cr>
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

import sys
from distutils.core import setup
from sphinx.setup_command import BuildDoc
sys.path.append('./src/')
import gtkspellcheck as m

cmdclass = {'build_sphinx': BuildDoc}
setup(name=m.__short_name__,
      version=m.__version__,
      description=m.__desc_long__,
      long_description=m.__desc_long__,
      author=m.__authors__,
      author_email=m.__emails__,
      url=m.__website__,
      license='GPLv3',
      package_dir={'': 'src'},
      packages=['gtkspellcheck', 'pylocales'],
      package_data={'pylocales' : ['locales.db']},
      cmdclass=cmdclass)