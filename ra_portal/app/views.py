from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, getData
from forms import LoginForm,EditForm,PostForm,SearchForm,CommentForm, ContainerForm,NewViewForm
from models import User, ROLE_USER, ROLE_ADMIN,Comment,View,Control_container
from datetime import datetime
from config import MAX_SEARCH_RESULTS
from flask.ext.wtf import Form
from werkzeug import secure_filename
from flask import send_from_directory
import sys, os
import json
from wtforms.ext.appengine.db import model_form
 

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
        g.user_views=[(i.id,i.name) for i in g.user.followed_views().all()]

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body = form.post.data, timestamp = datetime.utcnow(), author = g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts=''

    return render_template('index.html',
        title = 'Home',
        form = form,
        posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error=None
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email = request.form['openid']).first()
            if user is not None:
                remember_me = form.remember_me.data
                login_user(user, remember = remember_me)
                return redirect(request.args.get('next') or url_for('index'))
            else:
                error='Invalid credentials'
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        error=error)
            


@app.route('/logout')
def logout():
    logout_user()    
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    return render_template('user.html',
        user = user,
        posts = '')

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html',
        form = form)

@app.route('/home', methods = ['GET', 'POST'])
@login_required
def views():
    views = View.query.all()
    try:
        allViews= [(x, g.user.is_following(x)) for x in views]
    except:
        pass
    return render_template('views.html',
        allViews = allViews)

@app.route('/view/<id>')
@login_required
def one_view(id):
    name = View.query.filter_by(id=id).first().name
    view=View.query.filter_by(id=id).first().subscribed_controls().all()
    #data=getControlData.getNF(view)
    data=[(container,container.comments.all(),getData.getNF(container.name)) for container in view]
    return render_template('one_view.html',
        name = name, data=data)

@app.route('/all_containers')
@login_required
def all_containers():
    view=Control_container.query.all()
    name='All'
    data=[(container,container.comments.all(),getData.getNF(container.name)) for container in view]
    return render_template('one_view.html',
        name = name, data=data)

@app.route('/new_view', methods = ['GET','POST'])
@login_required
def new_view():
    form = NewViewForm()
    if form.validate_on_submit():
        view = View(name = form.name.data, description = form.desc.data, creation_date = datetime.utcnow(), user_id = g.user.id)
        db.session.add(view)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for("index"))
    elif request.method != "POST":
        pass
    return render_template("new_view.html", form=form)

@app.route('/follow_view/<id>')
@login_required
def follow_view(id):
    view = View.query.filter_by(id=id).first()
    u = g.user.follow_view(view)
    db.session.add(u)
    db.session.commit()
    return redirect(request.referrer or url_for('index'))

@app.route('/unfollow_view/<id>')
@login_required
def unfollow_view(id):
    view = View.query.filter_by(id=id).first()
    u = g.user.unfollow_view(view)
    db.session.add(u)
    db.session.commit()
    return redirect(request.referrer or url_for('index'))
    
@app.route('/search', methods = ['GET','POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query = g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Control_container.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    data=[(container,container.comments.all(),getData.getNF(container.name)) for container in results]
    return render_template('one_view.html',
        name = query, data=data, search=1)

@app.route('/edit_comment/<id>', methods = ['GET', 'POST'])
@login_required
def edit_comment(id):
    comment=Comment.query.filter_by(id=id).first()
    form = CommentForm(comment)
    if form.validate_on_submit():
        comment.happened = form.happened.data
        comment.text = form.text.data
        comment.incidentnum=form.incidentnum.data
        comment.realf=form.realf.data
        comment.monthlyf=form.monthlyf.data
        comment.newf=form.newf.data
        comment.freenotef=form.freenotef.data
        comment.user_id=g.user.id
        try:
            file = request.files['fileName']
            fileName = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
            comment.fileUrl=fileName
        except:
            print str(sys.exc_info())
        db.session.add(comment)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(request.form['previous_url']  or url_for('index'))
    elif request.method != "POST":
        form.happened.data = comment.happened 
        form.text.data = comment.text
        form.incidentnum.data = comment.incidentnum
        form.realf.data = comment.realf
        form.monthlyf.data = comment.monthlyf
        form.newf.data = comment.newf
        form.freenotef.data=comment.freenotef
        fileUrl = comment.fileUrl
    return render_template('edit_comment.html',
        form = form, comment=comment,action_form='',previous_url=request.referrer, fileUrl=fileUrl)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/new_comment/<container_id>', methods = ['GET', 'POST'])
@login_required
def new_comment(container_id):
        comment = Comment( noticed=datetime.now(),user_id=g.user.id,report_unit_id=container_id,happened=datetime.now())
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('edit_comment',id=comment.id))


@app.route('/delete_comment/<id>', methods = ['GET', 'POST'])
@login_required
def delete_comment(id):
    comment=Comment.query.filter_by(id=id).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(request.referrer or url_for('index'))
        
@app.route('/edit_container/<id>', methods = ['GET', 'POST'])
@login_required
def edit_container(id):
    container=Control_container.query.filter_by(id=id).first()
    form = ContainerForm(container)
    if form.validate_on_submit():
        if container.name==form.name.data:
            pass
        else:
            container.name =Control_container.make_unique_name(form.name.data)
        container.description = form.description.data
        container.meta = request.form['meta']
        container.g_config = form.g_config.data
        container.sql_script = form.sql_script.data
        container.update_time = form.update_time.data
        db.session.add(container)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect( request.form['previous_url'] or url_for('index'))

    elif request.method != "POST":        
        form.name.data = container.name 
        form.description.data = container.description
        meta = container.meta
        form.g_config.data = container.g_config
        form.sql_script.data = container.sql_script
        form.update_time.data = container.update_time

    return render_template('edit_container.html',
        form = form, meta=meta, container=container,id=container.id,previous_url=request.referrer)

@app.route('/new_container/', methods = ['GET', 'POST'])
@login_required
def new_container():
    name='new'+str(datetime.now())
    container=Control_container(name=name, meta='unknown')
    db.session.add(container)
    db.session.commit()
    return redirect(url_for('edit_container',id=container.id))

@app.route('/delete_container/<id>', methods = ['GET', 'POST'])
@login_required
def delete_container(id):
    db.session.execute('DELETE FROM comment WHERE report_unit_id='+str(id))
    db.session.execute('DELETE FROM view_control WHERE control_id='+str(id))
    db.session.execute('DELETE FROM user_control WHERE control_id='+str(id))
    db.session.execute('DELETE FROM control_container WHERE id='+str(id))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/_get_user_views', methods = ['GET'])
def _get_user_views():
    id = request.args.get('id')
    views =jsonify(v=[{'id':x.id, 'name':x.name,'isFollowing':x.is_following_container(id)} for x in g.user.views.all()])
    return views
   
@app.route('/_follow_container', methods = ['GET'])
def _follow_container():
    container_id = request.args.get('container_id')
    view_id = request.args.get('view_id')
    view = View.query.filter_by(id=view_id).first()
    v = view.follow_container(container_id)
    db.session.add(v)
    db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/_unfollow_container', methods = ['GET'])
def _unfollow_container():
    container_id = request.args.get('container_id')
    view_id = request.args.get('view_id')
    view = View.query.filter_by(id=view_id).first()
    v = view.unfollow_container(container_id)
    db.session.add(v)
    db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


