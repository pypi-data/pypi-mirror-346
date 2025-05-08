---
layout: post
title: 7. Output
---

G4CAMP keeps its output as NumPy arrays in form of 2D tables. They are:

 - **Vertices** (`PDGID`, `position`, `direction`, `time`, `energy`)
   - for e+/e- particles with $E_skip_min$ < E_kin < E_skip_max
 - **Tracks** (`UID`, `PDGID`, `position`, `time`, `energy` for each interaction point)
   - for all electrically charged particles above Cherenkov threshold 
   - for all other particles except optical photons
 - **Photons** (`position`, `direction`, `time`, `wavelength`)
    - from all propagated particles (skipped particles do not emit photons)
    
Script [run_g4camp](run_g4camp) stores these structures to HDF5 files.
