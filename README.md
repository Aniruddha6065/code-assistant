# Code Assistant

A web-based code assistant that helps answer questions about C, C++, Python, and Java programming languages. Built with Python Flask and featuring a modern, responsive UI.

## Features

- Simple and modern web interface with syntax highlighting
- Support for multiple programming languages (C, C++, Python, Java)
- Real-time responses with code examples
- Comprehensive coverage of programming concepts
- Responsive design for all devices
- Interactive suggestion tags for quick access to common topics

## Supported Topics

### Python
- Hello World programs
- Loops and iterations
- Functions and decorators
- Classes and objects
- Lists and dictionaries
- File handling
- Modules and packages
- Generators and lambda functions
- List comprehensions

### Java
- Hello World programs
- Loops and iterations
- Functions and methods
- Classes and objects
- Arrays and collections
- Interfaces and inheritance
- Enums and threads
- File handling
- Packages

### C
- Hello World programs
- Loops and iterations
- Functions
- Structures and unions
- Pointers and memory management
- Arrays
- File handling
- Bitwise operations
- Preprocessor directives

### C++
- Hello World programs
- Loops and iterations
- Functions
- Classes and objects
- Templates
- Smart pointers
- Vectors and strings
- File handling
- Operator overloading
- Namespaces

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/code-assistant.git
cd code-assistant
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Select a programming language from the dropdown menu
2. Type your question in the text area
3. Click "Ask Question" to get a response
4. The response will be displayed with syntax highlighting
5. Use the suggestion tags below to quickly try different topics

## Project Structure

```
code-assistant/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/
│   └── css/
│       └── style.css  # Stylesheet
├── templates/
│   └── index.html     # Main HTML template
└── README.md          # Project documentation
```

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask for the web framework
- Highlight.js for syntax highlighting
- Google Fonts for typography 