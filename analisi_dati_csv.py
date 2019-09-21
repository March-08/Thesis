
import time,sys,os,collections,csv,datetime,json
import numpy as np
import random
from ascii_graph import Pyasciigraph
import urllib.request
from geoip import geolite2
from prettytable import PrettyTable
import pprint


def calcola_intervalli(data):
	dictionary={}
	var=True
	#ip_addresses=list(ip_history.keys())
	for timestamp in data:
		list_ip=data[timestamp]
		for ip in list_ip:
			if ip not in dictionary:
				
				dictionary[ip]=[timestamp]
			elif ip in dictionary:
				dictionary[ip].append(timestamp)
	#ordino le liste del dizionario creato
	for ip in dictionary:
		dictionary[ip].sort()
	
	#dizionario per salvare gli intervalli
	intervals={}
	for ip in dictionary:
		intervals[ip]=[]
		list_timestamp=dictionary[ip]
		to_add=[]
		
		if(len(list_timestamp)==1):
			intervals[ip].append(list_timestamp)	
			
		else:	
		
			for index in range(len(list_timestamp)-1):
				to_add.append(list_timestamp[index])
				var=controllo_timestamp(list_timestamp,index)
				if(var):
						to_add.append(list_timestamp[index+1])
				else:

					if(len(to_add)>0):
						#intervals[ip].append(to_add)
						intervals[ip].append([to_add[0],to_add[-1]])
					to_add=[]
			

					'''if(list_timestamp[index+1]==list_timestamp[-1]):
						intervals[ip].append(list(list_timestamp[-1]))'''
				if(list_timestamp[index+1]==list_timestamp[-1]):
					if(len(to_add)>0):
						intervals[ip].append([to_add[0],to_add[-1]])
				
					
	
	return intervals
	#print(len(intervals))
	#print(intervals)		
	#pprint.pprint(dictionary)
	#print(dictionary)

def controllo_timestamp(list_timestamp,index):
	time2=float(list_timestamp[index+1].replace(",","."))
	time1=float(list_timestamp[index].replace(",","."))
	if((time2-time1)<350.0):
		return True
	else:
		return False	
	
	
	
		
			
		
		
				
				
				
		
		

def geolocate_ip(ip):
	ip=ip.replace("'","").strip()
	contents= urllib.request.urlopen("http://api.ipstack.com/"+str(ip)+"?access_key=cb3c2813536e2eb8a0d6dc61e65ad39e").read()
	json_contents=json.loads(contents)
	ip_addr=json_contents["ip"]
	continent=json_contents["continent_name"]
	country=json_contents["country_name"]
	city=json_contents["city"]
	ret="ip:" +ip +"\n" + "continent: " + continent+"\n"+"country: "+country+"\n"+"city: "+city+"\n"
	list=[ip,continent,country,city]
	return [ret,list]

def stats_on_geo(geo_data):
	continent_dic={}
	country_dic={}
	city_dic={}
	for raw in geo_data:
		continent=raw[1]
		country=raw[2]
		city=raw[3]
		
		if continent in continent_dic:
			continent_dic[continent]+=1
		elif continent not in continent_dic:
			continent_dic[continent]=1
		if country in country_dic:
			country_dic[country]+=1
		elif country not in country_dic:
			country_dic[country]=1
		if city in city_dic:
			city_dic[city]+=1
		elif city not in city_dic:
			city_dic[city]=1
	maximum_cont = max(continent_dic, key=continent_dic.get)  # Just use 'min' instead of 'max' for minimum.
	maximum_state = max(country_dic, key=country_dic.get)
	maximum_city = max(city_dic, key=city_dic.get)
	
	minimum_cont = min(continent_dic, key=continent_dic.get)
	minimum_state = min(country_dic, key=country_dic.get)
	minimum_city = min(city_dic, key=city_dic.get)
	#print(maximum_cont, continent_dic[maximum_cont])
	
	x = PrettyTable()
	x.field_names = ["continente max", "stato max", "citta max","continente min","stato min","citta min"]
	x.add_row([str(maximum_cont),str(maximum_state), str(maximum_city),str(minimum_cont),str(minimum_state), str(minimum_city)])	
	x.add_row([str(continent_dic[maximum_cont]),str(country_dic[maximum_state]),str(city_dic[maximum_city]),str(continent_dic[minimum_cont]),str(country_dic[minimum_state]),str(city_dic[minimum_city])])
	return x
	#fout.write("\n\n"+str(x))


