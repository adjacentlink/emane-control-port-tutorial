# Copyright (c) 2014-2015,2018 - Adjacent Link LLC, Bridgewater,
# New Jersey
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

try:
    import emane.shell.remotecontrolportapi_pb2 as remotecontrolportapi_pb2
except:
    import emanesh.remotecontrolportapi_pb2 as remotecontrolportapi_pb2

import struct
import collections

def transaction(sock,request):
    msg = request.SerializeToString()

    sock.send(struct.pack("!L%ds" % len(msg),len(msg),msg))

    # wait for response
    buf = str()
    messageLengthBytes = 0
    response = None

    while True:
        if not messageLengthBytes:
            data = sock.recv(4-len(buf))

            if not len(data):
                break

            if buf == None:
                buf=data
            else:
                buf+=data

            if(len(buf) == 4):
                (messageLengthBytes,) = struct.unpack('!I',buf)
                buf = str()

        else:
            data = sock.recv(messageLengthBytes-len(buf))

            if not len(data):
                break

            if buf == None:
                buf=data
            else:
                buf+=data

            if(len(buf) == messageLengthBytes):
                response = remotecontrolportapi_pb2.Response()
                response.ParseFromString(buf)
                messageLengthBytes = 0
                buf = str()
                break

    return response

def getManifest(sock,sequence):
    # create a Request message
    request = remotecontrolportapi_pb2.Request()

    # set the Request sequence number
    request.sequence = sequence

    # set the Request type
    request.type = remotecontrolportapi_pb2.Request.TYPE_REQUEST_QUERY

    # set the Request Query type
    request.query.type = remotecontrolportapi_pb2.TYPE_QUERY_MANIFEST

    response = transaction(sock,request)

    manifest = {}
    ManifestEntry = collections.namedtuple('ManifestEntry','buildId type plugin')


    dataType = {remotecontrolportapi_pb2.Response.Query.Manifest.NEM.Component.TYPE_COMPONENT_PHY : 'PHY',
                remotecontrolportapi_pb2.Response.Query.Manifest.NEM.Component.TYPE_COMPONENT_MAC : 'MAC',
                remotecontrolportapi_pb2.Response.Query.Manifest.NEM.Component.TYPE_COMPONENT_SHIM : 'SHIM',
                remotecontrolportapi_pb2.Response.Query.Manifest.NEM.Component.TYPE_COMPONENT_TRANSPORT : 'TRANSPORT'}

    if response.type == remotecontrolportapi_pb2.Response.TYPE_RESPONSE_QUERY:
        if response.query.type == remotecontrolportapi_pb2.TYPE_QUERY_MANIFEST:
            for nem in response.query.manifest.nems:
                manifest[nem.id] = []
                for component in nem.components:
                    manifest[nem.id].append(ManifestEntry(component.buildId,
                                                          dataType[component.type],
                                                          component.plugin))


    return manifest




def getConfigurationTypes(sock,sequence,buildId):
    # create a Request message
    request = remotecontrolportapi_pb2.Request()

    # set the Request sequence number
    request.sequence = sequence

    # set the Request type
    request.type = remotecontrolportapi_pb2.Request.TYPE_REQUEST_QUERY

    # set the Request Query type
    request.query.type = remotecontrolportapi_pb2.TYPE_QUERY_CONFIGURATION


    # set target build id
    request.query.configuration.buildId = buildId

    response = transaction(sock,request)

    mapping = {}

    for parameter in response.query.configuration.parameters:
        if parameter.values:
            mapping[parameter.name] = fromAny(parameter.values[0]).type

    return mapping

def fromAny(any):
    AnyEntry = collections.namedtuple('AnyEntry','value type')
    if any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_INT8:
        return AnyEntry(any.i32Value,'int8')
    elif any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_UINT8:
        return AnyEntry(any.u32Value,'uint8')
    elif any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_INT16:
        return AnyEntry(any.i32Value,'int16')
    elif any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_UINT16:
        return AnyEntry(any.u32Value,'uint16')
    elif any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_INT32:
        return AnyEntry(any.i32Value,'int32')
    elif any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_UINT32:
        return AnyEntry(any.u32Value,'uint32')
    elif any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_INT64:
        return AnyEntry(any.i64Value,'int64')
    elif any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_UINT64:
        return AnyEntry(any.u64Value,'uint64')
    elif any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_FLOAT:
        return AnyEntry(any.fValue,'float')
    elif any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_DOUBLE:
        return AnyEntry(any.dValue,'double')
    elif any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_STRING:
        return AnyEntry(any.sValue,'string')
    elif any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_BOOLEAN:
        return AnyEntry(any.bValue,'boolean')
    elif any.type == remotecontrolportapi_pb2.Any.TYPE_ANY_INETADDR:
        return AnyEntry(any.sValue,'inetaddr')

def toAny(any,value,valueType):

    if valueType == 'int8':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_INT8
        any.i32Value = value
    elif valueType == 'uint8':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_UINT8
        any.u32Value = value
    elif valueType == 'int16':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_INT16
        any.i32Value = value
    elif valueType == 'uint16':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_UINT16
        any.u32Value = value
    elif valueType == 'int32':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_INT32
        any.i32Value = value
    elif valueType == 'uint32':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_UINT32
        any.u32Value = value
    elif valueType == 'int64':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_INT64
        any.i64Value = value
    elif valueType == 'uint64':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_UINT64
        any.u64Value = value
    elif valueType == 'float':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_FLOAT
        any.fValue = value
    elif valueType == 'double':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_DOUBLE
        any.dValue = value
    elif valueType == 'string':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_STRING
        any.sValue = value
    elif valueType == 'boolean':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_BOOLEAN
        any.bValue = value
    elif valueType == 'inetaddr':
        any.type = remotecontrolportapi_pb2.Any.TYPE_ANY_INETADDR
        any.sValue = value

    return any
