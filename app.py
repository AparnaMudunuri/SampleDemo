#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask,render_template,request,redirect,url_for

import config

import pymysql


# In[ ]:


host="custom-mysql.gamification.svc.cluster.local"
port=3306
dbname="sampledb"
user="xxuser"
password="welcome1"

conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname,cursorclass=pymysql.cursors.DictCursor)


# In[ ]:


cursor = conn.cursor()


# In[ ]:


app = Flask(__name__)


# In[ ]:


retrive = f"Select * from XXIBM_PRODUCT_SKU where DESCRIPTION LIKE '%jac%' LIMIT 1;"
cursor.execute(retrive)
rows = cursor.fetchall()
len(rows)


# In[ ]:


url_dict = {}
@app.route('/')
def show_first():
    return render_template("index.html")

#@app.route('/show_index/<select_key>')
#def show_index(select_key):
#    return render_template("index.html", user_image = url_dict['URL'])



@app.route('/',methods=['POST','GET'])
def my_form_post():
    
   
    text = request.form['u']
    url_key = text.lower()
    
    retrive = f"Select * from XXIBM_PRODUCT_SKU where DESCRIPTION LIKE '%{url_key}%' LIMIT 1;"
    cursor.execute(retrive)
    rows = cursor.fetchall()
    
    if len(rows) != 0:
        url_dict = rows[0]
        select_key = url_dict['DESCRIPTION']
        
    else:
        retrive = "Select * from XXIBM_PRODUCT_SKU where DESCRIPTION ='none';"
        cursor.execute(retrive)
        rows = cursor.fetchall()
        url_dict = rows[0]
        select_key = url_dict['DESCRIPTION']
    
    print(select_key)
        


    return render_template("index.html", user_image = url_dict['u'])


# In[ ]:


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)


# In[ ]:




