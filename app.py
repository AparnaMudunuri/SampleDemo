#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask,render_template,request,redirect,url_for

import config

import pymysql

import os
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import json
import requests

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

cos_service_credentials = {
    "apikey": "_bAzHuCAN1yPz4Rcg5CZY1Tbp0UOpshuMhpoNkIvJAa3",
    "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
    "iam_apikey_description": "Auto-generated for key b766a2b2-aacd-4a78-aaed-1784769a82a6",
    "iam_apikey_name": "gamification-cos-standard-tkq",
    "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
    "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/693fe8ead49b44b192004113d21b15c2::serviceid:ServiceId-f6d85b01-d45a-4d92-831d-3e3efa44bb3c",
    "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/693fe8ead49b44b192004113d21b15c2:fce26086-5b77-42cc-b1aa-d388aa2853d7::"
}

endpoints = requests.get(cos_service_credentials['endpoints']).json()
iam_host = (endpoints['identity-endpoints']['iam-token'])
cos_host = (endpoints['service-endpoints']['regional']['us-south']['public']['us-south'])
auth_endpoint = "https://" + iam_host + "/oidc/token"
service_endpoint = "https://" + cos_host

cos = ibm_boto3.resource("s3",
    ibm_api_key_id=cos_service_credentials['apikey'],
    ibm_service_instance_id=cos_service_credentials['resource_instance_id'],
    ibm_auth_endpoint=auth_endpoint,
    config=Config(signature_version="oauth"),
    endpoint_url=service_endpoint
)


        

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
        
    def get_item(bucket_name, item_name):
      print("Retrieving item {0} from bucket {1}".format(item_name, bucket_name))
      try:
        obj = cos.Object(bucket_name, item_name).get()
        v2= obj['Body'].read()
        return obj['Body'].read()
      except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
      except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))
        
    bucket_name = "gamification-cos-standard-tkq"
    item_name = "1001.jpg"
    
    img = get_item(bucket_name, item_name)

    return render_template("index.html", user_image = img)


# In[ ]:


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)


# In[ ]:




