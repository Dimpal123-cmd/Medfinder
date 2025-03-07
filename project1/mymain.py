from werkzeug.utils import secure_filename

from pro import *
from flask import Flask, render_template, request, redirect, url_for,session
import pymysql
import time
import os

app=Flask(__name__)

app.config['UPLOAD_FOLDER']='./static/photos'

app.secret_key="super secret key"

@app.route("/",methods=["GET","POST"])
def welcome():
    if request.method=="POST":
        medname=request.form["T1"]
        cur=make_connection()
        sql="select * from medicinefinder where medname like '%" +medname+ "%'"
        cur.execute(sql)
        n=cur.rowcount
        if n>0:
            records=cur.fetchall()
            return render_template("Home.html",data=records)
        else:
            return render_template("Home.html", msg="no records found")
    else:
        return render_template("Home.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if(request.method=="POST"):
        email=request.form["T1"]
        password=request.form["T2"]
        cur = make_connection()
        sql="select * from logindata where email='"+email+"' AND password='"+password+"'"
        cur.execute(sql)
        n=cur.rowcount
        if(n==1): #correct email and password
            data=cur.fetchone()
            ut=data[2] #fetch usertype from column index 2
            #create session
            session["usertype"]=ut
            session["email"]=email
            #send to page
            if(ut=="admin"):
                return redirect(url_for("admin_home"))
            elif(ut=="medical"):
                return redirect(url_for("medical_home"))
            else:
                return render_template("LoginForm.html",msg="Invalid user")
        else:
            return render_template("LoginForm.html",msg="Either email or password is incorrect")
    else:
        return render_template("LoginForm.html")

@app.route("/logout")
def logout():
    #remove session
    if("usertype" in session):
        session.pop("usertype",None)
        session.pop("email",None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))




@app.route("/auth_error")
def auth_error():
    return render_template("AuthError.html")

@app.route("/admin_home", methods=["GET", "POST"])
def admin_home():
    #check session
    if("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="admin"):
            cur = make_connection()
            sql = "select * from admindata where email='"+e1+"'"
            photo = check_photo(e1)
            print(sql)
            cur.execute(sql)
            n=cur.rowcount
            if n==1:
                record = cur.fetchone()
                return render_template("AdminHome.html",data=record,photo=photo)
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))
@app.route("/upload_admin_photo",methods=["GET","POST"])
def upload_admin_photo():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'admin':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path = os.path.basename(file.filename)

                    #fetch extension of file
                    file_ext = os.path.splitext(path)[1][1:]
                    #rename the file to timestamp
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)
                    cur=make_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"

                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('photoupload_admin.html', result="success")
                        else:
                            return render_template('photoupload_admin.html', result="failure")
                    except:
                        return render_template('photoupload_admin.html', result="duplicate")
            else:
                return redirect(url_for("admin_home"))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route( "/change_admin_photo")
def change_admin_photo():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            photo = check_photo(email)
            cur=make_connection()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/photos/"+photo)
                return render_template('change_adminphoto.html',data="success")
            else:
                return render_template('change_adminphoto.html', data="failure")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))



@app.route("/medical_home", methods=["GET", "POST"])
def medical_home():
    # check session
    if ("usertype" in session):
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "medical"):
            cur = make_connection()
            sql = "select * from medicaldata where email='" + e1 + "'"
            photo = check_photo(e1)
            cur.execute(sql)
            n = cur.rowcount
            if n==1:
                record = cur.fetchone()
                return render_template("MedicalHome.html",data=record,photo=photo)
            else:
                return render_template("MedicalHome.html",msg="Profile not Found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))
@app.route("/upload_medical_photo",methods=["GET","POST"])
def upload_medical_photo():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'medical':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path = os.path.basename(file.filename)

                    #fetch extension of file
                    file_ext = os.path.splitext(path)[1][1:]
                    #rename the file to timestamp
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)
                    cur=make_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"

                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('photoupload_medical.html', result="success")
                        else:
                            return render_template('photoupload_medical.html', result="failure")
                    except:
                        return render_template('photoupload_medical.html', result="duplicate")
            else:
                return redirect(url_for("medical_home"))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route("/change_medical_photo")
def change_medical_photo():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='medical':
            photo = check_photo(email)
            cur=make_connection()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/photos/"+photo)
                return render_template('change_medicalphoto.html',data="success")
            else:
                return render_template('change_medicalphoto.html', data="failure")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route("/admin_reg",methods=["GET","POST"])
