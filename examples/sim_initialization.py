#!/usr/local/bin/python

#
# Copyright (c) 2016, Xerox Corporation (Xerox) and Palo Alto Research Center, Inc (PARC)
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
import os
import binascii
from simulator.simulator import Simulator
from simulator.node import Node
from simulator.delay import ExponentialDelay
from simulator.channel import Channel

repeat_count = 1000

for trial in range(0, repeat_count):
    # Set one manually...
    #seed = "\x61\xcb\x82\x90"

    seed = os.urandom(4)
    print "random.seed() = 0x{}".format(binascii.hexlify(seed))
    random.seed(seed)

    # Set message printing level
    Simulator.EXTRA_VERBOSE = False
    Simulator.VERBOSE = False
    Channel.VERBOSE = False
    Node.EXTRA_VERBOSE = False
    Node.EXTRA_VERBOSE = False

    sim = Simulator()
    loss_rate = 0.60       # loss rate (0.0 to 1.0)
    min_delay = 0.000001   # 1 micro-second minimum delay
    mean_dealy = 0.000020  # 20 micro-second delay

    delay_generator = ExponentialDelay(min_delay, mean_dealy)

    alice_output = Channel(sim, delay_generator, loss_rate)
    alice = Node(sim, "ALICE", True, alice_output)

    bob_output = Channel(sim, delay_generator, loss_rate)
    bob = Node(sim, "BOB  ", False, bob_output)

    alice.set_peer(bob)
    bob.set_peer(alice)

    sim.run_count(1000)

    alice.print_stats()
    bob.print_stats()

    print "trail {:6} Alice is {}, Bob is {}".format(
        trial + 1,
        "OK" if alice.data_ready else "NOT OK",
        "OK" if bob.data_ready else "NOT OK",
    )
    if not alice.data_ready or not bob.data_ready: raise RuntimeError("Terminated in failure mode")