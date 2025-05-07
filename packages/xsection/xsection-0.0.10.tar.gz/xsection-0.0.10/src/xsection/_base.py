

class Shape:
    """
    Base class for cross-section calculations.
    """

    def linspace(self, start, stop, num, radius=None, **kwds):
        """
        Create ``num`` copies of this section with centroids linearly aranged from ``start`` to ``stop``.
        """
        import numpy as np
        if radius is None:
            for x in np.linspace(start, stop, num=num):
                yield self.translate(x-self.centroid, **kwds)
