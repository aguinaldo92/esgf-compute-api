"""
Gridder Module.
"""

from cwt import parameter

class Gridder(parameter.Parameter):
    """ Gridder.
    
    Describes the regridder and target grid for an operation.

    Gridder from a known target grid.

    >>> Gridder('esmf', 'linear', 'T85')

    Gridder from a Domain.

    >>> new_grid = Domain([Dimension(90, -90, step=1)], name='lat')
    >>> Gridder('esmf', 'linear', new_grid)

    Gridder from a Variable.

    >>> tas = Variable('http://thredds/tas.nc', 'tas', name='tas')
    >>> Gridder('esmf', 'linear', tas)

    Attributes:
        tool: A String name of the regridding tool to be used.
        method: A String method that the regridding tool will use.
        grid: A String, Domain or Variable of the target grid.
    """
    def __init__(self, tool='esmf', method='linear', grid='T85'):
        """ Gridder Init. """
        super(Gridder, self).__init__('gridder')

        self._tool = tool
        self._method = method
        self.grid = grid

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @property
    def tool(self):
        """ Tool property. """
        return self._tool

    @property
    def method(self):
        """ Method property. """
        return self._method

    def parameterize(self):
        """ Parameterizes a gridder. """
        # Handle different types of grids
        # pylint: disable=no-member
        if isinstance(self.grid, str):
            grid = self.grid
        else:
            grid = self.grid.name

        return {
            'tool': self._tool,
            'method': self._method,
            'grid': grid,
        }

    def __repr__(self):
        return 'Gridder(tool=%r, method=%r, grid=%r)' % (
            self._tool,
            self._method,
            self.grid)

    def __str__(self):
        return 'tool=%s method=%s grid=%s' % (
            self._tool,
            self._method,
            self.grid)