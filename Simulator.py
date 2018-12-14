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

import heapq
import sys


class Simulator:
    VERBOSE = False
    EXTRA_VERBOSE = False

    def __init__(self):
        self._time = 0
        self._event_count = 0
        self._stop_after_count = None
        self._stop_after_time = None
        self._priority_queue = []
        self._running = False

    def time(self):
        """
        The current simulation time
        :return: seconds (float)
        """
        return self._time

    def schedule(self, event):
        expiry = self._time + event.delay
        heapq.heappush(self._priority_queue, (expiry, event))

        if Simulator.EXTRA_VERBOSE:
            print "{:>12.9f} schedule({})".format(self._time, event)

    def execute(self):
        self._clear_breaks()
        self._execute()

    def execute_steps(self, number_of_events):
        """
        Break the simulator after executing the given number of events.  The event count includes only
        valid events.

        :param number_of_events:
        :return:
        """
        self._clear_breaks()
        self._stop_after_count = self._event_count + number_of_events
        self._execute()

    def execute_duration(self, duration):
        """

        :param duration: Relative time to run in seconds (float)
        :return:
        """
        self._clear_breaks()
        self._stop_after_time = self._time + duration

    def _clear_breaks(self):
        self._stop_after_count = None
        self._stop_after_time = None

    def _check_break(self):
        result = False

        if self._stop_after_count is not None:
            if self._event_count > self._stop_after_count:
                result = True

        if self._stop_after_time is not None:
            if self._time > self._stop_after_time:
                result = True

        return result

    def _execute(self):
        if self._running: raise RuntimeError("Cannot call a run function while already running")
        self._running = True

        try:
            while len(self._priority_queue) > 0:
                # check for termination conditions
                if self._check_break():
                    break

                t, event = heapq.heappop(self._priority_queue)

                self._step_time(t)

                if event.valid():
                    self._run_event(event)

        except Exception as e:
            sys.stdout.flush()
            print "Exception in Simulation execute loop"
            print e
            raise

        print "{:>12.9f} simulation stopping ({} still in queue, {} total events executed)".format(
            self._time, len(self._priority_queue), self._event_count)

        self._running = False

    def _step_time(self, t):
        if Simulator.EXTRA_VERBOSE:
            print "{:>12.9f} Stepping simulation time to {:>12.9f}".format(self._time, t)

        self._time = t

    def _run_event(self, event):
        if Simulator.EXTRA_VERBOSE:
            print "{:>12.9f} Executing event {}".format(self._time, event)

        self._event_count += 1
        event.fire_callback()
