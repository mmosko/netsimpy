#
# Copyright (c) 2018, Xerox Corporation (Xerox) and Palo Alto Research Center, Inc (PARC)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL XEROX OR PARC BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


class Message(object):
    _message_id = 0

    @staticmethod
    def _next_id():
        next_id = Message._message_id
        Message._message_id += 1
        return next_id

    def __init__(self, payload=None, virtual_length=-1, headers=None):
        """
        A message has a payload and a stack of headers.  The length (in octets) of the message
        can be the actual length of the `payload` or specified by a `virtual_length`.  This allows sending
        large messages without actually allocating all that memory.

        The headers are stored in python stack order (a list via append() and pop()) so the lowest layer will
        be at the end of the list.  Headers are Messages themself, so they may have a virtual length.  This allows
        the payload to be a standard Python class and not worry about serializing in network form.

        If you add a header with a virtual length of 0, it will not count against the wire length and is purely
        a virtual header. An application, for example, could add such a header with metadata.

        :param payload:
        :param virtual_length: If non-negative, taken as the payload size
        :param headers: A stack of headers for the message
        """
        self._id = Message._next_id()

        self._headers = []
        if headers is not None:
            self._headers = headers

        self._payload = payload

        self._message_length = 0
        self._payload_length = 0
        if payload is not None:
            self._payload_length = len(payload)

        if virtual_length >= 0:
            self._payload_length = virtual_length

        self._set_message_length()

    def __repr__(self):
        return "{{Message: id {} mlen {} plen {} hdrs {} payload {}}}".format(
            self._id, self._message_length, self._payload_length, self._headers, self._payload)

    def _set_message_length(self):
        self._message_length = self._payload_length
        for header in self._headers:
            self._message_length += header.message_length()

    def payload_length(self):
        """
        Returns the defined length of the payload.  It may match the actual payload length or be
        a virtual length.  The virtual length could be longer or shorter than the payload.

        :return: Defined payload length (octets)
        """
        return self._payload_length

    def message_length(self):
        """
        Returns the total message encoding length, which includes all headers and the payload.
        The lengths may be virtual.

        :return: The total message length (octets)
        """
        return self._message_length

    def payload(self):
        return self._payload

    def push_header(self, header):
        self._headers.append(header)
        self._set_message_length()

    def pop_header(self, index):
        """
        Returns the last header added to the message.  May be None if no headers available.
        The header is removed from the stack of headers.
        :return:
        """
        header = None
        if self._headers:
            header = self._headers.pop()
            self._set_message_length()

        return header

    def peek_header(self):
        """
        Returns the top of stack header without removing it from the stack.

        :return: The top header (may be None)
        """
        header = None
        if self._headers:
            # returns the last element on the list
            header = self._headers[-1:]

        return header

