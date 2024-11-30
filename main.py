from flask.views import MethodView
from flask import Flask, render_template, redirect,request, jsonify,url_for
from data import SQLCursor
from datetime import datetime


app = Flask('real_time_chat')

global cursor 
cursor = SQLCursor()

global name
name = []

global response 
response = [""]

class ChatPage(MethodView) : 
    def get(self) : 
        username = name[-1]
        return render_template('chat_page.html', username = username)

class Results(MethodView) : 
    def post(self) : 
        if "submit" in request.form : 
            comment = request.form.get('comment')
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            cursor.insert_comment(name[-1], comment,current_time)
            page="/chat_page"
        else : 
            page = "."
        return redirect(page)
class SubmitName(MethodView) : 
    def post(self) : 
        username = request.form.get('username')
        if len(username) == 0 : 
            response.append("Please choose a username.")
            return redirect('/')
        else : 
            response.append("")
            name.append(username)
            return redirect('/chat_page')
class MainPage(MethodView) : 
    def get(self) : 
        print(response)
        return render_template('index.html', response=response[-1])
    
@app.route('/data')
def get_data() : 
    data = {'comments' : cursor.get_all_comments()}
    return jsonify(data)
app.add_url_rule('/chat_page', view_func = ChatPage.as_view('chat_page'))
app.add_url_rule('/submit', view_func=Results.as_view('submit'))
app.add_url_rule('/submit_name', view_func = SubmitName.as_view('submit_name'))
app.add_url_rule('/', view_func = MainPage.as_view('main_page'))
app.run(debug=True)