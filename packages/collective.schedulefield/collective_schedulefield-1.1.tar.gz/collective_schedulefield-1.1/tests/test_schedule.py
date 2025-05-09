from collective.schedulefield.schedule import Schedule
from collective.schedulefield.schedule import ScheduleWidget
from z3c.form.interfaces import NO_VALUE
from zope.publisher.browser import TestRequest
from zope.schema.interfaces import WrongContainedType

import pytest


class TestSchedule:

    def test_schedule_from_unicode_empty(self):
        field = Schedule()
        result = field.fromUnicode(None)
        assert result is None

    def test_schedule_from_unicode_valid_time(self):
        field = Schedule()
        input_data = '{"monday": {"morningstart": "08:00", "comment": "Work"}}'
        result = field.fromUnicode(input_data)
        assert result == input_data
        assert field._validate_format(None) is None
        # __import__("pdb").set_trace()

    def test_schedule_from_unicode_invalid_time(self):
        field = Schedule()
        input_data = '{"monday": {"morningstart": "50:50", "comment": "Work"}}'
        with pytest.raises(WrongContainedType):
            field.fromUnicode(input_data)

    def test_schedulewidget(self):
        request = TestRequest()
        widget = ScheduleWidget(request)
        widget.name = "schedule"
        assert widget.get_hour_value("monday", "morningstart") == ""
        assert widget.get_comment("monday") == ""
        assert widget.must_show_day("monday") is False
        widget.value = '{"monday": {"morningstart": "08:00", "comment": "kamoulox"},"tuesday": {}, "wednesday": {"morningstart": "__:__"}}'
        widget.update()
        assert isinstance(widget.value, dict)
        assert widget.value.get("monday").get("morningstart") == "08:00"
        assert widget.value.get("monday").get("comment") == "kamoulox"
        assert widget.klass == "schedule-widget"
        assert widget.css == "schedule"
        assert widget.days == (
            ("monday", "Monday"),
            ("tuesday", "Tuesday"),
            ("wednesday", "Wednesday"),
            ("thursday", "Thursday"),
            ("friday", "Friday"),
            ("saturday", "Saturday"),
            ("sunday", "Sunday"),
        )
        assert widget.day_sections == (
            "morningstart",
            "morningend",
            "afternoonstart",
            "afternoonend",
        )
        assert widget.extract() == NO_VALUE
        assert widget.get_hour_value("monday", "morningstart") == "08:00"
        assert widget.get_hour_value("tuesday", "morningstart") is None
        assert widget.get_comment("monday") == "kamoulox"
        assert widget.must_show_day("tuesday") is False
        assert widget.must_show_day("monday") is True

        assert widget._format("__:__") is None
