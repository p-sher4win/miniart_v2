from mongoengine import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# MONGO DB SCHEMA MODELS
# USERS MODEL
class Users(Document, UserMixin):
    meta = {
        'collection': 'users',
        'indexes': ['email']
    }

    name = StringField(required=True, max_length=150)
    email = StringField(required=True, unique=True, max_length=150)
    
    role = StringField(
        choices=["admin", "operator"],
        default="operator"
    )

    status = StringField(
        choices=["active", "suspended", "deactivated", "deleted"],
        default="active"
    )

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    @property
    def is_active(self):
        return self.status == "active"
    
    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_operator(self):
        return self.role == "operator"

    # auto-save updated_at on new updates
    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower().strip()
        self.updated_at = datetime.utcnow()
        return super(Users, self).save(*args, **kwargs)

    # CREATE A STRING
    def __repr__(self):
        return f"<User {self.email}>"
    

# AUTH_METHODS MODEL
class AuthMethods(Document):
    meta = {
        'collection': 'auth_methods',
        'indexes': [
            {
                'fields': ['user_id', 'provider'],
                'unique': True
            }
        ]
    }

    user_id = ReferenceField(Users, reverse_delete_rule=CASCADE, required=True)
    
    provider = StringField(
        choices=["local", "google", "firebase_email"],
        required=True
    )
    
    provider_uid = StringField(required=False, unique=True, sparse=True) # firebase uid or google uid
    
    username = StringField(required=False, unique=True, sparse=True, max_length=150)
    password_hash = StringField(required=False, max_length=512)

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    # PASSWORD HASHING
    @property
    def password(self):
        raise AttributeError("Password is not a readable!")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def clean(self):
        if self.provider == "local":
            if not self.password_hash:
                raise ValidationError("Local auth requires password")

        if self.provider in ["google", "firebase_email"]:
            if not self.provider_uid:
                raise ValidationError(f"{self.provider} requires provider_uid")
    
    # auto-save updated_at on new updates
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(AuthMethods, self).save(*args, **kwargs)

    # CREATE A STRING
    def __repr__(self):
        return f"<Auth {self.provider} for {self.user_id.id}>"