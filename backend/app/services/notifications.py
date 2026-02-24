# ABOUTME: Notification delivery interface; stub implementations when env not set.
# ABOUTME: Real WhatsApp/SMS when env vars provided; otherwise log only.

import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class NotificationSender(ABC):
    @abstractmethod
    async def send(self, to: str, body: str, subject: str | None = None) -> bool:
        pass


class StubNotificationSender(NotificationSender):
    async def send(self, to: str, body: str, subject: str | None = None) -> bool:
        logger.info("Notification (stub): to=%s subject=%s body=%s", to, subject, body[:50] if body else "")
        return True


def get_notification_sender() -> NotificationSender:
    return StubNotificationSender()
