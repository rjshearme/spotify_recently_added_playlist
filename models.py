from contextlib import contextmanager

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

import api
import constants
import tokens

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = sa.Column(sa.String(255), primary_key=True, autoincrement=False)
    name = sa.Column(sa.String(255))
    playlist_id = sa.Column(sa.String(255))
    recently_added_delta_days = sa.Column(sa.Integer)
    refresh_token = sa.Column(sa.String(255), nullable=False)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, name={self.name}>"

    @property
    def access_token(self):
        return tokens.get_access_token(self.refresh_token)


engine = sa.create_engine(constants.DATABASE_URL)

if __name__ == "__main__":
    Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()


def get_all_entries():
    with session_scope() as session:
        users = session.query(User).all()
        session.expunge_all()
    return users


def get_all_user_ids():
    with session_scope() as session:
        return session.query(User.user_id).all()


def create_user(refresh_token):
    user_id, name = api.get_user_id_and_name_from_refresh_token(refresh_token)
    with session_scope() as s:
        if user := s.query(User).get(user_id):
            user.refresh_token = refresh_token
            user.name = name
        else:
            user = User(user_id=user_id, name=name, refresh_token=refresh_token)
            s.add(user)
    return user_id


def update_user(user_id, **attributes):
    with session_scope() as s:
        user = s.query(User).get(user_id)
        for attribute_key, attribute_value in attributes.items():
            setattr(user, attribute_key, attribute_value)
    with session_scope() as s:
        user = s.query(User).get(user_id)
        s.expunge_all()
        return user


def get_playlist_id(user):
    if user.playlist_id:
        return user
    new_playlist_id = api.make_new_playlist(user)
    with session_scope() as s:
        session_user = s.query(User).get(user.user_id)
        session_user.playlist_id = new_playlist_id
    with session_scope() as s:
        updated_user = s.query(User).get(user.user_id)
        s.expunge_all()
    return updated_user
