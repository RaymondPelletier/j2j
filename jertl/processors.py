import jertl.ast.emitter as jae
import jertl.ast.builder as jab

from jertl.engine.interpreter import Interpreter
from jertl.engine.construct   import construct

from jertl.results import Match, Transformation, Collation, Inference

class Matcher:
    """Class which compares data to a structure and returns all Matches"""
    def __init__(self, structure):
        """__init__ Constructor

        Args:
            structure (str): pattern describing structure to be looked
                for
        """
        self._ast          = jab.ast_for_string(structure, 'structure')
        self._instructions = list(jae.emit_match(self._ast))

    def match_all(self, data):
        """match_all Generate all Matches of a structure to data.

        Args:
            data ((Sequence | Mapping | Number)): Python data structure
                to examine
        :yield: All possible Matches

        Returns:
            Match
        """
        interpreter = Interpreter(self._instructions)
        for bindings in interpreter.match_all(data):
            yield Match(self._ast, bindings)

    def match(self, data):
        """match Matches a structure to data.

        Args:
            data (_type_): Python data structure to match

        Returns:
            Match: (Sequence | Mapping | Number)
        """
        for m in self.match_all(data):
            return m


class Filler:
    """Class which performs fills"""
    def __init__(self, structure):
        """__init__ Constructor

        Args:
            structure (str): String describing structure to be used for
                creating new data structures
        """
        self._ast = jab.ast_for_string(structure, 'structure')

    def fill(self, **bindings):
        """fill Fills structure and returns data with structure variables replaced with their bindings

        Args:
            **bindings (KWArgs): Initial variable bindings

        Returns:
            (list | dict | str | Number): data
        """
        return construct(self._ast, bindings)


class Transformer:
    """A transformer with compile structure"""
    def __init__(self, transform):
        """__init__ Compiles transform and returns object capable for performing them

        Args:
            transform (str): String describing a transform
        """
        self._ast = jab.ast_for_string(transform, 'transform')
        self._source = self._ast.input
        self._target = self._ast.output
        self._instructions = list(jae.emit_match(self._source))

    def transform_all(self, data):
        """transform_all finds all possible transforms of data

        Args:
            data ((list | dict | str | Number)): Data structure to be
                transformed
        :yield: All possible transformations

        Returns:
            Transformation
        """
        interpreter = Interpreter(self._instructions)
        for bindings in interpreter.match_all(data):
            yield Transformation(self._source, self._target, bindings)

    def transform(self, data):
        """transform Finds a transform of data

        Args:
            data ((list | dict | str | Number)): Data structure to be
                transformed

        Returns:
            (list | dict | str | Number): A Transformation if one was
            found
        """
        for m in self.transform_all(data):
            return m


class Collator:
    """Class which performs collations"""
    def __init__(self, collation):
        """__init__ Compiles collation

        Args:
            collation (str): pattern describing a collation
        """
        self._ast = jab.ast_for_string(collation, 'collation')
        self._toplevel = {m.variable.identifier for m in self._ast}
        self._instructions = list(jae.emit_collation(self._ast, self._toplevel))

    def collate_all(self, **bindings):
        """collate_all Yield all possible collations of data

        Args:
            **bindings (KWArgs): Initial variable bindings
        :yield: All collations

        Returns:
            Collation
        """
        interpreter = Interpreter(self._instructions)
        for bindings in interpreter.match_all(None, bindings):
            structures = {m.variable.identifier: m.structure for m in self._ast}
            yield Collation(structures, bindings)

    def collate(self, **bindings):
        """collate Find a collation if any

        Args:
            **bindings (KWArgs): Initial variable bindings

        Returns:
            Optional(Collation): the First Collation
        """
        for m in self.collate_all(**bindings):
            return m


class Rule:
    """Class which finds inferences of a production rule"""
    def __init__(self, rule):
        """__init__ Compile pattern describing an inference rule

        Args:
            rule (str): Pattern describing an inference rule
        """
        self._ast = jab.ast_for_string(rule, 'rule_')
        self._toplevel = {m.variable.identifier for m in self._ast.matchers}
        self._instructions = list(jae.emit_collation(self._ast.matchers, self._toplevel))

    def infer_all(self, **bindings):
        """infer_all Yield all possible inferences of rule applied to data

        Args:
            **bindings (KWArgs): Initial variable bindings
        :yield: _description_

        Returns:
            _type_
        """
        interpreter = Interpreter(self._instructions)
        for bindings in interpreter.match_all(None, bindings):
            inputs  = {m.variable.identifier: m.structure for m in self._ast.matchers}
            outputs = {a.variable.identifier: a.structure for a in self._ast.setters}
            yield Inference(inputs, outputs, bindings)

    def infer(self, **bindings):
        """infer Finds an inference of rule applied to data (if any)

        Args:
            **bindings (KWArgs): Initial variable bindings

        Returns:
            Optional(Inference): An inference
        """
        for m in self.infer_all(**bindings):
            return m


__all__ = ['Matcher', 'Filler', 'Transformer', 'Collator', 'Rule']
