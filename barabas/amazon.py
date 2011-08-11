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

import random
import string
import urllib

import boto.s3.connection

def get_public_ipv4():
    """Returns the Public IPv4 of the running Amazon EC2 server"""
    f = urllib.open('http://169.254.169.254/latest/meta-data/public-ipv4')
    public_ip = f.read()
    f.close()
    return public_ip


class S3StorageManager():
    """ A Storage Manager that saves data in Amazon S3 service."""
    
    def __init__(self, key, secret, bucket_name, location):
        """Constructs the S3 Storage Manager"""
        self.__connection = boto.s3.connection.S3Connection(key, secret)
        self.__bucket = self.__connection.get_bucket(bucket_name, location)
    
    def save(self, input_file):
        """Saves a file into the storage manager. Returns the new keyname"""

        key = None
        while key == None:
            random_string = self.__random_key_name()
            key = self.__bucket.new_key(random_string)
            key.set_contents_from_string(random_string, replace=False)
            
            if key.get_contents_as_string() != random_string:
                key = None

        # TODO: make this  set_contents_from_stream with newer versions of boto
        key.set_contents_from_file(input_file, replace=True)
        return unicode(key.name)
    
    def open(self, file_pointer):
        """Opens an existing keyname"""
        return self.__bucket.get_key(file_pointer)
    
    def __random_key_name(self):
        def generate_random_string():
            """Empty docstring"""
            return ''.join(random.choice(string.letters + string.digits)
                           for i in xrange(128))

        keyname = generate_random_string()
        while self.__bucket.get_key(keyname) != None:
            keyname = generate_random_string()
        return keyname
        
