#!/usr/bin/env bash

#c++ -o cec20_test_func.o -c cec20_test_func.cpp
#c++ -o SOMA.o -c SOMA.cpp
#c++ -o JDE.o -c JDE.cpp
#c++ -o cec_2020 cec20_test_func.o SOMA.o JDE.o main.cpp


c++ -fPIC -shared -o SOMA.so cec20_test_func.cpp SOMA.cpp
c++ -fPIC -shared -o JDE.so cec20_test_func.cpp JDE.cpp

rm *.o
