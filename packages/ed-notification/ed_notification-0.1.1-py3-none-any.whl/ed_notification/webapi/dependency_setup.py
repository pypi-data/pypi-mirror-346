from ed_infrastructure.persistence.mongo_db.db_client import DbClient
from ed_infrastructure.persistence.mongo_db.unit_of_work import UnitOfWork
from ed_infrastructure.utils.email.email_sender import EmailSender
from ed_infrastructure.utils.sms.sms_sender import SmsSender
from rmediator.mediator import Mediator

from ed_notification.application.features.notification.handlers.commands import (
    SendNotificationCommandHandler, UpdateNotificationCommandHandler)
from ed_notification.application.features.notification.handlers.queries import (
    GetNotificationQueryHandler, GetNotificationsQueryHandler)
from ed_notification.application.features.notification.requests.commands import (
    SendNotificationCommand, UpdateNotificationCommand)
from ed_notification.application.features.notification.requests.queries import (
    GetNotificationQuery, GetNotificationsQuery)
from ed_notification.common.generic_helpers import get_config


def get_mediator() -> Mediator:
    # Dependencies
    config = get_config()
    db_client = DbClient(
        config["mongo_db_connection_string"], config["db_name"])
    uow = UnitOfWork(db_client)
    email_sender = EmailSender(config["resend_api_key"])
    sms_sender = SmsSender(config["infobig_key"])

    # Setup
    mediator = Mediator()

    requests_and_handlers = [
        (
            SendNotificationCommand,
            SendNotificationCommandHandler(uow, email_sender, sms_sender),
        ),
        (
            UpdateNotificationCommand,
            UpdateNotificationCommandHandler(uow),
        ),
        (GetNotificationQuery, GetNotificationQueryHandler(uow)),
        (GetNotificationsQuery, GetNotificationsQueryHandler(uow)),
    ]

    for request, handler in requests_and_handlers:
        mediator.register_handler(request, handler)

    db_client.start()
    return mediator
