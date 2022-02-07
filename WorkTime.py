from datetime import timedelta
from datetime import datetime
from os.path import exists


def workTime_log(log):
	f = open("workTime_log.txt", "a")
	f.write(log)
	f.close()

def TimeDiff(time1, time2):
	arr_t1 = time1.split(":")
	arr_t2 = time2.split(":")
	sum = timedelta(hours=int(arr_t1[0]),minutes=int(arr_t1[1]), seconds=int(arr_t1[2])) - timedelta(hours=int(arr_t2[0]),minutes=int(arr_t2[1]), seconds=int(arr_t2[2]))
	result = str(sum)
	if len(result) == 7: result="0"+result
	return result
	
def breakTime():
	#Sprawdzenie istniena Logu przerwy
	if exists("break_log.txt") == True:
		f = open("break_log.txt", "r")
		for x in f:
			pass
		try:
			lastLine=x
			
		except:
			lastLine=""
		f.close()

	#uwzglednienie tylko dzis
	date = now.strftime("%Y:%m:%d")
	try:
		arr = lastLine.split("|")
		if arr[0] == date:
			break_today = arr[4]
		else:
			break_today = "00:00:00"
	except:
		break_today = "00:00:00"
	
	return break_today

#Definiowanie danych czsu
now = datetime.now()
current_date = now.strftime("%Y:%m:%d")
current_time = now.strftime("%H:%M:%S")

# Default in START mode
mode = "start" 

#Sprawdzenie istniena  i odczyt ostatniego weirsza
if exists("workTime_log.txt") == True:
	f = open("workTime_log.txt", "r")
	workEnd = ""
	workStart = ""
	for x in f:
		arr_LogRow = x.split("|")
		if arr_LogRow[0] == current_date:
		
			# STOP mode, as record for current day was detected
			mode = "stop"
			#jezeli rekord jest z dnia beżącego oraz dotyczy konca pracy
			if arr_LogRow[2] != "": 
				workEnd = arr_LogRow[2] + "|" + workEnd
				
			#jezeli rekord jest z dnia beżącego oraz dotyczy rozpoczęcia pracy
			if arr_LogRow[1] != "": 
				workStart = arr_LogRow[1] + "|" + workStart
	try:
		lastLine=x
	except:
		lastLine=""
	f.close()	
else:
	workTime_log("Date|BeginTime|EndTime|WorkTime|BreakTime")

if mode == "start":
	#Log
	log = "\n" + current_date + "|"+ current_time + "|" + "" + "|" + "|"  
	workTime_log(log)
elif mode == "stop":
	#Wybór trybu
	if lastLine != "":
		
		#Wyliczenie czasu pracy
		arr_lastLine = lastLine.split("|")
		if current_date == arr_lastLine[0]:
		
			workStart_time = workStart.split("|") #arrays with all starts
			workEnd_time = workEnd.split("|") #arrays with all ends

			#Pierwszy zarejestroeany czas rozpoczecia pracy
			start_time = workStart_time[len(workStart_time)-2] 		
			end_time=current_time
			
			#Suma granicznych czasów pracy i wykorzystanej przerwy
			sum_time = TimeDiff(end_time, start_time)
			break_time=breakTime()
			
			#Realny czas pracy
			work_time=TimeDiff(sum_time, break_time)
			
			#Log
			log = "\n"+current_date + "|" + "" + "|" + end_time + "|" + sum_time + "|" + break_time 
			workTime_log(log)

			print("######### Summary of the  working day #########\n\n"+"Start of work:         "+start_time+"\n"+"End of work:           " + end_time + "\n\n"+"Summary time of work:  " + work_time+"\n"+"Summary time of break: "+break_time+"\n\n######### Summary of the  working day #########")
			ToDo = input("Hit ENTER to close")			
	else:
		print("There was no work start detected, work stop will be not processed")
else:
	print("No start/stop mode detected")