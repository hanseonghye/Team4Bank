from flask import Flask,render_template,redirect,request,session,flash
import re
import pymysql
import datetime
from flask_mail import Mail, Message


conn=pymysql.connect(
	host='localhost',
	user='root',
	password='a',
	db='user',
	charset='utf8'
)

curs=conn.cursor()


app=Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='hanseonghye12312@gmail.com'
app.config['MAIL_PASSWORD']='201524617!a'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

app.secret_key="2342asfkjawesld234kfjsld123111"


now_user=""
now_user_id=""
choice_account=""
loan_choice_account=""
now_accounts=""
status_login=0

EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class transfer_class:
	def __init__(self, date, what, who, money, sum):
		self.date=date
		self.what=what
		self.who=who
		self.money=money
		self.sum=sum

@app.route('/',methods=['GET'])
def index():
	return render_template("/hom2.html")

@app.route('/register', methods=['GET'])
def init_register():
	return render_template("register.html")

@app.route('/register', methods=['POST'])
def register():
	if len(request.form['email'])<1:
		flash('Email cannot be blank!')
		return redirect('/register')

	elif not EMAIL_REGEX.match(request.form['email']):
		flash('Invalid Email Address!')
		return redirect('/register')

	elif len(request.form['name'])<1:
		flash('first_name cannot be blank!')
		return redirect('/register')

	elif len(request.form['password'])<3:
		flash('password short! password is more than 8 character ')
		return redirect('/register')

	elif request.form['password_confirmation'] != request.form['password']:
		flash('password not match ! ')
		return redirect('/register')


	else:
		sql="SELECT * FROM userinfor WHERE id='{}'".format(request.form['id'])
		curs.execute(sql)
		id_check=curs.fetchall()

		if not id_check :
			new_name=request.form['name']
			new_Id=request.form['id']
			new_email=request.form['email']
			new_password=request.form['password']

			sql="INSERT INTO userinfor (name, id, pw, email) VALUES('{}', '{}','{}','{}')".format(new_name, new_Id, new_password, new_email)
			curs.execute(sql)
			conn.commit();
			return render_template("hom2.html")
		else :
			flash('can`t use this id')
			return redirect('/register')

@app.route('/login', methods=['GET'])
def login():
	return render_template("/login2.html")


@app.route('/do_login', methods=['GET'])
def do_login():
	login_id=request.args.get('id')
	login_password=request.args.get('password')

	if request.args.get('login') == 'login' :
		sql="SELECT * FROM userinfor WHERE id='{}' AND pw='{}'".format(login_id, login_password)
		curs.execute(sql)
		login_re=curs.fetchall()

		if not login_re :
			flash('invaild input ! ')
			return render_template("/login2.html")

		global now_user
		global now_user_id
		global status_login
		now_user=login_re[0][1]
		now_user_id=login_re[0][2]
		status_login=1;

		return render_template("/hom2.html",now_user_name=now_user)
	elif request.args.get('join') == 'join' :
		return render_template("/register.html")

@app.route('/logout', methods=['GET'])
def logout():
	global now_user
	global now_user_id
	global choice_account
	global now_accounts
	global status_login

	now_user=""
	now_user_id=""
	now_accounts=""
	choice_account=""
	status_login=0;

	return render_template("/hom2.html")

@app.route('/mybank', methods=['GET'])
def mybank():

	global status_login
	if status_login == 0 :
		return render_template("/login2.html")

	global now_user_id
	global now_accounts
	sql="SELECT * FROM accountinfor WHERE id='{}'".format(now_user_id)
	curs.execute(sql)
	now_accounts=curs.fetchall()

	return render_template("/my_bank2.html", now_accounts=now_accounts)

@app.route('/account_work', methods=['GET'])
def account_work():
	global now_user_id

	sql="SELECT * FROM accountinfor WHERE id='{}'".format(now_user_id)
	curs.execute(sql)
	account_infor=curs.fetchall()

	global choice_account
	choice_account= request.args.get('account')

	sql="SELECT * FROM accountinfor WHERE accountid='{}'".format(choice_account)
	curs.execute(sql)
	account_infor=curs.fetchall()
	now_money=account_infor[0][4]


	global now_user
	if request.args.get('transfer') == 'transfer' :
		return render_template("/transfer2.html",now_user_name=now_user,choice_account=choice_account)
	elif request.args.get('history') == 'history' :
		transfer_infor=[]
		sql="SELECT * FROM transferinfor WHERE sender_account='{}'".format(choice_account)
		curs.execute(sql)
		t_infor=curs.fetchall()
	
		for t in t_infor :
			transfer_infor.append(transfer_class(t[1], "send", t[3], t[4], t[8]))

		sql="SELECT * FROM transferinfor WHERE receiver_account='{}'".format(choice_account)
		curs.execute(sql)
		t_infor=curs.fetchall()
	
		for t in t_infor :
			transfer_infor.append(transfer_class(t[1], "receive", t[3], t[5], t[9]))

		return render_template("/history2.html", now_user_name=now_user,account_infor=account_infor ,now_money=now_money, choice_account=choice_account, transfer_infor=transfer_infor)


