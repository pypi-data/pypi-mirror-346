import sys
from lark import Lark

from pddl.helpers.base import call_parser
from pddl.parser.domain import DomainTransformer
from pddl.parser.problem import ProblemTransformer
from pddl.formatter import domain_to_string, problem_to_string


from lark.visitors import Transformer, merge_transformers

from pddl.parser import PARSERS_DIRECTORY as IMPORT_PARSERS_DIRECTORY


DOMPROB_GRAMMAR = r"""
    start: [domain_start] [problem_start]


    %ignore /\s+/
    %ignore COMMENT

    %import .domain.start -> domain_start
    %import .problem.start -> problem_start

    %import common.COMMENT -> COMMENT
    %import common.WS -> WS

"""

class DomainProblemTransformer(Transformer):
    """A transformer for domain + problems"""

    # def __init__(self, *args, **kwargs):
    #     """Initialize the domain transformer."""
    #     super().__init__(*args, **kwargs)

    def start(self, children):
        return children

    def domain_start(self, children):
        return children[0]

    def problem_start(self, children):
        return children[0]


class DomProbParser:
    """Domain and/or problem PDDL domain parser class."""

    def __init__(self):
        """Initialize."""
        self._transformer = merge_transformers(
            DomainProblemTransformer(),
            domain=DomainTransformer(),
            problem=ProblemTransformer(),
        )
        # need to use earley; lalr will not be able to recognise files with just problems (no left)
        # self._parser = Lark.open(DOMPROB_GRAMMAR_FILE, rel_to=__file__)
        self._parser = Lark(
            DOMPROB_GRAMMAR, parser="earley", import_paths=[IMPORT_PARSERS_DIRECTORY]
        )

    def __call__(self, text):
        """Call the object as a function
        Will return the object representing the parsed text/file which is an object
        of class pddl_parser.app_problem.APPProblem

        The call_parser() function is part of pddl package: will build a Tree from text and then an object pddl_parser.app_problem.APPProblem from the Tree
        """
        return call_parser(text, self._parser, self._transformer)

if __name__ == "__main__":
    # we can use this for quick testing/debugging
    file = sys.argv[1]
    with open(file, "r") as f:
        ptext = f.read()

    domain, problem = DomProbParser()(ptext)
    if domain:
        domprob = print(domain_to_string(domain))
    if problem:
        domprob = print(problem_to_string(problem))
