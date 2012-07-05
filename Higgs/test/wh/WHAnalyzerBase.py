'''

Generic base class for WH leptonic analysis.

WH has three objects:
    obj1
    obj2
    obj3

Objects 1 & 2 must be SS in the signal region.   The OS region is kept as a
control.  The subclasses must define the following functions:

    self.preselection - includes loose preselection on objects
    slef.sign_cut - returns true for SS (signal), false for OS
    self.obj1_id(row)
    self.obj2_id(row)
    self.obj3_id(row)

    self.event_weight(row) - general corrections
    self.obj1_weight(row) - returns double
    self.obj2_weight(row)
    self.obj3_weight(row)

    self.book_histos(folder) # books histograms in a given folder (region)
    self.fill_histos(histos, row, weight) # fill histograms in a given region

The output histogram has the following structure:

    ss/
        p1p2p3/   - signal region
        == Type1 FRs ==
        p1p2f3/   - object 3 fails
            w3/   - with weight 3 applied
        ... same for 1 and 2
        == Type2 FRs ==
        f1f2p3/   - objects 1 & 2 fail
            w1w2/
        == Type3 FRs ==
        f1f2f3/   - everything fails
            w3/   - extrapolate triple fakes to type2 region

    os/           - OS control region

'''

from FinalStateAnalysis.PlotTools.MegaBase import MegaBase

class WHAnalyzerBase(MegaBase):
    def __init__(self, tree, outfile, wrapper, **kwargs):
        super(WHAnalyzerBase, self).__init__(tree, outfile, **kwargs)
        # Cython wrapper class must be passed
        self.tree = wrapper(tree)
        self.out = outfile
        self.histograms = {}

    @staticmethod
    def build_wh_folder_structure():
        # Build list of folders, and a mapping of
        # (sign, ob1, obj2, ...) => ('the/path', (weights))
        #folders = []
        flag_map = {}
        for sign in ['ss', 'os']:
            for failing_objs in [(), (1,), (2,), (3,), (1,2), (1,2,3)]:
                cut_key = [sign == 'ss']
                region_label = ''
                for i in range(1,4):
                    if i in failing_objs:
                        region_label += 'f' + str(i)
                        cut_key.append(False)
                    else:
                        region_label += 'p' + str(i)
                        cut_key.append(True)
                # Figure out which objects to weight for FR
                weights_to_apply = []
                # Single fake
                if len(failing_objs) == 1:
                    weights_to_apply.append(
                        (failing_objs, "w%i" % failing_objs))
                if len(failing_objs) == 2:
                    weights_to_apply.append(
                        (failing_objs, "w%i%i" % failing_objs))
                if len(failing_objs) == 3:
                    weights_to_apply.append( ((3,), "w3") )

                #folders_to_add = [ (sign, region_label) ]
                # Which objects to weight for each region
                weights_to_add = []
                for failing_objs, weight_to_apply in weights_to_apply:
                    #folders_to_add.append( (sign, region_label, weight_to_apply) )
                    weights_to_add.append(weight_to_apply)

                flag_map[tuple(cut_key)] = ((sign, region_label), tuple(weights_to_add))
                #folders.extend(folders_to_add)

        return flag_map

    def begin(self):
        # Loop over regions, book histograms
        for _, folders in self.build_wh_folder_structure().iteritems():
            base_folder, weight_folders = folders
            folder = "/".join(base_folder)
            self.book_histos(folder) # in subclass
            # Each of the weight subfolders
            for weight_folder in weight_folders:
                self.book_histos("/".join(base_folder + (weight_folder,)))

    def process(self):
        # For speed, map the result of the region cuts to a folder path
        # string using a dictionary
        # key = (sign, obj1, obj2, obj3)
        cut_region_map = self.build_wh_folder_structure()

        # Reduce number of self lookups and get the derived functions here
        histos = self.histograms
        preselection = self.preselection
        sign_cut = self.sign_cut
        obj1_id = self.obj1_id
        obj2_id = self.obj2_id
        obj3_id = self.obj3_id
        fill_histos = self.fill_histos

        weight_func = self.event_weight

        # Which weight folders correspond to which weight functions
        weight_map = {
            'w1' : (self.obj1_weight, ),
            'w2' : (self.obj2_weight, ),
            'w3' : (self.obj3_weight, ),
            'w12' : (self.obj1_weight, self.obj2_weight),
        }

        for row in self.tree:
            # Apply basic preselection
            if not preselection(row):
                continue

            # Get the generic event weight
            event_weight = weight_func(row)

            # Get the cuts that define the region
            sign_result = sign_cut(row)
            obj1_id_result = obj1_id(row)
            obj2_id_result = obj2_id(row)
            obj3_id_result = obj3_id(row)

            # Figure out which folder/region we are in
            region_result = cut_region_map.get(
                (sign_result, obj1_id_result, obj2_id_result, obj3_id_result))

            # Ignore stupid regions we don't care about
            if region_result is None:
                continue

            base_folder, weights = region_result

            # Fill the un-fr-weighted histograms
            fill_histos(histos, base_folder, row, event_weight)

            # Now loop over all necessary weighted regions and compute & fill
            for weight_folder in weights:
                # Compute product of all weights
                fr_weight = event_weight
                # Figure out which object weight functions to apply
                for subweight in weight_map[weight_folder]:
                    fr_weight *= subweight(row)

                # Now fill the histos for this weight folder
                fill_histos(histos, base_folder + (weight_folder,), row, fr_weight)

    def finish(self):
        self.write_histos()

if __name__ == "__main__":
    import pprint
    pprint.pprint(WHAnalyzerBase.build_wh_folder_structure())
