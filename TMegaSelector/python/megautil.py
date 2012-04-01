'''

Tool for building tree selection functors using syntactic sugar.

Author: Evan K. Friis, UW Madison

The MetaTree object can be used to construct arbitrary cuts strings.

>>> tree = MetaTree()
>>> tree.muPt
Branch('muPt')
>>> mu_cut = tree.muPt > 20.0

Cut is a function that takes a TTree as the argument

>>> print mu_cut
branch[muPt] > 20.0


Make a fake tree:

>>> class Empty:
...    pass
>>> fake_tree = Empty()
>>> fake_tree.muPt = 25
>>> fake_tree.elecPt = 20

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

You can OR, AND and NOT (using ~) selectors:

>>> fake_tree.elecPt = 10
>>> mu_is_harder(fake_tree), mu_cut(fake_tree)
(True, False)
>>> anded_cut = mu_is_harder and mu_cut
>>> anded_cut(fake_tree)
False
>>> ored_cut = mu_is_harder or mu_cut
>>> ored_cut(fake_tree)
True
>>> mu_cut = tree.muPt < 30
>>> mu_is_harder(fake_tree), mu_cut(fake_tree)
(True, True)
>>> anded_cut = mu_is_harder and mu_cut
>>> anded_cut(fake_tree)
True
>>> nanded_cut = ~anded_cut
>>> nanded_cut(fake_tree)
False

For convenience, there are And and Or selectors which take a list:

>>> anded_cut = And(mu_is_harder, mu_cut)
>>> anded_cut(fake_tree)
True

The MetaTree object also keeps track of which branches are accessed:

>>> tree.active_branches()
['elecPt', 'muPt']

'''


import operator

_operator_names = {
    operator.lt : '<',
    operator.gt : '>',
    operator.ge : '>=',
    operator.le : '<=',
}

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
        def both(tree):
            return self(tree) and other(tree)
        return Selection(both, "%s and %s" % (self, other))

    def __or__(self, other):
        def either(tree):
            return self(tree) or other(tree)
        return Selection(either, "%s or %s" % (self, other))

    def __invert__(self):
        def invert_cut(tree):
            return not self(tree)
        return Selection(invert_cut, "!%s" % self)

class And(Selection):
    def __init__(self, *selections):
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

class TwoBranchOp(Selection):
    def __init__(self, b1, b2, op):
        def functor(tree):
            return op(getattr(tree, b1), getattr(tree, b2))
        repr = "branch[%s] %s branch[%s]" % (b1, _operator_names[op], b2)
        super(TwoBranchOp, self).__init__(functor, repr)

class OneBranchOp(Selection):
    def __init__(self, b1, val, op):
        def functor(tree):
            return op(getattr(tree, b1), val)
        repr = "branch[%s] %s %s" % (b1, _operator_names[op], val)
        super(OneBranchOp, self).__init__(functor, repr)

class Branch(object):
    def __init__(self, branch):
        self.branch = branch

    def handle_op(self, other, the_op):
        if isinstance(other, Branch):
            return TwoBranchOp(self.branch, other.branch, the_op)
        else:
            return OneBranchOp(self.branch, other, the_op)

    def __lt__(self, other):
        return self.handle_op(other, operator.lt)

    def __le__(self, other):
        return self.handle_op(other, operator.le)

    def __ge__(self, other):
        return self.handle_op(other, operator.ge)

    def __gt__(self, other):
        return self.handle_op(other, operator.gt)

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
