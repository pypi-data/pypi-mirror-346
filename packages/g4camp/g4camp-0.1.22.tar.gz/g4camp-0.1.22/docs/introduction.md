---
layout: post
title: 2. Introduction
---

## Geant4 Simulation Procedure
  In Geant4 simulation is performed as following. At each step lengths to any possible interaction are calculated and the minimal is chosen. This interaction "happens" with production of all secondary particles above the so-called cuts. In G4CAMP the cuts are adjusted to be around Cherenkov threshold for electrons. All the particles below this energy (E = 760 keV) are killed. All the produced particles are tracked in the same way.
  
## Physics Lists
User can choose between the following physics lists:
 - **Custom** (*default*): electromagnetic + hadronic + Cherenkov (*optional*)
 - Standard Geant4 physics lists (see [Reference Physics Lists](https://geant4.web.cern.ch/node/155)): 
   - **QGSP\_BETR**
   - **QGSP\_BIC**
   - **FTFP\_BERT**

> *NOTE*: Cherenkov photon emission can not be enabled with the standard Geant4 physics lists.

## Usage Modes
 - [Ready-to-run application (run_g4camp)](run_g4camp) \
  --- a command-line application allowing to use G4CAMP with zero coding \
 - [3D visualization](3d-visualization) \
 --- an example script to use Geant4 visualization
 - [Python module](python-module) \
 --- description of G4CAMP functionalty as a component

## Default Units

| Measurement       | Unit |
| ------ | --- |
| Energy            | GeV |
| Position          | meters |
| Time              | nanoseconds |
| Photon wavelength | nanometers  |
| ------ | --- |

## Particle Naming

Particles are iether named following Geant4 (e.g. `e-`, `mu+`, `gamma`, `pi0`, `anti_nu_e`]) or by their [PDGID codes](https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf).

## Primary Modes

There are two primary injection modes: 
 - `gun` is a custom particle injector and allows to avoid input macro files. Useful when G4CAMP is used as a Pyhon module.
 - `gps` is a standard Geant4 injector ([General Particle Source](https://www.fe.infn.it/u/paterno/Geant4_tutorial/slides_further/GPS/GPS_manual.pdf)) with a large number of configurations. Useful when G4CAMP is used as a standalone application. 

> *NOTE*: technically it would be possible to use the standard '/gun/' commands of Geant4, but this is disabled in order to avoid interferring with build-in G4CAMP mehtods for the source configuration.