@app.route('/history_account', methods=['POST'])
def history_account():
	global now_user_id
	global now_user

	sql="SELECT * FROM accountinfor WHERE id='{}'".format(now_user_id)
	curs.execute(sql)
	account_infor=curs.fetchall()

	account=request.form['account']
	date=request.form['date']
	what=request.form['what']

	sql="SELECT * FROM transferinfor "
	curs.execute(sql)
	account_history=curs.fetchall()

	re_history_account=[]

	if what == 'all' :
		for i in account_history :
			if i[6] == account :
				re_history_account.append(transfer_class(i[1], "send", i[3], i[4], i[8]))
			elif i[7] ==account :
				re_history_account.append(transfer_class(i[1], "receive", i[3], i[5], i[9]))
	elif what =='in' :
		for i in account_history :
			if i[7] ==account :
				re_history_account.append(transfer_class(i[1], "receive", i[3], i[5], i[9]))
	elif what =='out' :	
		for i in account_history :
			if i[6] == account :
				re_history_account.append(transfer_class(i[1], "send", i[3], i[4], i[8]))

	sql="SELECT * FROM accountinfor WHERE accountid='{}'".format(account)
	curs.execute(sql)
	account_infor=curs.fetchall()
	now_money=account_infor[0][4]
	print (now_money)


	return render_template("/history2.html", now_user_name=now_user, choice_account=account, now_money=now_money, transfer_infor=re_history_account,account_infor=account_infor )



@app.route('/send_money', methods=['POST'])
def send_money():
	global choice_account
	global now_user

	sql="SELECT * FROM accountinfor WHERE accountid='{}'".format(choice_account)
	curs.execute(sql)
	check_account=curs.fetchall()
	if  check_account[0][3] != request.form['password'] :
		return render_template("/transfer2.html")
	
	if request.form['send_money'] < 1 :
		return render_template("/transfer.html")

	if request.form['receiver_account'] < 1 :
		return render_template("/transfer2.html")

	want_send_money=int(request.form['send_money'])
	if  check_account[0][4] < want_send_money :
		return render_template("/transfer2.html")

	receiver_account=request.form['receiver_account']

	sql="SELECT * FROM accountinfor WHERE accountid='{}'".format(receiver_account)
	curs.execute(sql)
	sql_receiver_account=curs.fetchall()


	if not sql_receiver_account :
		re_receiver_account=receiver_account
		re_receiver='don`t know'
		re_receiver_money=want_send_money
	else :
		re_receiver_account=sql_receiver_account[0][3]
		re_receiver=sql_receiver_account[0][2]
		re_receiver_money=sql_receiver_account[0][5]+want_send_money


	now=datetime.datetime.now()
	date=now.strftime('%y-%m-%d, %H:%M')
	change_money=check_account[0][4]-want_send_money


	sql="INSERT INTO transferinfor (date, what, sender, receiver, money, receiver_sum, sender_sum, sender_account, receiver_account)VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(date, 'send',now_user, re_receiver, want_send_money,re_receiver_money, change_money, choice_account, re_receiver_account   )
	curs.execute(sql)
	conn.commit();

	sql="UPDATE accountinfor SET money={} WHERE accountid={}".format(change_money, choice_account)
	curs.execute(sql)
	conn.commit();
	global now_accounts

	return render_template("/my_bank2.html",now_accounts=now_accounts)

@app.route('/go_change_myinfor', methods=['POST'])
def go_change_myinfor():
	global status_login
	if status_login == 0 :
		return render_template("/login2.html")

	return render_template("/change_myinfor.html")

@app.route('/change_myinfor', methods=['POST'])
def change_myinfor():

	if request.form['password'] != request.form['re_password'] :
		flash('password not match ! ')
		return render_template("/change_myinfor.html")

	if request.form['email'] <1 :
		flash('email is blank ! ')
		return render_template("/change_myinfor.html")

	new_password=request.form['password']
	new_email=request.form['email']
	global now_user_id

	sql="UPDATE userinfor SET pw='{}', email='{}' WHERE id='{}'".format(new_password, new_email,now_user_id)
	curs.execute(sql)
	conn.commit();

	global now_accounts

	return render_template("/my_bank2.html",now_accounts=now_accounts)

@app.route('/loan', methods=['GET'])
def loan():

	global status_login
	if status_login == 0 :
		return render_template("/login2.html")
	global now_user_id

	global now_loan_accounts
	sql="SELECT * FROM loan_accountinfor WHERE id='{}'".format(now_user_id)
	curs.execute(sql)
	now_loan_accounts=curs.fetchall()

	return render_template("/loan2.html", now_loan_accounts=now_loan_accounts)

@app.route('/loan_history', methods=['GET'])
def loan_history():
	global now_user_id

	sql="SELECT * FROM loan_accountinfor WHERE id='{}'".format(now_user_id)
	curs.execute(sql)
	loan_history1=curs.fetchall()

	sql="SELECT * FROM return_loaninfor WHERE id='{}'".format(now_user_id)
	curs.execute(sql)
	loan_history=curs.fetchall()

	return render_template("/loan_history.html",loan_account_infor=loan_history1, loan_history=loan_history)

