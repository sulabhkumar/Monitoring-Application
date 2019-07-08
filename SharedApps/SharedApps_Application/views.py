from django.shortcuts import render,get_object_or_404
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from datetime import date
import MySQLdb as my
import pandas as pd
import csv
import time
from django import forms
import logging
import logging
from time import sleep
from pathlib import Path
import os
import shutil
import glob
import base64
import io
from django.http import FileResponse
log = logging.getLogger(__name__)



# Create your views here.
def index(request):
	connection=Databaseconnection(request)
	print('Database-view->',connection)
	print(connection[0],connection[1],connection[2],connection[3])
	Dbname=connection[0]
	username=connection[1]
	password=connection[2]
	host=connection[3]
	import mysql.connector
	database = mysql.connector.connect (host=host, user = username, passwd =password, db = Dbname)
	cursor = database.cursor()
	cursor1= database.cursor(buffered=True)
	cursor2= database.cursor(buffered=True)
	cursor3= database.cursor(buffered=True)
	cursor4= database.cursor(buffered=True)
	cursor5= database.cursor(buffered=True)
	cursor6= database.cursor(buffered=True)
	cursor7= database.cursor(buffered=True)
	cursor8= database.cursor(buffered=True)

	cursor1.execute("SELECT count(*),priority FROM incidentdb WHERE priority =  '4 - Low'" )
	low = cursor1.fetchone()
	print("low",low[0])
	log.debug(low)
	cursor.execute("SELECT count(*),priority FROM incidentdb WHERE priority =  '3 - Medium'" )
	Medium = cursor.fetchone()
	print("Medium",Medium[0])
	log.debug(Medium )
	cursor2.execute("SELECT count(*),priority FROM incidentdb WHERE priority =  '2 - High'" )
	high = cursor2.fetchone()
	print("high",high[0])
	log.debug(high )
	cursor3.execute("SELECT count(*),priority FROM incidentdb WHERE priority =  '1 - Critical'" )
	critical = cursor3.fetchone()
	print("critical",critical[0])
	log.debug(critical)
	priority_count = [critical[0],high[0],Medium[0],low[0]]
	print(priority_count)
	cursor4.execute("SELECT DISTINCT assigned_to,id FROM incidentdb order by assigned_to " )
	assignTo = cursor4.fetchall()
	print(len(assignTo))
	print("name->",assignTo)
	
	cursor5.execute("select count(*) from LogGraph where Activity='Add application' " )
	addcount = cursor5.fetchall()
	log.debug(addcount)
	cursor6.execute("select count(*) from LogGraph where Activity='Delete application' " )
	deletecount = cursor6.fetchall() 
	log.debug(deletecount)
	cursor7.execute("select count(*) from LogGraph where Activity='Update application' " )
	updatecount = cursor7.fetchall() 
	log.debug(updatecount)
	count=[]
	count.append(addcount[0][0])
	count.append(deletecount[0][0])
	count.append(updatecount[0][0])
	print("count",count)

	cursor8.execute("SELECT Application,expiredate FROM sharedapps_application_certificatedb order by expiredate asc limit 3 " )
	certificate = cursor8.fetchall()
	print("certificate->",certificate)
	log.debug(certificate)




	return render(request,'index.html',{'priority_count':priority_count,'assignTo':assignTo,'count':count,'certificate':certificate})