def valore_minimo(ip_history):
	ip_history_copy=ip_history.copy()
	min_ip=[]
	min_value=ip_history_copy[min(ip_history_copy, key=ip_history_copy.get)]
	for item in list(ip_history_copy):
		tmp=min(ip_history_copy, key=ip_history_copy.get)
		if(ip_history_copy[tmp]<=min_value):
			min_ip.append(tmp)
		del ip_history_copy[tmp]
	
	return [min_ip,min_value]

	
def calcola_varianza(ip_history,iterazioni):
	list=[]
	for ip in ip_history:
		list.append(1-(ip_history[ip]/iterazioni))
	var=np.var(list)
	return var


def calcola_media(ip_history,iterazioni):
	#sommo quante volte si e' presentato ogni nodo e lo divido per il numero dei nodi
	tot=0
	for ip in ip_history:
		tot+=(1-(ip_history[ip]/iterazioni))
	return tot/len(ip_history)

def nodi_stabili(ip_history,iterazioni):
	list_stabili=[]
	for ip in ip_history:
		if((ip_history[ip]/iterazioni)==(10/10)):
			list_stabili.append(ip)
	return list_stabili

def print_chart(ip_history,iterazioni):
	all_tuple=[]
	text=""
	for ip in ip_history:
		tuple=(str(ip),((ip_history[ip]*1.0)/iterazioni))
		all_tuple.append(tuple)
	graph=Pyasciigraph(human_readable="si",float_format="{0:,.6f}")
	for line in graph.graph("\n\n grafico della percentuale di connessione di ogni peer durante la monitorizzazione",all_tuple):
	#	print(line)
		text+=line
		text+="\n"
	return text
		

def read_csv(filename):
	with open(FILE_NAME) as f:
		reader = csv.reader(f)
		data = dict(reader)
		data_out={}
		for item in data:
			data_out[item]=data[item][1:-1].strip().split(",")
			data_out=collections.OrderedDict(sorted(data_out.items())) #ordino il diz in base alle chiavi 		
	
			
	return data_out
			
	
def create_ipHistory(data):
	#index=0
	ip_history={}
	for item in data:
		#else:
		peers_temp=data[item]
			
		#salvo lo storico degli ip
		for node in peers_temp:
				
			if node in ip_history:
				ip_history[node]+=1

			else:
				ip_history[node]=1
#				print(str(index) + " : " +str(ip_history[node]))
	return ip_history

#calcola la percentuale di nodi invariati dalla prima iterazione e la stampa la scrive su file
def percentuale_nodi_invariati(data):
	index = 0
	

	perc_temp=1
	fout.write("nodi connessi invariati: lancio    percentuale      numero-peer-connessi \n")
	fout.write("###################################################################### \n")
	avg_peers=0
	var=[]
	min=[]
	max=[]
	for item in data:
		if (index==0):
			peers_init=data[item]
			avg_peers=len(peers_init)
			var.append(len(peers_init))
			min.append([index,len(peers_init)])
			max.append([index,len(peers_init)])
			index+=1
		else:
			peers_temp=data[item]
			avg_peers+=len(peers_temp)
			var.append(len(peers_temp))
			count=0
			for ip_addr in peers_temp:
                		if(ip_addr in peers_init):
                        		count+=1
			perc=(count*1.0)/len(peers_init)

			
			if (perc<=1):
				fout.write("  %d   %f %%   %d\n" %(index,perc,len(peers_temp)))
				perc_temp=perc
				
			if (perc==0):	#quando sono cambiati tutti dall'inizio
				fout.write("tutti i nodi sono cambiati all'iterazione nr: " +str(index) +"\n")
			index+=1
			
			if(len(peers_temp)<min[0][1]):
				min=[]
				min.append([index,len(peers_temp)])
			if(len(peers_temp)==min[0][1]):
				min.append([index,len(peers_temp)])
			if(len(peers_temp)>max[0][1]):
				max=[]
				max.append([index,len(peers_temp)])
			if(len(peers_temp)==max[0][1]):
				max.append([index,len(peers_temp)])
	fout.write("\nstatistiche sul numero di peer connessi al full-node")
	fout.write("\n#####################################################################################################")
	fout.write("\nnumero max connessioni: lancio, numero-peer\n")
	fout.write(str(max)+"\n")
	fout.write("\nnumero min connessioni: lancio, numero-peer\n")
	fout.write(str(min))
	
	x = PrettyTable()
	x.field_names = ["media peer", "min connessioni", "nr. min connessioni","max connessioni","nr. max connessioni", "varianza","peer conosciuti"]
	x.add_row([str(avg_peers/len(data)),str(min[0][1]), str(len(min)),str(max[0][1]),str(len(max)), str(np.var(var)),str(len(ip_history))])
	fout.write("\n\n"+str(x))
	




