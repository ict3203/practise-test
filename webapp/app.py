from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape

app = Flask(__name__)

def is_xss_attack(search_term):
    # Simple check for potential XSS attack (you may need more sophisticated validation)
    return '<script>' in search_term

def is_sql_injection_attack(search_term):
    # Simple check for potential SQL injection attack (you may need more sophisticated validation)
    return "'" in search_term

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_term = request.form['search_term']

        # Validate for XSS attack
        if is_xss_attack(search_term):
            # If XSS attack, clear input and remain on home page
            return render_template('home.html', error='Invalid search term. Please try again.')

        # Validate for SQL injection attack
        if is_sql_injection_attack(search_term):
            # If SQL injection attack, clear input and remain on home page
            return render_template('home.html', error='Invalid search term. Please try again.')

        # If input is valid, go to a new page to display the search term
        return redirect(url_for('result', search_term=escape(search_term)))

    # For GET requests or initial load, render the home page
    return render_template('home.html', error=None)

@app.route('/result/<search_term>')
def result(search_term):
    return render_template('result.html', search_term=escape(search_term))

if __name__ == '__main__':
    app.run(debug=True)
