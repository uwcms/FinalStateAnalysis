'''

Generate the statements for the PATQuadLepton forward file

'''

for n_elec in reversed(range(5)):
   for n_muon in reversed(range(5 - n_elec)):
       n_tau = 4 - (n_muon + n_elec)
       type = 'typedef PATQuadFinalStateT<'
       type += ", ".join( ['pat::Electron']*n_elec +
                         ['pat::Muon']*n_muon +
                         ['pat::Tau']*n_tau )
       type += '> '
       name = 'PAT' + ''.join(['Elec']*n_elec +
                              ['Mu']*n_muon +
                              ['Tau']*n_tau ) + 'FinalState'
       type += name
       type += ';\n'
       type += 'FWD_TYPEDEFS(' + name + ')\n'
       print type,
