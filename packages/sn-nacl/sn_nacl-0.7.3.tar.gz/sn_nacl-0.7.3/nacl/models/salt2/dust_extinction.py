from dust_extinction.parameter_averages import CCM89, F04, F99, G16, G23


class DustExtinction:
    """
    A class that handles the different dust extinction laws
    """
    def __init__(self, Rv=3.1):
        """
        Initialising DustExtinction class
        """
        self.Rv = Rv

    def CCM89_dust(self):
        """
        Loads CCM89 (Cardelli, Clayton & Mathis (1989))
        """
        return CCM89(self.Rv)

    def F99_dust(self):
        """
        Loads F99 (Fitzpatrick (1999))
        """
        return F99(self.Rv)

    def F04_dust(self):
        """
        Loads F04 (Fitzpatrick (2004))
        """
        return F04(self.Rv)

    def G16_dust(self):
        """
        Loads G16 (Gordon et al. (2016))
        """
        return G16(self.Rv)

    def G23_dust(self):
        """
        Loads G23 (Gordon et al. (2023))
        """
        return G23(self.Rv)
