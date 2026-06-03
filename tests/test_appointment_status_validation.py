import pytest

from app.routes import normalize_appointment_status, validate_appointment_status


def test_normalize_appointment_status_accepts_common_aliases():
    assert normalize_appointment_status("cancel") == "cancelled"
    assert normalize_appointment_status("complete") == "completed"
    assert normalize_appointment_status("  COMPLETED  ") == "completed"


def test_validate_appointment_status_returns_clear_error_for_invalid_value():
    with pytest.raises(ValueError) as exc_info:
        validate_appointment_status("done")

    message = str(exc_info.value)
    assert "Invalid status 'done'" in message
    assert "scheduled, completed, cancelled, no-show, rescheduled" in message
    assert "cancel" in message and "complete" in message
