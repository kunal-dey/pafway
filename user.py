from mongoengine import (
    Document, 
    StringField, 
    EmailField, 
    EnumField, 
    BooleanField,
    ObjectIdField
)
from mongoengine.errors import DoesNotExist
from bson.objectid import ObjectId

from flask import request, url_for

from utils.db import *
from utils.custom_enums import Status
from utils.mail import send_email

MAIL_SUBJECT = "Registration Confiramtion Mail"
MAIL_BODY = "Please click the link to confirm your registration {}"
EMBEDDED_HTML = "<html>Please click the link to confirm your registration <a href='{}'> Confirm </html>"


class User(Document):

    #_id = StringField(required=True)
    name = StringField(max_length=50,required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=150)
    status = EnumField(enum = Status)

    activated = BooleanField(default=False)

    @classmethod
    def find_by_name(cls, name):
        with connect_to_db():
            try:
                return cls.objects.get(name = name)
            except DoesNotExist:
                return None

    @classmethod
    def find_by_email(cls, email):
        with connect_to_db():
            try:
                return cls.objects.get(email=email)
            except DoesNotExist:
                return None

    @classmethod
    def find_by_id(cls, id):
        with connect_to_db():
            try:
                return cls.objects.get(_id=ObjectId(id))
            except DoesNotExist:
                return None

    def get_json(self):
        return {
            "id": str(self._id),
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "status": self.status,
            "activated":self.activated
        }

    def send_confirmation_mail(self):
        link = request.url_root[:-1] + url_for("user.user_confirm", user_id=self._id)


        return send_email(
            [self.email],
            MAIL_SUBJECT,
            MAIL_BODY.format(link),
            EMBEDDED_HTML.format(link),
        )

    def save_to_db(self):
        with connect_to_db():
            self.save()