if( __name__=="__main__"):
	
	FILE_NAME=sys.argv[1]
	
	#creo il dizionario dal file csv
	data=read_csv(FILE_NAME)

	
	# da che data a che data sto monitorando
	time1= list(data.keys())[0]
	time2= list(data.keys())[-1]
	date_init = datetime.datetime.fromtimestamp(float(time1)).strftime('%Y-%m-%d %H:%M:%S')
	date_finish = datetime.datetime.fromtimestamp(float(time2)).strftime('%Y-%m-%d %H:%M:%S')

		

	#scrivo i risultati dell analisi su un file risultati.txt
	fout_name ="risultati_"+FILE_NAME+".txt"
	os.makedirs(os.path.dirname(fout_name), exist_ok=True)
	fout=open(fout_name,"w")
	
	fout.write("ho monitorato dal giorno : " + str(date_init)+"\n" + "al giorno : " +str(date_finish)+"\n\n")
	
	
		
	#quante volte ogni ip e' comparso, lo salvo in un dizionario
	ip_history=create_ipHistory(data)
	
	#geolocalizzo
	fout_geolocate ="geolocate_"+FILE_NAME+".txt"
	os.makedirs(os.path.dirname(fout_geolocate), exist_ok=True)
	fout_geolocate=open(fout_geolocate,"w")
	geo_data=[]
	for ip in ip_history:
		tmp=geolocate_ip(ip)[0]
		geo_data.append(geolocate_ip(ip)[1])
		
		fout_geolocate.write(str(tmp)+"\n\n")	
	
	stats=stats_on_geo(geo_data)
	fout_geolocate.write(str(stats)+"\n")
	fout_geolocate.close()
		
	#intervalli su file
	intervals=calcola_intervalli(data)
	fout_intervals ="intervalli_"+FILE_NAME+".txt"
	os.makedirs(os.path.dirname(fout_intervals), exist_ok=True)
	fint=open(fout_intervals,"w")
	pprint.pprint(intervals, stream=fint)
	
	#in che percentuale i nodi sono rimasti invariati dalla prima iterazione?
	#con che media un nodo crolla?
	percentuale_nodi_invariati(data)
		
	

media=calcola_media(ip_history,len(data))
varianza=calcola_varianza(ip_history,len(data))
nodi_min=valore_minimo(ip_history)[0]
nodi_stab=nodi_stabili(ip_history,len(data))
			
fout.write("\n\ni nodi che si sono presentati con meno frequenza sono: " +str(len(nodi_min))+ "\n"+str(nodi_min)+"\n")
fout.write("\ni nodi piu stabili sono : "+ str(len(nodi_stab)) + "\n"+str(nodi_stab) +"\n")
fout.write(print_chart(ip_history,len(data)))
fout.write("\n\n connessioni per ogni peer: \n\n" +  str(ip_history))

x = PrettyTable()
x.field_names = ["media di connessione peer", "varianza", "% minima di conn.","nr. nodi con % minima","nr. nodi stabili","nr. di lanci"]
x.add_row([str(media),str(varianza), str((valore_minimo(ip_history)[1]/len(data))),str(len(nodi_min)),str(len(nodi_stab)), str(len(data))])
fout.write("\n\n"+str(x))


print("analisi effettuata, file creato correttamente")






