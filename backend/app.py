from flask import Flask, request, abort, redirect, Response, url_for, make_response, render_template, flash
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user, logout_user
from flask_cors import CORS
from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import *
from datetime import datetime
from backend.db_models import  db, Users, Posts, Resumes, Userposts, Userresumes, Agreement
from backend.db_utils import db_create_user, db_delete_user, db_edit_user, show_users, db_create_post, db_delete_post,db_create_resume,db_delete_resume,db_edit_post,db_edit_resume

# TODO: написать тест клиента при помощи app.test_client_class = FlaskLoginClient из библиотеки flask_login

login_manager = LoginManager()
#format is format for converting date from string to datetime
format_date = '%Y-%m-%d'

app = Flask(__name__, instance_relative_config=False)
cors = CORS(app)
app.config.update(
    CORS_HEADERS='Content-Type',
    DEBUG=True,
    SECRET_KEY='secret_xxx',
    SQLALCHEMY_DATABASE_URI='sqlite:///doo.db'
)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

"""@app.route('/home')
def kek():
   return "<h1>" + 'noone' + "'s Home</h1>"""

#TODO: объединить дом для гостей и пользователей (при помощи куска кода в телеге) сделано на 50%
"""
@app.route('/home')
def home():
    if current_user.is_authenticated():
        if db.session.execute(db.select(Users.is_employer).filter_by(id=current_user.id)).scalar_one():
            resumes = db.session.execute(db.select(Resumes)).scalars()
        # TODO: арзделить пользователей, кому что показывает

            return resumes

        else:
            posts = db.session.execute(db.select(Posts)).scalars()
            return posts
            #return "<h1>" + current_user.username + "'s Home</h1>"""


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if request.form['datapost'] != "0":
            return redirect(url_for('show_post', postid= request.form['datapost']))
        else:
            return redirect(url_for('show_resume', resumeid= request.form['dataresume']))
    else:
        resumes = db.session.execute(db.select(Resumes)).scalars()
        posts = db.session.execute(db.select(Posts)).scalars()
        if current_user.is_authenticated:
            user = db.session.execute(db.select(Users).filter_by(id=current_user.id)).scalar_one_or_none()
            user = str(user.is_employer)
            print(user)
            return render_template('guest_home.html', resumes= resumes, posts = posts, is_employer = user)
        else:
            return render_template('guest_home.html', resumes= resumes, posts = posts, is_employer = "False")

        


