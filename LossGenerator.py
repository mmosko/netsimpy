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

# Called to generate a delay value

import abc
import random


class LossGenerator(object):
    """
    A Loss generator embodies some probability distribution and will return either True (loss indicated)
    or False (loss not indicated).
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def next(self):
        """
        Generate the next delay time in seconds
        :return: float (seconds)
        """
        pass


class UniformLoss(LossGenerator):
    """
    Generates a delay from an exponential distribution with the specified mean (1/lambda):

    TODO: Should generate its own seed and keep its own RNG stream
    """

    def __init__(self, loss_probability):
        """
        :param min_delay: Added to the exponential sample
        :param mean: the mean exponential delay (1 / lambda)
        """
        super(UniformLoss, self).__init__()
        if not 0.0 <= loss_probability <= 1.0: raise ValueError("loss probability must be [0, 1], got {}".format(loss_probability))
        self._loss_probability = loss_probability

    def next(self):
        r = random.random()
        return r < self._loss_probability


class MarkovLoss(LossGenerator):
    """
    A two-state markov loss process
    TODO: Should generate its own seed and keep its own RNG stream
    """

    _STATE_NO_LOSS = 1
    _STATE_LOSS = 2

    def __init__(self, loss_probability, recovery_probability):
        """

        :param loss_probability: The probability of going from no loss to loss state
        :param recovery_probability: The probability of going from loss state to no loss state
        """
        super(MarkovLoss, self).__init__()
        if not 0.0 <= loss_probability <= 1.0:
            raise ValueError("loss probability must be [0, 1], got {}".format(loss_probability))
        if not 0.0 <= recovery_probability <= 1.0:
            raise ValueError("loss recovery_probability must be [0, 1], got {}".format(recovery_probability))

        self._loss_probability = loss_probability
        self._recovery_probability = recovery_probability
        self._state = MarkovLoss._STATE_NO_LOSS

    def next(self):
        result = None
        r = random.random()
        if self._state == MarkovLoss._STATE_NO_LOSS:
            result = False
            if r < self._loss_probability:
                self._state = MarkovLoss._STATE_LOSS
                result = True
        else:
            result = True
            if r < self._recovery_probability:
                self._state = MarkovLoss._STATE_NO_LOSS
                result = False
        return result
