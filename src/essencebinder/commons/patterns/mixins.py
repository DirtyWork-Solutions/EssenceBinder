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
    def __init__(self, metadata: dict = None):
        self._metadata = {}
        if metadata is not None:
            for key, value in metadata.items():
                self._metadata[key] = value

    @property
    def metadata(self):
        return self._metadata


    def get_metadata(self):
        return self._metadata

    def set_metadata(self, metadata: dict):
        self._metadata = metadata

    def add_metadata(self, key: str, value: str):
        self._metadata[key] = value

    def remove_metadata(self, key: str):
        if key in self._metadata:
            del self._metadata[key]
        else:
            raise KeyError(f"Key '{key}' not found in metadata.")

    def __getitem__(self, key: str):
        return self._metadata[key]

    def __setitem__(self, key: str, value: str):
        self._metadata[key] = value

    def __delitem__(self, key: str):
        if key in self._metadata:
            del self._metadata[key]
        else:
            raise KeyError(f"Key '{key}' not found in metadata.")

    def __contains__(self, key: str):
        return key in self._metadata

    def __iter__(self):
        return iter(self._metadata)

    def __len__(self):
        return len(self._metadata)

    def __repr__(self):
        return f"{self.__class__.__name__}(Metadata={self._metadata})"



