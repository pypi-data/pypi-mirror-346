# from collective.geolocationbehavior.geolocation import IGeolocatable
from collective.schedulefield.behavior import IExceptionalClosureContent
from collective.schedulefield.behavior import IMultiScheduledContent
from collective.schedulefield.behavior import IScheduledContent
from collective.schedulefield.schedule import IScheduleWithTitle
from collective.schedulefield.schedule import ScheduleWithTitle
from collective.schedulefield.testing import FUNCTIONAL_TESTING
from collective.schedulefield.testing import INTEGRATION_TESTING
from plone import api
from pytest_plone import fixtures_factory

import pytest


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory(
        (
            (FUNCTIONAL_TESTING, "functional"),
            (INTEGRATION_TESTING, "integration"),
        )
    )
)


@pytest.fixture
def contents(portal, get_fti) -> list:
    """Create test contents."""
    response = {}
    with api.env.adopt_roles(
        [
            "Manager",
        ]
    ):

        response = []

        fti = get_fti("Document")
        fti.behaviors = fti.behaviors + (
            "collective.schedulefield.behavior.IScheduledContent",
            "collective.schedulefield.behavior.IExceptionalClosureContent",
            "collective.schedulefield.behavior.IMultiScheduledContent",
        )

        page = api.content.create(
            container=portal,
            type="Document",
            title="a page",
        )
        schedule = IScheduledContent(page)

        schedule.schedule = {
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
        exceptional_closure = IExceptionalClosureContent(page)
        exceptional_closure.exceptional_closure = [
            {
                "title": "first exceptional closure",
                "date": "2025-10-01",
            },
            {
                "title": "another exceptional closure",
                "date": "2026-01-01",
            },
        ]
        multi_schedule = IMultiScheduledContent(page)
        schedule1 = ScheduleWithTitle(schema=IScheduleWithTitle)
        schedule1.schedule = {
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
        }
        schedule2 = ScheduleWithTitle(schema=IScheduleWithTitle)
        schedule2.schedule = {
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
        }
        multi_schedule.multi_schedule = [schedule1, schedule2]
        # multi_schedule.multi_schedule = [
        #     {
        #         "title": "first schedule",
        #         "dates": [
        #             {"end_date": "2025-05-08", "start_date": "2025-05-05"},
        #             {"end_date": "2027-06-04", "start_date": "2026-04-02"},
        #         ],
        #         "schedule": {
        #             "monday": {
        #                 "comment": "",
        #                 "morningstart": "06:00",
        #                 "morningend": "10:00",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #             "tuesday": {
        #                 "comment": "",
        #                 "morningstart": "",
        #                 "morningend": "",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #             "wednesday": {
        #                 "comment": "",
        #                 "morningstart": "",
        #                 "morningend": "",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #             "thursday": {
        #                 "comment": "",
        #                 "morningstart": "",
        #                 "morningend": "",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #             "friday": {
        #                 "comment": "",
        #                 "morningstart": "",
        #                 "morningend": "",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #             "saturday": {
        #                 "comment": "",
        #                 "morningstart": "",
        #                 "morningend": "",
        #                 "afternoonstart": "15:00",
        #                 "afternoonend": "17:00",
        #             },
        #             "sunday": {
        #                 "comment": "",
        #                 "morningstart": "",
        #                 "morningend": "",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #         },
        #     }
        # ]
        # multi_schedule.multi_schedule.append(
        #     {
        #         "title": "second schedule",
        #         "dates": [{"end_date": "2025-01-02", "start_date": "2024-12-31"}],
        #         "schedule": {
        #             "monday": {
        #                 "comment": "",
        #                 "morningstart": "",
        #                 "morningend": "",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #             "tuesday": {
        #                 "comment": "",
        #                 "morningstart": "",
        #                 "morningend": "",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #             "wednesday": {
        #                 "comment": "",
        #                 "morningstart": "",
        #                 "morningend": "",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #             "thursday": {
        #                 "comment": "",
        #                 "morningstart": "10:00",
        #                 "morningend": "11:00",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #             "friday": {
        #                 "comment": "",
        #                 "morningstart": "",
        #                 "morningend": "",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #             "saturday": {
        #                 "comment": "",
        #                 "morningstart": "",
        #                 "morningend": "",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #             "sunday": {
        #                 "comment": "",
        #                 "morningstart": "",
        #                 "morningend": "",
        #                 "afternoonstart": "",
        #                 "afternoonend": "",
        #             },
        #         },
        #     }
        # )
        page.reindexObject()
        response.append(page.UID())
        return response
