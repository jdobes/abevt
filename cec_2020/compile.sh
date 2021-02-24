#!/usr/bin/env bash

c++ -o cec20_test_func.o -c cec20_test_func.cpp
c++ -o SOMA.o -c SOMA.cpp
c++ -o JDE.o -c JDE.cpp
c++ -o cec_2020 cec20_test_func.o SOMA.o JDE.o main.cpp

rm *.o
