from flask import Flask,request,render_template,flash,redirect
from app.preprocess import prep , dataloader
from app.prediction import prediction 
from werkzeug.utils import secure_filename
import os 
from app.ocr import ocr
import hashlib
import shutil
from app.evaluation import evaluation


def generate_secret_key():
    random_bytes = os.urandom(16)
    return hashlib.sha256(random_bytes).hexdigest()

secret_key = generate_secret_key()
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
    p_correct = proba[0][0][2]
    p_incorrect = proba[0][0][1]
    p_partial = proba[0][0][0]
    marks = evaluation(checking_type=checking_type,max_marks=max_marks,p_correct=p_correct,
        p_incorrect =  p_incorrect,p_partial =  p_partial,idx = idx)
    return render_template('result.html', marks=marks)

### SHIFT THEM INTO EVALUATION.PY
def evaluate_answer_image():
    # Temporary folder to store uploaded files
    temp_folder = 'temp_uploads'
    os.makedirs(temp_folder, exist_ok=True)  # Create temp folder if not exists
    
    # Check if the post request has the file part
    if 'ideal-answer-input' not in request.files or 'student-answer-input' not in request.files:
        flash('No file part')
        return render_template("error.html", redirect_url='img') 

    ideal_answer_file = request.files['ideal-answer-input']
    student_answer_file = request.files['student-answer-input']
    max_marks = request.form['max-marks']
    checking_type = request.form['checking-type']

    if not max_marks.strip():
        flash('Please enter maximum marks')
        return render_template("error.html", redirect_url='img') 
    
    if ideal_answer_file.filename == '' or student_answer_file.filename == '':
        flash('No selected file')
        return render_template("error.html", redirect_url='img')

    # Save uploaded files to temp folder
    ideal_answer_filename = secure_filename(ideal_answer_file.filename)
    student_answer_filename = secure_filename(student_answer_file.filename)
    
    ideal_answer_path = os.path.join(temp_folder, 'ideal_' + ideal_answer_filename)
    student_answer_path = os.path.join(temp_folder, 'student_' + student_answer_filename)
    
    ideal_answer_file.save(ideal_answer_path)
    student_answer_file.save(student_answer_path)

    try:
        # Perform OCR on the uploaded images
        ideal_text = ocr(ideal_answer_path)
        student_text = ocr(student_answer_path)

        # Process the extracted text (e.g., preprocess, convert to required format)
        ideal_processed = prep(ideal_text)
        student_processed = prep(student_text)

        # Perform evaluation based on processed text
        query = dataloader(ideal_processed, student_processed)
        proba, idx = prediction(query)
        
        p_correct = proba[0][0][2]
        p_incorrect = proba[0][0][1]
        p_partial = proba[0][0][0]
        
        marks = evaluation(checking_type=checking_type, max_marks=max_marks,
                           p_correct=p_correct, p_incorrect=p_incorrect,
                           p_partial=p_partial, idx=idx)
        
        return render_template('result.html', marks=marks)
    
    except Exception as e:
        # Handle any exceptions that may occur during OCR or evaluation
        print("Error:", e)
        flash('Error processing files')
        return render_template("error.html", redirect_url='img')
    
    finally:
        # Delete temporarily stored files after processing
        shutil.rmtree(temp_folder)
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
