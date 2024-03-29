import os
import MySQLdb
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from database import db_connect,user_reg,user_loginact,user_upload,user_viewimages,npa_reg,npa_loginact,show_images,search_db,inbox_upload,inbox_images
from database import db_connect,v_image,image_info
from database import db_connect 
from werkzeug.utils import secure_filename

 

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def FUN_root():
    return render_template("index.html")

@app.route("/index.html")
def logout():
    return render_template("index.html")

@app.route("/register.html")
def reg():
    return render_template("register.html")
@app.route("/userhome.html")
def uhome():
    return render_template("userhome.html")

@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/upload.html")
def up():
    return render_template("upload.html")

@app.route("/viewdata.html")
def up1():
    return render_template("viewdata.html")
@app.route("/npa.html")
def npa():
    return render_template("npa.html")
@app.route("/npalogin.html")
def npalogin():
    return render_template("npalogin.html")

@app.route("/p_home.html")
def npa_home():
    return render_template("p_home.html")
    
@app.route("/search.html")
def search():
    return render_template("search.html")
@app.route("/npa_upload.html")
def npa_image():
    return render_template("npa_upload.html")




# -------------------------------------------register-------------------------------------------------------
@app.route("/regact", methods = ['GET','POST'])
def registeract():
   if request.method == 'POST':    
      id="0"
      status = user_reg(id,request.form['username'],request.form['password'],request.form['email'],request.form['mobile'],request.form['address'])
      if status == 1:
       return render_template("login.html",m1="sucess")
      else:
       return render_template("register.html",m1="failed")
#--------------------------------------------Login-----------------------------------------------------
@app.route("/loginact", methods=['GET', 'POST'])
def useract():
    if request.method == 'POST':
        status = user_loginact(request.form['username'], request.form['password'])
        print(status)
        if status == 1:
            session['username'] = request.form['username']                             
            return render_template("userhome.html", m1="sucess")
        else:
            return render_template("login.html", m1="Login Failed")
#-------------------------------------------Upload Image----------------------------------
@app.route("/upload", methods = ['GET','POST'])
def upload():
   if request.method == 'POST':    
      id="0"
      print()
      print(request.form['name'])
      print(request.form['remark'])
      status = user_upload(id,request.form['name'],request.form['city'],request.form['landmark'],request.form['remark'],request.form['image'])
      if status == 1:
       return render_template("upload.html",m1="sucess")
      else:
       return render_template("upload.html",m2="failed")
#--------------------------------------View Images-----------------------------------------
@app.route("/viewimage.html")
def viewimages():
    data = user_viewimages(session['username'])
	 
    print(data)
    return render_template("viewimage.html",user = data)

#---------------------------------------Track-----------------------------------------------
@app.route("/track")
def track():
    name = request.args.get('name')
    iname = request.args.get('iname')
    print("sdfdffsfsfdfaffdfdfsfsf")
    print(name)
    print(iname)
    data = image_info(iname)
    print("dddddddddddddddddddddddddddd")
    print(data) 
    data = v_image(data)
    print("dddddddddddddddddddddddddddd")
    print(data)
    return render_template("viewdata.html",m1="sucess",users=data,im=iname)
    

#------------------------------authenticated parson----------------
@app.route("/regact_auth", methods = ['GET','POST'])
def auth_registeract():
   if request.method == 'POST':    
      id="0"
      status = npa_reg(id,request.form['username'],request.form['password'],request.form['email'],request.form['mobile'],request.form['address'])
      if status == 1:
       return render_template("login.html",m1="sucess")
      else:
       return render_template("register.html",m1="failed")


#------------------------------authenticated parson log in----------------
@app.route("/npaloginact", methods=['GET', 'POST'])
def npaact():
    if request.method == 'POST':
        status = npa_loginact(request.form['username'], request.form['password'])
        print(status)
        if status == 1:
            session['username'] = request.form['username']                             
            return render_template("p_home.html", m1="sucess")
        else:
            return render_template("login.html", m1="Login Failed")
#-------------------------upload----------------
@app.route("/npa_upload", methods = ['GET','POST'])
def npa_upload():
   if request.method == 'POST':    
      id="0"
      
      print(request.form['name'])
      print(request.form['remark'])
      status = user_upload(id,request.form['name'],request.form['city'],request.form['landmark'],request.form['remark'],request.form['image'])
      if status == 1:
        return redirect('/')
    #    return render_template("npa_upload.html",m1="sucess")
      else:
       return render_template("npa_upload.html",m2="failed")



#---------------------------------------view image--------------------

@app.route("/showimage.html")
def showimages():
    data = show_images(session['username'])
	 
    print(data)
    return render_template("showimage.html",user = data)

#-----------------------search--------------------------------
@app.route("/search",methods = ['GET','POST'])
def search_user():
     if request.method == 'POST':
        print(request.form['image'])
        data=search_db(request.form['image'])
        print(data)
        if data:
            search_data=data                   
            return render_template("match.html", m1="sucess",search_r=search_data)
        else:
            return render_template("search.html", m1="Login Failed")

#-----------inbox--------------------------------
@app.route("/msg",methods = ['GET','POST'])
def msg():
    name = request.args.get('name')
    city = request.args.get('city')
    landmark= request.args.get('landmark')
    remark= request.args.get('remark')
    image= request.args.get('image')
    print('--------------------------------')
    print(name,city,landmark,remark,image)

    status = inbox_upload(name,city,landmark,remark,image)#request.form['landmark'],request.form['remark'],request.form['image'])
    if status == 1:
        return render_template("match.html",m1="sucess")
    else:
        return render_template("search.html",m2="failed")
    # return render_template("search.html")

@app.route("/inbox")
def inbox():
    data = inbox_images(session['username'])
	 
    print(data)
    return render_template("inbox.html",user = data)





       
# ----------------------------------------------Update Item------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000,use_reloader=False)




