from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped , relationship, Relationship

engine = create_engine('sqlite:///doo.db', echo=True)  #


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Users(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    is_employer: Mapped[bool] = mapped_column()
    firstname: Mapped[str] = mapped_column(default='')
    lastname: Mapped[str] = mapped_column(default='')
    age: Mapped[datetime] = mapped_column(default=None)
    contact: Mapped[str] = mapped_column(default='')

    def get_id(self):
        return self.id

    def is_active(self):
        return self.is_active



    # is_resume: Mapped[bool] = mapped_column()


class Resumes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column()
    skills: Mapped[str] = mapped_column()
    job_time: Mapped[str] = mapped_column()
    job_salary: Mapped[str] = mapped_column()
    
class Posts(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column()
    skills: Mapped[str] = mapped_column()
    job_time: Mapped[str] = mapped_column()
    job_salary: Mapped[str] = mapped_column()
    seen: Mapped[int] = mapped_column(default=0)

class Userposts(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    userid: Mapped[int] = mapped_column()
    postid: Mapped[int] = mapped_column()


class Userresumes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    userid: Mapped[int] = mapped_column()
    resumeid: Mapped[int] = mapped_column()



class Agreement(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    userpostsid: Mapped[int] = mapped_column()
    userresumesid: Mapped[int] = mapped_column()
    is_agreed: Mapped[bool] = mapped_column(default=False)



"""users_list = db.Table(
    "user_list",
    sqlalchemy.Column("id", sqlalchemy.Integer()),
    sqlalchemy.Column("username", sqlalchemy.String()),
    sqlalchemy.Column("password", sqlalchemy.String()),
    sqlalchemy.Column("is_employer", sqlalchemy.BOOLEAN()), )


users_posts = db.Table(
    "user_posts",
    sqlalchemy.Column("id", sqlalchemy.Integer()),
    sqlalchemy.Column("userid", sqlalchemy.Integer()),
    sqlalchemy.Column("postid", sqlalchemy.Integer()))


users_resumes = db.Table(
    "user_resumes",
    sqlalchemy.Column("id", sqlalchemy.Integer()),
    sqlalchemy.Column("userid", sqlalchemy.Integer()),
    sqlalchemy.Column("resumeid", sqlalchemy.Integer()))"""

"""class Users(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    is_employer: Mapped[bool] = mapped_column()
    firstname: Mapped[str] = mapped_column(default='')
    lastname: Mapped[str] = mapped_column(default='')
    age: Mapped[datetime] = mapped_column(default=None)
    contact: Mapped[str] = mapped_column(default='')

    def get_id(self):
        return self.id

    def is_active(self):
        return self.is_active"""

if __name__ == "__main__":
    db.create_all()

# TODO: докрутить модели до 3 нормальной формы
# TODO: здесь же написать все методы взаимодействия с бд
# TODO: разобраться с alembic
