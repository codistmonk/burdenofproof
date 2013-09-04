#!/bin/bash

cmake ../.. && make

echo "========== BEGIN(testcpp output) =========="
cat testcpp.output
cat testcpp.error
echo "==========  END(testcpp output)  =========="
