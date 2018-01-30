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

import socket
from helpers import transaction,getManifest

try:
    import emane.shell.remotecontrolportapi_pb2 as remotecontrolportapi_pb2
except:
    import emanesh.remotecontrolportapi_pb2 as remotecontrolportapi_pb2

# create a socket
sock = socket.socket()

# connect to a running emulator instance
sock.connect(('node-1',47000))

# set the Request sequence number
sequence = 1

# retrieve the manifest from the running emulator instance
manifest = getManifest(sock,sequence)

# create a Request message
request = remotecontrolportapi_pb2.Request()

# set the Request sequence number
sequence += 1
request.sequence = sequence

# set the Request type
request.type = remotecontrolportapi_pb2.Request.TYPE_REQUEST_QUERY

# set the Request Query type
request.query.type = remotecontrolportapi_pb2.TYPE_QUERY_CONFIGURATION

# for this example, set the target build id to the smallest build id
# component contained in the smallest NEM id running in the emulator
request.query.configuration.buildId = \
  min([x.buildId for x in manifest[min(manifest)]])

print '-' * 25,'\n','request\n','-' * 25
print request

response = transaction(sock,request)

print '-' * 25,'\n','response\n','-' * 25
print response
