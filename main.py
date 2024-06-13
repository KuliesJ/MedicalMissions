from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import bcrypt
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'app.OsJoMeMi'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

@app.context_processor
def utility_processor():
    def is_admin():
        if 'user_id' in session:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT is_admin FROM users WHERE id = ?", (session['user_id'],))
            user = cursor.fetchone()
            conn.close()
            if user and user[0] == 1:
                return True
        return False
    
    return dict(is_admin=is_admin)

def is_admin():
        if 'user_id' in session:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT is_admin FROM users WHERE id = ?", (session['user_id'],))
            user = cursor.fetchone()
            conn.close()
            if user and user[0] == 1:
                return True
        return False

@app.route('/')
def index():
    return render_template("index.html")

def get_posts_by_section(section):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE section = ? ORDER BY `order` ASC, created_at DESC", (section,))
    posts = cursor.fetchall()
    conn.close()
    return posts

@app.route('/goals_and_services')
def goalsServices():
    posts = get_posts_by_section('goals_and_services')
    return render_template("goals_services.html", posts=posts)

@app.route('/next_mission')
def nextMission():
    posts = get_posts_by_section('next_mission')
    return render_template("next_mission.html", posts=posts)

@app.route('/donations')
def donations():
    return render_template("donations.html")

@app.route('/contact_us')
def contactUs():
    posts = get_posts_by_section('contact_us')
    return render_template("contact_us.html", posts=posts)

@app.route('/photo_videos')
def photoVideos():
    posts = get_posts_by_section('photo_videos')
    return render_template("photo_videos.html", posts=posts)

@app.route('/terms_and_conditions')
def termsAndConditions():
    posts = get_posts_by_section('terms_and_conditions')
    return render_template('terms.html', posts=posts)

@app.route('/about_peru')
def aboutPeru():
    return render_template('about_peru.html')

@app.route('/previous_missions')
def previousMissions():
    posts = get_posts_by_section('previous_missions')
    return render_template("previous_missions.html", posts=posts)

@app.route('/login_account', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE Email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[6]):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route('/create_post', methods=['GET', 'POST'])
def createPost():
    if 'user_id' not in session or not is_admin():
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title', None)
        subtitle = request.form.get('subtitle', None)
        content = request.form.get('content', None)
        image_file = request.files['image'] if 'image' in request.files else None
        section = request.form.get('section', None)
        
        if not (title or subtitle or content or image_file):
            return render_template('create_post.html', error="Please provide valid content.")
        
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_url = f'static/uploads/{filename}'
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO posts (title, subtitle, content, image, section) VALUES (?, ?, ?, ?, ?)",
                           (title, subtitle, content, image_url, section))
            conn.commit()
            conn.close()
        else:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO posts (title, subtitle, content, image, section) VALUES (?, ?, ?, ?, ?)",
                           (title, subtitle, content, None, section))
            conn.commit()
            conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('create_post.html')

@app.route('/edit_content', methods=['GET', 'POST'])
def editContent():
    if 'user_id' not in session or not is_admin():
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        section = request.form.get('section', None)
        if section:
            posts = get_posts_by_section(section)
            return render_template('edit_content.html', posts=posts, section=section)
    
    return render_template('select_section.html')

@app.route('/edit_posts', methods=['GET', 'POST'])
def editPosts():
    if 'user_id' not in session or not is_admin():
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        post_id = request.form.get('post_id')
        action = request.form.get('action')

        if action == 'edit':
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
            post = cursor.fetchone()
            conn.close()
            
            if post:
                return render_template('edit_post.html', post=post)
            else:
                flash('Post not found', 'error')
                return redirect(request.referrer or url_for('index'))

        elif action == 'save':
            title = request.form.get('title')
            subtitle = request.form.get('subtitle')
            content = request.form.get('content')
            image_file = request.files.get('image')
            
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            if image_file:
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                image_url = f'static/uploads/{filename}'
                cursor.execute("""
                    UPDATE posts SET title = ?, subtitle = ?, content = ?, image = ? WHERE id = ?
                """, (title, subtitle, content, image_url, post_id))
            else:
                cursor.execute("""
                    UPDATE posts SET title = ?, subtitle = ?, content = ? WHERE id = ?
                """, (title, subtitle, content, post_id))
            
            conn.commit()
            conn.close()

            flash('Post updated successfully', 'success')
            return redirect(url_for('index'))

        elif action == 'delete':
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT image FROM posts WHERE id = ?", (post_id,))
            post = cursor.fetchone()
            
            if post:
                image_path = post[0]
                cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
                conn.commit()
                conn.close()
                
                if image_path:
                    full_image_path = os.path.join(app.root_path, image_path)
                    if os.path.exists(full_image_path):
                        os.remove(full_image_path)
                
                flash('Post deleted successfully', 'success')
            else:
                flash('Post not found', 'error')
            
            return redirect(request.referrer or url_for('index'))
        elif action == 'move_up' or action == 'move_down':
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute("SELECT section, `order` FROM posts WHERE id = ?", (post_id,))
            post = cursor.fetchone()
            section, current_order = post[0], post[1]

            if action == 'move_up':
                new_order = current_order - 1
            elif action == 'move_down':
                new_order = current_order + 1

            cursor.execute("""
                UPDATE posts SET `order` = ? WHERE section = ? AND `order` = ?
            """, (current_order, section, new_order))
            cursor.execute("""
                UPDATE posts SET `order` = ? WHERE id = ?
            """, (new_order, post_id))

            conn.commit()
            conn.close()

            flash('Post order updated successfully', 'success')
            return redirect(request.referrer or url_for('index'))
        
    return redirect(request.referrer or url_for('index'))

        
        
    

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
