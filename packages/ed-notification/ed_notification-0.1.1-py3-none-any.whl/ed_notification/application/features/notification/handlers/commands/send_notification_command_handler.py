from datetime import UTC, datetime

from ed_domain.core.entities.notification import NotificationType
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from ed_domain.utils.email.abc_email_sender import ABCEmailSender
from ed_domain.utils.sms.abc_sms_sender import ABCSmsSender
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_notification.application.common.responses.base_response import \
    BaseResponse
from ed_notification.application.features.notification.dtos import (
    NotificationDto, SendNotificationDto)
from ed_notification.application.features.notification.requests.commands.send_notification_command import \
    SendNotificationCommand
from ed_notification.common.generic_helpers import get_new_id
from ed_notification.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(SendNotificationCommand, BaseResponse[NotificationDto])
class SendNotificationCommandHandler(RequestHandler):
    def __init__(
        self,
        uow: ABCUnitOfWork,
        email_sender: ABCEmailSender,
        sms_sender: ABCSmsSender,
    ):
        self._uow = uow
        self._email_sender = email_sender
        self._sms_sender = sms_sender

    async def handle(
        self, request: SendNotificationCommand
    ) -> BaseResponse[NotificationDto]:
        dto: SendNotificationDto = request.dto
        created = self._uow.notification_repository.create(
            {
                "id": get_new_id(),
                "user_id": dto["user_id"],
                "message": dto["message"],
                "read_status": False,
                "create_datetime": datetime.now(UTC),
                "update_datetime": datetime.now(UTC),
                "notification_type": NotificationType[dto["notification_type"]],
                "deleted": False,
            }
        )

        return BaseResponse[NotificationDto].success(
            "Notification sent",
            NotificationDto(**created),  # type: ignore
        )
