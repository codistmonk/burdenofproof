#!/bin/bash

export CC=gcc
cmake ../.. -DCMAKE_OSX_ARCHITECTURES=i386 && make
