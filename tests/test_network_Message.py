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

    def test_push_pop(self):
        message = Message()
        h1 = Message(payload='header 1', virtual_length=1)
        h2 = Message(payload='header 2', virtual_length=2)
        h3 = Message(payload='header 3', virtual_length=4)
        h4 = Message(payload='header 4', virtual_length=8)

        headers = [h1, h2, h3, h4]
        for h in headers:
            message.push_header(h)

        expected_message_length = 15
        self.assertEqual(message.message_length(), expected_message_length,
                         "Message length is %d, expected %d".format(message.message_length(), expected_message_length))

        while headers:
            expected_header = headers.pop()
            test_header = message.pop_header()
            expected_length = expected_message_length - test_header.message_length()

    def test_eq(self):
        h1 = Message(payload='header 1', virtual_length=1)
        h2 = Message(payload='header 2', virtual_length=2)
        h3 = Message(payload='header 3', virtual_length=4)
        h4 = Message(payload='header 4', virtual_length=8)
        m1 = Message(payload='blueberry', virtual_length=5, headers=[h1, h2, h3, h4])
        m2 = Message(payload='blueberry', virtual_length=5, headers=[h1, h2, h3, h4])
        m3 = Message(payload='blueberry', virtual_length=5, headers=[h1, h2, h3, h4])

        x1 = m1 == m2
        x2 = m2 == m3
        x3 = m3 == m1
        self.assertTrue(x1, "m1 != m2")
        self.assertTrue(x2, "m2 != m3")
        self.assertTrue(x3, "m3 != m1")

        # and test negatives
        m10 = Message(payload='carrot', virtual_length=5, headers=[h1, h2, h3, h4])
        m11 = Message(payload='blueberry', virtual_length=50, headers=[h1, h2, h3, h4])
        m12 = Message(payload='blueberry', virtual_length=5, headers=[h1, h2, h3])
        m13 = Message(payload='blueberry', virtual_length=5, headers=[h4, h2, h3, h1])
        m14 = Message(payload='blueberry', virtual_length=5, headers=[h1, h2, h4, h4])
        rejects = [m10, m11, m12, m13, m14]

        for m in rejects:
            x = m == x1
            self.assertFalse(x, "Should have rejected {}" % [m,])

