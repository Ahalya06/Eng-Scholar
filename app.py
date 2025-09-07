from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Directory to save uploaded notes
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Temporary storage for memes comments
memes_comments = []

# Dummy login credentials
USER_EMAIL = "admin@engihub.com"
USER_PASSWORD = "password123"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scholarships')
def scholarships():
    return render_template('scholarships.html')

@app.route('/internships')
def internships():
    return render_template('internships.html')

@app.route('/Courses')
def courses():
    return render_template('Courses.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    if request.method == 'POST':
        if 'note_file' in request.files:
            file = request.files['note_file']
            if file.filename != "":
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                return redirect(url_for('notes'))
    return render_template('notes.html', files=uploaded_files)
@app.route("/view-notes")
def view_notes():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("view_notes.html", files=files)

@app.route('/memes', methods=['GET', 'POST'])
def memes():
    global memes_comments
    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:
            memes_comments.append(comment)
        return redirect(url_for('memes'))
    return render_template('memes.html', comments=memes_comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == USER_EMAIL and password == USER_PASSWORD:
            return redirect(url_for('home'))
        else:
            error = "Invalid email or password!"
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)





