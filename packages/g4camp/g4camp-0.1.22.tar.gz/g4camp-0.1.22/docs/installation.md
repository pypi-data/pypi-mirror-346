---
layout: post
title: 1. Installation
---

## Requirements:

 - Python3
 - [Geant4](https://geant4.web.cern.ch) built with the following CMake options:
   - `GEANT4_BUILD_TLS_MODEL=global-dynamic` (required)
   - `GEANT4_USE_OPENGL_X11=ON`, `GEANT4_USE_QT=ON` (optional) for 3D visualization and GUI support \
See Section in "Building and Installing from Source" in [Installation guide](https://geant4-userdoc.web.cern.ch/UsersGuides/InstallationGuide/html/installguide.html)
 - [geant4_pybind](https://github.com/HaarigerHarald/geant4_pybind) package. The release version should match Geant4 version (see [releases](https://github.com/HaarigerHarald/geant4_pybind/releases))
 
## Getting g4camp

There are two ways:

 1. With pip:
```
pip install g4camp
```

 2. From [GIT repository](https://git.jinr.ru/malyshkin/g4camp):
```bash
git clone ...
```
or
```bash
git clone ...
```
