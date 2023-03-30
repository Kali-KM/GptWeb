from flask import Flask, render_template, request
import sys
import openai

app = Flask(__name__)
try:
    with open('.env', 'r') as f:
        data = f.read()
        openai.api_key = data[15:]
except:
    print('After creating the .env file you should note OPENAI_API_KEY=[YOUR_KEY] .')
    sys.exit(0)

messages = []
question_list = []
answer_list = []

@app.route('/error', methods=['GET'])
def err_page():
    return render_template('error.html')

@app.route('/run', methods=['POST'])
def run_route():
    messages.clear()
    question_list.clear()
    answer_list.clear()
    print('clear...')
    return 'success'

@app.route('/python', methods=['GET', 'POST'])
def home_pyhton():
    messages.append(
        {"role": "system", "content": "You are a coding tutor bot to help user write and optimize python code."}
    )
    question = request.form.get('question')
    if question:
        answer = ask_chatGPT(question)        
        if question not in question_list: 
            question_list.append(question) 
            answer_list.append(answer)
    else:
        answer = ""
    return render_template('home_python.html', question_list=question_list, answer_list=answer_list)

@app.route('/', methods=['GET', 'POST'])
def home():
    messages.append(
        {"role": "system", "content": "You are a helpful assistant."}
    )
    question = request.form.get('question')
    if question:
        answer = ask_chatGPT(question)        
        if question not in question_list: 
            question_list.append(question) 
            answer_list.append(answer)
    else:
        answer = ""
    return render_template('home.html', question_list=question_list, answer_list=answer_list)   

def ask_chatGPT(prompt):
    try:
        messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        result = {"role": "assistant", "content": response["choices"][0]["message"].content}
        messages.append(result)
    except openai.error.RateLimitError:
        return render_template('error_billing.html')
    except Exception as e:
        print(e)
        return render_template('error.html')
    return result["content"]


if __name__ == '__main__':
    app.run(debug=True)
    
