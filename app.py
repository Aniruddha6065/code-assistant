from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from models import db, User, History
from forms import LoginForm, RegistrationForm

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[os.getenv('RATE_LIMIT', '10/minute')]
)

# Initialize Google Gemini
google_api_key = os.getenv('GOOGLE_API_KEY')
if not google_api_key:
    logger.warning("GOOGLE_API_KEY not found in environment variables")
    logger.warning("Please set GOOGLE_API_KEY in your .env file")
    genai.configure(api_key="dummy-key")
else:
    logger.info("Google API key found and configured")
    genai.configure(api_key=google_api_key)
    try:
        # List available models
        models = genai.list_models()
        logger.info("Available models:")
        for model in models:
            logger.info(f"- {model.name}")
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")

# Load responses
def load_responses():
    try:
        with open('responses.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("responses.json file not found")
        return {}

RESPONSES = load_responses()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Check if user exists
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already exists')
                return redirect(url_for('register'))
            
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered')
                return redirect(url_for('register'))
            
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error: {str(e)}")
            flash('An error occurred during registration')
            return redirect(url_for('register'))
            
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/history')
@login_required
def history():
    user_history = History.query.filter_by(user_id=current_user.id).order_by(History.created_at.desc()).all()
    return render_template('history.html', history=user_history)

@app.route('/api/ask', methods=['POST'])
@limiter.limit(os.getenv('RATE_LIMIT', '10/minute'))
@login_required
def ask():
    try:
        data = request.json
        language = data.get('language', '').lower()
        question = data.get('question', '').strip()
        
        if not language or not question:
            return jsonify({'error': 'Language and question are required'}), 400
            
        # Try to find predefined response
        response = None
        for key in RESPONSES.get(language, {}):
            if key in question.lower():
                response = RESPONSES[language][key]
                break
        
        # If no predefined response, use Google Gemini
        if not response and google_api_key:
            try:
                logger.info(f"Using Google Gemini for question: {question}")
                model = genai.GenerativeModel('gemini-1.5-pro')
                prompt = f"You are a helpful programming assistant specializing in {language}. Please answer the following question: {question}"
                response = model.generate_content(prompt).text
                logger.info("Successfully got response from Google Gemini")
            except Exception as e:
                logger.error(f"Google Gemini error: {str(e)}")
                response = f"Sorry, I encountered an error while processing your request. Error details: {str(e)}"
        elif not response:
            logger.warning("No Google API key found and no predefined response available")
            response = "Sorry, I cannot process your request at this time. Please try again later."
        
        # Save to history
        history_entry = History(
            user_id=current_user.id,
            language=language,
            question=question,
            response=response
        )
        db.session.add(history_entry)
        db.session.commit()
        
        return jsonify({
            'response': response,
            'language': language,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded'}), 429

def init_app():
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    app = init_app()
    app.run(debug=True)
