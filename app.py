import uuid
import re
from flask import Flask, request, render_template, redirect, url_for
from database import save_payload, fetch_payload

app = Flask(__name__)

def generate_random_hash():
    return str(uuid.uuid4())

def sanitize_payload(payload):
    
    # No XSS allowed! I have filtered all the bad words out using regex!!!
    # Now no one can use bad javascript functions in the message!
    
    #Only these characters allowed!
    chars =  re.compile(r"^[a-zA-Z,'+\\.()]+$")
    
    #None of these words allowed!
    words= re.compile('alert|prompt|eval|setTimeout|setInterval|Function|location|open|document|script|url|HTML|Element|href|String|Object|Array|Number|atob|call|apply|replace|assign|on|write|import|navigator|navigation|fetch|Symbol|name|this|window|self|top|parent|globalThis|new|proto|construct|xss')
    print(payload)
    if len(payload)<200 and re.match(chars, payload) and not re.findall(words, payload):
        return False 
    return True



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_payload():
    payload = request.form['payload']
    
    # Sanitize payload
    error = sanitize_payload(payload)
    if error:
        return render_template('index.html', error=error)
    unique_hash = generate_random_hash()

    save_payload(payload, unique_hash)

    bot_url = f"/view/{unique_hash}"
    return render_template('index.html', payload=payload, bot_url=bot_url)

@app.route('/view/<hash>')
def view_payload(hash):
    payload = fetch_payload(hash)
    if not payload:
        return "Invalid URL!", 404
    return f"<html><body>{payload}<script>{payload}</script></body></html>"

if __name__ == '__main__':
    app.run(debug=True)
