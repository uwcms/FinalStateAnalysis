import ROOT
from pdb import set_trace
import array
import warnings

#warnings.simplefilter('ignore', DeprecationWarning)

def invert_case(letter):
    if letter.upper() == letter: #capital
        return letter.lower()
    else: #low case
        return letter.upper()

class PyTree(ROOT.TObject):
    '''Wrapper to fill ROOT Trees easily'''
    def __init__(self, name, title, branches):
        '''__init__(self, name, title, branches): 
        branches is a semicolon separated string 
        with branchname/type'''
        branch_names = branches.split(':')
        self.tree = ROOT.TTree(name, title)
        
        self.holders = [] #dict([(i.split) for i in branch_names])
        for name in branch_names:
            try:
                varname, vartype = tuple(name.split('/'))
            except:
                raise ValueError('Problem parsing %s' % name)
            inverted_type = invert_case(vartype)
            self.holders.append( (varname, array.array(inverted_type,[0]) ) )

        #just to make sure that python does not mess up with addresses while loading a list
        for name, varinfo in zip(branch_names, self.holders):
            varname, holder = varinfo
            self.tree.Branch(varname, holder, name)

    def InheritsFrom(self, ciccio):
        return False
    
    def Fill(self, to_fill):
        '''Fills the tree, accepts an iterable or an object 
        with attributes as the branch names'''
        #set_trace()
        if isinstance(to_fill, (tuple, list)):
            if len(to_fill) <> len(self.holders):
                raise ValueError('Not enough/ Too many values to fill!')
            for val_to_fill, holder_tuple in zip(to_fill, self.holders):
                try:
                    holder_tuple[1][0] = val_to_fill
                except OverflowError as e:
                    print "OverflowError detected! %s. Variable %s was fed with %s. It will be set to 0" % (e, holder_tuple[0], val_to_fill)
                    holder_tuple[1][0] = 0
        else:
            for varname, holder in self.holders:
                try:
                    holder[0] = getattr(to_fill, varname)
                except OverflowError as e:
                    print "OverflowError detected! %s. Variable %s was fed with %s. It will be set to 0" % (e, varname, getattr(to_fill, varname))
                    holder[0] = 0
            
        self.tree.Fill()

    def Write(self):
        self.tree.Write()
