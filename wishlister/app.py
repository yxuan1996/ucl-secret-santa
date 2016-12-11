from flask import Flask, render_template, json, request,redirect,session
from flask.ext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'suddenven'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Penguin123'
app.config['MYSQL_DATABASE_DB'] = 'bucketlist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/signuppage')
def showsignuppage():
        return render_template('signuppage.html')

@app.route('/userHome')
def userHome():
    return render_template('userHome.html')

@app.route('/sendemails')
def db():
    db = mysql.connect()
    cursor = db.cursor()
    cursor.execute("SELECT * from tbl_user")

    rows = cursor.fetchall()

    db.close()

    return rows

from random import randint
from optparse import OptionParser
import csv
import sys
import smtplib


filename = db()
participants = [line.rstrip('\n').split(',') for line in open(filename)]

def calculatePairs():
  giftlist = participants[:]
  random.shuffle(giftlist)
  length = len(giftlist)
  for x in range(0,(length-1)):
     pairs[giftlist[x][0]] = giftlist[x+1][0]
  pairs[giftlist[length-1][0]] = giftlist[0][0]
print(calculatePairs())

def sendMail():
 relay = "127.0.0.1"

 sender = 'secretsantauclporticode@gmail.com'
 subject = 'Secret Santa\n'
 text ='''This Christmas you will make this person happy by being their Secret Santa! \n
     This person has suggested a  of things that would make a nice Christmas Gift.\n
     And shhh!! Keep this secret!'''

 for n in participant
  i = participants.index(n)
  receipt = [pairs[n[0]]]
  gifttext = """Info about recipient:
  Name : %s
  Address:%s
          %s
          %s
  Wishlist: %s"""

  message= """
  From: %s
  To: %s
  Subject %s

  %s
  %s""" % (sender, receipt, subject,text, giftlist)

  print message
  server = smtplib.SMTP(relay)
  server.sendmail(sender,receipt,message)
  server.quit()

participants = []
pairs = {}
calculatePairs()
sendMail()

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['name']
        _email = request.form['email']
        _alist = request.form['alist']
        _blist = request.form['blist']
        _clist = request.form['clist']
        _housenumber = request.form['housenumber']
        _street = request.form['street']
        _postcode = request.form['postcode']
        _city = request.form['city']
        _country = request.form['country']

        # validate the received values
        if _name and _email and _alist and _blist and _clist and _housenumber and _street and _postcode and _city and _country:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            query = "INSERT INTO tbl_user (user_name, user_email, user_alist, user_blist, user_clist, user_housenumber, user_street, user_postcode, user_city, user_country) VALUES (_name, _email, _alist, _blist, _clist, _housenumber, _street, _postcode, _city, _country)"
            cursor.execute(query)
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        pass
        #cursor.close()
        #conn.close()

if __name__ == "__main__":
    app.run(port=5002)
