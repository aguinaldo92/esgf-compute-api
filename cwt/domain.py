"""
Domain Module.
"""

from cwt import dimension
from cwt import mask
from cwt import parameter

__all__ = ['Domain']

class Domain(parameter.Parameter):
    """ Domain.

    A domain consist of one or more dimensions. A mask can be associated with
    a domain, further construing the domain being represented.

    Simple domain.

    >>> domain = Domain([Dimesnion(90, -90, Dimension.values)])

    Domain with a mask.

    >>> domain = Domain([
            Dimension(90, -90, Dimension.values, name='lon'),
            Dimension(0, 90, Dimension.values, name='lat'),
        ],
        mask = Mask('http://thredds/clt.nc', 'clt', 'var_data<0.5'))

    Attributes:
        dimensions: List of Dimensions.
        mask: Mask to be applied to the domain.
        name: Name of the domain.
    """
    def __init__(self, dimensions=None, mask=None, name=None):
        """ Domain init. """
        super(Domain, self).__init__(name)

        if not dimensions:
            dimensions = []

        self.dimensions = dimensions
        self.mask = mask

    @classmethod
    def from_dict(cls, data):
        """ Creates domain from dict reperesentation. """
        blacklist = ['id', 'mask']

        name = None

        if 'id' in data:
            name = data['id']
        else:
            raise parameter.ParameterError('Domain must provide an id.')

        dimensions = []

        for key, value in data.iteritems():
            if key not in blacklist:
                dimensions.append(dimension.Dimension.from_dict(value, key))

        mask_data = None

        if 'mask' in data:
            mask_data = mask.Mask.from_dict(data['mask'])

        return cls(dimensions=dimensions, mask=mask_data, name=name)

    def get_dimension(self, names):
        if not isinstance(names, (list, tuple)):
            names = [names]

        for dim in self.dimensions:
            if dim.name in names:
                return dim

        return None

    def add_dimension(self, dimension):
        """ Add a dimension. """
        self.dimensions.append(dimension)

    def parameterize(self):
        """ Returns parameter for GET request. """
        param = {
            'id': self.name
        }

        for dimension in self.dimensions:
            param[dimension.name] = dimension.parameterize()

        if self.mask:
            param['mask'] = self.mask.parameterize()

        return param

    def __repr__(self):
        return ('Domain(dimensions=%r, mask=%r, name=%r)' %
                (self.dimensions, self.mask, self.name))
