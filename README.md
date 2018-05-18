## About ##

NEAT (NeuroEvolution of Augmenting Topologies) is a method developed by Kenneth O. Stanley for evolving arbitrary neural 
networks. This is a Python implementation of NEAT forked from the excellent project by @CodeReclaimers, with a modification in the data structure for the connections of the genome.

Instead of using a dictionary for the connections we are using a Red-Black tree in order to proof time complexity of data structures. At this moment only diabetes and card problems are enable for testing. The code in the rest of the data sets needs some fixing. Another remark is that you will find a lot of repetion in the code for the data sets as it was intended for them to be separated tests. This will be fixed soon.

Please see [Selected Publications](http://www.cs.ucf.edu/~kstanley/#publications) on Stanley's website in case you need more information about NEAT. 

A proper license is still missing from this repository in order to aknowledge @CodeReclaimers for their good work. 

The documentation of the original repository is available on [Read The Docs](http://neat-python.readthedocs.io).
