# -*- coding: utf-8 -*-
"""
    test_filter
    ~~~~~~~~~~~

    Test the ``:filter:`` option.
"""
import ast
from unittest import TestCase
import unittest
import nose
from sphinxcontrib.bibtex.transforms import filter_parser, get_parsed_filter


class TestFilterParser(TestCase):
    """Stateless encoder tests."""

    def test_simple_filter(self):
        parsed_line = filter_parser(ast.parse('year==2010').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): (arg.fields.get("year") == "2010")')

    def test_comp_eq(self):
        parsed_line = filter_parser(ast.parse('year == 2010').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): (arg.fields.get("year") == "2010")')

    def test_comp_lt(self):
        parsed_line = filter_parser(ast.parse('year < 2010').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): (arg.fields.get("year") < "2010")')

    def test_comp_le(self):
        parsed_line = filter_parser(ast.parse('year <= 2010').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): (arg.fields.get("year") <= "2010")')

    def test_comp_ge(self):
        parsed_line = filter_parser(ast.parse('year >= 2010').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): (arg.fields.get("year") >= "2010")')

    def test_comp_gt(self):
        parsed_line = filter_parser(ast.parse('year > 2010').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): (arg.fields.get("year") > "2010")')

    def test_comp_ne(self):
        parsed_line = filter_parser(ast.parse('year != 2010').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): (arg.fields.get("year") != "2010")')

    def test_comp_not(self):
        parsed_line = filter_parser(ast.parse('not year != 2010').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): ( not (arg.fields.get("year") != "2010"))')

    def test_and(self):
        parsed_line = filter_parser(ast.parse('year < 2010 and year > 2000').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): ((arg.fields.get("year") < "2010") '
                         'and (arg.fields.get("year") > "2000"))')

    def test_or(self):
        parsed_line = filter_parser(ast.parse('year < 2010 or year > 2000').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): ((arg.fields.get("year") < "2010") '
                         'or (arg.fields.get("year") > "2000"))')

    def test_comparators(self):
        parsed_line = filter_parser(ast.parse('2000 < year < 2010').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): ("2000" < arg.fields.get("year") < "2010")')

    def test_attr(self):
        parsed_line = filter_parser(ast.parse('type == "journal"').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): (arg.type == """journal""")')

    def test_attr(self):
        parsed_line = filter_parser(ast.parse('author == "toto"').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): (arg.fields.get("author") == """toto""")')

    def test_re(self):
        parsed_line = filter_parser(ast.parse('author % ".*toto.*"').body[0])
        self.assertEqual(parsed_line, 'bibtex_filter = lambda(arg): (re.match(""".*toto.*""", '
                         'arg.fields.get("author")))')


class PseudoRef(object):
    def __init__(self, reftype, year):
        self.type = reftype
        self.fields = {'year': str(year)}


class TestFilter(TestCase):

    def test_lambda(self):
        fn = get_parsed_filter('year == 2010')
        obj = PseudoRef('journal', 2010)
        self.assertTrue(fn(obj))
        obj = PseudoRef('inproceedings', 2011)
        self.assertFalse(fn(obj))
        fn = get_parsed_filter('type == "journal"')
        self.assertFalse(fn(obj))
        obj = PseudoRef('journal', 2010)
        self.assertTrue(fn(obj))



if __name__ == '__main__':
    unittest.main()