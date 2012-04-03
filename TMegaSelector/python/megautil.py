'''

Tool for building tree selection functors using syntactic sugar.

Author: Evan K. Friis, UW Madison

MetaTree Object
===============

The MetaTree object can be used to construct arbitrary cuts strings.

>>> tree = MetaTree()
>>> tree.muPt
Branch('muPt')
>>> mu_cut = tree.muPt > 20.0

mu_cut is a function that takes a TTree as the argument

>>> print mu_cut
Branch('muPt') > 20.0


Make a fake tree:

>>> class Empty:
...    pass
>>> fake_tree = Empty()
>>> fake_tree.muPt = 25
>>> fake_tree.elecPt = 20

Creating selectors
------------------

>>> mu_cut(fake_tree)
True
>>> mu_cut = tree.muPt < 20
>>> mu_cut(fake_tree)
False

You can do two-branch operations:

>>> mu_is_harder = tree.muPt > tree.elecPt
>>> mu_is_harder(fake_tree)
True
>>> fake_tree.elecPt = 50
>>> mu_is_harder(fake_tree)
False

Combining Selectors
-------------------

You can OR, AND and NOT (using &, |, and ~) selectors:

>>> fake_tree.elecPt = 10
>>> mu_is_harder(fake_tree), mu_cut(fake_tree)
(True, False)
>>> anded_cut = mu_is_harder & mu_cut
>>> anded_cut(fake_tree)
False
>>> ored_cut = mu_is_harder | mu_cut
>>> ored_cut(fake_tree)
True
>>> mu_cut = tree.muPt < 30
>>> mu_is_harder(fake_tree), mu_cut(fake_tree)
(True, True)
>>> anded_cut = mu_is_harder & mu_cut
>>> anded_cut(fake_tree)
True
>>> nanded_cut = ~anded_cut
>>> nanded_cut(fake_tree)
False

For convenience, there are And and Or selectors which take a list:

>>> anded_cut = And(mu_is_harder, mu_cut)
>>> anded_cut(fake_tree)
True

Mathematical Operations
-----------------------

Extracting bit information:

>>> fake_tree.elecPt = 10 #(0b1010)
>>> fourth_bit = tree.elecPt.bit(4)
>>> second_bit = tree.elecPt.bit(2)
>>> first_bit = tree.elecPt.bit(1)
>>> second_bit(fake_tree)
2
>>> first_bit(fake_tree)
0
>>> fourth_bit(fake_tree)
8

Branch Bookkeeping
------------------

The MetaTree object also keeps track of which branches are accessed:

>>> tree.active_branches()
['elecPt', 'muPt']

'''


import operator

class Selection(object):
    def __init__(self, selection, repr="Selection"):
        self.functor = selection
        self.repr = repr

    def __call__(self, x):
        return self.functor(x)

    def __repr__(self):
        return self.repr

    def __str__(self):
        return self.repr

    def __and__(self, other):
        ''' Bitwise & operator - AND the cuts '''
        return And(self, other)

    def __or__(self, other):
        ''' Bitwise | operator - OR the cuts '''
        return Or(self, other)

    def __invert__(self):
        ''' Bitwise ~ operator - invert the cuts '''
        def invert_cut(tree):
            return not self(tree)
        return Selection(invert_cut, "!%s" % self)

class And(Selection):
    def __init__(self, *selections):
        self.selections = selections
        def functor(tree):
            for selection in selections:
                if not selection(tree):
                    return False
            return True
        super(And, self).__init__(functor, "AND[%s]" % ' '.join(
            [str(x) for x in selections]))

class Or(Selection):
    def __init__(self, *selections):
        def functor(tree):
            for selection in selections:
                if selection(tree):
                    return True
            return False
        super(Or, self).__init__(functor, "OR[%s]" % ' '.join(
            [str(x) for x in selections]))

_operator_names = {
    operator.lt : '<',
    operator.gt : '>',
    operator.ge : '>=',
    operator.le : '<=',
}

class TwoValueOp(Selection):
    def __init__(self, val1, val2, op):
        getter1 = val1.getter
        getter2 = val2.getter
        def functor(tree):
            return op(getter1(tree), getter2(tree))
        repr = "%s %s %s" % (val1, _operator_names[op], val2)
        super(TwoValueOp, self).__init__(functor, repr)

class OneValueOp(Selection):
    def __init__(self, val1, val2, op):
        getter = val1.getter
        def functor(tree):
            return op(getter(tree), val2)
        repr = "%s %s %s" % (val1, _operator_names[op], str(val2))
        super(OneValueOp, self).__init__(functor, repr)

class Value(object):
    ''' An object which can get a real value from a tree '''
    def __init__(self, getter):
        # Initialize w/ functor to get value
        self.getter = getter

    def handle_op(self, other, the_op):
        if isinstance(other, Value):
            return TwoValueOp(self, other, the_op)
        else:
            return OneValueOp(self, other, the_op)

    def __lt__(self, other):
        return self.handle_op(other, operator.lt)

    def __le__(self, other):
        return self.handle_op(other, operator.le)

    def __ge__(self, other):
        return self.handle_op(other, operator.ge)

    def __gt__(self, other):
        return self.handle_op(other, operator.gt)

    def bit(self, n):
        # Get the nth bit of the value
        def bit_getter(tree):
            value = int(self.getter(tree))
            return value & (1 << (n-1))
        return bit_getter

class Branch(Value):
    def __init__(self, branch):
        self.branch = branch
        def getter(tree):
            return getattr(tree, branch)
        super(Branch, self).__init__(getter)
    def __repr__(self):
        return "Branch('%s')" % self.branch

class MetaTree(object):
    def __init__(self):
        self.touched_branches = set([])

    def active_branches(self):
        return sorted(self.touched_branches)

    def __getattr__(self, attr):
        self.touched_branches.add(attr)
        return Branch(attr)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
