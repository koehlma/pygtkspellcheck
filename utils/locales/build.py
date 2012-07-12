# -*- coding:utf-8 -*-

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

import os.path
import sqlite3
from xml.etree import ElementTree as etree

def build():
    databases = os.path.join(os.path.dirname(__file__), 'databases')
    locales = os.path.join(os.path.dirname(__file__), 'locales')
    languages = etree.parse(os.path.join(databases, 'iso639.xml')).findall('iso_639_entry')
    countries = etree.parse(os.path.join(databases, 'iso3166.xml')).findall('iso_3166_entry')
    database = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'locales.db'))
    database.execute('CREATE TABLE countries (name, official_name, alpha_2, alpha_3, numeric)')
    database.execute('CREATE TABLE languages (name, iso_639_2B, iso_639_2T, iso_639_1)')
    for country in countries:
        database.execute('INSERT INTO countries VALUES (?, ?, ?, ?, ?)', (country.get('name'), country.get('official_name'),
                                                                          country.get('alpha_2_code'), country.get('alpha_3_code'),
                                                                          country.get('numeric_code')))

    for language in languages:
        database.execute('INSERT INTO languages VALUES (?, ?, ?, ?)', (language.get('name'), language.get('iso_639_2B_code'),
                                                                       language.get('iso_639_2T_code'), language.get('iso_639_1_code')))
 
    database.commit()
    database.close()

if __name__ == '__main__':
    build()