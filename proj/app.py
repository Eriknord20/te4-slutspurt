from flask import Flask, render_template, request, redirect
from flask_babel import Babel, gettext
from models.base import Role, User, UserRole
from config import LANGUAGES
APP = Flask(__name__, static_url_path='/', static_folder='build/html/')
APP.config.from_pyfile('config.py')
BABEL = Babel(APP)


@BABEL.localeselector
def get_locale():
    result = request.accept_languages.best_match(LANGUAGES.keys())
    print(result)
    return result


@APP.route("/")
def index():
    """
    Redirects you to /user route
    """
    return redirect("/user")

# @APP.route("/user")
# def user():
#     return render_template("add.html")


@APP.route("/user", methods=['GET'])
def get_user():
    """
    Get all users form database

    :Returns: Renders a template that has a list of all users
    """
    user = User()
    role = Role()
    mylist = user.all_rel()
    roles = role.all()
    user.connection.kill()
    role.connection.kill()
    return render_template('add.html', result=mylist, result2=roles)


@APP.route("/user", methods=['POST'])
def add_user():
    """
    Submits user info to get inserted into to database table

    :Returns: redirects you back to the /user route
    :rtype: route
    """
    user = User()
    user_role = UserRole()
    formlist = []
    urlist = []
    if type(request.form['name'] == str):
        formlist.append(request.form['id'])
        formlist.append(request.form['name'])
    else:
        return redirect("/user")
    user.insert(formlist)
    user_id = user.find_by_name('user_name', request.form['name'])
    print(user_id)
    urlist.append(user_id[0][0])
    urlist.append(request.form['role'])
    print(urlist)
    user_role.insert(urlist)
    user.connection.kill()
    user_role.connection.kill()
    return redirect("/user")
    # redirect(url_for('success',name = mylist))


@APP.route("/user/<int:_id>", methods=['GET'])
def get_edit(_id):
    """
    Renders a form where you can update a users information

    :param _id:  The function uses the id of the user to find all the informatio
    :type _id: Integer

    :Returns: It returns a function that already has a users information filed in
    """
    user = User()
    role = Role()

    userdata = user.find_by_id(_id)
    roledata = role.get_role_by_user_id(_id)
    allroles = role.all()
    user.connection.kill()
    role.connection.kill()
    return render_template('update.html', userdata=userdata, roledata=roledata, allroles=allroles)


@APP.route("/user/<int:_id>", methods=['POST'])
def submit_edit(_id):
    """
    Submits a form where all changes to the user is updated in database table

    :param _id: The function uses the id of the user to find all the information
    :type _id: Integer

    :Return: It redirects you to /user route
    """
    user = User()
    user_role = UserRole()
    formlist = []
    formlist.append(_id)
    formlist.append(request.form['name'])
    keylist = ['id', 'user_name']
    print(request.form)
    ur_id = user_role.find_by_name('user_id', _id)
    for x in ur_id:
        user_role.delete(x[0])
    for form in request.form:
        if form[0] == 'name':
            user.update(keylist, formlist, _id)
        user_role.insert([_id, form[1]])
    user.connection.kill()
    user_role.connection.kill()
    return redirect("/user")


@APP.route('/user/<int:_id>/delete')
def delete(_id):
    """
    Submits a form where the users gets deleted from the database table ]

    :param _id: The function uses the id of the user to find all the information and then deletes it
    :type _id: Integer

    :Return: It redirects you to /user route
    """
    user = User()
    user_role = UserRole()
    user_role.delete(_id)
    user.delete(_id)
    user.connection.kill()
    user_role.connection.kill()
    return redirect('/user')


@APP.route('/show')
def show():
    """
    Shows all users

    :Return: returns a template with a list of all users
    """
    role = Role()
    rows = role.all()
    role.connection.kill()
    return render_template('result.html', result=rows)


@APP.route('/docs/<path:path>')
def serve_sphinx_docs(path='index.html'):
    """
    Renders a page where you can find all the documentation]

    :param path: defaults to 'index.html'
    :type path: str, optional

    :Return: Documention
    """
    return APP.send_static_file(path)
