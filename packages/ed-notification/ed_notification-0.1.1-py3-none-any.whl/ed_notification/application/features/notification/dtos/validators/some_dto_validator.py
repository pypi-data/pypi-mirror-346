from ed_notification.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator,
    ValidationResponse,
)
from ed_notification.application.features.user.dtos.some_create_dto import SomeCreateDto


class SomeDtoValidator(ABCDtoValidator[SomeCreateDto]):
    def validate(self, dto: SomeCreateDto) -> ValidationResponse:
        errors = []
        if not dto.data.isalpha():
            errors.append("Data is required")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
