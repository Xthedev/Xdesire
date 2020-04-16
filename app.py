import os
from flask import Flask , render_template, redirect, url_for, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import secure_filename
from datetime import datetime





app = Flask(__name__)
UPLOAD_FOLDER = 'static/books'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///desire.db'
db = SQLAlchemy(app)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password= db.Column(db.String(200), nullable=False)
    level= db.Column(db.String(200), nullable=False)
    dateadded= db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__():
        return '<Admin %r>'  % self.id


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author= db.Column(db.String(200), nullable=False)
    filename = db.Column(db.Text, nullable=False)
    picture = db.Column(db.Text, nullable=False)
    review = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(200), nullable=False)
    dateadded= db.Column(db.DateTime, default=datetime.utcnow)
 
    def __repr__():
        return '<Books %r>'  % self.id

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable= False)
    password = db.Column(db.String(200) ,nullable=False)
    fullname = db.Column(db.String(200) ,nullable=False)
    mobile = db.Column(db.String(200) ,nullable=False)
    likes = db.Column(db.String(200) ,nullable=False)
    dateadded= db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__():
        return '<Users %r>'  % self.id

class Purchases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable= False)
    fullname = db.Column(db.String(200) ,nullable=False)
    bookname = db.Column(db.String(200) ,nullable=False)
    price = db.Column(db.String(200) ,nullable=False)
    dateadded= db.Column(db.DateTime, default=datetime.utcnow)

    
    def __repr__():
        return '<Purchases %r>'  % self.id


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable= False)
    fullname = db.Column(db.String(200) ,nullable=False)
    message = db.Column(db.Text ,nullable=False)
    dateadded= db.Column(db.DateTime, default=datetime.utcnow)

    
    def __repr__():
        return '<Messages %r>'  % self.id

#Users.__table__.create(db.session.bind)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')
    

@app.route('/home')
def home():

    books = Books.query.order_by(Books.dateadded.desc()).limit(6).all()
    return render_template('home.html', books=books)


@app.route('/admin',methods =['GET', 'POST'])
def admin():
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        findadmin = Admin.query.filter_by(username=username).first()
        if findadmin is None :
            response = {
                        'error':True,
                        'message':'No Such Admin Exists'
                    }
            return jsonify(response)
        else:
            if password == findadmin.password:
                    response = {
                        'error':False,
                        'message':'Log In Was Successful, Redirecting'
                    }
                    return jsonify(response)
            else:
                    response = {
                        'error':True,
                        'message':'Sorry Very Wrong  Password'
                    }
                    return jsonify(response)
            
                
            #return render_template('admin/index.html')
    else:
        return render_template('admin/index.html')




@app.route('/logmein',methods =['GET', 'POST'])
def logmein():
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        finduser = Users.query.filter_by(email=email).first()
        if finduser is None :
            response = {
                        'error':True,
                        'message':'No Such Admin Exists'
                    }
            return jsonify(response)
        else:
            if password == finduser.password:
                    response = {
                        'error':False,
                        'message':'Log In Was Successful, Redirecting'
                    }
                    return jsonify(response)
            else:
                    response = {
                        'error':True,
                        'message':'Sorry Very Wrong  Password'
                    }
                    return jsonify(response)
            
                
            #return render_template('admin/index.html')
    else:
        return render_template('admin/index.html')


@app.route('/single/<int:id>')
def single(id):
    books = Books.query.get_or_404(id)
    return render_template('single.html', books=books)


@app.route('/drama')
def drama():
    books = Books.query.filter_by(genre='Drama & Romance').all()
    return render_template('genre.html', books = books)



@app.route('/fiction')
def fiction():
    books = Books.query.filter_by(genre='Fiction & Horror').all()
    return render_template('genre.html', books = books)



@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        books = Books.query.filter(Books.title.like('%'+search+'%')).all()
        return render_template('search.html', books = books)
    else:
        return render_template('search.html')


@app.route('/christian')
def christian():
    books= Books.query.filter_by(genre='Christian Books').all()
    return render_template('genre.html', books = books)



@app.route('/motivational')
def motivational():
    books= Books.query.filter_by(genre='Motivational Books').all()
    return render_template('genre.html', books = books)



@app.route('/business')
def business():
    books= Books.query.filter_by(genre='Business Books').all()
    return render_template('genre.html', books = books)



@app.route('/mymessages', methods=['GET','POST'])
def mymessages():
    if request.method == 'POST':
        email = request.form['email']    
        users = Users.query.filter_by(email=email).first()
        return render_template('messages.html',users =users)

    else:
        return render_template('messages.html')


