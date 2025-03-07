from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
# Create your views here.

def welcome(request):
    if(request.method=="POST"):
        med=request.POST["T1"]
        data = medicinedata.objects.filter(med_name__icontains=med)
        lst=[]
        for d in data:
            store=medicaldata.objects.get(email=d.email_of_medical)
            aa=[d.med_name,d.company,d.med_type,d.unit_price,d.description,store.store_name,store.owner,store.address,store.contact]
            lst.append(aa)
        return render(request, "welcome.html", {"records": lst})
    else:
        return render(request,'welcome.html')

def show_medicals_to_all(request):
    data = medicaldata.objects.all()
    return render(request, "ShowMedicalsToAll.html", {"records": data})

def login(request):
    if(request.method=="POST"):
        try:
            uid=request.POST["T1"]
            ps=request.POST["T2"]
            obj=Logindata.objects.get(userid=uid,password=ps)
            ut=obj.usertype
            #create session
            request.session["usertype"]=ut
            request.session["userid"]=uid
            #open home page
            if(ut=="admin"):
                return HttpResponseRedirect("../admin_home/")
            elif(ut=="medical"):
                return HttpResponseRedirect("../medical_home/")
            else:
                return render(request,"LoginForm.html",{"msg":"Contact to admin"})
        except:
            return render(request, "LoginForm.html", {"msg": "Either userid and/or password is incorrect"})
    else:
        return render(request,"LoginForm.html")
def logout(request):
    try:
        #delete parameters from session
        del request.session['userid']
        del request.session['usertype']
        return HttpResponseRedirect("../login/")
    except:
        return HttpResponseRedirect("../login/")

def auth_error(request):
    return render(request,"AuthError.html")

def admin_home(request):
    if request.session.has_key("usertype"):
        ut=request.session["usertype"]
        if ut=="admin":
            return render(request,'AdminHome.html')
        else:
            return HttpResponseRedirect("../auth_error/")
    else:
        return HttpResponseRedirect("../auth_error/")
def medical_home(request):
    if request.session.has_key("usertype"):
        ut=request.session['usertype']
        if ut=='medical':
            return render(request,'MedicalHome.html')
        else:
            return HttpResponseRedirect("../auth_error/")
    else:
        return HttpResponseRedirect("../auth_error/")



def admin_reg(request):
    if request.session.has_key("usertype"):
        ut=request.session["usertype"]
        if ut=="admin":
            if (request.method == "POST"):  # POST
                # receive form data
                a = request.POST["T1"]
                b = request.POST["T2"]
                c = request.POST["T3"]
                d = request.POST["T4"]
                e = request.POST["T5"]

                adm = admindata()
                lgn = Logindata()
                adm.name = a
                adm.address = b
                adm.contact = c
                adm.email = d

                lgn.userid = d
                lgn.password = e
                lgn.usertype = "admin"

                adm.save()
                lgn.save()

                return render(request, "AdminReg.html", {"vgt": "Data saved"})
            else:  # GET request
                return render(request, "AdminReg.html")
        else:
            return HttpResponseRedirect("../auth_error/")
    else:
        return HttpResponseRedirect("../auth_error/")


def medical_reg(request):
    if request.session.has_key("usertype"):
        ut=request.session["usertype"]
        if ut=="admin":
            if(request.method=="POST"):
                store_name=request.POST["T1"]
                owner=request.POST["T2"]
                lno = request.POST["T3"]
                add = request.POST["T4"]
                contact = request.POST["T5"]
                email = request.POST["T6"]
                password = request.POST["T7"]

                md=medicaldata()
                lgn = Logindata()

                md.store_name=store_name
                md.owner=owner
                md.lno=lno
                md.address=add
                md.contact=contact
                md.email=email

                lgn.userid=email
                lgn.password=password
                lgn.usertype="medical"

                md.save()
                lgn.save()
                return render(request,"MedicalReg.html",{"vgt":"DATA SAVED"})
            else:
                return render(request,"MedicalReg.html")
        else:
            return HttpResponseRedirect("../auth_error/")
    else:
        return HttpResponseRedirect("../auth_error/")



def show_admins(request):
    if request.session.has_key("usertype"):
        ut=request.session["usertype"]
        if ut=="admin":
            data=admindata.objects.all()
            return render(request,"ShowAdmins.html",{"records":data})
        else:
            return HttpResponseRedirect("../auth_error/")
    else:
        return HttpResponseRedirect("../auth_error/")



def show_medicals(request):
    if request.session.has_key("usertype"):
        ut=request.session["usertype"]
        if ut=="admin":
            data=medicaldata.objects.all()
            return render(request,"ShowMedicals.html",{"records":data})
        else:
            return HttpResponseRedirect("../auth_error/")
    else:
        return HttpResponseRedirect("../auth_error/")



