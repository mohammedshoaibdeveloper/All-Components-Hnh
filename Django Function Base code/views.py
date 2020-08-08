Signup,Login ,Forget throug email,email verification , contact,Profile

def signup(request):
    if request.method=="POST":
        
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password1']
        password_encrpt=pbkdf2_sha256.hash(password)
        checkuser_name = User_Signup.objects.filter(username=username)
        checkuser_email = User_Signup.objects.filter(email=email)
        if checkuser_name or checkuser_email:
            thank=True
            msg="The username or email is already"
            return render(request,'index.html',{'msg':msg,'thank':thank})
           
        # mail verification
        token=random.randint(1000,100000)

        
        html_content=f'''
            <h1 style="text-align:center; font-family: 'Montserrat', sans-serif;">Finish creating your account</h1>
                <p> 
        Your email address has been registered with lms. To validate your account and activate your ability to send email campaigns, please complete your profile by clicking the link below:</p>
            <div style='width:300px; margin:0 auto;'> <a href='http://127.0.0.1:8000/verification/{token}/{username}' style=" background-color:#0066ff; border: none;  color: white; padding: 15px 32px;  text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; font-family: PT Sans, sans-serif;" >click here</a>
        </div>
            '''
        
        data=User_Signup(username=username,email=email,password=password_encrpt,token=token)
        data.save()
        thank=True
        msg="your account is successfully created please check your email and verify your account"
        subject, from_email, to = 'Verify Account', 'no-replay@gwadarengineeringworks.com', email
        msgsend = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msgsend.attach_alternative(html_content, "text/html")
        msgsend.send()
        
        return render(request,'index.html',{'msg':msg,'thank':thank})
        

    return redirect('/')
       


  
def login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        try:
            data=User_Signup.objects.get(email=email)
            if data:
                encrpt=data.password
                role=data.role
                encrpt=pbkdf2_sha256.verify(password,encrpt)
            if encrpt and role=="null":
                data=User_Signup.objects.get(email=email)
                request.session['username'] = data.username
                request.session['userid'] = data.sno
                request.session['role'] = data.role
                thank=True
                msg="Successfully Login"
                return render(request,'index.html',{'thank':thank,'msg':msg})
            elif encrpt and role=="Teacher":
                data=User_Signup.objects.get(email=email)
                request.session['username'] = data.username
                request.session['userid'] = data.sno
                request.session['role'] = data.role
                thank=True
                msg="Successfully Login"
                return render(request,'dashboard/page-dashboard.html',{'thank':thank,'msg':msg})

            else:
                thank=True
                msg="Password Incorrect"
                return render(request,'index.html',{'thank':thank,'msg':msg})
               
            
        except User_Signup.DoesNotExist:
            thank=True
            msg="Email Doesnot Exist"
            return render(request,'index.html',{'thank':thank,'msg':msg})

            
            
    return redirect('/')

     
       
      
    

# verification 
def verification(request,verification,username):
    data= User_Signup.objects.get(username=username)
   
    if data.token==verification:
        updata= User_Signup.objects.get(username=username)
        updata.verify='verified'
        updata.save()
        return redirect('/login')
        
# end verification



def forgetrequest(request):
    
    email=request.GET.get('email')
  
    token=random.randint(1000,100000)
 
    data=User_Signup.objects.get(email=email)
    username=data.username
    data.token=token
    data.save()

    subject, from_email, to = 'Forget Password', 'no-replay@gwadarengineeringworks.com', email
    html_content = f'''
            <h1 style="text-align:center; font-family: 'Montserrat', sans-serif;">Finish creating your account</h1>
                <p> 
        Your email address has been registered with lms. To validate your account and activate your ability to send email campaigns, please complete your profile by clicking the link below:</p>
            <div style='width:300px; margin:0 auto;'> <a href='http://127.0.0.1:8000/forget/{token}/{username}' style=" background-color:#0066ff; border: none;  color: white; padding: 15px 32px;  text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; font-family: PT Sans, sans-serif;" >click here</a>
        </div>
            '''
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse('sent')

def forget(request,verification,username):
    token=verification
    username=username
    return render(request,'forget.html',{'token':token,'username':username})

