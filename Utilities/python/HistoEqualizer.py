
class HistoEqualizer(object):
    def __init__(self, from_histo, to_histo):
        self.from_histo = from_histo
        self.to_histo = to_histo
        self.from_cdf, self.from_cdf_inverted =  from_histo.cdf(
            include_overflows=True, include_inverse=True, smooth=True)
        self.to_cdf, self.to_cdf_inverted =  to_histo.cdf(
            include_overflows=True, include_inverse=True, smooth=True)

    def __call__(self, x):
        from_y = self.from_cdf(x)
        to_x = self.to_cdf_inverted(from_y)
        return to_x