def edit_medical(request):
    if request.session.has_key("usertype"):
        ut = request.session["usertype"]
        if ut == "admin":
             if(request.method=="POST"):
                 store_name = request.POST["H1"]
                 data=medicaldata.objects.filter(store_name=store_name)
                 return render(request,"EditMedical.html",{"record":data})
             else:
                 return HttpResponseRedirect("../show_medicals/")
        else:
            return HttpResponseRedirect("../auth_error/")
    else:
        return HttpResponseRedirect("../auth_error/")



def edit_medical1(request):
    if request.session.has_key("usertype"):
        ut=request.session["usertype"]
        if ut=="admin":
            if (request.method=="POST"):
                store_name = request.POST["T1"]
                owner = request.POST["T2"]
                lno = request.POST["T3"]
                add = request.POST["T4"]
                contact = request.POST["T5"]
                email = request.POST["T6"]
                md=medicaldata.objects.get(store_name=store_name)
                md.owner = owner
                md.lno = lno
                md.address = add
                md.contact = contact
                md.email = email
                md.save()
                return render(request,"EditMedical1.html",{"vgt":"Data Updated Successfully"})
            else:
                return HttpResponseRedirect("../show_medicals/")
        else:
            return HttpResponseRedirect("../auth_error/")

    else:
        return HttpResponseRedirect("../auth_error/")




def delete_medical(request):
    if request.session.has_key("usertype"):
        ut=request.session["usertype"]
        if ut=="admin":
            if(request.method=="POST"):
                store_name = request.POST["H1"]
                data = medicaldata.objects.filter(store_name=store_name)
                return render(request,"DeleteMedical.html", {"record": data})
            else:
                return HttpResponseRedirect("../show_medicals/")
        else:
            return HttpResponseRedirect("../auth_error/")
    else:
        return HttpResponseRedirect("../auth_error/")





def delete_medical1(request):
    if request.session.has_key("usertype"):
        ut = request.session["usertype"]
        if ut == "admin":
            if (request.method=="POST"):
                store_name = request.POST["T1"]
                md = medicaldata.objects.get(store_name=store_name)
                md.delete()
                return render(request,"DeleteMedical1.html",{"vgt":"Data Deleted Successfully"})
            else:
                return HttpResponseRedirect("../show_medicals/")
        else:
            return HttpResponseRedirect("../auth_error/")
    else:
        return HttpResponseRedirect("../auth_error/")

def check_med(medname,lno,email):
    f=False
    try:
        med=medicinedata.objects.filter(med_name=medname,lno=lno,email_of_medical=email)
        for d in med:
            f=True
    except:
        f=False
    return f
def medicine_reg(request):
    if request.session.has_key("usertype"):
        ut=request.session["usertype"]
        em=request.session["userid"]
        if ut=="medical":
            if(request.method=="POST"):
                medicine_name=request.POST["T1"]
                company=request.POST["T2"]
                lno = request.POST["T3"]
                medicine_type = request.POST["T4"]
                description = request.POST["T5"]
                unit_price = request.POST["T6"]

                if(check_med(medicine_name,lno,em)==False):
                    md=medicinedata()

                    md.med_name=medicine_name
                    md.company=company
                    md.lno=lno
                    md.med_type=medicine_type
                    md.description=description
                    md.unit_price=unit_price
                    md.email_of_medical=em

                    md.save()

                    return render(request,"MedicineReg.html",{"vgt":"DATA SAVED"})
                else:
                    return render(request, "MedicineReg.html", {"vgt": "Medicine already exists"})
            else:
                return render(request,"MedicineReg.html")
        else:
            return HttpResponseRedirect("../auth_error/")
    else:
        return HttpResponseRedirect("../auth_error/")



def show_medicines(request):
    if request.session.has_key("usertype"):
        ut=request.session["usertype"]
        email=request.session["userid"]
        if ut=="medical":
            data=medicinedata.objects.filter(email_of_medical=email)
            return render(request,"ShowMedicines.html",{"records":data})
        else:
            return HttpResponseRedirect("../auth_error/")
    else:
        return HttpResponseRedirect("../auth_error/")
def edit_medicine(request):
    if request.session.has_key("usertype"):
        ut=request.session["usertype"]
        email=request.session["userid"]
        if ut=="medical":
            if (request.method == "POST"):
                med_name = request.POST["H1"]
                data = medicaldata.objects.filter(med_name=med_name)
                return render(request, "EditMedicine.html", {"record": data})


        else:
            return HttpResponseRedirect("../auth_error/")
    else:
        return HttpResponseRedirect("../auth_error/")



def edit_medicine1(request):
    if request.session.has_key("usertype"):
        ut=request.session["usertype"]
        email=request.session["userid"]
        if ut=="medical":
            if (request.method == "POST"):
                medicine_name = request.POST["T1"]
                company = request.POST["T2"]
                lno = request.POST["T3"]
                medicine_type = request.POST["T4"]
                description = request.POST["T5"]
                unit_price = request.POST["T6"]
                md = medicinedata.objects.get(med_name=medicine_name)
                md.save()
                return render(request, "EditMedicine1.html", {"vgt": "Medicine Updated Successfully"})
            else:
                return HttpResponseRedirect("../auth_error/")
        else:
            return HttpResponseRedirect("../auth_error/")



