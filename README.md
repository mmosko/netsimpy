# Introduction

netsimpy - The simple network simulator in Python: an easy-to-use discrete event simulator.

## Files
The `simulator/` directory is the discrete event simulator.  It's a basic hand-crafted message passing
discrete event simulator.

Simulation executables:

* `sim_initialization.py`: Runs 1000 trials with different random number seeds for syncing two fresh nodes.
* `sim_reboot.py`: Runs trials of syncing two nodes, passing data, then rebooting one or more of the nodes.

## Usage

    python sim_x.py

## Core Simulator
The core simulator is made up of 'Simulator.py' and 'Event.py'.  As a discrete event simulator, it is only concerned
with tracking the time and scheduling events with delays.

## Network Model
The network layer uses message passing between layers:

    MacLayer <-> PhyLayer <-> Channel

The messages model the typical ISO/IEEE layer model of request/indicate and send/recv.  The messages correspond
(loosly) to SDUs between layers.

```text
+----v----------^-------+
| request    indicate   |
|       MAC Layer       |
|  send        recv     |     
+----v----------^-------+
     |          |
+----v----------^-------+
| request    indicate   |
|       PHY Layer       |
|  send        recv     |     
+----v----------^-------+
     |          |
+----v----------^-------+
| request    indicate   |
|       Channel         |
|  send        recv     |     
+----v----------^-------+
```
