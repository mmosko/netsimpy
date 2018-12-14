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

import random
import collections
import abc
from netsimpy.DelayGenerator import DelayGenerator
from netsimpy.Simulator import Simulator
from Layer import Layer
from netsimpy.network import SDU
from netsimpy.Event import Event


_default_layer_delay = 1E-6

class Channel(Layer):
    def __init__(self, layer_delay=_default_layer_delay):
        """
        The channel does not maintain a queue.  The phy/mac must do that.

        :param data_rate: bits per second
        :param layer_delay: delay (seconds) to pass data up to mac, default 1us
        """
        self._attached_phys = []
        self._layer_delay = layer_delay

    @abc.abstractmethod
    def _receive_request(self, sdu):
        pass

    @abc.abstractmethod
    def _receive_indication(self, sdu):
        pass

    def attach(self, phy_layer):
        """
        Attach the given phy layer to the chanel.  After a short delay, the phy_layer should
        receive a `BusyIndication` or `IdleIndication` SDU

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

    def _broadcast(self, sdu):
        for phy in self._attached_phys:
            phy.receive(sdu)

    def _send_to_phy(self, phy, sdu):
        Simulator.sim().schedule(Event(self._layer_delay, phy.receive, sdu))


class FifoChannel(Channel):
    """
    Pass packets to all attached PHYs with a given propagation delay generator and
    given loss generator.  The packet is received or lost by all stations with the same loss probability.
    The channel will go busy for all phys when any one starts transmitting and only goes idle after
    the right amount of time.
    """

    _STATE_IDLE = 1
    _STATE_TRANSMITTING = 2

    def attach(self, phy_layer):
        # Overloaded method from Channel
        super(FifoChannel, self).attach(phy_layer)
        self._send_to_phy(phy_layer, self._channel_state_sdu())

    def __init__(self, layer_delay=_default_layer_delay, delay_generator=None, loss_generator=None):
        super(FifoChannel, self).__init__(layer_delay)
        self._busy = False

    def _receive_request(self, sdu):
        """
        delay the SDU by the channel time, then broadcast to all attached phys (including the sender)
        :param sdu:
        :return:
        """
        if self._busy: raise RuntimeError("Channel busy")
        self._busy = True
        self._propagate(sdu)

    def _receive_indication(self, sdu):
        raise RuntimeError("Should never receive an indication at the channel")

    def _propagate(self, message):
        # delay is the message time plus the random channel delay
        delay = self._calculate_delay(message)

    def _calculate_delay(self, sdu):
        pass

    def _timer_callback(self, event):
        pass

    def _channel_state_sdu(self):
        if self._busy:
            return SDU.BusyIndication()
        else:
            return SDU.IdleIndication()

    def _broadcast_channel_state(self):
        self._broadcast(self._channel_state_sdu())