@app.route('/loan_history_infor', methods=['POST'])
def loan_history_infor():
	global now_user
	global now_user_id

	loan_account=request.form['loan_account']
	date=request.form['date']

	sql="SELECT * FROM loan_accountinfor WHERE id='{}".format(now_user_id)
	curs.execute(sql)
	loan_history1=cure.fetchall()

	sql="SELECT * FROM loan_accountinfor WHERE loan_account='{}".format(loan_account)
	curs.execute(sql)
	loan_history=cure.fetchall()
	loan=loan_history[0]

	sql="SELECT * FROM loan_transferinfor WHERE loan_account='{}".format(loan_account)
	curs.execute(sql)
	loan_history=cure.fetchall()

	return render_template("/loan_history.html", loan_account_infor=loan_account_infor, loan_history=loan_history1, loan_account=loan)



@app.route('/return_loan', methods=['GET'])
def return_loan():
	global now_user_id
	sql="SELECT * FROM loan_accountinfor WHERE id='{}'".format(now_user_id)
	curs.execute(sql)
	loan_infor=curs.fetchall()

	sql="SELECT * FROM accountinfor WHERE id='{}'".format(now_user_id)
	curs.execute(sql)
	account_infor=curs.fetchall()

	return render_template("/return_loan.html", loan_infor=loan_infor, account_infor=account_infor)

@app.route('/send_loan_money', methods=['POST'])
def send_loan_money():
	global now_user_id
	global now_user
	account=request.form['account']
	loan_account=request.form['loan_account']
	money=int(request.form['send_money'])


	sql="SELECT * FROM accountinfor WHERE accountid='{}'".format(account)
	curs.execute(sql)
	check_account=curs.fetchall()



	if check_account[0][3] != request.form['password'] :
		print ("11")
		return render_template("return_loan.html")

	if check_account[0][4] < money :
		print(check_account[0][4])
		return render_template("return_loan.html")

	sender_change_money=check_account[0][4]-money

	sql="SELECT * FROM loan_accountinfor WHERE loan_account='{}'".format(loan_account)
	curs.execute(sql)
	sql_receiver_account=curs.fetchall()

	now=datetime.datetime.now()
	date=now.strftime('%y-%m-%d, %H:%M')
	change_money=sql_receiver_account[0][4]-money

	sql="INSERT INTO return_loaninfor (date, money, sum, account, loan_account, id) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(date,money, change_money,account, loan_account,now_user_id )
	curs.execute(sql)
	conn.commit()

	sql="INSERT INTO transferinfor (date, what, sender, receiver, money, receiver_sum, sender_sum, sender_account, receiver_account)VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(date, 'send',now_user, "my-loan", money,"my-loan", sender_change_money, account, loan_account   )
	curs.execute(sql)
	conn.commit()

	sql="UPDATE accountinfor SET money={} WHERE accountid='{}'".format(sender_change_money, account)
	curs.execute(sql)
	conn.commit()

	sql="UPDATE loan_accountinfor SET loan_money={} WHERE loan_account='{}'".format(change_money, loan_account)
	curs.execute(sql)
	conn.commit()


	sql="SELECT * FROM return_loaninfor WHERE id='{}'".format(now_user_id)
	curs.execute(sql)
	loan_history=curs.fetchall()

	return render_template("loan_history.html", loan_history=loan_history)

@app.route("/consulting", methods=['GET'])
def consulting():
	return render_template("/consulting.html")

@app.route("/email", methods=['post','get'])
def email():

	if request.method=='POST':

		senders = request.form['name']
		senders_email= request.form['email_address']
		receiver = 'hans12312@naver.com'
		title=request.form['title']
		content = request.form['email_content']
		content="name : " + senders+"\n"+"sender mail : " + senders_email+"\n\n"+content
		receiver = receiver.split(',')
        
        for i in range(len(receiver)):
        	receiver[i] = receiver[i].strip()
           
        result = send_email(senders, receiver,title ,content)
        
        if not result:
        	return render_template('consulting.html')
        else:
        	return render_template('consulting.html')

    
def send_email(senders, receiver, title,content):
    try:
    	title="[team4bank] "+title
        mail = Mail(app)
        msg = Message(title, sender = senders, recipients = receiver)
        msg.body = content
        mail.send(msg)
    except Exception:
    	print("bbb")
        pass 
    finally:
        pass


@app.route('/aboard', methods=['GET'])
def aboard():
	return render_template("/aboard.html")

@app.route('/exchange', methods=['GET'])
def  exchange():
	return render_template("/exchange.html")


@app.route('/aboard_transfer', methods=['GET'])
def aboard_transfer():
	return render_template("/aboard_transfer.html")


@app.route('/ok_oversea_transfer', methods=['POST'])
def ok_oversea_transfer():
	global status_login
	if status_login == 0 :
		return render_template("/login2.html")	
	return render_template("/ok_oversea_transfer.html")


if __name__ == "__main__":
    app.run(port=5001, debug=True)