# TODO: дописать, что при неправильном вводе профиля, или пароля редирект и рядом ошибку
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.execute(db.select(Users).filter_by(username=username)).scalar_one_or_none()
        # print(user)
        if user != None:
            if user.password == password:
                print('Logged in..')
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("Wrong password")
                return redirect(url_for('login'))
                #return abort(401)
        else:
            flash("User doesnt exist")
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        input_date = datetime.strptime(request.form['birth_date'], format_date)
        age = input_date

        if request.form['is_employer']== "True":
            is_employer = True
        else:
            is_employer = False
        db_create_user(username, password, is_employer, firstname, lastname, age)
        return redirect(url_for('home'), 302, Response("Registered Successfully"))
    else:
        return render_template('register.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/delete_profile")
@login_required
def delete_profile():
    db_delete_user(current_user.id)
    logout_user()

    return redirect(url_for('home'))


@app.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = db.session.execute(db.select(Users).filter_by(username=current_user.username)).scalar_one()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['new_password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        input_date = datetime.strptime(request.form['birth_date'], format_date)
        age = input_date
        db_edit_user(user, username, password, firstname, lastname, age)
        return redirect(url_for('home'))

    else:
        return render_template('edit_profile.html', user_material = user)


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def show_bio():
    if request.method == 'POST':
        print(request.form['data'])
        return redirect(url_for('show_post', postid = request.form['data']))
    else:
        # TODO: показать резюме или свои объявления в зависимости от типа пользователя
        user = db.session.execute(db.select(Users).filter_by(username=current_user.username)).scalar_one()
        if user.is_employer is True:
            postsid = db.session.execute(db.select(Userposts.postid).filter_by(userid=current_user.id)).scalars().all()
            #postsid = Userposts.query.get_or_404()
            print(postsid)
            if postsid is not None:
                posts = db.session.execute(db.select(Posts).filter(Posts.id.in_(postsid))).scalars().all()
                print(posts)
                return render_template('profile.html',rows = posts, profile = user)
        else:
            resumesid = db.session.execute(db.select(Userresumes.resumeid).filter_by(userid=current_user.id)).scalars()
            if resumesid is not None:
                resumes = db.session.execute(db.select(Resumes).filter(Resumes.id.in_(resumesid))).scalars()
                # db.session.execute(db.select(Posts).filter_by(id.in_(postsid)).).scalars()
                return render_template('profile.html',rows = resumes, profile = user)
        #return {'username': user.username, 'id': user.id, 'firstname':user.firstname, 'lastname':user.lastname}


@app.route("/profile/<id>", methods=['GET', 'POST'])
def show_guest_bio(id):
    if request.method == 'POST':
        print(request.form['data'])
        return redirect(url_for('show_post', postid = request.form['data']))
    else:
        # TODO: показать резюме или свои объявления в зависимости от типа пользователя
        user = db.session.execute(db.select(Users).filter_by(id=id)).scalar_one()
        if user.is_employer is True:
            postsid = db.session.execute(db.select(Userposts.postid).filter_by(userid=id)).scalars().all()
            #postsid = Userposts.query.get_or_404()
            print(postsid)
            if postsid is not None:
                posts = db.session.execute(db.select(Posts).filter(Posts.id.in_(postsid))).scalars().all()
                print(posts)
                return render_template('guest_profile.html',rows = posts, profile = user)
        else:
            resumesid = db.session.execute(db.select(Userresumes.resumeid).filter_by(userid=id)).scalars()
            if resumesid is not None:
                resumes = db.session.execute(db.select(Resumes).filter(Resumes.id.in_(resumesid))).scalars()
                # db.session.execute(db.select(Posts).filter_by(id.in_(postsid)).).scalars()
                return render_template('guest_profile.html',rows = resumes, profile = user)


@app.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post_method():
    if current_user.is_employer:
        if request.method == 'POST':
        # TODO: написать скрипт создания поста
            newpostid =db_create_post(current_user.id,
                    request.form['title'],
                    request.form['text'],
                    request.form['skills'],
                    request.form['job_time'],
                    request.form['job_salary'])
            return redirect(url_for('show_post',postid = newpostid ))
        else:
            return render_template('create_post.html')
    else:
        redirect(url_for('home'))
    

@app.route("/post/<postid>", methods=['GET', 'POST'])
def show_post(postid):
    if request.method == 'POST':
        if request.form['button'] == 'Delete':
            db_delete_post(postid)
            return redirect(url_for('show_bio'))
        elif request.form['button'] == 'View':
            if current_user.id == request.form['data']:
                return redirect(url_for('show_bio'))
            else:
                return redirect(url_for('show_guest_bio',id = request.form['data']))
        else:
            return redirect(url_for('edit_post', postid = postid))

    else:

        post = db.session.execute(db.select(Posts).filter_by(id = postid)).scalar_one()
        post.seen += 1
        db.session.commit()
        userpost = db.session.execute(db.select(Userposts).filter_by(postid = postid)).scalar_one_or_none()
        if current_user.is_authenticated:
            if userpost == None or current_user.id != userpost.userid:
                return render_template("post.html", post= post, is_owner = "False", userpost = userpost, is_authenticated = "True")

            else:
                return render_template("post.html", post= post, is_owner = "True", userpost = userpost, is_authenticated = "True")
        else:
            return render_template("post.html", post= post, is_owner = "False", userpost = userpost, is_authenticated = "False")


# TODO: когда вызываю нажав на кнопку в объявлении редактировать(которую видит только автор), происходит редирект на этот юрл, postid= post.id
@app.route("/edit_post/<postid>", methods=['GET', 'POST'])
@login_required
def edit_post(postid):
    if request.method == 'POST':
        old_post = db.session.execute(db.select(Posts).filter_by(id = postid)).scalar_one()
        db_edit_resume(old_post, request.form['title'], request.form['text'], request.form['skills'], request.form['job_time'], request.form['job_salary'])
        return redirect(url_for('show_post', postid = postid))
    else:
        old_post = db.session.execute(db.select(Posts).filter_by(id = postid)).scalar_one()
        return render_template('edit_post.html', post_material = old_post)
# TODO: написать все темплейты для страниц



@app.route("/create_resume", methods=['GET', 'POST'])
@login_required
def create_resume_method():
    if request.method == 'POST':
        # TODO: написать скрипт создания поста
        newresumeid =db_create_resume(current_user.id,
                    request.form['title'],
                    request.form['text'],
                    request.form['skills'],
                    request.form['job_time'],
                    request.form['job_salary'])
        return redirect(url_for('show_resume',resumeid = newresumeid ))
    else:
        return render_template('create_resume.html')
    

@app.route("/resume/<resumeid>", methods=['GET', 'POST'])
def show_resume(resumeid):
    if request.method == 'POST':
        if request.form['button'] == 'Delete':
            db_delete_resume(resumeid)
            return redirect(url_for('show_bio'))
        else:
            return redirect(url_for('edit_resume', resumeid = resumeid))

    else:

        resume = db.session.execute(db.select(Resumes).filter_by(id = resumeid)).scalar_one()
        is_owner = db.session.execute(db.select(Userresumes).filter_by(resumeid = resumeid)).scalar_one_or_none()
        if current_user.is_authenticated:
            if is_owner == None or current_user.id != is_owner.userid:
                return render_template("resume.html", resume=resume, is_owner="False")
            else:
                return render_template("resume.html", resume=resume, is_owner="True")
        else:
            return render_template("resume.html", resume = resume, is_owner = "False")


# TODO: когда вызываю нажав на кнопку в объявлении редактировать(которую видит только автор), происходит редирект на этот юрл, postid= post.id
@app.route("/edit_resume/<resumeid>", methods=['GET', 'POST'])
@login_required
def edit_resume(resumeid):
    if request.method == 'POST':
        old_resume = db.session.execute(db.select(Resumes).filter_by(id = resumeid)).scalar_one()
        db_edit_resume(old_resume, request.form['title'], request.form['text'], request.form['skills'], request.form['job_time'], request.form['job_salary'])
        return redirect(url_for('show_resume', resumeid = resumeid))
    else:
        old_resume = db.session.execute(db.select(Resumes).filter_by(id = resumeid)).scalar_one()
        return render_template('edit_resume.html', resume_material = old_resume)

"""
@app.route('/user_list')
def user_list():
    user_list = Userposts.query.all()
    print(user_list)
    return render_template('graph.html', rows=user_list)

@app.route('/post_list')
def post_list():
    if request.method == 'POST':
        pass
    else:
        post_list = db.session.execute(db.select(Agreement).filter_by(ownerid =current_user.id)).scalars().all()
        resume = db.session.execute(db.select(Resumes))
    
    return render_template('graph.html', rows=post_list)

@app.route('/feedback_list')
def feedback_listing():
    user_list = Users.query.all()
    print(user_list)
    return render_template('graph.html', rows=user_list)"""

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

"""
@app.errorhandler(NoResultFound)
def user_doesnt_exist(e):
    return Response('<p>Object does not exist</p>')"""


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    get_user = db.session.execute(db.select(Users).filter_by(id=userid)).scalar_one_or_none()

    return get_user


@login_manager.unauthorized_handler
def unauthorized():
    if request.blueprint == 'api':
        abort(HTTPStatus.UNAUTHORIZED)
    return redirect(url_for('login'))
#TODO: придумать как возвращать при логине на первую страницу next=request.url


if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug=True)
