'''

Generate the statements for the PATFiveLepton forward file

'''

for n_elec in reversed(range(6)):
    for n_muon in reversed(range(6 - n_elec)):
        for n_tau in reversed(range(6 - n_elec - n_muon)):
            # Don't make very unlikely final states
            n_pho = 5 - (n_muon + n_elec + n_tau)
            if n_pho > 2:
                continue
            if n_tau and n_pho:
                continue
            type = 'typedef PATFiveFinalStateT<'
            type += ", ".join(['pat::Electron'] * n_elec +
                              ['pat::Muon'] * n_muon +
                              ['pat::Tau'] * n_tau +
                              ['pat::Photon'] * n_pho)
            type += '> '
            name = 'PAT' + ''.join(['Elec'] * n_elec +
                                   ['Mu'] * n_muon +
                                   ['Tau'] * n_tau +
                                   ['Pho'] * n_pho) + 'FinalState'
            type += name
            type += ';\n'
            type += 'FWD_TYPEDEFS(' + name + ')\n'
            print type,
