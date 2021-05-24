from flask import (Flask, request, render_template, redirect) 
import os
import sqlite3
import json

with open('logged.json','r') as f:
    log = json.load(f)
with open('data.json', 'r') as file:
    data  = json.load(file)

class User:
    def __init__(self, username, email, password, ips, data):
        self.username = username
        self.email = email
        self.password = password
        self.ips = ips
        self.data = data
    
    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password

    def getIp(self):
        return self.ips

    def getSite(self):
        return self.data
    # def __str__(self):
    #     return str(self.username, self.email, self.password)

class Password:
    def __init__(self, site, used, password):
        self.site = site
        self.used = used
        self.password = password

    def getSite(self):
        return self.site
    
    def getUsed(self):
        return self.used

    def getPassword(self):
        return self.password

    # def __str__(self):
    #     return str(self.site, self.used, self.password)

def startup():
    if  not os.path.exists('data.db'):
        with open('data.db', 'w') as file:
            pass

    if not os.path.exists('userdata.db'):
        with open('userdata.db', 'w') as file2:
            pass

    
def addUser(username, password, email):
    data.append(User(username, email, password, ips = [], data = []).__dict__)
    with open('data.json', 'w') as file:
        json.dump(data, file, indent =4)




def addSite(username, site, used, password):
    for i in data:
        if i['username'] == username:
            list_ = i['data']

    list_.append(Password(site, used, password).__dict__)

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


def listUsers():
    user = []
    for i in data:
        user.append(i['username'])

    return user

def delete(user, site):
    for i in data:
        if i['username'] == user:
            sites = i['data']
    for i in sites:
        if i['site'] == site:
            index = sites.index(i)
            del sites[index]
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

def update(site, newpasword, newusername, user):
    for i in data:
        if i['username'] == user:
            list_ = i['data']
    for i in list_:
        if i['site'] == site:
            i['used'] = newusername
            i['password'] = newpasword
    with open('data.json','w') as file:
        json.dump(data, file, indent=4)

def listSites(username):
    sites = None
    for i in data:
        if i['username'] == username:
            sites = i['data']

    return sites

def checkUserExists(user):
    if user not in listUsers():
        return False
    return True

def checkSiteExists(site, user):
    if site not in listSites(user):
        return False
    return True

def filterLogin(name, pw):
    if name == "" or pw == "":
        return 'Field Error'
    elif not checkUserExists(name):
        return 'User not found'
    for i in data:
        if i['username'] == name:
            if i['password'] != pw:
                return 'Password error'
            else:
                return 'redirect'
def filterSignup(name, pw):
    if name == "" or pw == "":
        return 'Field Error'
    elif checkUserExists(name):
        return 'User not found'

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        if request.remote_addr in log.keys():
            return redirect('https://github.com') 
        else:
            return render_template()
    return render_template('index.html', logmsg= 'login')


@app.route('/dashboard', methods=['GET', 'POST'])
def home():
    return 'Hello this is a password Manager Dashboard'

@app.route('/login', methods = ['GET', 'POST'])
def login_screen():
    if request.method == 'POST':
        name = request.form.get('username')
        pw = request.form.get('password')

        if filterLogin(name, pw) == 'Field Error':
            return render_template('login.html',show = True,  logmsg = 'Please do not leave any field empty', sigmesg = 'Please do not leave any field empty')    

        elif filterLogin(name,pw) == 'User not found':
            return render_template('login.html',show = True, logmsg = 'User not found!')    


        elif filterLogin(name,pw) == 'Password error':
            return render_template('login.html', show = True, sigmesg = 'Password incorrect')    
        elif filterLogin(name, pw) == 'redirect':
            # if name not in log.keys():
            #     log[name] = []
            # log[name].append(request.remote_addr)
            if request.remote_addr not in log.keys():
                log[request.remote_addr] = name
            with open('logged.json', 'w') as f:
                json.dump(log, f, indent=4)
            return redirect('https://github.com/')

        else:
                    
            return render_template('login.html')
    else:
        if request.remote_addr in log.keys():
                # log[request.remote_addr] = name
                #    with open('logged.json', 'w') as f:
                # json.dump(log, f, indent=4)
                return redirect('https://github.com/')   
        return render_template('login.html', show = False)

@app.route('/signup', methods = ['GET', 'POST'])
def sign_up_screen():
    if request.method == 'POST':
        name = request.form.get('username')
        pw = request.form.get('password')
        email = request.form.get('email')

        if filterSignup(name, pw) == 'Field Error':
            return render_template('signup.html',show = True,  logmsg = 'Please do not leave any field empty', sigmesg = 'Please do not leave any field empty')    

        elif filterSignup(name,pw) == 'User not found':
            return render_template('signup.html',show = True, logmsg = 'User Already exists')

        else:
            addUser(name, pw, email)
            return redirect('/login')
                
    else:
        if request.remote_addr in log.keys():
                return redirect('https://github.com/')   
        return render_template('signup.html', show = False)



@app.route('/home')
def add_page():
    user = log.get(request.remote_addr)
    tabledata = []
    for i in data:
        if i['username'] == user:
            tabledata = i['data']
    return render_template('add.html', tabledata = tabledata)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        user = log[request.remote_addr]
        site = request.form.get('name')
        used = request.form.get('email')
        password = request.form.get('pw')
        if "" not in (used, site, password): 
            if site not in listSites(user):
                addSite(user, site, used, password)
                return render_template('adding.html', typ = "green")
            else:
                return render_template("adding.html", typ = "red", msg = "Site already exists in the database")
        else:
            return render_template('adding.html', typ = "red", msg = "Please do not leave any fields blank")
    else:
        return render_template('adding.html', typ = "none")

@app.route('/del', methods = ['GET', 'POST'])
def delete1():
    if request.method == 'POST':
        user = log[request.remote_addr]
       
        site = request.form.get('name')
        if site != "":
            delete(user, site)
            return render_template('del.html', typ = "green")
        else:
            return render_template('del.html', typ = "red", msg = "Please do not leave any fields blank")
    else:
        return render_template('del.html', typ = "none")
@app.route('/update', methods = ['GET', 'POST'])
def up():
    if request.method == 'POST':
        user = log[request.remote_addr]
        used = request.form.get('email')
        password = request.form.get('pw')
        site = request.form.get('name')
        if site != "":
            update(site, password, used, user)
            return render_template('update.html', typ = "green")
        else:
            return render_template('update.html', typ = "red", msg = "Please do not leave any fields blank")
    else:
        return render_template('upadte.html', typ = "none")
if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1')
