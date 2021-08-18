from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser


class UsersService(ServiceWithResult):

    def process(self):
        if self.is_valid():
            self.result = self._queryset
        return self

    @property
    def _queryset(self):
        return CustomUser.objects.all()
