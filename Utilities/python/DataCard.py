import functools
import operator

class DataCardChannel(object):
    def __init__(self, name, file):
        self.name = name
        self.signal_name = None
        self.samples = set([])
        self.systematics = {}
        self.dir = file.Get(self.name)

    def get_rate(self, name):
        return self.dir.Get(name).Integral()

    def add_signal(self, name):
        self.signal_name = name
        self.samples.add((0, name))

    def add_background(self, name):
        max_added = max(idx for idx, sample in self.samples)
        self.samples.add((max_added + 1, name))

    def obs_data(self):
        return self.dir.Get('data_obs').Integral()

    def add_sys(self, name, value, sample):
        sys_dict = self.systematics.setdefault(name, {})
        if isinstance(sample, basestring):
            sys_dict[sample] = value
        else:
            for sample_item in sample:
                sys_dict[sample_item] = value


    def get_process_columns(self, systematics):
        for idx, sample in self.samples:
            bin_name = self.name
            process_name = sample
            process_code = idx
            rate = self.get_rate(sample)
            output = [bin_name, process_name, process_code, rate]
            for sys in systematics:
                value = '-'
                affected_samples = self.systematics.get(sys)
                if affected_samples:
                    if sample in affected_samples:
                        value = '%0.2f' % (affected_samples[sample])
                output.append(value)
            yield output

class DataCard(object):
    def __init__(self, name, description, channels, shape_file):
        self.name = name
        self.description = description
        self.channels = channels
        self.shape_file = shape_file

    def n_bins(self):
        return len(self.channels)

    def nuisances(self):
        all_systematics = set([])
        for channel in self.channels:
            for sys in channel.systematics.keys():
                all_systematics.add(sys)
        return all_systematics

    def write(self, stream):
        stream.write("# " + self.name + '\n')
        stream.write("# " + self.description + '\n')
        stream.write("imax %i\n" % self.n_bins())
        #stream.write("jmax %i\n" % self.n_backgrounds())
        stream.write("jmax *\n")
        #stream.write("kmax %i\n" % len(self.nuisances()))
        stream.write("kmax *\n")
        stream.write('------------\n')
        stream.write(
            "shapes * * %s $CHANNEL/$PROCESS $CHANNEL/$PROCESS_$SYSTEMATIC\n" %
            self.shape_file)

        obs_bin_names = []
        obs_bin_data = []
        for channel in self.channels:
            obs_bin_names.append(channel.name)
            obs_bin_data.append(channel.obs_data())

        stream.write('bin ' + ' '.join('%s' % x for x in obs_bin_names))
        stream.write('\n')
        stream.write('observation ' + ' '.join('%s' % x for x in obs_bin_data))
        stream.write('\n')
        stream.write('------------\n')

        columns = []

        row_labels = [
            'bin',
            'process',
            'process',
            'rate',
        ]
        nuisances = self.nuisances()
        row_labels.extend(nuisances)
        columns.append(row_labels)

        # A column giving the type of systematics.  We have to skip the first
        # few rows
        sys_type_labels = [ '', '', '', '', ]
        sys_type_labels.extend('lnN' for x in nuisances)
        columns.append(sys_type_labels)

        # Add data
        print nuisances
        for channel in self.channels:
            columns.extend(channel.get_process_columns(nuisances))

        # Write the columns
        for irow in xrange(len(row_labels)):
            for column in columns:
                #print column
                stream.write('  ' + '%s' % column[irow])
            stream.write('\n')

