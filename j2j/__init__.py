# SPDX-FileCopyrightText: 2022-present RaymondPelletier <68929475+RaymondPelletier@users.noreply.github.com>
# SPDX-License-Identifier: Apache-2.0

from .processors import Matcher, Filler, Transformer, Collator, Rule

def match(structure, data):
    """Matches a structure to data.

    Args:
        structure (str): A pattern defining the structure to compare to
            data.
        data ((Sequence | Mapping | Number)): Python data to compare
            structure against

    Returns:
        Optional(Match): A description of match
    """
    return Matcher(structure).match(data)

def match_all(structure, data):
    """Generate all Matches of a structure to data.

    Args:
        structure (str): A pattern defining the structure to compare to
            the target data.
        data ((Sequence | Mapping | Number)): Python data to match
    :yield: All possible matches

    Returns:
        generator (of Match)
    """
    yield from Matcher(structure).match_all(data)

def compile_match(structure):
    """Compiles a structure pattern for later use.

    Args:
        structure (str): A pattern defining the structure to compare to
            the target data.

    Returns:
        Matcher: An object which can be used to match template to
        objects
    """
    return Matcher(structure)

def fill(structure, **bindings):
    """Populate a structure.

    Args:
        structure (str): A pattern defining the structure to compare to
            the target data.
        **bindings (KWARgs): values for free variables referenced by
            template

    Returns:
        Dict | Sequence | Number: A filled template
    """
    return Filler(structure).fill(**bindings)

def compile_fill(structure):
    """Compiles a structure for later filling.

    Args:
        structure (str): A pattern defining the structure to compare to
            the target data.

    Returns:
        Filler: A filler
    """
    return Filler(structure)

def transform(transform, data):
    """Matches a structure to data and fills a target structure.

    Args:
        transform (str): A pattern describing structures for matching
            and filling.
        data (Dict | Sequence | Number): Data to match against.

    Returns:
        Optional(Transformation):: A Transformation
    """
    return Transformer(transform).transform(data)

def transform_all(transform, data):
    """Generate all Transforms of data given Transformation specification.

    Args:
        transform (str): A pattern describing structures for matching
            and filling.
        data (KwArgs): Data to match against.
    :yield: All possible transforms of the sources

    Returns:
        generator (of Transformation)
    """
    yield from Transformer(transform).transform_all(data)

def compile_transform(transform):
    """Compiles a transform pattern for later reuse.

    Args:
        transform (str): Pattern describing a transform.

    Returns:
        Transformer: A transformer
    """
    return Transformer(transform)


def collate(collation, **bindings):
    """Match all matchers to targets

    Args:
        collation (str): Specification of collation.
        sources (KwArgs): Data to match against.

    Returns:
        Optional(Collation): A Collation
    """
    return Collator(collation).collate(**bindings)

def collate_all(collation, **sources):
    """Yields all matches to targets

    Args:
        collation (str): Specification of collation.
        **sources (KwArgs): Data to match against.
    :yield:          All possible collations:

    Returns:
        generator (of Collation):
    """
    yield from Collator(collation).collate_all(**sources)

def compile_collate(collation):
    """Compiles a template for later reuse.

    Args:
        collation (str): Specification of collation.
        sources (KwArgs): Data to match against.

    Returns:
        Collator: A collator
    """
    return Collator(collation)

def infer(rule, **sources):
    """Applies a production rule agains sources and generates new data according to output structures

    Args:
        rule (str): Pattern describing a production rule.
        **sources (KwArgs): Data to match against.

    Returns:
        Optional(Inference): An inference
    """
    return Rule(rule).infer(**sources)

def infer_all(rule, **sources):
    """Generate all application of rule.

    Args:
        rule (str): Pattern describing a production rule.
        **sources (KwArgs): Data to match against.
    :yield: All possible inferences

    Returns:
        generator of Inferences
    """
    yield from Rule(rule).infer_all(**sources)

def compile_rule(rule):
    """Compiles a inference rule for later reuse.

    Args:
        rule (str): Pattern describing a production rule.

    Returns:
        Rule: A rule
    """
    return Rule(rule)

__all__ = ['match',     'match_all',     'compile_match', 
           'fill',                       'compile_fill',
           'transform', 'transform_all', 'compile_transform',
           'collate',   'collate_all',   'compile_collate',
           'infer',     'infer_all',     'compile_rule']