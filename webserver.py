from flask import Flask
from flask import request
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

app = Flask(__name__)

gauth = GoogleAuth()
auth_url = gauth.GetAuthUrl() # Create authentication url user needs to visit

@app.route("/")
def hello_world():
    return "<p><a href='" + str(auth_url) + "'>Login</a></p>"

@app.route("/success") # See the client_secrets.json file to change this route
# one could use save_credentials_backend to type dict to save the secret to a cookie and load it later
def success():
    code = request.args.get('code')
    if code:
        try:
            response = "<p>Code: " + code + "</p><br><br>"
            gauth.Auth(code) # Authorize and build service from the code
            #gauth.SaveCredentialsFile("mycreds.txt") # Replace this by a dict backend, and save result to session cookie
            drive = GoogleDrive(gauth)
            file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
            for file in file_list:
                response += f"<p>title: {file['title']}, id: {file['id']}</p>"
            return response
        except Exception as e:
            print(e)
            return f"<p>Error: {e}</p>"
    else:
        return "<p> YOU MUST AUTHENTICATE YOURSELF !</p>"