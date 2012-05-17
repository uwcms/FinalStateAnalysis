from FinalStateAnalysis.MetaData.higgs_tables import cross_section_info

for mass in [170, 180, 190, 200]:
    info = cross_section_info('ZH', mass, 7)
    print "============================"
    print " m = %i " % mass
    print " pdf = %0.3f/%0.3f" % (1 + info['pdf-'], 1 + info['pdf+'])
    print " scale = %0.3f/%0.3f" % (1 + info['scale-'], 1 + info['scale+'])

