from flask import Flask,request,render_template,flash,redirect
from preprocess import prep , dataloader
from prediction import prediction 
from werkzeug.utils import secure_filename
import os 
from ocr import ocr
import secrets

secret_key = secrets.token_hex(16)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png'}
app.secret_key = secret_key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/img')
def img():
    return render_template('img.html')

@app.route('/manual')
def manual():
    return render_template('manual.html')

@app.route('/help')
def help():
    return render_template('help.html')
@app.route('/training')
def train():
    return render_template('train.html')
def evaluate_answers_manual():
    ideal_answer = request.form['ideal-answer']
    student_answer = request.form['student-answer']
    max_marks = request.form['max-marks']
    checking_type = request.form['checking-type']
    
    if not ideal_answer.strip() or not student_answer.strip() or not max_marks.strip():
        flash('Please fill in all the required fields.')
        return render_template('error.html',redirect_url='manual')

    ideal = prep(ideal_answer)
    student = prep(student_answer)

 
    query = dataloader(ideal,student)

    proba , idx = prediction(query)
 

    return render_template('result.html', marks={idx})

### SHIFT THEM INTO EVALUATION.PY
def evaluate_answer_image():
    # Check if the post request has the file part
    if 'ideal-answer-input' not in request.files or 'student-answer-input' not in request.files:
        flash('No file part')
        return render_template("error.html",redirect_url='img') 

    ideal_answer_file = request.files['ideal-answer-input']
    student_answer_file = request.files['student-answer-input']
    max_marks = request.form['max-marks']
    checking_type = request.form['checking-type']


    if not max_marks.strip():
        flash('Please enter maximum marks')
        return render_template("error.html",redirect_url='img') 
    if ideal_answer_file.filename == '' or student_answer_file.filename == '':
        flash('No selected file')
        return render_template("error.html",redirect_url='img')

    if ideal_answer_file and allowed_file(ideal_answer_file.filename) and student_answer_file and allowed_file(student_answer_file.filename):

        ideal_answer_filename = secure_filename(ideal_answer_file.filename)
        student_answer_filename = secure_filename(student_answer_file.filename)
        
        ideal_answer_path = os.path.join(app.config['UPLOAD_FOLDER'], 'ideal'+ideal_answer_filename)
        student_answer_path = os.path.join(app.config['UPLOAD_FOLDER'], 'student'+student_answer_filename)
        
        ideal_answer_file.save(ideal_answer_path)
        student_answer_file.save(student_answer_path)

        ideal = ocr(ideal_answer_path)
        student = ocr(student_answer_path)

        ideal = prep(ideal)
        student = prep(ideal)

        query = dataloader(ideal,student)

        proba , idx = prediction(query)
        return render_template('result.html',marks={idx})
    
    else :
        return render_template('error.html',redirect_url='img')

@app.route('/result/', methods=['POST'])
def result():
    img = request.form.get('image')
    if img == None:
        return evaluate_answers_manual()
    else : 
  
        return evaluate_answer_image()
@app.route('/img', methods=['POST'])
def index():
        # Handle ideal answer image upload
        ideal_answer_image = request.files.get('ideal_answer_image', None)
        if ideal_answer_image:
            ideal_answer_filename = secure_filename(ideal_answer_image.filename)
            ideal_answer_image.save(os.path.join(app.config['UPLOAD_FOLDER'], ideal_answer_filename))

        # Handle student answer image upload
        student_answer_image = request.files.get('student_answer_image', None)
        if student_answer_image:
            student_answer_filename = secure_filename(student_answer_image.filename)
            student_answer_image.save(os.path.join(app.config['UPLOAD_FOLDER'], student_answer_filename))

        

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__=="__main__":
    app.run(debug=True)