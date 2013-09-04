#!/bin/bash

cmake ../.. -DCMAKE_OSX_ARCHITECTURES=i386 && make

echo ========== BEGIN(testcpp output) ==========
cat testcpp.output
cat testcpp.error
echo ==========  END(testcpp output)  ==========
