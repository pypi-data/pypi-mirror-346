---
layout: post
title: 3. Skipping Cascades
---

## Skipping cascades

Simulation of cascade development is time consuming. In practise it is often replaced by a parametrization (see e.g. [Raedel, Wiebusch 2013](https://doi.org/10.1016/j.astropartphys.2013.01.015)). G4CAMP allows either to run a full simulation down to the Cherenkov threshold of electrons, or kill particles in a certain energy range [`E_skip_min`, `E_skip_max`] saving its interaction vertex, i.e. position, direction, time and energy (see 'Vertex' in [Output](output)).

`E_skip_min` and `E_skip_max` are set with respect to the initial energy of the primary particle. The rule is applied for the particles starting pure electro-magnetic cascades: `e-`, `e+`, `gamma` (can be changed in future)

### Example

`E_init` = 10 TeV \
`E_skip_min` = 0.001 \
`E_skip_max` = 0.01

Then all particles above 0.01 * 10 TeV = 100 GeV are tracked. If the energy of electron, positron or gamma is within [10 GeV, 100 GeV] it is killed and the vertex is stored. In all other cases particles are tracked untill their energy becomes lower than the Cherenkov threshold of electrons.