def saveIncident(request):
	if request.method == 'POST':
		uploaded_file = request.FILES['document']
		print("Uploadfile name->",uploaded_file.name)
		print("Uploadfile name->",uploaded_file.size)
		log.debug(uploaded_file.name)

		#FileName=uploaded_file.name
		fs = FileSystemStorage()
		FileName=str(date.today())+'_'+str(datetime.now().hour)+'-'+str(datetime.now().minute)+'_'+uploaded_file.name
		print("FileName->",FileName)
		fs.save(FileName,uploaded_file)
		print("file Upload Successfully")
		log.debug("file Upload Successfully")
		#Read latest file in the media floder
		# print(latest_file)
		Data='F:/website/website/media'+'/'+FileName

		print("Data",Data)
		cleandata = pd.read_csv(Data, error_bad_lines=False)
		# overwriting column with replaced value of age
		cleandata["description"]= cleandata["description"].str.replace("'", "\\'", case = False)
		cleandata["description"]= cleandata["description"].str.replace('"', '\\"', case = False)
		cleandata.to_csv('F:/website/website/media/'+'clean'+FileName, index=False)
		NewFile='F:/website/website/media/'+'clean'+FileNam
		print(NewFile)
		log.debug(NewFile)

		import csv
		import mysql.connector
		connection=Databaseconnection(request)
		print(connection[0],connection[1],connection[2],connection[3])
		Dbname=connection[0]
		username=connection[1]
		password=connection[2]
		host=connection[3]
		database = mysql.connector.connect (host=host, user = username, passwd =password, db = Dbname)
		cursor = database.cursor()
		with open(NewFile, newline='',  encoding="utf8") as csvfile:
			next(csvfile)
			reader=csv.reader(csvfile)
			count=0
			for row in reader:
				# Prepare SQL query to INSERT a record into the database.
				check=row[0]
				state=row[2]
				priority=row[1]
				assigned_to=row[3]
				short_description=row[4]
				cmdb_ci=row[5]
				u_affected_user_email=row[6]
				sys_created_on=row[7]
				assignment_group_name=row[8]
				description=row[9]
				sys_updated_on=row[10]
				sys_updated_by=row[11]

				print("id",check)
				print("state",state)
				cursor.execute("SELECT count(*),id FROM incidentdb WHERE id =  %s",(check,) )
				msg = cursor.fetchone()
				print(count,"MSG-->",msg)
				log.debug(msg)


				count=count+1
				if msg[0] == 0:
					sql = "INSERT INTO incidentdb(id,priority,state,assigned_to,short_description,cmdb_ci,u_affected_useremail,sys_created_on,assignment_groupname,descriptions,Tsys_updated_on,sys_updated_by) VALUES ('%s','%s', '%s','%s','%s', '%s','%s','%s', '%s','%s','%s', '%s');" % (row[0], row[1], row[2],row[3], row[4], row[5],row[6], row[7], row[8],row[9], row[10],row[11])
					print(sql)
					print("After_Sql_id",check)
					log.debug("After_Sql_id",check)
					try:
					# Execute the SQL commandl
						print("IN_Try_id",check)
						cursor.execute(sql)
						# Commit your changes in the database
						print("id in commit",check)
						log.debug("id in commit",check)
						database.commit()
					except my.Error as e:
						print(e)
						log.error(e)
						# Rollback in case there is any error
						database.rollback()
					print("Successfully Store Data in Database")
					log.debug("Successfully Store Data in Database")
				else:
					print("Duplicate")
					log.warn("Duplicate")
					cursor.execute("UPDATE incidentdb SET priority = %s,state = %s,assigned_to = %s,short_description= %s,cmdb_ci= %s,u_affected_useremail=%s,sys_created_on = %s,assignment_groupname = %s,descriptions = %s,Tsys_updated_on = %s,sys_updated_by = %s WHERE id = %s",(priority,state,assigned_to,short_description,cmdb_ci,u_affected_user_email,sys_created_on,assignment_group_name,description,sys_updated_on,sys_updated_by,check))
					database.commit()
					print(cursor.rowcount, "record(s) affected")
					print("Update Rows Sucessfully")
					log.debug("Update Rows Sucessfully")
		# time.sleep(5)
# Move solved incident to backup Database
		import mysql.connector
		import csv
		import mysql.connector
		connection=Databaseconnection(request)
		print(connection[0],connection[1],connection[2],connection[3])
		log.debug(connection[0],connection[1],connection[2],connection[3])
		Dbname=connection[0]
		username=connection[1]
		password=connection[2]
		host=connection[3]
		database = mysql.connector.connect (host=host, user = username, passwd =password, db = Dbname)


		Dbid=[]
		cursor1 = database.cursor()
		cursor1.execute("SELECT id FROM incidentdb")
		msg = cursor1.fetchall()
		Dbid=[i[0] for i in msg]

		print("Dbid->",Dbid)
		log.debug("Dbid->",Dbid)

		with open(NewFile, newline='',  encoding="utf8") as csvfile:
		    next(csvfile)
		    i=0
		    csvid=[]
		    reader=csv.reader(csvfile)
		    for row in reader:
		        csvid.append(row[0])    
		    print("csvid->",csvid)
		    log.debug("csvid->",csvid)


		remain=set(Dbid)-set(csvid)
		remainlist=list(remain)
		print("remainList->",remainlist)
		length = len(remain)
		print("length",length)
		print(type(remainlist))
		if Dbid != csvid:
		    if length == 0:   
		        print("nothing to backup")
		    elif length == 1:
		        Rid=str(list(remain)[0])
		        print("Rid=",Rid)
		        print("type",type(Rid))
		        cursor1.execute("INSERT INTO backup SELECT * FROM incidentdb WHERE id = %s",(Rid,))
		        database.commit()
		        print("insert in Backup Database Successfully")
		        log.debug("insert in Backup Database Successfully")
		        cursor1.execute("DELETE FROM incidentdb WHERE id = %s",(Rid,))
		        database.commit()
		    else:
		        cursor1.execute("INSERT INTO backup SELECT * FROM incidentdb WHERE id IN %s" % str(tuple(remainlist)))
		        database.commit()
		        print("insert in Backup Database Successfully")
		        log.debug("insert in Backup Database Successfully")
		        cursor1.execute("DELETE FROM incidentdb WHERE id IN %s" % str(tuple(remainlist)))
		        database.commit()
		        print("Delete from Table Successfully")
		        log.debug("Delete from Table Successfully")


	return render(request,'saveIncident.html')



def basic(request):
	return render(request,'basic.html')

