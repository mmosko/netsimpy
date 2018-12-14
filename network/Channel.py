#
# Copyright (c) 2016-2018, Xerox Corporation (Xerox) and Palo Alto Research Center, Inc (PARC)
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

from netsimpy.DelayGenerator import DelayGenerator
from netsimpy.Simulator import Simulator
from netsimpy.Event import Event
import random
import collections
import abc
from Layer import Layer
from netsimpy.network import SDU


class Channel(Layer):
    def __init__(self):
        """
        """
        self._attached_phys = []

    @abc.abstractmethod
    def _receive_request(self, sdu):
        pass

    @abc.abstractmethod
    def _receive_indication(self, sdu):
        pass

    def attach(self, phy_layer):
        """
        Attach the given phy layer to the chanel.

        :param phy_layer:
        :return: None
        """
        self._attached_phys.append(phy_layer)

    def detach(self, phy_layer):
        """
        Detach the given phy_layer from the channel

        :param phy_layer:
        :return: None
        """
        self._attached_phys.remove(phy_layer)

    def broadcast(self, request_sdu):
        # convert the request_sdu to an indication_sdu then send to all phys
        indication = SDU.Indication(request_sdu.payload())
        for phy in self._attached_phys:
            phy.receive(indication)

class FifoChannel(Channel):
    """
    Pass packets to all attached PHYs with a given propagation delay generator and
    given loss generator.  The packet is received or lost by all stations with the same loss probability.
    """
    def __init__(self, delay_generator, loss_generator):
        super(FifoChannel, self).__init__()

    def _receive_request(self, sdu):
        """
        delay the SDU by the channel time, then broadcast to all attached phys (including the sender)
        :param sdu:
        :return:
        """
        # delay it back to ourself
        pass

    def _receive_indication(self, sdu):
        pass

