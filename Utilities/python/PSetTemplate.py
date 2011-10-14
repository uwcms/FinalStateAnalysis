import FWCore.ParameterSet.Config as cms
import string

def _replace_all(pset, **replacements):
    for param_name in pset.parameterNames_():
        param = pset.getParameter(param_name)
        if isinstance(param, cms.PSet):
            _replace_all(param, **replacements)
        elif isinstance(param, cms.vstring):
            updated = cms.vstring()
            if not param.isTracked():
                updated = cms.untracked.vstring()
            for item in param:
                template = string.Template(item)
                updated.append(template.substitute(**replacements))
            param = updated
            setattr(pset, param_name, param)
        elif isinstance(param, cms.string):
            template = string.Template(param.value())
            replaced = template.substitute(**replacements)
            if param.isTracked():
                param = cms.string(replaced)
            else:
                param = cms.untracked.string(replaced)
            setattr(pset, param_name, param)
        elif isinstance(param, cms.VPSet):
            for subpset in param:
                _replace_all(subpset, **replacements)

class PSetTemplate(object):
    ''' Wrapper around a cms.PSet that does string based replacements.

    >>> pset = cms.PSet(
    ...   acut = cms.untracked.string('${acut}'),
    ...   subPSet = cms.PSet(
    ...       subcut = cms.string('${subcut}'),
    ...       notaffected = cms.double(0.6),
    ...       subcuts = cms.vstring('not_changed', '$doot'),
    ...   ),
    ...   subVPSet = cms.VPSet(cms.PSet(subcut = cms.string('${subcut}')),
    ...                        cms.PSet(subcut2 = cms.string('${subcut}'))),
    ... )
    >>> template = PSetTemplate(pset)
    >>> replaced = template.replace(
    ...      subcut='subcutrep', doot='dootrep', acut='hi')
    >>> replaced.acut
    cms.untracked.string('hi')
    >>> # Sub-Psets are also replaced
    >>> replaced.subPSet.subcut
    cms.string('subcutrep')
    >>> # As are vstrings
    >>> replaced.subPSet.subcuts[1]
    'dootrep'
    >>> replaced.subPSet.subcuts[0]
    'not_changed'
    >>> replaced.subVPSet[0].subcut
    cms.string('subcutrep')
    >>> # The original PSet is unaffected.
    >>> pset.acut
    cms.untracked.string('${acut}')
    >>> # You must replace all the strings
    >>> try:
    ...    missing_key = template.replace(doot='dootrep', acut='hi')
    ... except KeyError as err:
    ...    print err
    "The PSetTemplate::replace was not passed the required key 'subcut'"

    '''
    def __init__(self, *psets, **kwargs):
        # Build it the normal way
        self.pset = cms.PSet(*psets, **kwargs)

    def clone(self, *args, **kwargs):
        return PSetTemplate(self.pset.clone(*args, **kwargs))

    def replace(self, **kwargs):
        output = self.pset.clone()
        try:
            _replace_all(output, **kwargs)
        except KeyError as err:
            raise KeyError("The PSetTemplate::replace was not passed"
                           " the required key %s" % err)
        return output

if __name__ == "__main__":
    import doctest
    doctest.testmod()

