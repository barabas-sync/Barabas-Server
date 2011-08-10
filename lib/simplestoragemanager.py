# vim: set expandtab set ts=4 tw=4
#
# This file is part of Barabas Server.
#
# Copyright (C) 2011 Nathan Samson
# Barabas Server is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Barabas Server is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Barabas Server.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import random
import string

class SimpleStorageManager:
    def __init__(self, base_path):
        self.__base_path = base_path
    
    def save(self, input_file):
        fullpath, file_pointer = self.__find_filename()

        f = open(fullpath, "wb")
        input_read = input_file.read(4096)
        while input_read:
            f.write(input_read)
            input_read = input_file.read(4096)
        f.close()
        return unicode(file_pointer)
    
    def open(self, file_pointer):
        return open(os.path.join(self.__base_path, file_pointer))
        
    def __find_filename(self):
        def generate_random_string():
            return ''.join(random.choice(string.letters + string.digits) for i in xrange(10))

        filename = generate_random_string()
        fullpath = os.path.join(self.__base_path, filename)
        while (os.path.isfile(fullpath) or os.path.isdir(fullpath)):
            filename = generate_random_string()
            fullpath = os.path.join(self.__base_path, filename)
        return (fullpath, filename)
