import ROOT

def compare_shapes(sample_reader, region1, region2, variable, rebin=1):
    frame = variable.frame()
    cutType1, signType1 = region1
    #dataHist1 = sample_reader.dataHist(cutType1, signType1, variable)
    dataHist1 = sample_reader.histPdf(cutType1, signType1, variable, rebin)
    cutType2, signType2 = region2
    #dataHist2 = sample_reader.dataHist(cutType2, signType2, variable)
    dataHist2 = sample_reader.histPdf(cutType2, signType2, variable, rebin)

    dataHist1.plotOn(
        frame,
        ROOT.RooFit.LineColor(ROOT.EColor.kBlue),
    )
    dataHist2.plotOn(
        frame,
        ROOT.RooFit.LineColor(ROOT.EColor.kRed),
    )

    legend = ROOT.TLegend(0.65, 0.65, 0.85, 0.85)
    legend.AddEntry(frame.getObject(0),
                    sample_reader.name + " - " + " ".join(region1), "l")
    legend.AddEntry(frame.getObject(1),
                    sample_reader.name + " - " + " ".join(region2), "l")
    legend.SetFillStyle(0)

    to_keep = [legend, dataHist1, dataHist2]

    frame.addObject(legend)
    frame.GetYaxis().SetTitle("")
    frame.SetMaximum(frame.GetMaximum()*2)

    return frame, to_keep

def compare_samples(sample1, sample2, region1, region2, variable, rebin=1):
    frame = variable.frame()
    cutType1, signType1 = region1
    cutType2, signType2 = region2
    dataHist1 = sample1.histPdf(cutType1, signType1, variable, rebin)
    dataHist2 = sample2.histPdf(cutType2, signType2, variable, rebin)

    dataHist1.plotOn(
        frame,
        ROOT.RooFit.LineColor(ROOT.EColor.kBlue),
    )
    dataHist2.plotOn(
        frame,
        ROOT.RooFit.LineColor(ROOT.EColor.kRed),
    )

    legend = ROOT.TLegend(0.65, 0.65, 0.85, 0.85)
    legend.AddEntry(frame.getObject(0),
                    sample1.name + " - " + " ".join(region1), "l")
    legend.AddEntry(frame.getObject(1),
                    sample2.name + " - " + " ".join(region2), "l")
    legend.SetFillStyle(0)

    to_keep = [legend, dataHist1, dataHist2]

    frame.addObject(legend)
    frame.GetYaxis().SetTitle("")
    frame.SetMaximum(frame.GetMaximum()*2)

    return frame, to_keep

def compare_samples3(samples, region, variable, rebin=1):
    frame = variable.frame()
    legend = ROOT.TLegend(0.55, 0.55, 0.9, 0.9)
    to_keep = [legend]
    legend.SetFillStyle(0)

    good_colors = [ROOT.EColor.kBlack, ROOT.EColor.kBlue, ROOT.EColor.kRed]

    for i, (sample, color) in enumerate(zip(samples, good_colors)):
        print region
        cutType, signType = region
        dataHist = sample.histPdf(cutType, signType, variable, rebin)

        dataHist.plotOn(
            frame,
            ROOT.RooFit.LineColor(color),
        )

        legend.AddEntry(frame.getObject(i),
                        sample.name + " - " + " ".join(region), "l")
        to_keep.append(dataHist)


    frame.addObject(legend)
    frame.GetYaxis().SetTitle("")
    frame.SetMaximum(frame.GetMaximum()*2)

    return frame, to_keep