@app.route('/software')
def software():
    books= Books.query.filter_by(genre='Software & Technology').all()
    return render_template('genre.html', books = books)


@app.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')



@app.route('/adminbooks', methods=['GET','POST'])
def homebooks():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        picture = request.form['picture']
        file = request.files['file']
        review= request.form['review']
        genre= request.form['genre']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        tosend = Books(title=title, author = author, filename= filename , picture=picture,review = review ,genre=genre )
        try:
            db.session.add(tosend)
            db.session.commit()
            return redirect('/adminbooks')
        except:
            
            return('Please go back an error occured')

    else:
        books = Books.query.order_by(Books.dateadded.desc()).all()
        return render_template('admin/books.html',books= books)



@app.route('/editbook/<int:id>')
def editbook(id):
    books= Books.query.get_or_404(id)

    return render_template('admin/editbook.html',books=books)



@app.route('/update', methods=['GET','POST'])
def updatebook():
    
    if request.method == 'POST':
        id= request.form['id']
        title = request.form['title']
        author = request.form['author']
        picture = request.form['picture']
        review = request.form['review']
        books = Books.query.get_or_404(id)
        try:
            books.title=title
            books.author=author
            books.picture = picture
            books.review = review
            db.session.commit()
            return redirect('/adminbooks')
        except:
            return('Please go back an error occured')

@app.route('/delbook', methods=['GET','POST'])
def deletebook():
    if request.method== 'POST' :
         bookid = request.form['bookid']
         book = Books.query.get_or_404(bookid)
         db.session.delete(book)
         db.session.commit()

         return redirect('/adminbooks')
    else:
         return redirect('/adminbooks')



@app.route('/users')
def users():
    users = Users.query.order_by(Users.dateadded.desc()).all()
    return render_template('admin/users.html', users = users)


@app.route('/admins')
def admins():
    admins = Admin.query.order_by(Admin.dateadded.desc()).all()
    return render_template('admin/admins.html', admins = admins)

@app.route('/purchases')
def purchases():
    purchases = Purchases.query.order_by(Purchases.dateadded.desc()).all()
    return render_template('admin/purchases.html',purchases=purchases )


@app.route('/messages')
def messages():
    messages = Messages.query.order_by(Messages.dateadded.desc()).all()
    return render_template('admin/messages.html',messages=messages)


@app.route('/newadmin' , methods=['GET','POST'])
def newadmin():
    username = request.form['username']
    password = request.form['password']
    level = request.form['level']
    toadd = Admin(username=username,password=password, level=level)
    try:
        db.session.add(toadd)
        db.session.commit()
        return redirect('/admins')
    except:
        return redirect('/')
    return render_template('admin/admins.html', admins = admins)

@app.route('/deladmin' , methods=['GET' ,'POST'])
def deladmin():

    if request.method== 'POST' :
        admin = request.form['admin']
        admin= Admin.query.filter_by(id=admin).first()
        try:
            db.session.delete(admin)
            db.session.commit()
            return redirect('/admins')
        except:
                return redirect('/admins')
    else:
        return page_not_found('Could Not Add Admin')

@app.route('/delmessages/<int:id>')
def delmessage(id):
    message= Messages.query.get_or_404(id)
    try:
        db.session.delete(message)
        db.session.commit()
        return redirect('/messages')
    except:
        return('nothing to delete')

@app.route('/delusers' , methods=['GET' ,'POST'])
def delusers():

    if request.method== 'POST' :
        userid = request.form['userid']
        users = Users.query.filter_by(id=userid).first()
        try:
            db.session.delete(users)
            db.session.commit()
            return redirect('/users')
        except:
                return redirect('/users')
    else:
        return page_not_found('Could Not Add Admin')





@app.route('/newuser' , methods=['GET','POST'])
def newuser():
    if request.method== 'POST' :
         email = request.form['email']
         check= Users.query.filter_by(id=email).first()
         if check is None:
             return('Already exists')
         else:
            fullname = request.form['fullname']
            mobile = request.form['mobile']
            likes = request.form['likes']
            password = request.form['password']
            users = Users(email=email , fullname=fullname, mobile = mobile, likes=likes ,password = password)
        
            db.session.add(users)
            db.session.commit()

         return redirect('/users')
    else:
         return ('You did not send any data')





