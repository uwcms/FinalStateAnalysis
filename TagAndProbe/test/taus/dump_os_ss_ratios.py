from templates import get_th1
from templates import data_name_map


regions = ['sig', 'qcd', 'wjets']
types = ['Pass', 'Fail']

for sample in data_name_map.keys():
    print ""
    for type in types:
        for region in regions:
            extras = ['']
            if 'zjets' in sample and 'sig' in region:
                extras = ['/realTau', '/fakeTau']
            for extra in extras:
                n_OS = get_th1(sample, region + type + 'OS' + extra, 'AbsTauEta').Integral()
                n_SS = get_th1(sample, region + type + 'SS' + extra, 'AbsTauEta').Integral()
                print " ".join([sample, "OS/SS in", region, type + extra, "%0.2f" % (n_OS/n_SS)])


def get_purity(sample, region, extra=''):
    target = get_th1(sample, region + extra, 'AbsTauEta').Integral()
    total = 0
    data = get_th1('data', region, 'AbsTauEta').Integral()
    for all_sample in data_name_map.keys():
        if 'data' in all_sample:
            continue
        total += get_th1(all_sample, region, 'AbsTauEta').Integral()

    print "%s purity in %s region is %0.2f, data: %0.0f, %s mc: %0.0f" % (
    sample, region, target/total, data, sample, target)

get_purity('qcd', 'qcdPassOS')
get_purity('qcd', 'qcdPassSS')
get_purity('qcd', 'qcdFailOS')
get_purity('qcd', 'qcdFailSS')

get_purity('wjets', 'wjetsPassOS')
get_purity('wjets', 'wjetsPassSS')
get_purity('wjets', 'wjetsFailOS')
get_purity('wjets', 'wjetsFailSS')

get_purity('zjets', 'sigPassSS', '/realTau')
