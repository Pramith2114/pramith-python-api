from datetime import datetime, date
from types import SimpleNamespace

from app.models import User, Doctor
from app.routes import serialize_appointment_detail


class FakeQuery:
    def __init__(self, results):
        self._results = list(results)

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self._results.pop(0) if self._results else None


class FakeDb:
    def __init__(self, patient, doctor, doctor_user):
        self._patient = patient
        self._doctor_user = doctor_user
        self._doctor = doctor
        self._user_call_count = 0

    def query(self, model):
        if model is User:
            result = [self._patient] if self._user_call_count == 0 else [self._doctor_user]
            self._user_call_count += 1
            return FakeQuery(result)
        if model is Doctor:
            return FakeQuery([self._doctor])
        raise AssertionError(f"Unexpected model: {model}")


def test_serialize_appointment_detail_includes_doctor_user_details():
    patient = SimpleNamespace(
        id="11111111-1111-1111-1111-111111111111",
        name="Alice Patient",
        mobile="+94770000001",
        email="alice@example.com",
        role="patient",
        is_verified=True,
        created_at=datetime(2024, 1, 1),
        username=None,
        is_active=True,
        updated_at=datetime(2024, 1, 2),
    )

    doctor_user = SimpleNamespace(
        id="22222222-2222-2222-2222-222222222222",
        name="Dr. Smith",
        mobile="+94770000002",
        email="dr.smith@example.com",
        role="doctor",
        is_verified=True,
        created_at=datetime(2024, 1, 1),
        username=None,
        is_active=True,
        updated_at=datetime(2024, 1, 2),
    )

    doctor = SimpleNamespace(
        id="33333333-3333-3333-3333-333333333333",
        user_id=doctor_user.id,
        specialization="Cardiology",
        profile_picture=None,
        address="Main Street",
        city="Colombo",
        state="Western",
        country="Sri Lanka",
        about_me="Experienced cardiologist",
        working_time="09:00-17:00",
        experience=10,
        consultation_fee=1500.0,
        patients=100,
        rating=4.8,
        reviews=50,
        verification_status="approved",
        document_type=None,
        file_url=None,
        verified_at=None,
        created_at=datetime(2024, 1, 1),
        updated_at=datetime(2024, 1, 2),
    )

    appointment = SimpleNamespace(
        id="44444444-4444-4444-4444-444444444444",
        patient_id=patient.id,
        doctor_id=doctor.id,
        appointment_date=date(2024, 2, 10),
        time_slot="09:00-09:30",
        status="scheduled",
        notes="Initial consultation",
        created_at=datetime(2024, 1, 1),
        updated_at=datetime(2024, 1, 2),
    )

    response = serialize_appointment_detail(FakeDb(patient, doctor, doctor_user), appointment)

    assert response.patient.name == "Alice Patient"
    assert response.patient.email == "alice@example.com"
    assert response.doctor is not None
    assert response.doctor.user is not None
    assert response.doctor.user.name == "Dr. Smith"
    assert response.doctor.user.email == "dr.smith@example.com"
