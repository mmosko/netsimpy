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


class Delay(object):
    """
    Convenience abstract base class for Delay instances.

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


class ExponentialDelay(object):
    """
    Generates a delay from an exponential distribution with the specified mean (1/lambda):

    TODO: Should generate its own seed and keep its own RNG stream
    """

    def __init__(self, min_delay, mean):
        """
        :param min_delay: Added to the exponential sample
        :param mean: the mean exponential delay (1 / lambda)
        """
        super(ExponentialDelay, self).__init__()
        if mean <= 0.0: raise ValueError("Mean must be positive, got {}".format(mean))
        self._beta = mean
        self._min = min_delay

    def next(self):
        return random.expovariate(1/self._beta) + self._min


class UniformDelay(object):
    """
    TODO: Should generate its own seed and keep its own RNG stream
    """

    def __init__(self, lower, upper):
        super(UniformDelay, self).__init__()
        self._lower = lower
        self._upper = upper

    def next(self):
        return random.uniform(self._lower, self._upper)


Delay.register(ExponentialDelay)
Delay.register(UniformDelay)

