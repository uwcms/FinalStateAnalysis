'''

Translates HiggsAnalysis.CombinedLimit.DatacardParser formatted output
into .txt datacard

Effectively a wrapper around

HiggsAnalysis/CombinedLimit/scripts/combineCards.py

Author: Evan K. Friis, UW

'''

def write_card(stream, *args, **kwargs):
    # Collect information about the cards
    obsline = []; obskeyline = [] ;
    keyline = []; expline = []; systlines = {}
    signals = []; backgrounds = []; shapeLines = []
    paramSysts = {}; flatParamNuisances = {}
    cmax = 5 # column width

    def write_ln(*args):
        # Write a single line to the output
        stream.write(' '.join(args) + '\n')

    # If we are running multiple input cards, give them nice names
    input_cards_and_labels = []
    for label, card in kwargs.iteritems():
        input_cards_and_labels.append((label, card))

    for ich, card in enumerate(args):
        label = "ch%d" % (ich+1)
        input_cards_and_labels.append((label, card))

    for label, DC in input_cards_and_labels:
        singlebin = (len(DC.bins) == 1)
        if not singlebin: label += "_";
        # expectations
        for b in DC.bins:
            bout = label if singlebin else label+b
            obskeyline.append(bout)
            for (p,e) in DC.exp[b].items(): # so that we get only self.DC.processes contributing to this bin
                expline.append("%.4f" % e)
                keyline.append((bout, p, DC.isSignal[p]))
        # systematics
        for (lsyst,nofloat,pdf,pdfargs,errline) in DC.systs:
            systeffect = {}
            if pdf == "param":
                if paramSysts.has_key(lsyst):
                   if paramSysts[lsyst] != pdfargs: raise RuntimeError, "Parameter uncerainty %s mismatch between cards." % lsyst
                else:
                    paramSysts[lsyst] = pdfargs
                continue
            for b in DC.bins:
                bout = label if singlebin else label+b
                if not systeffect.has_key(bout): systeffect[bout] = {}
                for p in DC.exp[b].keys(): # so that we get only self.DC.processes contributing to this bin
                    r = str(errline[b][p]);
                    if type(errline[b][p]) == list: r = "%.3f/%.3f" % (errline[b][p][0], errline[b][p][1])
                    elif type in ("lnN",'gmM'): r = "%.3f" % errline[b][p]
                    if errline[b][p] == 0: r = "-"
                    if len(r) > cmax: cmax = len(r) # get max col length, as it's more tricky do do it later with a map
                    systeffect[bout][p] = r
            if systlines.has_key(lsyst):
                (otherpdf, otherargs, othereffect, othernofloat) = systlines[lsyst]
                if otherpdf != pdf:
                    if (pdf == "lnN" and otherpdf.startswith("shape")):
                        if systlines[lsyst][0][-1] != '?': systlines[lsyst][0] += '?'
                        for b,v in systeffect.items(): othereffect[b] = v;
                    elif (pdf.startswith("shape") and otherpdf == "lnN"):
                        if pdf[-1] != '?': pdf += '?'
                        systlines[lsyst][0] = pdf
                        for b,v in systeffect.items(): othereffect[b] = v;
                    elif (pdf == "shape?" and otherpdf == "shape") or (pdf == "shape" and otherpdf == "shape?"):
                        systlines[lsyst][0] = "shape?"
                        for b,v in systeffect.items(): othereffect[b] = v;
                    else:
                        raise RuntimeError, "File %s defines systematic %s as using pdf %s, while a previous file defines it as using %s" % (fname,lsyst,pdf,otherpdf)
                else:
                    if pdf == "gmN" and int(pdfargs[0]) != int(otherargs[0]):
                        raise RuntimeError, "File %s defines systematic %s as using gamma with %s events in sideband, while a previous file has %s" % (fname,lsyst,pdfargs[0],otherargs[0])
                    for b,v in systeffect.items(): othereffect[b] = v;
            else:
                pdfargs = [ str(x) for x in pdfargs ]
                systlines[lsyst] = [pdf,pdfargs,systeffect,nofloat]
        # flat params
        for K in DC.flatParamNuisances.iterkeys():
            flatParamNuisances[K] = True
        # put shapes, if available
        if len(DC.shapeMap):
            for b in DC.bins:
                bout = label if singlebin else label+b
                p2sMap  = DC.shapeMap[b]   if DC.shapeMap.has_key(b)   else {}
                p2sMapD = DC.shapeMap['*'] if DC.shapeMap.has_key('*') else {}
                for p, x in p2sMap.items():
                    # FIXME
                    dirname = ''
                    xrep = [xi.replace("$CHANNEL",b) for xi in x]
                    if xrep[0] != 'FAKE' and dirname != '': xrep[0] = dirname+"/"+xrep[0]
                    shapeLines.append((p,bout,xrep))
                for p, x in p2sMapD.items():
                    if p2sMap.has_key(p): continue
                    xrep = [xi.replace("$CHANNEL",b) for xi in x]
                    if xrep[0] != 'FAKE' and dirname != '': xrep[0] = dirname+"/"+xrep[0]
                    shapeLines.append((p,bout,xrep))
        else: # always add fake shapes
            for b in DC.bins:
                bout = label if singlebin else label+b
                shapeLines.append(('*',bout,['FAKE']))
        # combine observations, but remove line if any of the datacards doesn't have it
        if len(DC.obs) == 0:
            obsline = None
        elif obsline != None:
            obsline += [str(DC.obs[b]) for b in DC.bins];

    bins = []
    for (b,p,s) in keyline:
        if b not in bins: bins.append(b)
        if s:
            if p not in signals: signals.append(p)
        else:
            if p not in backgrounds: backgrounds.append(p)

    #import pdb; pdb.set_trace()

    write_ln("cardwriter output")
    write_ln("imax %d number of bins" % len(bins))
    write_ln("jmax %d number of processes minus 1" % (len(signals) + len(backgrounds) - 1))
    write_ln("kmax %d number of nuisance parameters" % (len(systlines) + len(paramSysts)))
    write_ln("-" * 130)

    if shapeLines:
        chmax = max([max(len(p),len(c)) for p,c,x in shapeLines]);
        cfmt = "%-"+str(chmax)+"s ";
        for (process,channel,stuff) in shapeLines:
            write_ln("shapes", cfmt % process, cfmt % channel, ' '.join(stuff))
        write_ln("-" * 130)

    if obsline:
        cmax = max([cmax]+[len(l) for l in obskeyline]+[len(x) for x in obsline])
        cfmt = "%-"+str(cmax)+"s";
        write_ln("bin         ", "  ".join([cfmt % x for x in obskeyline]))
        write_ln("observation ", "  ".join([cfmt % x for x in obsline]))

    write_ln("-" * 130)

    pidline = []; signals = []; backgrounds = []
    for (b,p,s) in keyline:
        if s:
            if p not in signals: signals.append(p)
            pidline.append(-signals.index(p))
        else:
            if p not in backgrounds: backgrounds.append(p)
            pidline.append(1+backgrounds.index(p))
    cmax = max([cmax]+[max(len(p),len(b)) for p,b,s in keyline]+[len(e) for e in expline])
    hmax = max([10] + [len("%-12s[nofloat]  %s %s" % (l,p,a)) for l,(p,a,e,nf) in systlines.items()])
    cfmt  = "%-"+str(cmax)+"s"; hfmt = "%-"+str(hmax)+"s  ";
    write_ln(hfmt % "bin",     "  ".join([cfmt % p for p,b,s in keyline]))
    write_ln(hfmt % "process", "  ".join([cfmt % b for p,b,s in keyline]))
    write_ln(hfmt % "process", "  ".join([cfmt % x for x in pidline]))
    write_ln(hfmt % "rate",    "  ".join([cfmt % x for x in expline]))

    write_ln("-" * 130)

    sysnamesSorted = systlines.keys(); sysnamesSorted.sort()
    for name in sysnamesSorted:
        (pdf,pdfargs,effect,nofloat) = systlines[name]
        if nofloat: name += "[nofloat]"
        systline = []
        for b,p,s in keyline:
            try:
                systline.append(effect[b][p])
            except KeyError:
                systline.append("-");
        write_ln(hfmt % ("%-21s   %s  %s" % (name, pdf, " ".join(pdfargs))), "  ".join([cfmt % x for x in systline]))
    for (pname, pargs) in paramSysts.items():
        write_ln("%-12s  param  %s" %  (pname, " ".join(pargs)))

    for pname in flatParamNuisances.iterkeys():
        write_ln("%-12s  flatParam" % pname)
