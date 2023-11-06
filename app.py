from flask import Flask
from flask import render_template, redirect, url_for, make_response
from flask import request



import pdfai
import os


app = Flask(__name__)
app.secret_key = "____"
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),"uploads")
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True



@app.route("/", methods=["GET", "POST"])
def index():

    response = make_response(render_template("index.html", title="EduAssist | Home"))
    response.set_cookie("samesite", "Lax")
    response.set_cookie("start_chat","false",path=request.path)


    files_to_read = []
    if request.method == "POST":

        files = request.files.getlist("pdfs")
        for file in files:
            filename=os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
            file.save(filename)
            files_to_read.append(filename)
        

        chatpage = make_response(redirect("/document-chat"))
        chatpage.set_cookie("files",str(files_to_read))
        
        return chatpage

    return response


@app.route("/document-chat", methods=["GET", "POST"])
def document_chat_page():

    start_chat = request.cookies.get("start_chat")


    files_to_read = eval(request.cookies.get("files"))
    cookie=make_response()
    chats = []
    file_content = ""
    if start_chat == "false":
        for file in files_to_read:
            data = pdfai.readPDF(file)
            file_content += data
        text_chunks = pdfai.generateTextChunks(file_content)
        knowledge_base = pdfai.createKnowledgeBase(text_chunks)
        chain = pdfai.createQAChain(knowledge_base)

        cookie.delete_cookie("start_chat")
        cookie.set_cookie("start_chat","true")

    if request.method == "POST":
        query = request.form.get("query")

        response = pdfai.generateAnswers(chain, knowledge_base, query)
        chats.append((query,response))
        return render_template("document_chat.html", title="EduAssist | Chat", chats=chats)

    return render_template("document_chat.html", title="EduAssist | Chat")


if __name__ == "__main__":
    app.run(debug=True)
