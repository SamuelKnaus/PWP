"""
This module is used to set up a dummy database
It uses the definitions of the api module and adds dummy data to the database
"""

import api
from database.models import User, UserType
from helper.encryption_helper import EncryptionHelper

DB = api.DB

# set up the environment
DB.create_all()
DB.session.rollback()

# create the dummy user
USER_1 = User(
    username="dummyGuy",
    email_address="red.unicorn@gmail.com",
    password=EncryptionHelper.encrypt_password("thisisnotapassword"),
    role=UserType.BASIC_USER
)

USER_2 = User(
    username="dummyAdmin",
    email_address="omnipotent.pencil@yahoo.com",
    password=EncryptionHelper.encrypt_password("1234"),
    role=UserType.ADMIN
)

USER_3 = User(
    username="grantorinohurricane",
    email_address="grantorinohurricane@gmail.com",
    password=EncryptionHelper.encrypt_password("Grantorino1234"),
    role=UserType.BASIC_USER
)

USER_4 = User(
    username="lightningbasketball",
    email_address="lightningbasketbal@gmail.com",
    password=EncryptionHelper.encrypt_password("Basketball1234"),
    role=UserType.BASIC_USER
)

USER_5 = User(
    username="johnkennedy",
    email_address="kennedyj@moviereview.com",
    password=EncryptionHelper.encrypt_password("$KenJon9908"),
    role=UserType.ADMIN
)

USER_6 = User(
    username="sannelily",
    email_address="sanne.lily@gmail.com",
    password=EncryptionHelper.encrypt_password("thisisnotapassword"),
    role=UserType.BASIC_USER
)

DB.session.add(USER_1)
DB.session.add(USER_2)
DB.session.add(USER_3)
DB.session.add(USER_4)
DB.session.add(USER_5)
DB.session.add(USER_6)
DB.session.commit()
