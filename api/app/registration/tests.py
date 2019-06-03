import json
from app import db, bcrypt, LOGGER

from datetime import datetime, timedelta

from app import app, db
from app.utils.testing import ApiTestCase
from app.users.models import AppUser, PasswordReset, UserCategory, Country, UserComment
from app.events.models import Event, EventRole
from app.registration.models import Offer
from app.registration.models import RegistrationForm
from app.applicationModel.models import ApplicationForm
from app.responses.models import Response


INVITED_GUEST = {
    'event_id': 1,
    'email_address': 'something@email.com',
    'role': 'jedi'
}

INVITED_GUEST_2 = {
    'event_id': 1,
    'email_address': 'something2@email.com',
    'role': 'jedi'
}

INVITED_GUEST_NEW_USER = {
    'event_id': 1,
    'email_address': 'new@email.com',
    'role': 'jedi'
}
USER_DATA = {
    'email': 'newsomething@email.com',
    'firstname': 'Some',
    'lastname': 'Thing',
    'user_title': 'Mr',
    'nationality_country_id': 1,
    'residence_country_id': 1,
    'user_gender': 'Male',
    'affiliation': 'University',
    'department': 'Computer Science',
    'user_disability': 'None',
    'user_category_id': 1,
    'user_primaryLanguage': 'Zulu',
    'user_dateOfBirth':  datetime(1984, 12, 12).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
}

REGISTRATION_FORM = {
    # 'offer_id':1,
    'event_id': 1,
}


class RegistrationFormTest(ApiTestCase):

    def seed_static_data(self):

        test_user = AppUser('something@email.com', 'Some', 'Thing', 'Mr', 1, 1,
                            'Male', 'University', 'Computer Science', 'None', 1,
                            datetime(1984, 12, 12),
                            'Zulu',
                            '123456')
        test_user.verified_email = True
        db.session.add(test_user)

        test_user2 = AppUser('something2@email.com', 'Some', 'Thing', 'Mr', 1, 1,
                             'Male', 'University', 'Computer Science', 'None', 1,
                             datetime(1984, 12, 12),
                             'Zulu',
                             '123456')
        test_user2.verified_email = True
        db.session.add(test_user2)
        db.session.add(UserCategory('Postdoc'))
        db.session.add(Country('South Africa'))

        event_admin = AppUser('event_admin@ea.com', 'event_admin', '1', 'Ms', 1,
                              1, 'F', 'NWU', 'Math', 'NA', 1, datetime(1984, 12, 12), 'Eng', '123456')
        event_admin.verified_email = True
        db.session.add(event_admin)

        self.event1 = Event('Indaba', 'Indaba Event',
                            datetime.now(), datetime.now())
        self.event2 = Event('IndabaX', 'IndabaX Sudan',
                            datetime.now(), datetime.now())
        db.session.add(self.event1)
        db.session.add(self.event2)

        adminRole = EventRole('admin', 3, 1)
        db.session.add(adminRole)

        db.session.add(test_user2)
        db.session.add(Event('Cmt', 'Cmt Event', datetime.now(), datetime.now()))
        #
        # offer = Offer(
        #     user_id=1,
        #     event_id=1,
        #     offer_date=datetime.now(),
        #     expiry_date=datetime.now() + timedelta(days=15),
        #     payment_required='yes',
        #     travel_award='no award',
        #     updated_at=datetime.now())
        # db.session.add(offer)
        #
        # db.session.add(RegistrationForm(event_id=1))
        db.session.commit()

        self.event1_id = self.event1.id
        self.event2_id = self.event2.id
        self.headers = self.get_auth_header_for("something@email.com")
        self.adminHeaders = self.get_auth_header_for("event_admin@ea.com")

        db.session.flush()

    def get_auth_header_for(self, email):
        body = {
            'email': email,
            'password': '123456'
        }
        response = self.app.post('api/v1/authenticate', data=body)
        data = json.loads(response.data)
        header = {'Authorization': data['token']}
        return header

    def test_create_registration_form(self):
        self.seed_static_data()
        response = self.app.post(
            '/api/v1/registration-form', data=REGISTRATION_FORM, headers=self.headers)
        data = json.loads(response.data)
        LOGGER.debug(
            "Reg-form: {}".format(data))
        assert response.status_code == 201
        assert data['registration_form_id'] == 1

    def test_get_form(self):
        self.seed_static_data()
        event_id = 1
        offer_id = 1
        response = self.app.get(
            '/api/v1/registration-form?offer_id='+str(offer_id)+'&event_id='+str(event_id), headers=self.headers)
        LOGGER.debug(
            "Reg-form: {}".format(json.loads(response.data)))
        assert response.status_code == 201

