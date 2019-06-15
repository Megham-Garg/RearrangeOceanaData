import pymongo as pm
import pandas as pd
import math
import threading

client= pm.MongoClient('localhost',27017)	#create client to connect to the server
db= client.new_database				#create new database
usersM= db.usersM				#create collection for Mumbai30-50.xlsx
usersTR= db.usersTR				#create collection for Tonk-Rajasthan.xlsx
usersSM= db.usersSM				#create collection for Sawai-Madhopur.xlsx
usersSMR= db.usersSMR				#create collection for Sawai-Madhopur-Rajasthan.xlsx

SM_xl= pd.ExcelFile('Sawai-Madhopur.xlsx')
TR_xl= pd.ExcelFile('Tonk-Rajasthan.xlsx')
df1=pd.read_excel('Sawai-Madhopur-Rajasthan.xlsx')
list_of_fields=list(pd.read_excel('Sawai-Madhopur-Rajasthan.xlsx').columns)
list_of_fields.remove('Name of the Subscriber')
list_of_fields.remove('Telephone Number')
list_of_fields.remove('ID')

#create of list of dictionaries
list1=df1.to_dict(orient='records')	
list2=pd.read_excel('Mumbai30-50.xlsx').to_dict(orient='records')
list3=pd.read_excel(TR_xl,'Sheet1').to_dict(orient='records')
list4=pd.read_excel(TR_xl,'Sheet2').to_dict(orient='records')
list5=list()
for i in  range(10):
    list5+=pd.read_excel(SM_xl,'Sheet{}'.format(i+1)).to_dict(orient='records') #create of list of dictionaries

'''
to order the data of list2
'''
def ordered_dictM(d):
    d['Age']= d.pop('Age')
    d['Phone Number']= d.pop('Mobile No.')
    if(type(d['Phone Number'])==int):
        if(d['Phone Number'] > 9999999999999):
            d['Phone Number']='Invalid'
    if(type(d['Phone Number'])==str):
        if(len(d['Phone Number']) > 13):
            d['Phone Number']='Invalid'
    return d


'''
to order the data of list3
'''
def ordered_dictTR1(d):
    d['Name']= d.pop('Customer Name')
    d['Phone Number']= d.pop('Phone Number')
    d['Address']= d.pop('Customer Address')
    d['City']= d.pop('City')
    return d


'''
to order the data of list4
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
to order the data of list1
'''
def ordered_dictSMR(d):
    d['Name']= d.pop('Name of the Subscriber')
    d['Phone number']= d.pop('Telephone Number')
    d['ID']= d.pop('ID')
    for item in list_of_fields:
        d[item]=d.pop(item)
    return d

def checkEmpty(d):
    for key in d:
        if(type(d[key])==int):
            if(math.isnan(d[key])):
                d[item]=''
    return d


'''
to order the data of list5
'''
def ordered_dictSM(d):
    for ok in ['Name','Gender','mobile','address']:
        for key in d.keys():
            if key==ok:
                d[ok]= d.pop(ok)
    return d

#insert data into corresponding collections
def insert5(l):
    for item in l:
        db.usersSM.insert_one(ordered_dictSM(item))

def insert2(l):
    for item in l:
        db.usersM.insert_one(ordered_dictM(item))

def insert3(l):
    for item in l:
        db.usersTR.insert_one(ordered_dictTR1(item))

def insert4(l):
    for item in l:
        db.usersTR.insert_one(ordered_dictTR2(item))

def insert1(l):
    for item in l:
        db.usersSMR.insert_one(ordered_dictSMR(checkEmpty(item)))

if __name__ == "__main__":
    t1=threading.Thread(target=insert1,args=(list1,))
    t2=threading.Thread(target=insert2,args=(list2,))
    t3=threading.Thread(target=insert3,args=(list3,))
    t4=threading.Thread(target=insert4,args=(list4,))
    t5=threading.Thread(target=insert5,args=(list5,))

    #start the thread
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    #end the thread
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()