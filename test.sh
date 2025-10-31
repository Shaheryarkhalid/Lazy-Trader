#! /bin/sh


echo "------------------------------- Running tests in functions -------------------------------"
python -m unittest discover -s functions 


echo "------------------------------- Running tests in Alpaca -------------------------------"
python -m unittest discover -s Alpaca

echo "------------------------------- Running tests in AI -------------------------------"
python -m unittest discover -s AI



