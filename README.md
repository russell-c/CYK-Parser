# CYK-Parser
Simple CYK Parse program that accepts the grammar rules in Chomsky Normal Form and calculates the most probable parse of sentences entered by the user.

Grammar is stored as a dictionary and most probable parse is stored in a graph. The most probable parse here is calculated using the probability of each terminal combination possible using the non-terminals in a given sentence.

This program is based on an algorithm by Ernest Davis and is implemented in python 3.6. The algorithm improves on other established parsing algorithms by providing easy retrieval of the graph that stores the parse and the probability of said parse.
