from typing import Any

import pytest
from aioresponses import aioresponses

from mcp_tracker.tracker.custom.client import TrackerClient
from mcp_tracker.tracker.custom.errors import IssueNotFound
from mcp_tracker.tracker.proto.types.issues import IssueComment


class TestIssueGetComments:
    async def test_success(
        self, tracker_client: TrackerClient, sample_comment_data: dict[str, Any]
    ) -> None:
        comments_response = [sample_comment_data]

        with aioresponses() as m:
            m.get(
                "https://api.tracker.yandex.net/v3/issues/TEST-123/comments",
                payload=comments_response,
            )

            result = await tracker_client.issue_get_comments("TEST-123")

            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], IssueComment)
            assert result[0].text == "This is a test comment"

    async def test_not_found(self, tracker_client: TrackerClient) -> None:
        with aioresponses() as m:
            m.get(
                "https://api.tracker.yandex.net/v3/issues/NOTFOUND-123/comments",
                status=404,
            )

            with pytest.raises(IssueNotFound) as exc_info:
                await tracker_client.issue_get_comments("NOTFOUND-123")

            assert exc_info.value.issue_id == "NOTFOUND-123"


class TestIssueAddComment:
    async def test_add_comment_success(
        self, tracker_client: TrackerClient, sample_comment_data: dict[str, Any]
    ) -> None:
        with aioresponses() as m:
            m.post(
                "https://api.tracker.yandex.net/v2/issues/TEST-123/comments",
                payload=sample_comment_data,
            )

            result = await tracker_client.issue_add_comment(
                "TEST-123", "This is a test comment"
            )

            assert isinstance(result, IssueComment)
            assert result.text == "This is a test comment"
            assert result.id == 123

    async def test_add_comment_with_attachments(
        self, tracker_client: TrackerClient, sample_comment_data: dict[str, Any]
    ) -> None:
        with aioresponses() as m:
            m.post(
                "https://api.tracker.yandex.net/v2/issues/TEST-123/comments",
                payload=sample_comment_data,
            )

            result = await tracker_client.issue_add_comment(
                "TEST-123",
                "Comment with attachments",
                attachment_ids=["attach-1", "attach-2"],
            )

            assert isinstance(result, IssueComment)

    async def test_add_comment_with_summonees(
        self, tracker_client: TrackerClient, sample_comment_data: dict[str, Any]
    ) -> None:
        with aioresponses() as m:
            m.post(
                "https://api.tracker.yandex.net/v2/issues/TEST-123/comments",
                payload=sample_comment_data,
            )

            result = await tracker_client.issue_add_comment(
                "TEST-123",
                "Comment with summonees",
                summonees=["user1", "user2"],
            )

            assert isinstance(result, IssueComment)

    async def test_add_comment_not_add_to_followers(
        self, tracker_client: TrackerClient, sample_comment_data: dict[str, Any]
    ) -> None:
        with aioresponses() as m:
            m.post(
                "https://api.tracker.yandex.net/v2/issues/TEST-123/comments?isAddToFollowers=false",
                payload=sample_comment_data,
            )

            result = await tracker_client.issue_add_comment(
                "TEST-123",
                "Comment without adding to followers",
                is_add_to_followers=False,
            )

            assert isinstance(result, IssueComment)

    async def test_add_comment_not_found(self, tracker_client: TrackerClient) -> None:
        with aioresponses() as m:
            m.post(
                "https://api.tracker.yandex.net/v2/issues/NOTFOUND-123/comments",
                status=404,
            )

            with pytest.raises(IssueNotFound) as exc_info:
                await tracker_client.issue_add_comment("NOTFOUND-123", "Test comment")

            assert exc_info.value.issue_id == "NOTFOUND-123"
