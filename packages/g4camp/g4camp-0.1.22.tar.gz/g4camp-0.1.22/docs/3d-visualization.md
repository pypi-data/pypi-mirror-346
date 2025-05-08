---
layout: post
title: 5. Example with Visualization
---

## Example with visualization

G4CAMP provides [Examples](https://git.jinr.ru/malyshkin/g4camp/-/tree/main/g4camp/examples). To run the example with 3D visualization you need:

 - `vis.mac` configuration [file](https://git.jinr.ru/malyshkin/g4camp/-/blob/main/g4camp/examples/vis.mac)
 - set Geant4 environment variables:
```bash
source /path/to/geant4-install/bin/geant4.sh
```

Run it:

```bash
python -m g4camp.examples.example_vis.py
```

You should get a window with 3D visualization. If you have built your Geant4 with QT5 support you should also get GUI with the list of available commands with descriptions (left side) and prompt (bottom right). Otherwise you will have prompt in your terminal. Type 'help' to see the available commands.

You can configure the primary source and start simulation:
```
/gun/particle mu-
/gun/energy 1 TeV
/gun/position 0 0 10 m
/run/beamOn 1
```
