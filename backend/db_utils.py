from backend.db_models import *
def db_create_user(username, password, is_employer, firstname, lastname, age):
    new_user = Users(
        username=username,
        password=password,
        is_employer=is_employer,
        firstname=firstname,
        lastname=lastname,
        age=age
    )
    db.session.add(new_user)
    db.session.commit()


def db_edit_user(old_user, username, password, firstname, lastname, age):
    new_user = Users(
        username=username,
        password=password,
        is_employer=True,
        firstname=firstname,
        lastname=lastname,
        age=age)
    old_user.username = new_user.username
    if password != "":
        old_user.password = new_user.password
    old_user.firstname = new_user.firstname
    old_user.lastname = new_user.lastname
    old_user.age = age
    db.session.commit()


def db_delete_user(userid):
    user = db.session.execute(db.select(Users).filter_by(id=userid)).scalar_one()
    db.session.delete(user)
    db.session.commit()


def db_create_post(userid, title, text, skills, jobtime, jobsalary):
    new_post = Posts(
        title=title,
        text=text,
        skills=skills,
        job_time=jobtime,
        job_salary=jobsalary
    )
    db.session.add(new_post)
    db.session.commit()
    userpost = Userposts(
        userid=userid,
        postid=new_post.id
    )
    db.session.add(userpost)
    db.session.commit()
    return new_post.id


def db_create_resume(userid, title, text, skills, jobtime, jobsalary):
    new_post = Resumes(
        title=title,
        text=text,
        skills=skills,
        job_time=jobtime,
        job_salary=jobsalary
    )
    db.session.add(new_post)
    db.session.commit()
    userresume = Userresumes(
        userid=userid,
        resumeid=new_post.id
    )
    db.session.add(userresume)
    db.session.commit()
    return new_post.id


def db_edit_post(old_post, title, text, skills, jobtime, jobsalary):
    new_post = Posts(
        title=title,
        text=text,
        skills=skills,
        job_time=jobtime,
        job_salary=jobsalary
    )
    old_post.title = new_post.title
    old_post.text = new_post.text
    old_post.skills = new_post.skills
    old_post.job_time = new_post.job_time
    old_post.job_salary = new_post.job_salary
    db.session.commit()


def db_edit_resume(old_resume, title, text, skills, jobtime, jobsalary):
    new_resume = Resumes(
        title=title,
        text=text,
        skills=skills,
        job_time=jobtime,
        job_salary=jobsalary
    )
    old_resume.title = new_resume.title
    old_resume.text = new_resume.text
    old_resume.skills = new_resume.skills
    old_resume.job_time = new_resume.job_time
    old_resume.job_salary = new_resume.job_salary
    db.session.commit()


def show_users():
    users = Users.query.all()
    return users


def db_delete_post(postid):
    post = db.session.execute(db.select(Posts).filter_by(id=postid)).scalar_one_or_none()
    userpost = db.session.execute(db.select(Userposts).filter_by(postid=postid)).scalar_one()
    db.session.delete(post)
    db.session.delete(userpost)
    db.session.commit()


def db_delete_resume(resumeid):
    resume = db.session.execute(db.select(Posts).filter_by(id=resumeid)).scalar_one_or_none()
    userresume = db.session.execute(db.select(Userresumes).filter_by(resumeid=resumeid)).scalar_one()
    db.session.delete(resume)
    db.session.delete(userresume)
    db.session.commit()

def db_create_agreement(userid,postid):
    userpost = db.session.execute(db.select(Userposts.id).filter_by(postid = postid)).scalar_one()
    userresume = db.session.execute(db.select(Userresumes.id).filter_by(userid = userid)).scalars().first()
    agreement = Agreement(
                        userpostsid = userpost,
                        userresumesid = userresume
    )
    db.session.add(agreement)
    db.session.commit()


def db_find_agreement(ownerid, postid):
    user = db.session.execute(db.select(Users).filter_by(id= ownerid)).scalar_one_or_none()
    agreeement_list = list(list())
    if user.is_employer is True:
        userpost = db.session.execute(db.select(Userposts).filter_by(postid = postid)).scalar_one()
        agreeements = db.session.execute(db.select(Agreement).filter_by(userpostsid = userpost.id)).scalars().all()
        for agreement in agreeements:
            userresumes = db.session.execute(db.select(Userresumes).filter(Userresumes.resumeid.in_(agreement.userresumesid))).scalars().all()
            for userresume in userresumes:
                instance = [ownerid,postid,userresume.userid,userresume.resumeid,agreement.id]
                agreeement_list.append(instance)
    return agreeement_list


def db_apply_agreement(callback, agreementid):
    if callback :
        agreement = db.session.execute(db.select(Agreement).filter_by(id = agreementid)).scalar_one()
        agreement.is_agreed = True
        db.session.commit()
    else:
        agreement = db.session.execute(db.select(Agreement).filter_by(id = agreementid)).scalar_one()
        db.session.delete(agreement)
        db.session.commit()


