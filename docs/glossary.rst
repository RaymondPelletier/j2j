Glossary
========

pattern
    A string describing elements of the jertl mini-language for processing data structures
    Elements include structures, transforms, collations, and rules

structures
    Used both for matching and as template for Filling

binding
    A mapping from an identifier to data

variable
    reference to data. variables are indicated in mini-language via identifiers

identifier
    string used as name of a variable

rule
    sequence of conditions which when satisfied implies a set of actions to be taken

inference
    describes conditions and results of the application of a rule to data.

vararg
    structure construct indicating that a variable should be bound to a slice of an array

kwargs
    structure construct indicating that a variable could be bound to an object containing all key value pairs
    not already referenced in the enclosing object structure

matcher
    mini-language construct defining a condition which is satisfied when a variable matches
    a structure

setter
    mini-language construct defining an action which results in a variable being bound
    to a filled template

focus
    data being matched
