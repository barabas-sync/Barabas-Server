#!/usr/bin/env python

from distutils.core import setup

setup(name='Barabas',
      version='0.1',
      description='Barabas Server Program',
      author='Nathan Samson',
      author_email='nathan.samson@student.ua.ac.be',
      url='http://github.com/barabas-sync/Barabas-Server/',
      packages=['barabas', 'barabas.database', 'barabas.identity',
                'barabas.network', 'barabas.network.channels',
                'barabas.network.terminals', 'barabas.objects'],
      scripts=['barabasd'],
      data_files=[('/etc', ['barabas-server.cfg.example']),
                  ('/etc/init.d/', ['init/barabasd'])
                 ]
     )
