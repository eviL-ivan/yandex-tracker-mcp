import pytest
from aioresponses import aioresponses

from mcp_tracker.tracker.custom.client import TrackerClient
from mcp_tracker.tracker.custom.errors import IssueNotFound
from mcp_tracker.tracker.proto.types.issues import IssueAttachment


class TestIssueGetAttachments:
    async def test_success(self, tracker_client: TrackerClient) -> None:
        attachment_data = {
            "self": "https://api.tracker.yandex.net/v3/issues/TEST-123/attachments/1",
            "id": "attachment-123",
            "name": "test_file.txt",
            "content": "https://api.tracker.yandex.net/v3/issues/TEST-123/attachments/1/content",
            "createdBy": {
                "self": "https://api.tracker.yandex.net/v3/users/1234567890",
                "id": "user123",
                "display": "Test User",
            },
            "createdAt": "2023-01-01T12:00:00.000+0000",
            "mimetype": "text/plain",
            "size": 1024,
        }
        attachments_response = [attachment_data]

        with aioresponses() as m:
            m.get(
                "https://api.tracker.yandex.net/v3/issues/TEST-123/attachments",
                payload=attachments_response,
            )

            result = await tracker_client.issue_get_attachments("TEST-123")

            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], IssueAttachment)
            assert result[0].name == "test_file.txt"

    async def test_not_found(self, tracker_client: TrackerClient) -> None:
        with aioresponses() as m:
            m.get(
                "https://api.tracker.yandex.net/v3/issues/NOTFOUND-123/attachments",
                status=404,
            )

            with pytest.raises(IssueNotFound) as exc_info:
                await tracker_client.issue_get_attachments("NOTFOUND-123")

            assert exc_info.value.issue_id == "NOTFOUND-123"


class TestAttachmentUploadTemp:
    async def test_upload_temp_attachment_success(
        self, tracker_client: TrackerClient
    ) -> None:
        attachment_response = {
            "self": "https://api.tracker.yandex.net/v2/attachments/temp-123",
            "id": "temp-attachment-123",
            "name": "screenshot.png",
            "content": "https://api.tracker.yandex.net/v2/attachments/temp-123/content",
            "createdBy": {
                "self": "https://api.tracker.yandex.net/v3/users/1234567890",
                "id": "user123",
                "display": "Test User",
            },
            "createdAt": "2023-01-01T12:00:00.000+0000",
            "mimetype": "image/png",
            "size": 2048,
        }

        with aioresponses() as m:
            m.post(
                "https://api.tracker.yandex.net/v2/attachments?filename=screenshot.png",
                payload=attachment_response,
            )

            result = await tracker_client.attachment_upload_temp(
                "screenshot.png",
                b"fake image content",
            )

            assert isinstance(result, IssueAttachment)
            assert result.id == "temp-attachment-123"
            assert result.name == "screenshot.png"

    async def test_upload_with_mimetype(self, tracker_client: TrackerClient) -> None:
        attachment_response = {
            "self": "https://api.tracker.yandex.net/v2/attachments/temp-456",
            "id": "temp-attachment-456",
            "name": "document.pdf",
            "content": "https://api.tracker.yandex.net/v2/attachments/temp-456/content",
            "createdBy": {
                "self": "https://api.tracker.yandex.net/v3/users/1234567890",
                "id": "user123",
                "display": "Test User",
            },
            "createdAt": "2023-01-01T12:00:00.000+0000",
            "mimetype": "application/pdf",
            "size": 4096,
        }

        with aioresponses() as m:
            m.post(
                "https://api.tracker.yandex.net/v2/attachments?filename=document.pdf",
                payload=attachment_response,
            )

            result = await tracker_client.attachment_upload_temp(
                "document.pdf",
                b"fake pdf content",
                mimetype="application/pdf",
            )

            assert isinstance(result, IssueAttachment)
            assert result.id == "temp-attachment-456"
            assert result.name == "document.pdf"
            assert result.mimetype == "application/pdf"