@app.route('/adduser' , methods=['GET','POST'])
def adduser():
    if request.method== 'POST' :
         email = request.form['email']
         check= Users.query.filter_by(id=email).first()
         if check is None:
            fullname = request.form['fullname']
            mobile = request.form['mobile']
            likes = request.form['likes']
            password = request.form['password']
            users = Users(email=email , fullname=fullname, mobile = mobile, likes=likes ,password = password)
                
            try:
                db.session.add(users)
                db.session.commit()
                response ={
                    'error':False,
                    'message':'User Registered Successfully'
                }
                return jsonify(response)
            except:
                response ={
                    'error':True,
                    'message':'Sorry An Error Occured'
                }
                return jsonify(response)
            
         else:
            response ={
                        'error':True,
                        'message':'User Already Exists'
                    }
            return jsonify(response)

                    
    else:
         return ('You did not send any data')

@app.route('/updateuserdetails',methods=['GET','POST'])
def userdetails():
    if request.method == 'POST' :
        email = request.form['email']
        password=request.form['password']
        mobile = request.form['mobile']
        fullname = request.form['fullname']
        likes = request.form['likes']
        
        users= Users.query.filter_by(email=email).first()
        try:
            users.email=email
            users.password =password
            users.mobile = mobile
            users.fullname = fullname
            users.likes = likes
            db.session.commit()
            return render_template('messages.html', users=users)
        except:
            return('an error occured')
    else:
        return ('an error occured')

@app.route('/sendmessage', methods=['GET','POST'])
def sendmessage():
    if request.method=='POST':
        email= request.form['email']
        fullname= request.form['fullname']
        message = request.form['message']
        toadd = Messages(email=email,fullname=fullname,message=message)
        try:
            db.session.add(toadd)
            db.session.commit()
            response ={  'error': False , 'message':'Message Sent Successfully'}
            return jsonify(response)
        except:
            response ={  'error': True , 'message':'Could Not Sent Message'}
            return jsonify(response)

@app.route('/savepurchase', methods=['GET','POST'])
def savepurchase():
    if request.method=='POST':
        email= request.form['email']
        fullname= request.form['fullname']
        bookname = request.form['bookname']
        toadd = Purchases(email=email,fullname=fullname,bookname=bookname,price='200')
        try:
            db.session.add(toadd)
            db.session.commit()
            response ={  'error': False , 'message':'Purchases Saved'}
            return jsonify(response)
        except:
            response ={  'error': True , 'message':'Could Not Save Purchases'}
            return jsonify(response)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404





































# import os
# from flask import Flask , render_template, redirect, url_for, request, jsonify, flash
# from flask_sqlalchemy import SQLAlchemy

# from werkzeug.utils import secure_filename
# from datetime import datetime


# app = Flask(__name__)
# UPLOAD_FOLDER = 'static/images'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lois.db'
# db = SQLAlchemy(app)



# class News(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     dateadded= db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__():
#         return '<News %r>'  % self.id

# class Messages(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(200), nullable=False)
#     website= db.Column(db.Text, nullable=False)
#     message = db.Column(db.Text,nullable = False)
#     datesent= db.Column(db.DateTime, default=datetime.utcnow)


#     def __repr__():
#         return '<Messages %r>'  % self.id


# class Gallery(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     dateuploaded= db.Column(db.DateTime, default=datetime.utcnow)
#     title= db.Column(db.String(200), nullable=False)
#     def __repr__():
#         return '<Gallery %r>'  % self.id



# class Scratchcard(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     pin = db.Column(db.Text, nullable=False)
#     dateadded= db.Column(db.DateTime, default=datetime.utcnow)
#     assigned = db.Column(db.Integer, nullable=False)
#     def __repr__():
#         return '<Scratchcard %r>'  % self.id

# #Scratchcard.__table__.create(db.session.bind)

# #Gallery.__table__.create(db.session.bind)

# class Students(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     fullname = db.Column(db.Text, nullable=False)
#     passport = db.Column(db.Text, nullable=False)
#     waec = db.Column(db.Text, nullable=False)
#     birth = db.Column(db.Text, nullable=False)
#     mobile = db.Column(db.Text, nullable=False)
#     address = db.Column(db.Text, nullable=False)
#     email = db.Column(db.Text, nullable=False)
#     course = db.Column(db.Text, nullable=False)
#     studytype = db.Column(db.Text, nullable=False)
#     accommodation = db.Column(db.Text, nullable=False)
#     programme = db.Column(db.Text, nullable=False)
#     cardpin = db.Column(db.Text, nullable=False)
#     discipline = db.Column(db.Text, nullable=False)

#     def __repr__():
#         return '<Students %r>'  % self.id



# #Students.__table__.create(db.session.bind)  


# @app.route('/')
# def index():
#     news = News.query.order_by(News.dateadded).limit(3).all()
#     return render_template('index.html' ,news= news)

