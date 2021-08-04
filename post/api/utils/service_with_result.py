from abc import ABC

from service_objects.services import Service


class ServiceWithResult(Service, ABC):
    """
    Add result field into Service object
    """
    custom_validations = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None
        self.response_status = None

    def run_custom_validations(self):
        for custom_validation in self.__class__.custom_validations:
            getattr(self, custom_validation)()
