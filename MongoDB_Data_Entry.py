import pymongo as pm
import pandas as pd
import math
import threading

client= pm.MongoClient('localhost',27017) #make a client to connect to mongodb default port
db= client.new_database1    #create a database
users= db.users             #create a collection

SM_xl= pd.ExcelFile('Sawai-Madhopur.xlsx')  #create a dataframe in pandas
TR_xl= pd.ExcelFile('Tonk-Rajasthan.xlsx')  #create a dataframe in pandas
df1=pd.read_excel('Sawai-Madhopur-Rajasthan.xlsx')  #create a dataframe in pandas
list1=df1.to_dict(orient='records') #create a list of dictionaries in python
list_of_fields=list(pd.read_excel('Sawai-Madhopur-Rajasthan.xlsx').columns) #create a list of fields in Sawai-Madhopur-Rajasthan.xlsx

#remove these fields from the list
list_of_fields.remove('Name of the Subscriber')
list_of_fields.remove('Telephone Number')
list_of_fields.remove('ID')

list2=pd.read_excel('Mumbai30-50.xlsx').to_dict(orient='records')   #create a list of dictionaries in python
list3=pd.read_excel(TR_xl,'Sheet1').to_dict(orient='records')   #create a list of dictionaries in python
list4=pd.read_excel(TR_xl,'Sheet2').to_dict(orient='records')   #create a list of dictionaries in python
list5=list()
for i in  range(10):
    list5+=pd.read_excel(SM_xl,'Sheet{}'.format(i+1)).to_dict(orient='records')     #create a list of dictionaries in python

'''
order data of each dictionary passed for Mumbai30-50.xlsx
'''
def ordered_dictM(d):
    d['Age']= d.pop('Age')
    d['Phone Number']= d.pop('Mobile No.')
    if(type(d['Phone Number'])==int):           #check validity of input
        if(d['Phone Number'] > 9999999999999):
            d['Phone Number']='Invalid'
    if(type(d['Phone Number'])==str):
        if(len(d['Phone Number']) > 13):        #check validity of input
            d['Phone Number']='Invalid'
    return d

'''
order data of each dictionary passed for Tonk-Rajasthan.xlsx sheet1
'''
def ordered_dictTR1(d):
    d['Name']= d.pop('Customer Name')
    d['Phone Number']= d.pop('Phone Number')
    d['Address']= d.pop('Customer Address')
    d['City']= d.pop('City')
    return d

'''
order data of each dictionary passed for Tonk-Rajasthan.xlsx sheet2
'''
def ordered_dictTR2(d):
    d['First Name']= d.pop('Name')
    d['Last Name']= d.pop('Last Name')
    d['Phone number']= d.pop('Number')
    d['Alternate Phone number']=d.pop('Alt number')
    d['ADDRESS_LINE1']= d.pop('ADDRESS_LINE1')
    d['ADDRESS_LINE2']= d.pop('ADDRESS_LINE2')
    d['ADDRESS_LINE3']= d.pop('ADDRESS_LINE3')
    d['city']= d.pop('CITY')
    d['ZIP']= d.pop('ZIP')
    return d


'''
order data of each dictionary passed for Sawai-Madhopur-Rajasthan.xlsx
'''
def ordered_dictSMR(d):
    d['Name']= d.pop('Name of the Subscriber')
    d['Phone number']= d.pop('Telephone Number')
    d['ID']= d.pop('ID')
    for item in list_of_fields:
        d[item]=d.pop(item)
    return d

'''
check if any field of a dictionary is empty
'''
def checkEmpty(d):
    for key in d:
        if(type(d[key])==int):      #to avoid TypeError
            if(math.isnan(d[key])):
                d[item]=''
    return d

'''
order data of each dictionary passed for Sawai-Madhopur.xlsx
'''
def ordered_dictSM(d):
    for ok in ['Name','Gender','mobile','address']:
        for key in d.keys():
            if key==ok:
                d[ok]= d.pop(ok)
    return d

'''
to insert data in the collection users in new_database1 in MongoDB
'''
def insert5(l):
    for item in l:
        db.users.insert_one(ordered_dictSM(item))

def insert2(l):
    for item in l:
        db.users.insert_one(ordered_dictM(checkEmpty(item)))

def insert3(l):
    for item in l:
        db.users.insert_one(ordered_dictTR1(checkEmpty(item)))

def insert4(l):
    for item in l:
        db.users.insert_one(ordered_dictTR2(checkEmpty(item)))

def insert1(l):
    for item in l:
        db.users.insert_one(ordered_dictSMR(checkEmpty(item)))

#will run if not imported
if __name__ == "__main__":

    #define threads where target is function and args is arguements to be passed
    t1=threading.Thread(target=insert1,args=(list1,))
    t2=threading.Thread(target=insert2,args=(list2,))
    t3=threading.Thread(target=insert3,args=(list3,))
    t4=threading.Thread(target=insert4,args=(list4,))
    t5=threading.Thread(target=insert5,args=(list5,))

    #start threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    #join threads when done
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