def admin_reg():
    if "usertype" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "admin":
            if (request.method == "POST"):
                print("This POST request")
                # receive form data
                name = request.form["T1"]  # T1->name of textfield case-sensitive
                address = request.form["T2"]
                contact = request.form["T3"]
                email = request.form["T4"]
                password = request.form["T5"]
                usertype = "admin"

                cur = make_connection()
                s1 = "insert into admindata values('" + name + "','" + address + "','" + contact + "','" + email + "')"
                s2 = "insert into logindata values('" + email + "','" + password + "','" + usertype + "')"
                msg = ""
                try:
                    # send data to tables
                    cur.execute(s1)
                    m = cur.rowcount
                    cur.execute(s2)
                    n = cur.rowcount

                    if (m == 1 and n == 1):
                        msg = "Data saved and login created"
                    elif (m == 1):
                        msg = "Only data is saved"
                    elif (n == 1):
                        msg = "Only login is created"
                    else:
                        msg = "No data saved and no login created"
                except pymysql.err.IntegrityError:
                    msg = "Error : cannot register, email already in use"
                return render_template("AdminReg.html", vgt=msg)

            else:  # GET request
                print("This is GET request")
                return render_template("AdminReg.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/show_admins")
def show_admins():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "admin":
                cur = make_connection()
                sql="select * from admindata"
                cur.execute(sql)
                n=cur.rowcount
                if(n>0):
                    records=cur.fetchall()
                    return render_template("ShowAdmins.html",data=records)
                else:
                    return render_template("ShowAdmins.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))

@app.route("/medical_reg",methods=["GET","POST"])
def medical_reg():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "admin":

            if(request.method=="POST"):
                print("This POST request")
                #receive from data
                storename=request.form["T1"]# T1 -> name of textfield case-sensitive
                owner = request.form["T2"]
                address = request.form["T3"]
                contact = request.form["T4"]
                lno = request.form["T5"]
                email = request.form["T6"]
                password = request.form["T7"]
                usertype = "medical"

                cur = make_connection()
                s1 = "insert into medicaldata values('" + storename + "','" + owner + "','" + address + "','" + contact + "','" + lno + "','" + email + "')"
                s2 = "insert into logindata values('" + email + "','" + password + "','" + usertype + "')"
                msg = ""
                try:
                    #send data to tables
                    cur.execute(s1)
                    m = cur.rowcount
                    cur.execute(s2)
                    n = cur.rowcount

                    if (m == 1 and n == 1):
                        msg = "Data saved and login created"
                    elif (m == 1):
                        msg = "Only data is saved"
                    elif (n == 1):
                        msg = "Only login is created"
                    else:
                        msg = "No data saved and no login created"
                except pymysql.err.IntegrityError:
                    msg = "Error : cannot register, email already in use"
                return render_template("MedicalReg.html", vgt=msg)

            else:  # GET request
                print("This is GET request")
                return render_template("MedicalReg.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/show_medicals")
def show_medicals():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "admin":
            cur = make_connection()
            sql="select * from medicaldata"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                records=cur.fetchall()
                return render_template("ShowMedical.html",data=records)
            else:
                return render_template("ShowMedical.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/edit_medical",methods=["GET","POST"])
def edit_medical():
    if "email" in session:
        ut = session["usertype"]
        if ut == "admin":
            if(request.method=="POST"):
                email=request.form["H1"]
                cur = make_connection()
                sql = "select * from medicaldata where email='"+email+"'"
                cur.execute(sql)
                n = cur.rowcount
                if(n==1):
                    record=cur.fetchone()
                    return render_template("EditMedical.html",data=record)
                else:
                    return render_template("EditMedical.html",msg="No data found")
            else:
                return redirect(url_for("show_medicals"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/edit_medical_1",methods=["GET","POST"])
def edit_medical_1():
    if "email" in session:
        ut = session["usertype"]
        if ut == "admin":
            if(request.method=="POST"):
                # receive from data
                storename = request.form["T1"]  # T1 -> name of textfield case-sensitive
                owner = request.form["T2"]
                address = request.form["T3"]
                contact = request.form["T4"]
                lno=request.form["T5"]
                email=request.form["T6"]
                cur = make_connection()
                sql = "update medicaldata set storename='" + storename + "',owner='" + owner + "',address='" + address + "',contact='" + contact + "',lno='" + lno + "' where email='" + email + "'"
                cur.execute(sql)
                n = cur.rowcount
                if (n == 1):
                    return render_template("EditMedical1.html", msg="Data changes saved")
                else:
                    return render_template("EditMedical1.html", msg="Error: cannot save")
            else:
                return redirect(url_for("show_medicals"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/delete_medical",methods=["GET","POST"])
def delete_medical():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "admin":
            if (request.method == "POST"):
                email = request.form["H1"]
                cur = make_connection()
                sql = "select * from medicaldata where email='" +email+ "'"
                cur.execute(sql)
                n = cur.rowcount
                if (n == 1):
                    record = cur.fetchone()
                    return render_template("DeleteMedical.html", data=record)
                else:
                    return render_template("DeleteMedical.html", msg="No data found")
            else:
                return redirect(url_for("show_medicals"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/delete_medical_1",methods=["GET","POST"])
def delete_medical_1():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "admin":
            if(request.method=="POST"):
                # receive from data

                email = request.form["T6"]

                cur = make_connection()
                sql = "delete from medicaldata where email='" +email+ "'"
                cur.execute(sql)
                n = cur.rowcount
                if (n == 1):

                    return render_template("DeleteMedical1.html", msg="Data changes saved")
                else:
                    return render_template("DeleteMedical1.html", msg="Error: cannot save")
            else:
                return redirect(url_for("show_medicals"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/add_medicine",methods=["GET","POST"])
def add_medicine():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "medical":
            if(request.method=="POST"):
                print("This POST request")
                #receive from data
                medname = request.form["T1"]
                medlno = request.form["T2"]
                company = request.form["T3"]
                medtype = request.form["T4"]
                price = request.form["T5"]
                description= request.form["T6"]

                cur = make_connection()
                s1 = "insert into medicinedata values(0 ,'" + medname + "','" + medlno + "','" + company + "','" + medtype + "','" + price + "','" + description + "','"+em+"')"
                msg = ""
                try:
                    #send data to tables
                    cur.execute(s1)
                    m = cur.rowcount

                    if (m == 1):
                        msg = "Data saved "
                    else:
                        msg = "No data saved "
                except pymysql.err.IntegrityError:
                    msg = "Error : cannot register, email already in use"
                return render_template("AddMedicine.html", vgt=msg)
            else:  # GET request
                print("This is GET request")
                return render_template("AddMedicine.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/show_medicine")
def show_medicine():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "medical":

            cur=make_connection()
            sql="select * from medicinedata where medical_email='"+em+"'"
            cur.execute(sql)
            n=cur.rowcount
            print("total rows selected:",n)
            if(n>0):
                records=cur.fetchall()
                return render_template("ShowMedicine.html",data=records)
            else:
                return render_template("ShowMedicine.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/edit_medicine",methods=["GET","POST"])
def edit_medicine():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "medical":
            if(request.method=="POST"):
                medid=request.form["H1"]
                cur=make_connection()
                sql = "select * from medicinedata where medid="+medid
                print(sql)
                cur.execute(sql)
                n = cur.rowcount
                if(n==1):
                    record=cur.fetchone()
                    return render_template("EditMedicine.html",data=record)
                else:
                    return render_template("EditMedicine.html",msg="No data found")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/edit_medicine_1",methods=["GET","POST"])
def edit_medicine_1():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "medical":
            if(request.method=="POST"):
                # receive from data

                medname = request.form["T1"]
                medlno = request.form["T2"]
                company = request.form["T3"]
                medtype = request.form["T4"]
                price = request.form["T5"]
                description = request.form["T6"]
                medid = request.form["T0"]


                cur=make_connection()
                sql = "update medicinedata set medname='" + medname + "',medlno='" + medlno + "',company='" + company + "',medtype='" + medtype + "',price='" + price + "',description='" + description + "' where medid=" + medid
                cur.execute(sql)
                n = cur.rowcount
                if (n == 1):
                    return render_template("EditMedicine1.html", msg="Data changes saved")
                else:
                    return render_template("EditMedicine1.html", msg="Error: cannot save")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/delete_medicine",methods=["GET","POST"])
def delete_medicine():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "medical":

            if (request.method == "POST"):
                medid = request.form["H1"]
                cur=make_connection()
                sql = "select * from medicinedata where medid='" +medid+ "'"
                print(sql)
                cur.execute(sql)
                n = cur.rowcount
                if (n == 1):
                    record = cur.fetchone()
                    return render_template("DeleteMedicine.html", data=record)
                else:
                    return render_template("DeleteMedicine.html", msg="No data found")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/delete_medicine_1",methods=["GET","POST"])
def delete_medicine_1():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "medical":
            if(request.method=="POST"):
                # receive from data

                medid = request.form["T0"]

                cur=make_connection()
                sql = "delete from medicinedata where medid='" +medid+ "'"
                print(sql)
                cur.execute(sql)
                n = cur.rowcount
                if (n == 1):

                    return render_template("DeleteMedicine1.html", msg="Data changes saved")
                else:
                    return render_template("DeleteMedicine1.html", msg="Error: cannot save")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/admin_pass_change",methods=["GET","POST"])
def admin_pass_change():
    if "email" in session:
        ut=session["usertype"]
        email =session["email"]
        if ut == "admin":
            if request.method =="POST":
                a = request.form["t1"]
                b = request.form["t2"]
                cur=make_connection()
                sql = "update logindata set password = '"+b+"' where email='"+email+"' and password='"+a+"' "
                cur.execute(sql)
                n = cur.rowcount
                if n==1:
                    return render_template("AdminChangePassword.html", msg1="Password Changed")
                else:
                    return render_template("AdminChangePassword.html",msg="Invalid Old Password")
            else:
                return render_template("AdminChangePassword.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/medical_pass_change",methods=["GET","POST"])
def medical_pass_change():
    if "email" in session:
        ut=session["usertype"]
        email =session["email"]
        if ut == "medical":
            if request.method =="POST":
                a = request.form["t1"]
                b = request.form["t2"]

                cur=make_connection()
                sql = "update logindata set password = '"+b+"' where email='"+email+"' and password='"+a+"' "
                cur.execute(sql)
                n = cur.rowcount
                if n==1:
                    return render_template("MedicalChangePassword.html", msg1="Password Changed")
                else:
                    return render_template("MedicalChangePassword.html",msg="Invalid Old Password")
            else:
                return render_template("MedicalChangePassword.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/medical_edit_profile",methods=["GET","POST"])
def medical_edit_profile():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "medical":

            cur=make_connection()
            sql = "select * from medicaldata where email='" + em + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n == 1:
                data = cur.fetchone()
                return render_template("MedicalProfile.html", data=data)
            else:
                return render_template("MedicalProfile.html", msg="Profile not Found")

        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))




@app.route("/medical_edit_profile_1",methods=["GET","POST"])
def medical_edit_profile_1():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "medical":
            if request.method=="POST":
                storename = request.form["T1"]
                owner = request.form["T2"]
                address = request.form["T3"]
                contact = request.form["T4"]
                lno = request.form["T5"]

                cur=make_connection()

                sql="update medicaldata set storename='" + storename + "',owner='" + owner + "',address='" + address + "',contact='" + contact + "',lno='" + lno + "' where email='" + em + "'"
                cur.execute(sql)
                n=cur.rowcount
                if (n == 1):
                    return render_template("MedicalProfile1.html",msg="Data changes saved")
                else:
                    return render_template("MedicalProfile1.html",msg="Error: Cannot Save")
            else:
                return redirect(url_for("medical_home"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))
@app.route("/admin_edit_profile",methods=["GET","POST"])
def admin_edit_profile():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "admin":

            cur=make_connection()
            sql = "select * from admindata where email='" + em + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n == 1:
                data = cur.fetchone()
                return render_template("AdminProfile.html", data=data)
            else:
                return render_template("AdminProfile.html", msg="Profile not Found")

        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/admin_edit_profile_1",methods=["GET","POST"])
def admin_edit_profile_1():
    if "email" in session:
        ut = session["usertype"]
        em = session["email"]
        if ut == "admin":
            if request.method=="POST":
                storename = request.form["T1"]
                owner = request.form["T2"]
                address = request.form["T3"]
                contact = request.form["T4"]
                lno = request.form["T5"]

                cur=make_connection()

                sql="update admindata set storename='" + storename + "',owner='" + owner + "',address='" + address + "',contact='" + contact + "',lno='" + lno + "' where email='" + em + "'"
                cur.execute(sql)
                n=cur.rowcount
                if (n == 1):
                    return render_template("AdminProfile1.html",msg="Data changes saved")
                else:
                    return render_template("AdminProfile1.html",msg="Error: Cannot Save")
            else:
                return redirect(url_for("admin_home"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/all_medicals")
def all_medicals():
    cur=make_connection()
    sql="select * from medicaldata"
    cur.execute(sql)
    n=cur.rowcount
    if(n>0):
        records=cur.fetchall()
        return render_template("AllMedical.html",data=records)
    else:
        return render_template("AllMedical.html",msg="No data found")


if __name__=="__main__":
    app.run(debug=True)