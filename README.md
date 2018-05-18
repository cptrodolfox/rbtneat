[![Build Status](https://travis-ci.org/CodeReclaimers/neat-python.svg)](https://travis-ci.org/CodeReclaimers/neat-python)
[![Coverage Status](https://coveralls.io/repos/CodeReclaimers/neat-python/badge.svg?branch=master&service=github)](https://coveralls.io/github/CodeReclaimers/neat-python?branch=master)

## About ##

NEAT (NeuroEvolution of Augmenting Topologies) is a method developed by Kenneth O. Stanley for evolving arbitrary neural 
networks. This is a Python implementation of NEAT forked from the excellent project by @CodeReclaimers, with a modification in the data structure for the connections of the genome.

Instead of using a dictionary for the connections we are using a Red-Black tree in order to proof time complexity of data structures. 

Please see [Selected Publications](http://www.cs.ucf.edu/~kstanley/#publications) on Stanley's website in case you need more information about NEAT.

A proper license is still missing from this repository in order to aknowledge @CodeReclaimers for their good work. 

The documentation of the original repository is available on [Read The Docs](http://neat-python.readthedocs.io).
