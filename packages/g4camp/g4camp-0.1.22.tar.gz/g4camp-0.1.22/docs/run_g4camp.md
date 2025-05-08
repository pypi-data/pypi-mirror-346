---
layout: post
title: 4. Standalone Application (run_g4camp)
---

You can use `run_g4camp` script to run configure and run simulation like this:

```bash
python -m g4camp.run_g4camp -p gun --gun_particle e+ --gun_energy 1000 --gun_position -10 0 20 --gun_direction 0 0.2 0 -n 10 -o output.h5
```

It generates 10 positrons of 1 TeV (1000 GeV) at (-10, 0, 20) meters with direction (0, 0.2 1)

If you want to skip cascade starters (e-/e+/gamma) within energy range [0.001, 0.05]*1 TeV run add `--skip_min` and `--skip_max` arguments:

```bash
python -m g4camp.run_g4camp -p gun --gun_particle e+ --gun_energy 1000 --gun_position -10 0 20 --gun_direction 0 0.2 0 -n 10 -o output.h5 --skip_min 0.001 --skip_max 0.05
```


 skipping e+ and e- with E within [0.001, 0.05] GeV energy range and outputs vertices, tracks and photons into an HDF5 file (output.h5 in this example).

For the full list of available commands in the `run_g4camp` script type:

```bash
python -m g4camp.run_g4camp --help
```
You can also configure the source with the standard Geant4 '/gps' commands by specifying them in a macro file:

```bash
python -m g4camp.run_g4camp -n 10 -p gps --gps_macro muons.mac --skip_min 0.001 --skip_max 0.05 -o output.h5
```

with the content of 'muons.mac' like this:

```
/gps/particle mu-
/gps/energy 10 TeV
/gps/position 0 0 0 m
/gps/direction 0 0 1
```
> *NOTE*: A detailed description of `/gps/` commands: [Geant4 General Particle Source](https://www.fe.infn.it/u/paterno/Geant4_tutorial/slides_further/GPS/GPS_manual.pdf)
