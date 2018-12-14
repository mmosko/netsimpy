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


class Event(object):
    """
    Events are what get scheduled in the simulator.  An event has a non-negative delay (may be 0),
    a callback, and a data parameter (may be None) to pass to the callback.

    Example:
        delay = 0.025 # 25 milli-seconds

        # call a private method of this object.  Will automatically pass the "self" parameter.
        event = Event(delay, self._timeout_callback, None)
        self._sim.schedule(event)
    """

    _event_id = 0

    @staticmethod
    def next_event_id():
        next_id = Event._event_id
        Event._event_id += 1
        return next_id

    def __init__(self, delay, callback, data):
        """

        :param delay: The relative time to queue the event (seconds, float)
        :param callback: A callback function of the form 'callback(event)'
        :param data:
        """
        if delay < 0.0: raise ValueError("delay must be non-negative")
        if callback is None: raise ValueError("callback must not be None")

        self._id = Event.next_event_id()
        self._delay = delay
        self._callback = callback
        self._data = data
        self._valid = True

    def __repr__(self):
        return "{{Event: id {} delay {} callback {} data {}}}".format(
            self._id, self._delay, self._callback, self._data)

    def delay(self):
        return self._delay

    def fire_callback(self):
        self._callback(self)

    def data(self):
        return self._data

    def is_valid(self):
        """
        A valid event should be executed by the scheduler.  An invalid (false) event should be skipped.

        :return: True for a valid event, False for invalid
        """
        return self._valid

    def invalidate(self):
        """
        If you invalidate an event, it will not be executed.  This is an alternative to
        removing an event from the event queue.

        :return: None
        """
        self._valid = False
