Syntax and Semantics
====================

The mini-language used by jertl contains elements which could be called "JSON adjacent".
The syntax for data structures will be recognizable by developers who have worked with JSON.
This is more so for Python developers given there are elements of the syntax which are identical
to that of the structural matching used in Python's `match` statement.

Literals
^^^^^^^^

The syntax for literals follows that of JSON.

>>> jertl.match('true', True) is not None
True

>>> jertl.match('false', False) is not None
True

>>> jertl.match('null', None) is not None
True

For numbers to be considered a match they *must* be of the same type.

>>> jertl.match('4', 4.0) is not None
False

whereas

>>> jertl.match('4', 4) is not None
True

Strings are specified using double quotes

>>> jertl.match('"a string"', 'a string') is not None
True

Single quoted strings are not allowed.

>>> jertl.match("'a string'", 'a string') is not None
Traceback (most recent call last):
...
jertlParseError: line 1: 0 token recognition error at: '''


Variables
^^^^^^^^^

In a matching context unbound variables match whatever data is in the current focus

>>> jertl.match('x', True).bindings
{'x': True}

Once a variable is bound it must match to the same value wherever the variable occurs in the pattern

>>> jertl.match('[x, x]', [False, False]).bindings
{'x': False}

if not the match fails

>>> jertl.match('[x, x]', [4, 4.0]).bindings
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'NoneType' object has no attribute 'bindings'

In a fill context unbound variables are not allowed.

>>> jertl.fill('[x]')
Traceback (most recent call last):
...
jertlFillException: x not bound

Anonymous variables are indicated using an underscore '_'.
Like regular variables these match anything but do not result in a binding.
When used multiple times in a pattern they do not have to match to the same value.

>>> jertl.match('[_, _, _]', [1, 2, 3]).bindings
{}

Structures
^^^^^^^^^^

Arrays
......

Arrays are represented by a comma seperated list of expressions surrounded by brackets.
Each expression must match its corresponding item in the data being matched.

>>> jertl.match('[1, 2.0, true, null, "string"]', [1, 2.0, True, None, 'string']) is not None
True

Splat expressions indicate a variable to be bound to a slice of the list being matched.
These can only occur within a list expression

>>> jertl.match('[*before, 3, *after]', [1, 2, 3, 4]).bindings
{'before': [1, 2], 'after': [4]}

As with non-splatted variables, once it is bound it must match to the same value
wherever it occurs in the pattern

>>> jertl.match('[*x, y, *x]', [1,2,3,4,1,2,3]).bindings
{'x': [1, 2, 3], 'y': 4}

The splatted variable does not need to be splatted each time

>>> jertl.match('[*x, x]', [1,2,3,[1,2,3]]).bindings
{'x': [1, 2, 3]}

Patterns containing splatted variables can result in multiple matches.

>>> for match in jertl.match_all('[*before, x, *after]', [1, 2, 3, 4]):
...     print(match.bindings)
...
{'before': [], 'x': 1, 'after': [2, 3, 4]}
{'before': [1], 'x': 2, 'after': [3, 4]}
{'before': [1, 2], 'x': 3, 'after': [4]}
{'before': [1, 2, 3], 'x': 4, 'after': []}

Anonymous variables may also be splatted.

>>> for match in jertl.match_all('[*_, x, *_]', [1, 2, 3, 4]):
...     print(match.bindings)
...
{'x': 1}
{'x': 2}
{'x': 3}
{'x': 4}

Objects
.......

The syntax of objects is a superset of that of JSON.
Key/value pairs are seperated by colons.
Pairs are surrounded by curly braces "{}"
Names *must* be a string literal.
Values can be any expression.
In addition the last item in an object pattern can be a double splatted variable ("\*\*variable").

>>> jertl.match('{"integer": 1, "boolean": true, "anything": anything, "list": [*list]}',
...            {'integer': 1, 'boolean': True, 'anything': {'inner': 'object'}, 'list': ['a', 'list']}).bindings
{'anything': {'inner': 'object'}, 'list': ['a', 'list']}

Double splat variables are bound to whatever key/value patterns which were not tested by the structure pattern.

>>> jertl.match('{"x": x, "y": y, **double_splat}',
...            {'x': 1, 'y': 2, 'z': 3, 'name': 'Harry'}).bindings
{'x': 1, 'y': 2, 'double_splat': {'z': 3, 'name': 'Harry'}}

Once a double splatted is bound it must match to the same value wherever it occurs in the pattern

>>> jertl.match('[{"x": x, **double_splat}, {"y": y, **double_splat}]',
...            [{'x': 1, 'z': 3, 'name': 'Harry'}, {'y': 2, 'z': 3, 'name': 'Harry'}]).bindings
{'x': 1, 'double_splat': {'z': 3, 'name': 'Harry'}, 'y': 2}

Anonymous variables may be double splatted but this doesn't do anything useful.

Operations
^^^^^^^^^^

Simple transforms
.................

The pattern for simple transforms is two structure patterns one each side of the IMPLICATION token

.. code-block::

    <structure> --> <structure>

For example

.. code-block::

    '{"name": name, "status": "employed"} --> {"name": name, "status": "retired"}'


Targeted matches
................

Conjoins and rules, which can match to multiple data structure, explicitly identify which structure to use.
The targeted match pattern specifies the variable which is bound to the data to be examined

.. code-block::

    <variable> ~ <structure>

For example

.. code-block::

     'employee ~ {"name": name, "status": "employed"}'

The variable, in this case ``employee``, *must* be bound.

Targeted fills
..............

Similarly, rules can perform multiple fill operations.
The targeted fill pattern specifies the variable which is to bound to filled structure.

.. code-block::

    <variable> := <structure>

For example

.. code-block::

     'retiree :- {"name": name, "status": "retired"}'

The variable, in this case ``retiree``, *must not* be bound.

Collations
..........

The syntax for collations are a sequence of targeted matches seperated by whitespace

.. code-block::

    supervisor ~ {"underlings": [*_, name, *_]}
    employee   ~ {"name": name}

Rules
.....

rule are a sequence of targeted matches seperated by whitespace followed by IMPLIES,
then a sequence of targetted fills seperated by whitespace

.. code-block::

    movies       ~ [*_, {"title": title, "MPAA rating": rating},        *_]
    MPAA_ratings ~ [*_, {"rating": rating, "explanation": explanation}, *_]
   -->
    movie       := {"title": title, "contents": explanation}


Comments
^^^^^^^^

Everything following a double slash ('//') is ignored.
