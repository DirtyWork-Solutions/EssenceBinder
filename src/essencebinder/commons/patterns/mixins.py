class HasWeightMixin:  # TODO: Move this out to forged??
    """
    TODO: Mixin class docs
    """
    def __init__(self, weighting: int | float = 1):
        self._weight = weighting


    @property
    def relation_weight(self):
        return self._weight

    def get_weight(self):
        return self._weight

    def set_weight(self, weighting: int | float):
        self._weight = weighting

    def add_weight(self, weighting: int | float):
        self._weight += weighting

    def subtract_weight(self, weighting: int | float):
        self._weight -= weighting

    def __eq__(self, other):
        if isinstance(other, HasWeightMixin):
            return self._weight == other.get_weight()
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, HasWeightMixin):
            return self._weight < other.get_weight()
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, HasWeightMixin):
            return self._weight <= other.get_weight()
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, HasWeightMixin):
            return self._weight > other.get_weight()

    def __ge__(self, other):
        if isinstance(other, HasWeightMixin):
            return self._weight >= other.get_weight()
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, HasWeightMixin):
            return self._weight != other.get_weight()
        return NotImplemented


class HasMetadataMixin:  # TODO: Create a metadata mixin
    pass