# contact
def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        subject=request.POST['subject']
        data=Contact(Full_name=name,Email=email,subject=subject,Message=message)
        if data:
            data.save()
            Thank = True
            message="Your Response is Recorded"
            return render(request,'page-contact.html',{'message':message,'Thank':Thank})  
        else:
            
            message="Please Fill Correctly"
            return render(request,'page-contact.html',{'message':message,'Thank':Thank})  
    return render(request,'page-contact.html')

# profile 
def profile(request):
    try:
        if request.method=="POST":
            data=AdminAccount.objects.get(SId=request.session['adminid'])
            firstname=request.POST['fname']
            lastname=request.POST['lname']
            email=request.POST['email']
            phone=request.POST['phone']
            uname=request.POST['uname']
            image=request.FILES.get('img',False)

            data.SFname=firstname
            data.SLname=lastname
            data.SEmail=email
            data.SUsername=uname
            data.SContactNo=phone
            if image:
                data.SProfile=image
            data.save()
            return HttpResponse('Update Successfully')


        userdata = list()
        data=AdminAccount.objects.filter(SId=request.session['adminid'])
        for x in data:
            datas=Seradmin(x)
            userdata.append(datas.data)
        return HttpResponse(json.dumps(userdata))

    except:
        return redirect('/superadmin/')


# Insert Update Delete View Search

def adminform(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    try:
        if request.method == "POST":
            Formtitle=request.POST['Formtitle']
            data=Form.objects.filter(Formtitle__icontains=Formtitle,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            return render(request,'uniadmin/adminform.html',{'data':data})
        
        
        result = urlopen('http://just-the-time.appspot.com/')
        result = result.read().strip()
        result_str = result.decode('utf-8')
        present=result_str[:10]
        present = pd.to_datetime(present).date()
    
        data=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
        past=data.UniversityId.UniPackage.PackDurationEnd
        unidata=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
    
        if past >= present and unidata.UniStatus == "Active":
            data=Form.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-FormId')[:]
            return render(request,'uniadmin/adminform.html',{'data':data})
        else:
            data=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            data.UniStatus="Disable"
            data.save()
            return redirect('/university/login')
    except:
        return redirect('/university/')
def addadminform(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    try:
        if request.method=="POST":
            Formtitle=request.POST['Formtitle']
            FormFile=request.FILES['FormFile']
            FileCategory=request.POST['FileCategory']
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=Form(Formtitle=Formtitle,FormFile=FormFile,uniId=uniid,branchId=branchid,FileCategory=FileCategory)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('adminform')
    except:
        return redirect('/university/')
#adminformSuggestion 
def adminformSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    try:
        if request.is_ajax():
            q = request.GET.get('term', '')
            print(q)
            projects = Form.objects.filter(Formtitle__istartswith=q)[:5]
            results = []
            for project in projects:
                project_json = {}
                project_json['id'] = project.FormId 
                project_json['value'] = project.Formtitle
                project_json['label'] = project.Formtitle
                results.append(project_json)
            print(results)
            data = json.dumps(results)
        else:
            data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    except:
        return redirect('/university/')
def deleteadminform(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    try:
        data=Form.objects.filter(FormId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminform')
    except:
        return redirect('/university/')
def showform(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    try:
        userdata = list()
        id=request.GET['uid']
        request.session['formadmin']=id
        
        data=Form.objects.filter(FormId=id)
        for x in data:
            datas=SerForm(x)
            
            userdata.append(datas.data)
        return HttpResponse(json.dumps(userdata))
    except:
        return redirect('/university/')
   
  
def editadminform(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    try:
        if request.method=="POST":
            Formtitle=request.POST['FFormtitle']
            FileCategory=request.POST['FFileCategory']
            bid=request.session['formadmin']
            data=Form.objects.get(FormId=bid)
            FormFile=request.FILES.get('FFormFile',False)
            
            if FormFile:
                data.FormFile=FormFile
            data.Formtitle=Formtitle
            data.FileCategory=FileCategory
            data.save()
            del request.session['formadmin']
            messages.success(request,"Update Successfully")
            return redirect('adminform')
        
    except:
        return redirect('/university/')
    return render(request,'uniadmin/adminform.html')



# Social media integration

#provider

    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    path('accounts/',include('allauth.urls')),
    path('google', views.base, name='google'),
    # direct call url in Html Page