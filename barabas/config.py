#! /usr/bin/env python
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

import ConfigParser
import os.path
import sys

def load_config_file()
    config = ConfigParser.ConfigParser()
    
    config_path = None
    config_paths = ['barabas-server.cfg', '/etc/barabas-server.cfg']
    for config_path in config_paths:
        if os.path.isfile(config_path):
            break
        else:
            config_path = None
    if config_path == None:
        return None
    config.read(config_path)
    return config

def load_database(config):
    """Load the database with info from the configuration file"""
    module = config.get('Database', 'module')
    __import__(module)
    constructor_name = config.get('Database', 'constructor')
    constructor = sys.modules[module].__dict__[constructor_name]
    
    args = {}
    for (name, value) in config.items('Database'):
        if name not in ['module', 'constructor']:
            args[name] = value
    
    return constructor(**args)

def load_storage_manager(config):
    """Load the storage manager with info from the configuration file"""
    module = config.get('Storage', 'module')
    __import__(module)
    constructor_name = config.get('Storage', 'constructor')
    constructor = sys.modules[module].__dict__[constructor_name]
    
    args = {}
    for (name, value) in config.items('Storage'):
        if name not in ['module', 'constructor']:
            args[name] = value
    
    return constructor(**args)

def get_public_ip(config):
    """Returns the Public IP as defined in the config file.
    
       Can return None if te public IP is the same as the IP where
       clients connect to. Cases where the server is behind NAT are able
       to return None. Cases where the server is behind a Load Balancer
       that is not sticky (Thank you Amazon) have to return something.
    """
    
    if config.has_option('Server', 'public_ip'):
        return config.get('Server', 'public_ip')
    elif config.has_option('Server', 'public_ip_module'):
        module = config.get('Server', 'public_ip_module')
        __import__(module)
        function_name = config.get('Server', 'public_ip_function')
        return sys.modules[module].__dict__[function_name]()
    else:
        return None