def DisplayIncident(request):
	print("In FETCH remaingTime")
	log.debug("In FETCH remaingTime")
	connection=Databaseconnection(request)
	print('Database-view->',connection)
	print(connection[0],connection[1],connection[2],connection[3])
	Dbname=connection[0]
	username=connection[1]
	password=connection[2]
	host=connection[3]
	import mysql.connector
	import pandas as pd
	import sqlalchemy
	from sqlalchemy import create_engine
	engine = sqlalchemy.create_engine("mysql+pymysql://"+username+":"+password+"@"+host+":3306/"+Dbname+"")
	Data=pd.read_sql_table("incidentdb",engine)
	import pandas as pd
	import sys
	import time
	import datetime as dt
	from datetime import datetime
	from datetime import timedelta
	import datetime

	Data['Remaining Resolution Time']=0
	Data['Remaining Response Time']=0


	Time=[]
	ApplicationType=[]
	stateval=[]
	assignname=[]


	EndTime=Data.sys_created_on
	statevalue=Data.priority
	TypeofApplication=Data.assignment_groupname
	assign = Data.assigned_to

	for time in EndTime:
	    Time.append(time)
	    print(time)

	for Type in TypeofApplication:
	    ApplicationType.append(Type)
	    print(Type)

	for value in statevalue:
	    stateval.append(value)
	    print(value)

	for name in assign:
            assignname.append(name)
            print(name)

	length=len(Data)
	for i in range(0,length):
	    Actualstartime= dt.datetime.strptime(Time[i], '%Y-%m-%d %H:%M:%S')
	    print("Actualstartime->",Actualstartime)
	    if ApplicationType[i]== 'VTAS-VAST-SA-AzureADMFA' or ApplicationType[i] == 'VTAS-VAST-SA-Perforce' or ApplicationType[i] == 'VTAS-VAST-SA-STASH' or ApplicationType[i] == 'VTAS-VAST-SA-AzureADSSO':
	            print('platinum')
	            log.debug('platinum')

	            if stateval[i] == '4 - Low':
	                Actulendtimes= dt.datetime.strptime(Time[i], '%Y-%m-%d %H:%M:%S') + timedelta(days=10)
	                ActualResponseTime=dt.datetime.strptime(Time[i],  '%Y-%m-%d %H:%M:%S') + timedelta(hours=18)
	            elif stateval[i] == '3 - Medium':
	                Actulendtimes= dt.datetime.strptime(Time[i],  '%Y-%m-%d %H:%M:%S') + timedelta(days=5)
	                ActualResponseTime=dt.datetime.strptime(Time[i],  '%Y-%m-%d %H:%M:%S') + timedelta(hours=9)
	            elif stateval[i] == '2 - High':
	                Actulendtimes= dt.datetime.strptime(Time[i], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
	                ActualResponseTime=dt.datetime.strptime(Time[i], '%Y-%m-%d %H:%M:%S') + timedelta(hours=2)
	            elif stateval[i] == '1 - Critical':
	                Actulendtimes= dt.datetime.strptime(Time[i],  '%Y-%m-%d %H:%M:%S') + timedelta(hours=4)
	                ActualResponseTime=dt.datetime.strptime(Time[i],  '%Y-%m-%d %H:%M:%S') + timedelta(hours=1)
	           
	    else:
	        print('Gold')
	        log.debug('Gold')
	        if stateval[i] == '4 - Low':
	            Actulendtimes= dt.datetime.strptime(Time[i],  '%Y-%m-%d %H:%M:%S') + timedelta(days=12)
	            ActualResponseTime=dt.datetime.strptime(Time[i], '%Y-%m-%d %H:%M:%S') + timedelta(hours=20)
	        elif stateval[i] == '3 - Medium':
	            Actulendtimes= dt.datetime.strptime(Time[i],  '%Y-%m-%d %H:%M:%S') + timedelta(days=6)
	            ActualResponseTime=dt.datetime.strptime(Time[i],  '%Y-%m-%d %H:%M:%S') + timedelta(hours=12)
	        elif stateval[i] == '2 - High':
	            Actulendtimes= dt.datetime.strptime(Time[i], '%Y-%m-%d %H:%M:%S') + timedelta(hours=24)
	            ActualResponseTime=dt.datetime.strptime(Time[i],  '%Y-%m-%d %H:%M:%S') + timedelta(hours=2)
	        elif stateval[i] == '1 - Critical':
	            Actulendtimes= dt.datetime.strptime(Time[i],  '%Y-%m-%d %H:%M:%S') + timedelta(hours=4)
	            ActualResponseTime=dt.datetime.strptime(Time[i],  '%Y-%m-%d %H:%M:%S') + timedelta(hours=1)

	    now = datetime.datetime.now()
	    if Actulendtimes < now:
	    	print(Actulendtimes,now)
	    	remainingResolutionTime = 0
	    else:
	        remainingResolutionTime=Actulendtimes - now 
	        print("RemainingResolutionTime ->",remainingResolutionTime)
	        Data['Remaining Resolution Time'][i]=remainingResolutionTime


	    if ActualResponseTime < now or assignname[i] is not None:
	        remainingResponseTime = 0
	    else:
	        remainingResponseTime=ActualResponseTime - now 
	        print("RemainingResponseTime ->",remainingResponseTime)
	        Data['Remaining Response Time'][i]=remainingResponseTime
	        
	        
	inform =Data.values.tolist()

  

  

	return render(request,'DisplayIncident.html', {'Data':inform})









#--------------------------------------Certificate-----------------------------------------#
from SharedApps_Application.models import certificateDb
from SharedApps_Application.forms import CertificateForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from shutil import copyfile
import mysql.connector


def download(request, pk):
# this url is for download
	try:
	    obj = certificateDb.objects.get(pk=pk)
	    #obj1= certificateDb.objects.get(Application=Application)
	    print("obj",obj.File)
	    File=str(obj.File)
	    Filename=File.split('/', 1)[-1]
	    print(Filename)

	except certificateDb.DoesNotExist as exc:
	    return JsonResponse({'status_message': 'No Resource Found'})
	get_binary = obj.bytes
	if get_binary is None:
	    return JsonResponse({'status_message': 'Resource does not contian image'})
	if isinstance(get_binary, memoryview):
	    binary_io = io.BytesIO(get_binary.tobytes())
	else:
	    binary_io = io.BytesIO(get_binary)
	response = FileResponse(binary_io)
	response['Content-Type'] = 'application/x-binary'
	response['Content-Disposition'] = 'attachment; filename="{}.csr"'.format(Filename) # You can set custom filename, which will be visible for clients.
	return response


def convertToBinaryData(latest_file):
    #Convert digital data to binary format
    with open(latest_file, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insertBLOB(request,Application,environment):
    print("Inserting BLOB into python_employee table")
    connection=Databaseconnection(request)
    print(connection[0],connection[1],connection[2],connection[3])
    Dbname=connection[0]
    username=connection[1]
    password=connection[2]
    host=connection[3]
    connection = mysql.connector.connect (host=host, user = username, passwd =password, db = Dbname,auth_plugin='mysql_native_password')
    list_of_files = glob.glob('F:/SharedApps/SharedApps/media/CSR/*.csr')
    latest_file = max(list_of_files, key=os.path.getctime)
    print('latest_file',latest_file)
	
    try:
        cursor = connection.cursor()
        sql = """ UPDATE `sharedapps_application_certificatedb` set
                          `bytes` = (%s) WHERE `Application` = (%s) and `environment_type`=(%s) """

        csrfile = convertToBinaryData(latest_file)
       
        # Convert data into tuple format

        insert_blob_tuple = (csrfile,Application,environment)
        result  = cursor.execute(sql, insert_blob_tuple)
        connection.commit()
        print(' result', result)
        print ("Image and file inserted successfully as a BLOB into python_employee table", result)
        files = glob.glob('F:/SharedApps/SharedApps/media/CSR/*')
        for f in files:
        	os.remove(f)
    except mysql.connector.Error as error :
    	connection.rollback()
    	print("Failed inserting BLOB data into MySQL table {}".format(error))
		


def list(request):
	certificatedata = certificateDb.objects.all()
	context = {
	'certificatedata': certificatedata
	}
	return render(request, 'list.html',context)

def save_form(request,Applicationname,environmenttype,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True

			certificatedata = certificateDb.objects.all()
			data['list'] = render_to_string('list_2.html',{'certificatedata':certificatedata})
			log.debug("Successfully save Certificate")
			insertBLOB(request,Applicationname,environmenttype)
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

def certificate_create(request):
	if request.method == 'POST':
		form = CertificateForm(request.POST, request.FILES or None)
		print(request.FILES)
		if form.is_valid():
			Filename=form.cleaned_data['File']
			# print('File',File)
			Applicationname=form.cleaned_data['application']
			environmenttype=form.cleaned_data['environment_type']
			print(Filename,Applicationname,environmenttype)	
			log.debug("Successfully create Certificate")
	else:
		form = CertificateForm()
		Applicationname=""
		environmenttype=""
	return save_form(request,Applicationname,environmenttype,form,'certificate_create.html')

def certificate_update(request,id):
	certificate = get_object_or_404(certificateDb,id=id)
	if request.method == 'POST':
		print(request.FILES)
		form = CertificateForm(request.POST, request.FILES or None,instance=certificate)
		if form.is_valid():
			Filename=form.cleaned_data['File']
			# print('File',File)
			Applicationname=form.cleaned_data['application']
			environmenttype=form.cleaned_data['environment_type']
			print(Filename,Applicationname,environmenttype)	
			log.debug("Successfully Update Certificate")
	else:
		form = CertificateForm(instance=certificate)
		Applicationname=""
		environmenttype=""
	return save_form(request,Applicationname,environmenttype,form,'certificate_update.html')


def certificate_delete(request,id):
	data = dict()
	certificate = get_object_or_404(certificateDb,id=id)
	if request.method == "POST":
		certificate.delete()
		data['form_is_valid'] = True
		
		certificatedata = certificateDb.objects.all()
		data['list'] = render_to_string('list_2.html',{'certificatedata':certificatedata})
		log.debug("Successfully Delete Certificate")
	else:
		context = {'certificate':certificate}
		data['html_form'] = render_to_string('certificate_delete.html',context,request=request)

	return JsonResponse(data)

	#-------------------------------------Service_Account---------------------------------------#


from SharedApps_Application.models import serviceDb
from SharedApps_Application.forms import serviceForm
from django.http import JsonResponse
from django.template.loader import render_to_string

def service_account(request):

	services = serviceDb.objects.all()
	context ={
	'services': services
	}
	
	return render(request, 'service_account.html',context)

def save_all(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			services = serviceDb.objects.all()
			data['service_account'] = render_to_string('service_account_list.html',{'services':services})
			log.debug("Successfully save Service Account")
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

def service_account_create(request):
	if request.method == 'POST':
		form = serviceForm(request.POST)
		log.debug("Successfully Create Service Account")
	else:
		form = serviceForm()
	return save_all(request,form,'service_account_create.html')

def service_account_update(request,id):
	service= get_object_or_404(serviceDb,id=id)
	if request.method == 'POST':
		form = serviceForm(request.POST,instance=service)
		log.debug("Successfully Update Service Account")
	else:
		form = serviceForm(instance=service)
	return save_all(request,form,'service_account_update.html')

def service_account_delete(request,id):
	print("id",id)
	data = dict()
	service = get_object_or_404(serviceDb,id=id)
	if request.method == "POST":
		service.delete()
		data['form_is_valid'] = True
		
		services = serviceDb.objects.all()
		data['service_account'] = render_to_string('service_account_list.html',{'services':services})
		log.debug("Successfully Delete Service Account")
	else:
		context = {'service':service}
		data['html_form'] = render_to_string('service_account_delete.html',context,request=request)

	return JsonResponse(data)




def upload(request):
	from time import sleep
	from pathlib import Path
	import os
	import shutil
	import glob
	import os
	import mysql.connector
	import csv
	import string
	import pandas as pd
	if request.method == 'POST':
		print("IN_upload")
		uploaded_file = request.FILES['document']
		print("Uploadfile name->",uploaded_file.name)
		NewFile=uploaded_file.name
		suffix = ".csv";
		end= NewFile.endswith(suffix)
		if end == False:
			error="Please select Only CSVfile"
			print("Error:Please select Only CSVfile")
			log.debug("Error:Please select Only CSVfile")
			return render(request,'upload.html',{'error':error})
		elif end == True:
			try:
				print("end",end)
				print(uploaded_file.size)
				fs = FileSystemStorage()
				fs.save(uploaded_file.name,uploaded_file)
				print("File Upload Successfully")
				log.debug("File Upload Successfully")
				list_of_files = glob.glob('F:/Testing (3)/Testing/Testing/media/*.csv')
				latest_file = max(list_of_files, key=os.path.getctime)
				print(latest_file)
				location=latest_file.replace("\\", "/")
				#print(location)
				latestfile1 = location.split("/")
				print("latestfile1=", latestfile1)
				latestfile1.reverse()
				print("reverse=", latestfile1)
				NewFile = latestfile1[0]
				print("NewFile=", NewFile)
				connection=Databaseconnection(request)
				print(connection[0],connection[1],connection[2],connection[3])
				Dbname=connection[0]
				username=connection[1]
				password=connection[2]
				host=connection[3]
				database = mysql.connector.connect (host=host, user = username, passwd =password, db = Dbname)


				cursor = database.cursor()
				Data=pd.read_csv(location,dtype='unicode')
				Data['ResultReason']=Data['ResultReason'].str.replace("'", " ", case = False)
				Data['ResultReason']=Data['ResultReason'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty1Name']=Data['Target1ModifiedProperty1Name'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty1Name']=Data['Target1ModifiedProperty1Name'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty1OldValue']=Data['Target1ModifiedProperty1OldValue'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty1OldValue']=Data['Target1ModifiedProperty1OldValue'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty1NewValue']=Data['Target1ModifiedProperty1NewValue'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty1NewValue']=Data['Target1ModifiedProperty1NewValue'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty2Name']=Data['Target1ModifiedProperty2Name'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty2Name']=Data['Target1ModifiedProperty2Name'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty2OldValue']=Data['Target1ModifiedProperty2OldValue'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty2OldValue']=Data['Target1ModifiedProperty2OldValue'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty2NewValue']=Data['Target1ModifiedProperty2NewValue'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty2NewValue']=Data['Target1ModifiedProperty2NewValue'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty3Name']=Data['Target1ModifiedProperty3Name'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty3Name']=Data['Target1ModifiedProperty3Name'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty3OldValue']=Data['Target1ModifiedProperty3OldValue'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty3OldValue']=Data['Target1ModifiedProperty3OldValue'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty3NewValue']=Data['Target1ModifiedProperty3NewValue'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty3NewValue']=Data['Target1ModifiedProperty3NewValue'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty4Name']=Data['Target1ModifiedProperty4Name'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty4Name']=Data['Target1ModifiedProperty4Name'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty4OldValue']=Data['Target1ModifiedProperty4OldValue'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty4OldValue']=Data['Target1ModifiedProperty4OldValue'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty4NewValue']=Data['Target1ModifiedProperty4NewValue'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty4NewValue']=Data['Target1ModifiedProperty4NewValue'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty5Name']=Data['Target1ModifiedProperty5Name'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty5Name']=Data['Target1ModifiedProperty5Name'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty5OldValue']=Data['Target1ModifiedProperty5OldValue'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty5OldValue']=Data['Target1ModifiedProperty5OldValue'].str.replace('"', ' ', case = False)
				Data['Target1ModifiedProperty5NewValue']=Data['Target1ModifiedProperty5NewValue'].str.replace("'", " ", case = False)
				Data['Target1ModifiedProperty5NewValue']=Data['Target1ModifiedProperty5NewValue'].str.replace('"', ' ', case = False)
				Data['Target2Type']=Data['Target2Type'].str.replace("'", " ", case = False)
				Data['Target2Type']=Data['Target2Type'].str.replace('"', ' ', case = False)
				Data['Target2DisplayName']=Data['Target2DisplayName'].str.replace("'", " ", case = False)
				Data['Target2DisplayName']=Data['Target2DisplayName'].str.replace('"', ' ', case = False)
				Data['Target2ObjectId']=Data['Target2ObjectId'].str.replace("'", " ", case = False)
				Data['Target2ObjectId']=Data['Target2ObjectId'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty1Name']=Data['Target2ModifiedProperty1Name'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty1Name']=Data['Target2ModifiedProperty1Name'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty1OldValue']=Data['Target2ModifiedProperty1OldValue'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty1OldValue']=Data['Target2ModifiedProperty1OldValue'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty1NewValue']=Data['Target2ModifiedProperty1NewValue'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty1NewValue']=Data['Target2ModifiedProperty1NewValue'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty2Name']=Data['Target2ModifiedProperty2Name'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty2Name']=Data['Target2ModifiedProperty2Name'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty2OldValue']=Data['Target2ModifiedProperty2OldValue'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty2OldValue']=Data['Target2ModifiedProperty2OldValue'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty2NewValue']=Data['Target2ModifiedProperty2NewValue'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty2NewValue']=Data['Target2ModifiedProperty2NewValue'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty3Name']=Data['Target2ModifiedProperty3Name'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty3Name']=Data['Target2ModifiedProperty3Name'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty3OldValue']=Data['Target2ModifiedProperty3OldValue'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty3OldValue']=Data['Target2ModifiedProperty3OldValue'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty3NewValue']=Data['Target2ModifiedProperty3NewValue'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty3NewValue']=Data['Target2ModifiedProperty3NewValue'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty4Name']=Data['Target2ModifiedProperty4Name'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty4Name']=Data['Target2ModifiedProperty4Name'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty4OldValue']=Data['Target2ModifiedProperty4OldValue'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty4OldValue']=Data['Target2ModifiedProperty4OldValue'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty4NewValue']=Data['Target2ModifiedProperty4NewValue'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty4NewValue']=Data['Target2ModifiedProperty4NewValue'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty5Name']=Data['Target2ModifiedProperty5Name'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty5Name']=Data['Target2ModifiedProperty5Name'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty5OldValue']=Data['Target2ModifiedProperty5OldValue'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty5OldValue']=Data['Target2ModifiedProperty5OldValue'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty5NewValue']=Data['Target2ModifiedProperty5NewValue'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty5NewValue']=Data['Target2ModifiedProperty5NewValue'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty5NewValue']=Data['Target2ModifiedProperty5NewValue'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty5NewValue']=Data['Target2ModifiedProperty5NewValue'].str.replace('"', ' ', case = False)
				Data['Target2ModifiedProperty5NewValue']=Data['Target2ModifiedProperty5NewValue'].str.replace("'", " ", case = False)
				Data['Target2ModifiedProperty5NewValue']=Data['Target2ModifiedProperty5NewValue'].str.replace('"', ' ', case = False)
				Data['Target3Type']=Data['Target3Type'].str.replace("'", " ", case = False)
				Data['Target3Type']=Data['Target3Type'].str.replace('"', ' ', case = False)
				Data['Target3DisplayName']=Data['Target3DisplayName'].str.replace("'", " ", case = False)
				Data['Target3DisplayName']=Data['Target3DisplayName'].str.replace('"', ' ', case = False)
				Data['Target3ObjectId']=Data['Target3ObjectId'].str.replace("'", " ", case = False)
				Data['Target3ObjectId']=Data['Target3ObjectId'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty1Name']=Data['Target3ModifiedProperty1Name'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty1Name']=Data['Target3ModifiedProperty1Name'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty1OldValue']=Data['Target3ModifiedProperty1OldValue'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty1OldValue']=Data['Target3ModifiedProperty1OldValue'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty1NewValue']=Data['Target3ModifiedProperty1NewValue'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty1NewValue']=Data['Target3ModifiedProperty1NewValue'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty2Name']=Data['Target3ModifiedProperty2Name'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty2Name']=Data['Target3ModifiedProperty2Name'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty2Name']=Data['Target3ModifiedProperty2Name'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty2Name']=Data['Target3ModifiedProperty2Name'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty2OldValue']=Data['Target3ModifiedProperty2OldValue'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty2OldValue']=Data['Target3ModifiedProperty2OldValue'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty2NewValue']=Data['Target3ModifiedProperty2NewValue'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty2NewValue']=Data['Target3ModifiedProperty2NewValue'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty3Name']=Data['Target3ModifiedProperty3Name'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty3Name']=Data['Target3ModifiedProperty3Name'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty3OldValue']=Data['Target3ModifiedProperty3OldValue'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty3OldValue']=Data['Target3ModifiedProperty3OldValue'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty3NewValue']=Data['Target3ModifiedProperty3NewValue'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty3NewValue']=Data['Target3ModifiedProperty3NewValue'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty4Name']=Data['Target3ModifiedProperty4Name'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty4Name']=Data['Target3ModifiedProperty4Name'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty4OldValue']=Data['Target3ModifiedProperty4OldValue'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty4OldValue']=Data['Target3ModifiedProperty4OldValue'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty4NewValue']=Data['Target3ModifiedProperty4NewValue'].str.replace("'", "", case = False)
				Data['Target3ModifiedProperty4NewValue']=Data['Target3ModifiedProperty4NewValue'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty5Name']=Data['Target3ModifiedProperty5Name'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty5Name']=Data['Target3ModifiedProperty5Name'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty5OldValue']=Data['Target3ModifiedProperty5OldValue'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty5OldValue']=Data['Target3ModifiedProperty5OldValue'].str.replace('"', ' ', case = False)
				Data['Target3ModifiedProperty5NewValue']=Data['Target3ModifiedProperty5NewValue'].str.replace("'", " ", case = False)
				Data['Target3ModifiedProperty5NewValue']=Data['Target3ModifiedProperty5NewValue'].str.replace('"', ' ', case = False)
				Data1=Data.fillna(" ")
				Data1['AdditionalDetail6Key']=Data1['AdditionalDetail6Key'].apply(str)

				file='C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/'+NewFile
				#print(file)

				Data1.to_csv(file, index=False)

				sql ="""LOAD DATA INFILE '"""+file+"""' INTO TABLE FinalTest1 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES;"""
				print(sql)
				cursor.execute(sql)
				database.commit()
				z=1
				print("Successfully Store Data in Database")
				log.debug("Successfully Store Data in Database")
				return render(request,'upload.html',{'b':z})
			except Exception as e:
				Error="Something went wrong please try after sometime"
				print(e)
				log.error(e)
				return render(request,'upload.html',{'Error':Error})

	return render(request,'upload.html')







#---------------------------------------------------------------------------------------------------------#


#-----------------------------------------------------------------#DisplayLogs#--------------------------------------#
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def displayLogs(request):
	from django.http import HttpResponseRedirect
	from django.shortcuts import render
	# from .forms import NameForm

	count=0
	flag=0
	# form = NameForm()
	v1=0
	v2=0
	v3=0
	v4=0
	#----for_combine_search----------------------------------------------#

	if request.POST.get('Day', False):
		Day = request.POST['Day']
		Date1=Day.split("-")
		Date2=Date1[0]+'-'+Date1[1]+'-'+Date1[2]
		print("Date2",Date2)
		Date3= Date2 + 'T' + '00:00:00' + '.0000000' + '+' + '00:00'
		print(Date3)
		dt=int(Date1[2])
		dt1=dt+1
		dt2=str(dt1)
		print("increment",dt1)
		if dt1 <= 9:
			Date4=Date1[0]+'-'+Date1[1]+'-'+'0'+dt2+ 'T' + '00:00:00' + '.0000000' + '+' + '00:00'
			print("Date4",Date4)
			log.debug("Date4",Date4)
		
		else:
			Date4=Date1[0]+'-'+Date1[1]+'-'+dt2+ 'T' + '00:00:00' + '.0000000' + '+' + '00:00'
			print("Date4",Date4)
		v1=1
		flag=1
		if count == 0:
			query='Date >=  '+'\''+(Date3)+'\' AND  Date <  '+'\''+(Date4)+'\''
			count = count+1
			print("Day->",query)
			log.debug("Day->",query)

		elif count > 0:
			query1=' AND Date >=  '+'\''+(Date3)+'\' AND  Date <  '+'\''+(Date4)+'\''
			query =query + query1
			count = count+1
			print("Day->",query)
			log.debug("Day->",query)
			
	if request.POST.get('Activity', False):
		Activity = request.POST['Activity']
		Activity=Activity.strip()
		#print("Activity1=",Activity1)
		v2=1
		flag=1
		if count  == 0:
			query ='Activity = '+'\''+(Activity)+'\''
			count = count+1
			print("Activity->",query)
			log.debug("Activity->",query)
			
		elif count > 0:
			query2 =' AND Activity = '+'\''+(Activity)+'\''
			query=query + query2
			print("Activity->",query)
			log.debug("Activity->",query)


	if request.POST.get('ActorUserPrincipalName', False):
		ActorUserPrincipalName = request.POST['ActorUserPrincipalName']
		ActorUserPrincipalName=ActorUserPrincipalName.strip()
		#print("ActorUserPrinicipalName1=",ActorUserPrinicipalName1)
		v3=1
		flag=1
		if count  == 0:
			query ='ActorUserPrincipalName = '+'\''+(ActorUserPrincipalName)+'\''
			count = count+1
			print("Actor->",query)
			log.debug("Actor->",query)
		elif count > 0:
			query3 =' AND ActorUserPrincipalName = '+'\''+(ActorUserPrincipalName)+'\''
			query =query + query3

			count = count+1
			print("Actor",query)
			log.debug("Actor->",query)

	if request.POST.get('Target1DisplayName', False):
		Target1DisplayName = request.POST['Target1DisplayName']
		Target1DisplayName=Target1DisplayName.strip()
		#print("Target1Name1=",Target1Name1)
		v4=1
		flag=1
		if count  == 0:
			query ='Target1DisplayName = '+'\''+(Target1DisplayName)+'\''
			count = count+1
			print("Target->",query)
			log.debug("Target->",query)
		elif count > 0:
			query4= ' AND Target1DisplayName ='+'\''+(Target1DisplayName)+'\''
			query =query + query4
			count = count+1
			print("Target->",query)
			log.debug("Target->",query)

	import mysql.connector
	connection=Databaseconnection(request)
	print(connection[0],connection[1],connection[2],connection[3])
	Dbname=connection[0]
	username=connection[1]
	password=connection[2]
	host=connection[3]
	con = mysql.connector.connect (host=host, user = username, passwd =password, db = Dbname)
	cur1 = con.cursor(buffered=True)
	cur=con.cursor()




	if flag == 0:
		offset=0

		page = request.GET.get('page')
		print("page",page)
		if page is None:
			page=1
			page1=int(page)
			next1=page1+1
			next2=page1+2
			next3=page1+3
			next=str(next1)
			next1=str(next2)
			next2=str(next3)
		else: 
			page = request.GET.get('page')
			page1=int(page)
			next1=page1+1
			next2=page1+2
			next3=page1+3
			next=str(next1)
			next1=str(next2)
			next2=str(next3)
		# page=1
		pagenum=int(page)
		print("page",page)
		limits=12
		offset=(pagenum)*12
		print("offset",offset)
		sql = "SELECT * FROM FinalTest1  order by Date  desc LIMIT %s, %s "
		print("sql",sql)
		cur.execute(sql,(limits,offset,))
		user_list=cur.fetchall()
		searchlen=len(user_list)
		print("Search length->",searchlen)
		paginator = Paginator(user_list, 12)
		page = request.GET.get('page')
		sql1="SELECT count(*) FROM LogGraph"
		log.debug(sql1)
		cur1.execute(sql1)
		count=cur1.fetchone()[0]
		totalpage=int(count/12)
		print('totalpage',totalpage)
		totalone=totalpage - 1
		totaltwo=totalpage - 2
		flag=0
		print("flag",flag)
		
		try:
			users = paginator.page(page)
			print("users.number",users.number)
			print(' users.paginator.page_range', users.paginator.page_range)
			
			totalone=totalpage - 1
			totaltwo=totalpage - 2
			
			
		except PageNotAnInteger:
			users = paginator.page(1)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)

		return render(request,'displayLogs.html',{'users': users,'searchlen':count,'next':next,'next1':next1,'next2':next2,'totalpage':totalpage,'totalone':totalone,'totaltwo':totaltwo,'flag':flag})

	

	elif flag == 1:
		offset=0

		page = request.GET.get('page')
		print("page",page)
		if page is None:
			page=1
			page1=int(page)
			next1=page1+1
			next2=page1+2
			next3=page1+3
			next=str(next1)
			next1=str(next2)
			next2=str(next3)
		else: 
			page = request.GET.get('page')
			page1=int(page)
			next1=page1+1
			next2=page1+2
			next3=page1+3
			next=str(next1)
			next1=str(next2)
			next2=str(next3)
		# page=1
		pagenum=int(page)
		print("page",page)
		limits=12
		offset=(pagenum)*12
		print("offset",offset)
		sql = "SELECT * FROM FinalTest1 where "+query+" LIMIT 100"
		print("sql->",sql)
		log.debug("sql->",sql)
		
		cur.execute(sql)
		print("query",query)
		log.debug("query",query)
		user_list=cur.fetchall()
		searchlen=len(user_list)
		print("Search length->",searchlen)
		paginator = Paginator(user_list, 12)
		page = request.GET.get('page')

		sql1="SELECT count(*) FROM FinalTest1 where "+query
		cur1.execute(sql1)
		count=cur1.fetchone()[0]
		totalpage=count/12
		print('totalpage',totalpage)
		totalone=totalpage - 1
		totaltwo=totalpage - 2
		try:
			users = paginator.page(page)
			print("users.number",users.number)
			print(' users.paginator.page_range', users.paginator.page_range)
			totalone=totalpage - 1
			totaltwo=totalpage - 2
			print("users",users)
		except PageNotAnInteger:
			users = paginator.page(1)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)

		
		print("Search length->",searchlen)
		log.debug("Search length->",searchlen)
		return render(request,'displayLogs.html',{'users': users,'searchlen':count,'next':next})

import pandas as pd
def Databaseconnection(request):
	Database=pd.read_csv('F:/SharedApps/datbaseconnection.csv')
	connection=[]
	print("Database->",Database)
	print("123->",Database['Username'][0])
	connection.append(Database['Database'][0])
	connection.append(Database['Username'][0])
	connection.append(Database['Password'][0])
	connection.append(Database['Host'][0])
	print(connection)
	log.debug(connection)
	
	return connection





def handler404(request):
    return render(request,'404.html')


def handler500(request):
    return render(request,'404.html')



