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

>>> fake_tree.elecId = 10 #(0b1010)
>>> fourth_bit = tree.elecId.bit(4)
>>> second_bit = tree.elecId.bit(2)
>>> first_bit = tree.elecId.bit(1)
>>> second_bit(fake_tree)
2
>>> first_bit(fake_tree)
0
>>> fourth_bit(fake_tree)
8

Applying absolute value:

>>> fake_tree.negativeNumber = -50
>>> absolute_cut = abs(tree.negativeNumber) > 30
>>> absolute_cut(fake_tree)
True
>>> absolute_cut = abs(tree.negativeNumber) < -30
>>> absolute_cut(fake_tree)
False

Adding and subtracting:

>>> fake_tree.elecId
10
>>> plussed_cut = tree.elecId + 6 > 15
>>> plussed_cut(fake_tree)
True
>>> plussed_cut = tree.elecId + 4 > 15
>>> plussed_cut(fake_tree)
False
>>> minused_cut = tree.elecId - 6 > 3
>>> minused_cut(fake_tree)
True
>>> minused_cut = tree.elecId - 6 > 5
>>> minused_cut(fake_tree)
False

Iterating over selections
-------------------------

And(...) selections support iteration over the subselections.
Nested And(...) selections are expanded.

>>> cut_1 = tree.muPt < 30
>>> cut_2a = tree.muPt > 10
>>> cut_2b = tree.elecPt > 10
>>> cut_3 = tree.elecPt < 20
>>> anded_cut = And(cut_1, And(cut_2a, cut_2b), cut_3)

Note that cuts 2a and 2b are nested in a sub-And(...) object.

>>> for cut in anded_cut:
...     print cut
Branch('muPt') < 30
Branch('muPt') > 10
Branch('elecPt') > 10
Branch('elecPt') < 20

Explaining what happened
------------------------

You cane make a cut "explain" itself.

>>> cut_2a.explain(fake_tree)
'[25.00 > 10.00]'
>>> fake_tree.elecPt = 50
>>> anded_cut.explain(fake_tree)
"[Branch('elecPt') < 20 failed]"

Branch Bookkeeping
------------------

The MetaTree object also keeps track of which branches are accessed:

>>> tree.active_branches()
['elecId', 'elecPt', 'muPt', 'negativeNumber']

'''


import operator

class Selection(object):
    def __init__(self, selection, repr="Selection"):
        self.functor = selection
        self.repr = repr
        self.last_result = None
        self.last_entry = None

    def __call__(self, x):
        return self.functor(x)

    def cached_select(self, tree, entry):
        ''' Same as call, but caches the result from the last entry '''
        if entry == self.last_entry:
            return self.last_result
        else:
            result = self(tree)
            self.last_entry = entry
            self.last_result = result
            return result

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

    def explain(self, tree):
        ''' Explain what this cut does, given the TTree '''
        return "NotImplemented"

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

    def explain(self, tree):
        ''' Figure out which cut caused the And to fail '''
        passed = True
        first_to_fail = None
        for subselection in self:
            if not subselection(tree):
                first_to_fail = subselection
                passed = False
                break
        if passed:
            return "[PASSED]"
        return "[%s failed]" % first_to_fail

    def __iter__(self):
        ''' Iterator over selections.

        Subselections where are "ANDs" are expanded.
        '''
        for selection in self.selections:
            if isinstance(selection, And):
                for subselection in selection:
                    yield subselection
            else:
                yield selection

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
        self.getter1 = getter1
        self.getter2 = getter2
        self.op = op
        def functor(tree):
            return op(getter1(tree), getter2(tree))
        repr = "%s %s %s" % (val1, _operator_names[op], val2)
        super(TwoValueOp, self).__init__(functor, repr)

    def explain(self, tree):
        ''' Explain the result of this cut '''
        return "[%0.2f %s %0.2f]" % (
            self.getter1(tree), _operator_names[self.op], self.getter2(tree))


class OneValueOp(Selection):
    def __init__(self, val1, val2, op):
        getter = val1.getter
        self.getter = getter
        self.val = val2
        self.op = op
        def functor(tree):
            return op(getter(tree), val2)
        repr = "%s %s %s" % (val1, _operator_names[op], str(val2))
        super(OneValueOp, self).__init__(functor, repr)

    def explain(self, tree):
        ''' Explain the result of this cut '''
        return "[%0.2f %s %0.2f]" % (
            self.getter(tree), _operator_names[self.op], self.val)

class Value(object):
    ''' An object which can get a real value from a tree '''
    def __init__(self, getter, repr=""):
        # Initialize w/ functor to get value
        self.getter = getter
        self.repr = repr

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
        return Value(bit_getter, "%s.bit(%i)" % (repr(self), n))

    def __abs__(self):
        # Apply absolute value
        def abs_applyer(tree):
            return abs(self.getter(tree))
        return Value(abs_applyer, "|%s|" % repr(self))

    def __sub__(self, other):
        # Subtract some other value
        def subtractor_value(tree):
            return self.getter(tree) - other.getter(tree)
        # Used if the other value is just a plain type like a float
        def subtractor_plain(tree):
            return self.getter(tree) - other
        if isinstance(other, Value):
            return Value(subtractor_value,
                         "%s - %s" % (repr(self), repr(other)))
        else:
            return Value(subtractor_plain,
                         "%s - %s" % (repr(self), repr(other)))

    def __add__(self, other):
        # Subtract some other value
        def adder_value(tree):
            return self.getter(tree) + other.getter(tree)
        # Used if the other value is just a plain type like a float
        def adder_plain(tree):
            return self.getter(tree) + other
        if isinstance(other, Value):
            return Value(adder_value, "%s + %s" % (repr(self), repr(other)))
        else:
            return Value(adder_plain, "%s + %s" % (repr(self), repr(other)))

    def __call__(self, tree):
        return self.getter(tree)

    def __repr__(self):
        return self.repr

    def explain(self, tree):
        ''' Just print out the value of ourself '''
        return "[%s = %0.2f]" % (repr(self), self.getter(tree))

class Branch(Value):
    def __init__(self, branch):
        self.branch = branch
        def getter(tree):
            return getattr(tree, branch)
        super(Branch, self).__init__(getter, repr="Branch('%s')" % self.branch)

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
