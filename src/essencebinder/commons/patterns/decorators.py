from typing import Optional

from essencebinder.commons.patterns.mixins import HasMetadataMixin

from forged.elements.reporting.reported import logger as log

def hasmetadata(metadata: Optional[dict] = None):
    """
    Decorator to add metadata to a class using the HasMetadataMixin.

    :param metadata: A dictionary of metadata to initialize the class with.
    """
    log.warning(f"The Metadata decorator and Mixin are future features. They should be used with caution and are not "
                f"fully implemented yet.")
    def decorator(cls):
        class Wrapped(cls, HasMetadataMixin):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.set_metadata(metadata or {})
        return Wrapped
    return decorator