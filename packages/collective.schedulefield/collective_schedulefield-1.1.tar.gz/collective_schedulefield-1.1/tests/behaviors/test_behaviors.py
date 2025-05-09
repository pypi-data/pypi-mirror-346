from collective.schedulefield.behavior import ExceptionalClosureContent
from collective.schedulefield.behavior import ScheduledContent
from plone import api

import pytest


class TestBehaviors:

    @pytest.fixture(autouse=True)
    def _init(self, portal, contents):
        self.portal = portal
        self.contents = contents

    @pytest.mark.parametrize(
        "behavior",
        [
            "collective.schedulefield.behavior.IExceptionalClosureContent",
            "collective.schedulefield.behavior.IMultiScheduledContent",
            "collective.schedulefield.behavior.IScheduledContent",
        ],
    )
    def test_has_behaviors(self, get_behaviors, behavior):
        assert behavior in get_behaviors("Document")

    def test_schedules(self, contents):
        """Test if the behavior is correctly applied to the content."""

        excepted_schedule = {
            "monday": {
                "comment": "a comment",
                "morningstart": "08:00",
                "morningend": "12:00",
                "afternoonstart": "13:00",
                "afternoonend": "17:00",
            },
            "tuesday": {
                "comment": "",
                "morningstart": "09:00",
                "morningend": "12:00",
                "afternoonstart": "",
                "afternoonend": "",
            },
            "wednesday": {
                "comment": "",
                "morningstart": "",
                "morningend": "",
                "afternoonstart": "14:00",
                "afternoonend": "18:00",
            },
            "thursday": {
                "comment": "",
                "morningstart": "",
                "morningend": "",
                "afternoonstart": "",
                "afternoonend": "",
            },
            "friday": {
                "comment": "",
                "morningstart": "",
                "morningend": "",
                "afternoonstart": "",
                "afternoonend": "",
            },
            "saturday": {
                "comment": "",
                "morningstart": "",
                "morningend": "",
                "afternoonstart": "",
                "afternoonend": "",
            },
            "sunday": {
                "comment": "",
                "morningstart": "",
                "morningend": "",
                "afternoonstart": "",
                "afternoonend": "",
            },
        }
        excepted_multi_schedule = [
            {
                "title": "first schedule",
                "dates": [
                    {"end_date": "2025-05-08", "start_date": "2025-05-05"},
                    {"end_date": "2027-06-04", "start_date": "2026-04-02"},
                ],
                "schedule": {
                    "monday": {
                        "comment": "",
                        "morningstart": "06:00",
                        "morningend": "10:00",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                    "tuesday": {
                        "comment": "",
                        "morningstart": "",
                        "morningend": "",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                    "wednesday": {
                        "comment": "",
                        "morningstart": "",
                        "morningend": "",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                    "thursday": {
                        "comment": "",
                        "morningstart": "",
                        "morningend": "",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                    "friday": {
                        "comment": "",
                        "morningstart": "",
                        "morningend": "",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                    "saturday": {
                        "comment": "",
                        "morningstart": "",
                        "morningend": "",
                        "afternoonstart": "15:00",
                        "afternoonend": "17:00",
                    },
                    "sunday": {
                        "comment": "",
                        "morningstart": "",
                        "morningend": "",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                },
            },
            {
                "title": "second schedule",
                "dates": [{"end_date": "2025-01-02", "start_date": "2024-12-31"}],
                "schedule": {
                    "monday": {
                        "comment": "",
                        "morningstart": "",
                        "morningend": "",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                    "tuesday": {
                        "comment": "",
                        "morningstart": "",
                        "morningend": "",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                    "wednesday": {
                        "comment": "",
                        "morningstart": "",
                        "morningend": "",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                    "thursday": {
                        "comment": "",
                        "morningstart": "10:00",
                        "morningend": "11:00",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                    "friday": {
                        "comment": "",
                        "morningstart": "",
                        "morningend": "",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                    "saturday": {
                        "comment": "",
                        "morningstart": "",
                        "morningend": "",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                    "sunday": {
                        "comment": "",
                        "morningstart": "",
                        "morningend": "",
                        "afternoonstart": "",
                        "afternoonend": "",
                    },
                },
            },
        ]
        excepted_exceptional_closure = [
            {"title": "first exceptional closure", "date": "2025-10-01"},
            {"title": "another exceptional closure", "date": "2026-01-01"},
        ]

        page = api.content.get(UID=contents[0])
        assert hasattr(page, "schedule")
        assert hasattr(page, "exceptional_closure")
        assert hasattr(page, "multi_schedule")

        assert page.schedule == excepted_schedule
        assert page.exceptional_closure == excepted_exceptional_closure
        assert page.multi_schedule[0].schedule == excepted_multi_schedule[0]
        assert page.multi_schedule[1].schedule == excepted_multi_schedule[1]

        # __import__("pdb").set_trace()

    def test_scheduled_content_context(self):
        scheduled = ScheduledContent("kamoulox")
        assert scheduled.context == "kamoulox"

    def test_exceptional_closure_content_context(self):
        exceptional_closure = ExceptionalClosureContent("kamoulox")
        assert exceptional_closure.context == "kamoulox"
