# jertl - A minimally viable Python package for processing structured data

Where developers declaratively define and execute common operations on complex data structures.

Operations are specified using a mini-language in which target structures are visually similar to their textual representation.

## Examples

### Matching

```python
>>> movie = {"title": "Pinocchio", "MPAA rating": "PG"}
>>>
>>> match = jertl.match('{"title": title, "MPAA rating": "PG"}', movie)
>>>
>>> if match is not None:
...     print(match.bindings['title'])
...
Pinocchio
```

### Filling

```python
>>> jertl.fill('{"name": name, "age": age, "status": status}',
...            name="Ray",
...            age=66,
...            status='employed')
{'name': 'Ray', 'age': 66, 'status': 'employed'}
```

### Transforming

```python
>>> ray = {'name': 'Ray', 'age': 66, 'status': 'employed'}
>>>
>>> retire = '{"status": "employed", **the_rest} --> {"status": "retired", **the_rest}'
>>>
>>> transformation = jertl.transform(retire, ray)
>>> transformation.filled
{'status': 'retired', 'name': 'Ray', 'age': 66}
```

### Collating

```python
>>> jeremy = {'name': 'Jeremy'}
>>> jeff   = {'name': 'Jeff', 'underlings': ['Jimmy', 'Johnny', 'Jeremy', 'Joe']}
>>>
>>> supervises = '''
...     supervisor ~ {"underlings": [*_, name, *_]}
...     employee   ~ {"name": name}
...     '''
>>>
>>> collation = jertl.collate(supervises, supervisor=jeff, employee=jeremy)
>>> collation is not None
True
```

### Inferring

```python
>>> rule = '''
...    //
...    // Create a list of movies with their ratings explained
...    //
...    movies       ~ [*_, {"title": title, "MPAA rating": rating},        *_]
...    MPAA_ratings ~ [*_, {"rating": rating, "explanation": explanation}, *_]
... -->
...    movie       := {"title": title, "contents": explanation}
...'''
...
>>> movies = [{'title': 'Toy Story',                          'MPAA rating': 'G'},
...           {'title': 'South Park: Bigger, Longer & Uncut', 'MPAA rating': 'NC-17'}]
...
>>> MPAA_ratings = [{'rating':      'G',
...                  'summary':     'GENERAL AUDIENCES',
...                  'explanation': 'Nothing to offend parents for viewing by children.'},
...                 {'rating':      'PG',
...                  'summary':     'PARENTAL GUIDANCE SUGGESTED',
...                  'explanation': 'May contain some material parents might not like for their young children'},
...                 {'rating':      'PG-13',
...                  'summary':     'PARENTS STRONGLY CAUTIONED',
...                  'explanation': 'Some material may be inappropriate for pre-teens.'},
...                 {'rating':      'R',
...                  'summary':     'RESTRICTED',
...                  'explanation': 'Contains some adult material.'},
...                 {'rating':      'NC-17',
...                  'summary':     'NO ONE 17 AND UNDER ADMITTED',
...                  'explanation': 'Clearly for adults only.'}]
...
>>> for inference in jertl.infer_all(rule, movies=movies, MPAA_ratings=MPAA_ratings):
...     print(inference.fills['movie'])
...
{'title': 'Toy Story', 'contents': 'Nothing to offend parents for viewing by children.'}
{'title': 'South Park: Bigger, Longer & Uncut', 'contents': 'Clearly for adults only.'}
```

## Installation

```bash
pip install jertl
```

## License

`jertl` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.
