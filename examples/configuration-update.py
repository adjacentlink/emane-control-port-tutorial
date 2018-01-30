#!/usr/bin/env python
# Copyright (c) 2015,2018 - Adjacent Link LLC, Bridgewater, New Jersey
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

import sys
import socket
import helpers

try:
    import emane.shell.remotecontrolportapi_pb2 as remotecontrolportapi_pb2
except:
    import emanesh.remotecontrolportapi_pb2 as remotecontrolportapi_pb2

# optionally specify the txpower value
if len(sys.argv) > 1:
    txPowerdBm = float(sys.argv[1])
else:
    txPowerdBm = 30

# create a socket
sock = socket.socket()

# connect to a running emulator instance
sock.connect(('node-1',47000))

# set the Request sequence number
sequence = 1

# retrieve the manifest from the running emulator instance
manifest = helpers.getManifest(sock,sequence)

phyLayerBuildId = None

# find the PHY component build id for the lowest NEM instance
for buildId,componentType,_ in  manifest[min(manifest)]:
    if componentType == 'PHY':
        phyLayerBuildId =  buildId
        break

# increment sequence
sequence += 1

# retrieve current configuration to build a parameter type mapping
configurationTypes = helpers.getConfigurationTypes(sock,sequence,buildId)

# create a Request message
request = remotecontrolportapi_pb2.Request()

request.update.configuration.buildId = phyLayerBuildId

# set the Request sequence number
sequence += 1
request.sequence = sequence

# set the Request type
request.type = remotecontrolportapi_pb2.Request.TYPE_REQUEST_UPDATE

# set the Request Update type
request.update.type = remotecontrolportapi_pb2.TYPE_UPDATE_CONFIGURATION

# create a new configuration parameter
parameter = request.update.configuration.parameters.add()

# set the parameter name
parameter.name = 'txpower'

# create an Any instance to hold the value
any = parameter.values.add()

# set the Any value and type
helpers.toAny(any,txPowerdBm, configurationTypes['txpower'])

print '-' * 25,'\n','request\n','-' * 25
print request

response = helpers.transaction(sock,request)

print '-' * 25,'\n','response\n','-' * 25
print response
