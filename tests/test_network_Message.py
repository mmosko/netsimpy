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

import unittest
from netsimpy.network.Message import Message


class TestMessage(unittest.TestCase):

    def test_empty(self):
        message = Message()
        self.assertIsNotNone(message, "Message is None")
        self.assertIsNone(message.payload(), "payload is not none")
        self.assertEqual(message.payload_length(), 0, "Payload length is %d, expected 0".format(message.payload_length()))
        self.assertEqual(message.message_length(), 0, "Message length is %d, expected 0".format(message.message_length()))

    def test_payload_only(self):
        payload = 'All good things must come to an end'
        expected_length = len(payload)
        message = Message(payload)
        self.assertIsNotNone(message, "Message is None")
        self.assertIsNotNone(message.payload(), "payload is None")
        self.assertEqual(message.payload(), payload, "Payloads do not match")
        self.assertEqual(message.payload_length(), expected_length,
                         "Payload length is %d, expected %d".format(message.payload_length(), expected_length))
        self.assertEqual(message.message_length(), expected_length,
                         "Message length is %d, expected %d".format(message.message_length(), expected_length))

    def test_payload_virtual_length(self):
        payload = 'All good things must come to an end'
        expected_length = 257
        message = Message(payload=payload, virtual_length=expected_length)
        self.assertIsNotNone(message, "Message is None")
        self.assertIsNotNone(message.payload(), "payload is None")
        self.assertEqual(message.payload(), payload, "Payloads do not match")
        self.assertEqual(message.payload_length(), expected_length,
                         "Payload length is %d, expected %d".format(message.payload_length(), expected_length))
        self.assertEqual(message.message_length(), expected_length,
                         "Message length is %d, expected %d".format(message.message_length(), expected_length))

    def test_payload_and_headers(self):
        payload = 'All good things must come to an end'
        hdr_payload = 'Some more quickly than others'
        header = Message(payload=hdr_payload)
        message = Message(payload=payload)
        message.push_header(header)
        expected_message_length = len(payload) + len(hdr_payload)
        self.assertIsNotNone(message, "Message is None")
        self.assertIsNotNone(message.payload(), "payload is None")
        self.assertEqual(message.payload(), payload, "Payloads do not match")
        self.assertEqual(message.message_length(), expected_message_length,
                         "Message length is %d, expected %d".format(message.message_length(), expected_message_length))

    def test_payload_and_headers_init(self):
        payload = 'All good things must come to an end'
        hdr_payload = 'Some more quickly than others'
        header = Message(payload=hdr_payload)
        # put in two headers
        message = Message(payload=payload, headers=[header, header])
        expected_message_length = len(payload) + len(hdr_payload) * 2
        self.assertIsNotNone(message, "Message is None")
        self.assertIsNotNone(message.payload(), "payload is None")
        self.assertEqual(message.payload(), payload, "Payloads do not match")
        self.assertEqual(message.message_length(), expected_message_length,
                         "Message length is %d, expected %d".format(message.message_length(), expected_message_length))

    def test_payload_and_headers_virtual(self):
        payload = 'All good things must come to an end'
        hdr_payload = 'Some more quickly than others'
        header = Message(payload=hdr_payload, virtual_length=10)
        message = Message(payload=payload, virtual_length=20)
        message.push_header(header)
        expected_message_length = 30
        self.assertIsNotNone(message, "Message is None")
        self.assertIsNotNone(message.payload(), "payload is None")
        self.assertEqual(message.payload(), payload, "Payloads do not match")
        self.assertEqual(message.message_length(), expected_message_length,
                         "Message length is %d, expected %d".format(message.message_length(), expected_message_length))
