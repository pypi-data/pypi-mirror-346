---
layout: post
title: 6. Python Module
---

A simple use of G4CAMP as a python module can be like this:

```python
from g4camp.g4camp import g4camp

# initialize and configure
sim = g4camp(...)
sim.setXXX(...)
sim.configure()

# run simulation
for data in sim.run(n_events=10):
    particles = data.particles
    tracks = data.tracks
    photons = data.photons
    # do something else...
```

Also refer to [Example-1](https://git.jinr.ru/malyshkin/g4camp/-/blob/main/g4camp/examples/example_1.py) and [Example-2](https://git.jinr.ru/malyshkin/g4camp/-/blob/main/g4camp/examples/example_2.py)

## Initialization

Initilization is made by calling `g4camp()`. The arguments are the following:

 - `physics`: 'Custom' or any standard Geant4 physics list ('QGSP_BERT', 'FTFP_BERT', and others, see [Reference Physics Lists](https://geant4.web.cern.ch/node/155))
 - `optics` (bool): enable/disable emission of Cherenkov photons. Can only be enabled for the 'Custom' physics.
 - `primary_generator`: 'gun' or 'gps' (see Primary Modes in [Introduction](introduction))
 - `gun_args`: dictionary of gun source parameters:
   - `particle`: particle type (e-, e+, gamma, mu- etc.)
   - `energy`: energy in GeV
   - `position`: positio in meters
   - `direction`: X, Y, Z components of direction vector \
   *Note that the gun can also be configured by `setGunXXX()` methods*


## Configuration

Configuration is done via `setXXX()` methods and should be followed by method `configure()`.

 - `setDetectorHeight(val)`: height of the cylindrical simulation volume
 - `setDetectorRadius(val)`: radius of the cylindrical simulation volume
 - `setGPSMacro(macro)`: path to macro file with Geant4 [General Particle Source](https://www.fe.infn.it/u/paterno/Geant4_tutorial/slides_further/GPS/GPS_manual.pdf) commands to configure the primary particle source in mode `gps`.
 - `setGunParticle(pname)`: name of the particle (e.g. 'e-', 'e+', 'gamma', 'mu-' etc.)
 - `setGunEnergy(ene_val, ene_unit)`: energy value and unit for the `gun` source
 - `setGunPosition(x_val, y_val, z_val, pos_unit)`: position X, Y, Z components and unit for the `gun` source
 - `setGunDirection(dx, dy, dz)`: direction X, Y, Z components for the `gun` source
 - `setSkipMinMax(skip_min, skip_max)`: energy range for cascade starter particles to be skipped, see [Skipping Cascades](skipping-cascades))
 - `setPhotonSuppressionFactor(val)`: only `1/val` of the total number of photons will be produced
 - `setRandomSeed(val)`: random seed for simulation
 - `setCut(particle, cut_value, cut_unit)`: set individual production cuts for particles
 - `setVerbose(control_verbose, tracking_verbose, run_verbose, em_process_verbose, had_process_verbose)`: set verbosity of Geant4 output with integer values (0 -- no output, 1 -- minimal output, 2 -- extended output)
 - `applyGeant4Command(command, arguments)`: apply a standard Geant4 command, e.g. `command='/run/printProgress'`, `arguments=[100]` would apply '/run/printProgress 100' (to print event id of each 100th event).
 
## Running
 
The `run(n_events)` function of `g4camp` returns a generator of event-by-event output data.

An example: 

```python
from g4camp.g4camp import g4camp

sim = g4camp(primary_generator='gps', optics=False)
sim.setDetectorHeight(1000)
sim.setDetectorRadius(500)
sim.setSkipMinMax(0.0, 0.01)
sim.setVerbose(tracking_verbose=1)
sim.configure()

# One event at 0 0 0
sim.applyGeant4Command('/gps/particle e-')
sim.applyGeant4Command('/gps/energy 1 TeV')
sim.applyGeant4Command('/gps/position 0 0 0')
sim.applyGeant4Command('/gps/direction 0 0 1')
#
for data in sim.run(n_events=1):
    particles = data.particles
    tracks = data.tracks
    print(f"\n{len(tracks):>6} tracks, {len(particles):>6} cascade starters;\n")
    
# Many events at random positions and directions
sim.applyGeant4Command('/gps/pos/type Volume')
sim.applyGeant4Command('/gps/pos/shape Cylinder')
sim.applyGeant4Command('/gps/pos/halfz 400 m')
sim.applyGeant4Command('/gps/pos/radius 400 m')
sim.applyGeant4Command('/gps/pos/center 0 0 500 m')
sim.applyGeant4Command('/gps/dir/type iso')
sim.configure()
sim.setVerbose(tracking_verbose=0)
#
for ievt, data in enumerate(sim.run(n_events=10)):
    particles = data.particles
    tracks = data.tracks
    primary = tracks[0]
    uid, pdgid, x, y, z, t, E = primary
    print(f"Event #{ievt}")
    print(f"Position:   {x:.1f}, {y:.1f}, {z:.1f} m")
    print(f"{len(tracks):>6} tracks, {len(particles):>6} cascade starters;\n")
```
