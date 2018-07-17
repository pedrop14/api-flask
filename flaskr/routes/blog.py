import functools

from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, jsonify)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

blog_bp = Blueprint('blog', __name__)
blog_bp.endpoint = '/'  

@blog_bp.route('/blog')
def index():
    db = get_db()
    posts = db.execute( 
        """
        SELECT p.id, title, body, created, author_id, username
        FROM post p JOIN user u ON p.author_id = u.id
        ORDER BY created DESC
        """
    ).fetchall()
    return jsonify(posts)

@blog_bp.route('/create', methods= ('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )