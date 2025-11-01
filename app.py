from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "your_secret_key_change_this_in_production"

# Directory to save uploaded notes
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory user storage (replace with database in production)
users = {}

# Temporary storage for memes comments
memes_comments = []

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not name or not email or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))
        
        if email in users:
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))
        
        # Store user with hashed password
        users[email] = {
            'name': name,
            'password': generate_password_hash(password)
        }
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users and check_password_hash(users[email]['password'], password):
            session['user_email'] = email
            session['user_name'] = users[email]['name']
            flash(f'Welcome back, {users[email]["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('landing'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user_name=session.get('user_name'))

@app.route('/scholarships')
@login_required
def scholarships():
    return render_template('scholarships.html')

@app.route('/internships')
@login_required
def internships():
    return render_template('internships.html')

@app.route('/Courses')
@login_required
def courses():
    return render_template('Courses.html')

@app.route('/projects')
@login_required
def projects():
    return render_template('projects.html')

@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        if 'note_file' in request.files:
            file = request.files['note_file']
            branch = request.form.get('branch')
            
            if file.filename != "" and branch:
                # Create branch-specific folder
                branch_folder = os.path.join(app.config['UPLOAD_FOLDER'], branch)
                os.makedirs(branch_folder, exist_ok=True)
                
                # Save file
                file.save(os.path.join(branch_folder, file.filename))
                flash('Note uploaded successfully!', 'success')
                return redirect(url_for('notes'))
    
    return render_template('notes.html')

@app.route("/view-notes")
@login_required
def view_notes():
    # Get all files organized by branch
    notes_by_branch = {}
    
    if os.path.exists(app.config["UPLOAD_FOLDER"]):
        for branch in os.listdir(app.config["UPLOAD_FOLDER"]):
            branch_path = os.path.join(app.config["UPLOAD_FOLDER"], branch)
            if os.path.isdir(branch_path):
                files = os.listdir(branch_path)
                if files:
                    notes_by_branch[branch] = files
    
    return render_template("view_notes.html", notes_by_branch=notes_by_branch)

@app.route('/uploads/<branch>/<filename>')
@login_required
def uploaded_file(branch, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], branch), filename)

@app.route('/memes', methods=['GET', 'POST'])
@login_required
def memes():
    global memes_comments
    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:
            memes_comments.append({
                'user': session.get('user_name'),
                'comment': comment
            })
            flash('Comment added!', 'success')
        return redirect(url_for('memes'))
    return render_template('memes.html', comments=memes_comments)

if __name__ == "__main__":
    app.run(debug=True)