# @app.route('/news')
# def news():
#     news = News.query.order_by(News.dateadded.desc()).all()
#     return render_template('news.html',news= news)
   
    
# @app.route('/single/<int:id>', methods=['GET'])
# def single(id):
#     single= News.query.get_or_404(id)
#     return render_template('single.html', single= single)

# @app.route('/gallery')
# def gallery():
#     gallery = Gallery.query.order_by(Gallery.dateuploaded.desc()).all()
#     return render_template('gallery.html',gallery=gallery)


# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/contact',methods =['POST','GET'])
# def contact():
#     if request.method == 'POST' :
#         email = request.form['email']
#         name = request.form['name']
#         message = request.form['message']
#         website = request.form['website']
#         toadd = Messages(name=name,email=email,message=message, website= website)
#         try:
#             db.session.add(toadd)
#             db.session.commit()
#             response={ 'error':False ,'message':'Message Sent Successfully'  }
#             return jsonify(response)
#         except:
#             response={ 'error':True ,'message':'Message Was Not Sent , An Error Occured'  }
#             return jsonify(response)

#     else:
#         return render_template('contact.html')



# @app.route('/faq')
# def faq():
#     return render_template('faq.html')

# @app.route('/apply')
# def apply():
#     return render_template('apply.html')


# @app.route('/alldiploma')
# def alldiploma():
#     return render_template('alldiploma.html')



# @app.route('/ijmb')
# def ijmb():
#     return render_template('ijmb.html')



# @app.route('/international')
# def international():
    
#     return render_template('abroad.html')



# @app.route('/begin')
# def begin():
    
#     return render_template('students/index.html')

# @app.route('/admin')
# def admin():
#     return render_template('admin/index.html')


# @app.route('/dashboard')
# def dashboard():
#     return render_template('admin/dashboard.html')


# @app.route('/scratchcard')
# def scratchcard():
#     scratchcard = Scratchcard.query.order_by(Scratchcard.dateadded.desc()).all()
#     return render_template('admin/scratchcard.html',scratchcard=scratchcard)

# @app.route('/messages')
# def messages():
#     messages = Messages.query.order_by(Messages.datesent.desc()).all()
#     return render_template('admin/messages.html',messages=messages)


# @app.route('/adminnews', methods=['GET' ,'POST'])
# def adminnews():
#     if request.method == 'POST':
#         item = request.form['newsid']
#         theitem = News.query.get_or_404(item)
#         try :
#             db.session.delete(theitem)
#             db.session.commit()
#             return redirect('/addnews')
#         except:
#             return('could not delete item, refresh page')
#     else:
#         news= News.query.order_by(News.dateadded.desc()).all()
#         return render_template('admin/news.html', news=news)

# @app.route('/addnews', methods=['GET','POST'])
# def addnews():
#      if request.method== 'POST' :
#          title = request.form['title']
#          content = request.form['content']
#          addnews = News(title=title, content = content)
#          db.session.add(addnews)
#          db.session.commit()

#          return redirect('/adminnews')
#      else:
#         return render_template('admin/addnews.html')



# @app.route('/delnews', methods=['GET','POST'])
# def deletenews():
#     if request.method== 'POST' :
#          newsid = request.form['newsid']
#          news = News.query.get_or_404(newsid)
#          db.session.delete(news)
#          db.session.commit()

#          return redirect('/adminnews')
#     else:
#          return redirect('/adminnews')


# @app.route('/delmessages', methods=['GET','POST'])
# def delmessages():
#     if request.method== 'POST' :
#          newsid = request.form['newsid']
#          news = Messages.query.get_or_404(newsid)
#          db.session.delete(news)
#          db.session.commit()

#          return redirect('/messages')
#     else:
#          return redirect('/messages')



# @app.route('/delperson', methods=['GET','POST'])
# def delperson():
#     if request.method== 'POST' :
#          newsid = request.form['newsid']
#          news = Students.query.get_or_404(newsid)
#          db.session.delete(news)
#          db.session.commit()

#          return redirect('/application')
#     else:
#          return redirect('/application')


# @app.route('/viewperson/<int:id>')
# def viewperson(id):
#     person = Students.query.get_or_404(id)
#     return render_template('admin/viewperson.html', person=person)


# @app.route('/admingallery')
# def admingallery():
#     gallery = Gallery.query.order_by(Gallery.dateuploaded.desc()).all()
#     return render_template('admin/gallery.html',gallery=gallery)

# @app.route('/application')
# def application():
#     application = Students.query.order_by(Students.id.desc()).all()
#     return render_template('admin/application.html',application=application)



# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/uploadpicture',methods=['POST','GET'])
# def uploadpicture():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return ('No file found')
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return ('U didnt select a file, click back to go back')
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             title = request.form['caption']
#             additem = Gallery(name=filename , title = title)
#             db.session.add(additem)
#             db.session.commit()
#             return redirect('/admingallery')
#     else:
#         return('Nothing to upload, click back to go back')





# @app.route('/delimages/<int:id>')
# def deleteimages(id):
#     todelete = Gallery.query.get_or_404(id)
#     db.session.delete(todelete)
#     db.session.commit()
#     return redirect('/admingallery')


# @app.route('/addscratchcard', methods=['GET','POST'])
# def addscratchcard():
#     if request.method == 'POST':
#         pin = request.form['mys']
#         toadd = Scratchcard(pin=pin,assigned='0')

#         try:
#             db.session.add(toadd)
#             db.session.commit()
#             response = {
#             'error': False, 'message':'Successfully Added'
#             }
#             return jsonify(response)
#         except:
#             response = {
#             'error': True, 'message':'You didnt Send Anything'
#             }
#             return jsonify(response)
#     else:
#         response = {
#             'error': True, 'message':'You didnt Send Anything'
#             }
#         return jsonify(response)


# @app.route('/sendapp', methods =['GET', 'POST'])
# def sendapp():
#     if request.method == 'POST':
#         scratch = request.form['scratch']
#         findscratch = Scratchcard.query.filter_by(pin=scratch).first()
#         if findscratch is None :

#               message ='The Scratchcard Pin Does Not Exist'
#               return render_template('students/index.html',message=message)
#         else:
#             if findscratch.assigned==1:
#                 message ='Someone Has Already Been Assigned the Scratch Card You Tried To Use, Stop Being Dubious.'
#                 return render_template('students/index.html',message=message)
#             else:
#                 findscratch.assigned='1'

#                 fullname = request.form['name']
#                 file = request.files['passport']
#                 passportname =secure_filename(file.filename)
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], passportname))
#                 file = request.files['birth']        
#                 birthname = secure_filename(file.filename)
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], birthname))
#                 file = request.files['waec']
#                 waecname =secure_filename(file.filename)
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], waecname))
#                 mobile = request.form['mobile']
#                 address= request.form['address']
#                 email = request.form['email']
#                 course = request.form['course']
#                 studytype = request.form['studytype']
#                 accomodation = request.form['accomodation']
#                 programme = request.form['programme']
#                 discipline = request.form['discipline']

#                 addtodb = Students(fullname=fullname,passport=passportname,waec=waecname,birth=birthname,mobile=mobile,address=address,email=email,course=course,studytype=studytype,accommodation=accomodation,programme=programme,discipline=discipline,cardpin=scratch)
#                 db.session.add(addtodb)
#                 db.session.commit()
#                 return('Successful')

#         # check if the post request has the file part
#         # if 'file' not in request.files:
#         #     flash('No file part')
#         #     return ('No file found')
#         # file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         # if file.filename == '':
#         #     flash('No selected file')
#         #     return ('U didnt select a file, click back to go back')
#         # if file and allowed_file(file.filename):
#         #     filename = secure_filename(file.filename)
#         #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         #     title = request.form['caption']
#         #     additem = Gallery(name=filename , title = title)
#         #     db.session.add(additem)
#         #     db.session.commit()
#         #     return redirect('/admingallery')
#     else:
#         return('Nothing to upload, click go back')

# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('404.html'), 404




# # addnews = News(title='DE-LOIS EDUCATIONAL SERVICES IS AFFILIATED TO FEDERAL COLLEGE OF EDUCATION (TECHNICAL) AKOKA YABA, LAGOS IN RESPECT TO DIPLOMA COURSES',  content =''' De-Lois Educational services is in affiliation with FCE(T), Akoka Yaba Lagos, to run her Diploma courses.  At De-Lois Educational services, you can run Diploma courses like Computer Science,Public Administration, Business Administration, Accounting, Media and Film Production, Cinematography, Office Technology e.t.c..   Lectures for these category of courses are scheduled for both week-days and week-ends. This is to allow all working class and adult category of students, as well as busy types to enjoy the six (6) month Diploma Programme conveniently which can also be used to further secure University Admission for Degree certificate      ''' )
# # db.session.add(addnews)
# # db.session.commit()

# # additem = Gallery(name='circ.jpg',title='DE-LOIS EDUCATION SERVICES')
# # db.session.add(additem)
# # db.session.commit()



# if __name__ == "__main__":
#     app.run(debug=True)



if __name__ == "__main__":
    app.run(debug=True)