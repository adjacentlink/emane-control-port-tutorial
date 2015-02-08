#!/usr/bin/env python
# Copyright (c) 2015 - Adjacent Link LLC, Bridgewater, New Jersey
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# * Neither the name of Adjacent Link LLC nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import os
import glob
from emanesh import Manifest,ManifestException
from pprint import pprint

# look to see if the EMANEMANIFESTPATH environment variable exists, if
# not use the default installation location
manifestpath = os.getenv('EMANEMANIFESTPATH',
                         '/usr/share/emane/manifest')

info = {}

# process all the XML files in the manifest path locations
for directory in manifestpath.split(':'):
    for manifestXML in glob.glob("%s/*.xml" % directory):
        try:
            # create a Manifest instance for each file
            manifest = Manifest(manifestXML)
            info[manifest.getName()] = manifest
        except ManifestException:
            pass
            
if not info:
    print "warning: no plugin manifest XML loaded. Check EMANEMANIFESTPATH."
    exit(1)

# show the modifiable configuration, clearable statistics and
# tables and txpower configuration info for the emane phy
if 'emanephy' in info:
    emanephy = info['emanephy']

    print '-' * 40,'\n','running-state modificable configuration\n','-' * 40
    pprint(emanephy.getModifiableConfiguration())
    print

    print '-' * 40,'\n','clearable statistics\n','-' * 40
    pprint(sorted(emanephy.getClearableStatistics()))
    print
    
    print '-' * 40,'\n','clearable tables\n','-' * 40
    pprint(sorted(emanephy.getClearableTables()))
    print

    print '-' * 40,'\n','txpower configuration info\n','-' * 40
    pprint(emanephy.getConfigurationInfo('txpower'))
