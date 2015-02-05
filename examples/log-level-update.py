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

import socket
import helpers 
import emanesh.remotecontrolportapi_pb2 as remotecontrolportapi_pb2

# create a socket
sock = socket.socket()  

# connect to a running emulator instance
sock.connect(('node-1',47000))

# create a Request message
request = remotecontrolportapi_pb2.Request()

# set the Request type
request.type = remotecontrolportapi_pb2.Request.TYPE_REQUEST_UPDATE

# set the Request sequence number
request.sequence = 1

# set the Request Query type
request.update.type = remotecontrolportapi_pb2.TYPE_UPDATE_LOGLEVEL

# set the emulator log level to DEBUG
request.update.logLevel.level = 4

print '-' * 25,'\n','request\n','-' * 25
print request

response = helpers.transaction(sock,request)

print '-' * 25,'\n','response\n','-' * 25
print response
