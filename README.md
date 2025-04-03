# SLR Parser Web Application

This is a Flask-based web application that simulates an SLR (Simple LR) parser. The application takes a parsing table, grammar rules, and an input string in JSON format and determines whether the input string is accepted or rejected based on the provided grammar and parsing table.

## Features
- Input parsing table and grammar rules in JSON format.
- Parses an input string according to SLR parsing rules.
- Displays parsing steps, stack movements, and actions taken.
- Provides clear error messages for incorrect inputs.
- Responsive UI with a clean design using Bootstrap.

## Installation & Setup

### Prerequisites
Make sure you have Python installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).

### Clone the Repository
```sh
git clone https://github.com/your-username/slr-parser.git
cd slr-parser
```

### Install Dependencies
```sh
pip install flask
```

### Run the Application
```sh
python app.py
```
The application will start on `http://127.0.0.1:5000/`.

## Usage
1. Open the web application in your browser.
2. Enter the parsing table in JSON format.
3. Enter the grammar rules in JSON format.
4. Input the string to parse.
5. Click the **Parse** button.
6. View the parsing result and step-by-step parsing process.

### Input String
```
a b
```

## File Structure
```
slr-parser/
│── static/
│   └── style.css  # CSS file for styling
│── templates/
│   └── index.html # HTML template for UI
│── app.py         # Main Flask application
│── README.md      # Project documentation
```

## Technologies Used
- **Flask** - Backend framework
- **HTML/CSS** - Frontend UI
- **Bootstrap** - Styling & responsiveness
- **Python** - Logic & parsing implementation

