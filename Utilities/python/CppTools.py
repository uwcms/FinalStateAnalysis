'''

Defines tools for building C++ functions from python inputs.

These can then be loaded into ROOT as macros, and accessed from TTree::Draw

Run doctests by:
     python -m doctest CppTools.py

Author: Evan K. Friis, UW Madison

'''

class CppKinematicBinning(object):
    '''

    Defines a list of kinematic bins.  The __str__ method converts it to C++
    code implementing the kinematic selections and values.

    The class should be initialized by passing a list of a tuples, where each
    tuple corresponds to the constructor arguments of CppKinematicBin.

    Example:

    >>> bins = CppKinematicBinning([
    ...   ('eta', 0, 1.4, 6),
    ...   ('eta', 1.4, None, 7),
    ... ])
    >>> print str(bins)
    if (eta >= 0 && eta < 1.4) {
       return 6;
    }
    if (eta >= 1.4) {
       return 7;
    }
    <BLANKLINE>
    >>> # These can be nested.
    >>> bins = CppKinematicBinning([
    ...   ('eta', 0, 1.4, CppKinematicBinning([
    ...      ('pt', 0, 20, 6),
    ...      ('pt', 20, 60, 7)]))
    ... ])
    >>> print str(bins)
    if (eta >= 0 && eta < 1.4) {
       if (pt >= 0 && pt < 20) {
          return 6;
       }
       if (pt >= 20 && pt < 60) {
          return 7;
       }
    }
    <BLANKLINE>
    '''

    def __init__(self, bins, indent=0):
        self.bins = [CppKinematicBin(*bin) for bin in bins]
        self.indent = indent
    def __str__(self):
        if self.indent:
            for bin in self.bins:
                bin.indent = self.indent
        return ''.join(str(x) for x in self.bins)

class CppKinematicBin(object):
    '''

    Defines C++ code for a bin in some phase space.

    The __str__ method of this returns a C++ string that applies the appropriate
    selection and returns the correct value.

    The "greater than" is always inclusive.

    Example:

    >>> bin = CppKinematicBin('eta', 0, 1.4, 6)
    >>> print str(bin)
    if (eta >= 0 && eta < 1.4) {
       return 6;
    }
    <BLANKLINE>
    >>> # You can use open ended available
    >>> bin = CppKinematicBin('eta', None, 1.4, 6)
    >>> print str(bin)
    if (eta < 1.4) {
       return 6;
    }
    <BLANKLINE>
    >>> bin = CppKinematicBin('eta', 1.4, None, 6)
    >>> print str(bin)
    if (eta >= 1.4) {
       return 6;
    }
    <BLANKLINE>
    '''

    tab = '   '
    def __init__(self, label, min, max, value, indent=0):
        self.label = label
        self.min = min
        self.max = max
        self.indent = indent
        self.val = value
        # If the value is a simple type, make it say "return X"
        if isinstance(self.val, int) or isinstance(self.val, float) or \
           isinstance(self.val, basestring):
            self.val = 'return %s;\n' % str(self.val)

    def __str__(self):
        # Figure out conditional
        indent_str = self.tab*self.indent
        output = indent_str
        if self.min is None:
            output += 'if ({label} < {max}) {{\n'.format(
                label=self.label, max=self.max)
        elif self.max is None:
            output += 'if ({label} >= {min}) {{\n'.format(
                label=self.label, min=self.min)
        else:
            output += 'if ({label} >= {min} && {label} < {max}) {{\n'.format(
                label=self.label, min=self.min, max=self.max)
        # Add the meat
        if hasattr(self.val, 'indent'):
            self.val.indent = self.indent + 1
        # Add an extra indent if necessary
        if isinstance(self.val, int) or isinstance(self.val, float) or \
           isinstance(self.val, str):
            output += indent_str + self.tab
        output += str(self.val)
        output += indent_str + '}\n'
        return output

class CppFunctionWrapper(object):
    '''

    Wrap a string convertible object in a C++ functions

    Example:
    >>> func = CppFunctionWrapper('myFunc', '   return 999;\\n', 'eta', 'pt')
    >>> print str(func)
    float myFunc(float eta, float pt) {
       return 999;
    }
    <BLANKLINE>
    >>> # You can declare unused variables (to prevent compiler warnings) via:
    >>> func = CppFunctionWrapper('myFunc', '   return 999;\\n', 'eta', 'pt',
    ... unused=['pt'])
    >>> print str(func)
    float myFunc(float eta, float /*pt*/) {
       return 999;
    }
    <BLANKLINE>
    '''
    def __init__(self, name, meat, *vars, **kwargs):
        self.name = name
        self.meat = meat
        self.vars = vars
        self.default = kwargs.get('default')
        self.warn = kwargs.get('warn')
        if hasattr(self.meat, 'indent'):
            self.meat.indent = self.meat.indent + 1
        if 'unused' in kwargs:
            new_vars = []
            for var in self.vars:
                if var in kwargs['unused']:
                    new_vars.append('/*%s*/' % var)
                else:
                    new_vars.append(var)
            self.vars = new_vars

    def __str__(self):
        output = 'float %s(' % self.name
        output += ', '.join('float %s' % x for x in self.vars)
        output += ') {\n'
        output += str(self.meat)
        if self.warn is not None:
            output += CppKinematicBin.tab + self.warn.format(
                name = self.name
            )
        if self.default is not None:
            output += CppKinematicBin.tab + 'return %s;\n' % self.default
        output += '}\n'
        return output
