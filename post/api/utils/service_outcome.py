from rest_framework import status
from service_objects.errors import InvalidInputsError


class ServiceOutcome:
    """
    Wrapper to execute Service objects
    """
    def __init__(self, service_object, service_object_attributes=None, service_object_files=None):
        self._errors = {}
        self._result = None
        self._response_status = None
        self._outcome = self.execute(service_object, service_object_attributes, service_object_files)

    def execute(self, service_object, service_object_attributes, service_object_files):
        try:
            outcome = service_object.execute(service_object_attributes, service_object_files)
            self._response_status = outcome.response_status
            if bool(outcome.errors):
                self._errors = outcome.errors
            else:
                self._result = outcome.result
            return outcome
        except InvalidInputsError as input_errors:
            self._errors = input_errors.errors
            self._response_status = status.HTTP_400_BAD_REQUEST
            return None

    @property
    def valid(self):
        return not bool(self._errors)

    @property
    def service(self):
        return self._outcome

    @property
    def result(self):
        return self._result

    @property
    def errors(self):
        return self._errors

    @property
    def response_status(self):
        return self._response_status
