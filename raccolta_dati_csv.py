
'''lanciare il programma con il primo paramento: che indichi il nome del file che verra creato'''

import os,json,time,datetime,sys,csv,collections
from shutil import copyfile

if (__name__=='__main__'):

	TARGET=300	#tempo di attesa tra due lanci
#	LANCI=int(sys.argv[2]) 	#10=10min 60=1ora  1440=1giorno 10080=1set 


	try:
		date_input=sys.argv[1]
	except:
		print("non hai inserito la data come argomento!")
		sys.exit(0)


	date_init = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	filename = "./"+str(date_input)+"/"+date_init+".txt"
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	csv_dict={}
	
	i=0
	while(True):
#	for i in range(LANCI):	
		out=os.popen("/home/btc-user/bin/bitcoin-cli getpeerinfo").read()
		data=json.loads(out)
		i+=1
	
		f=open(filename,"a")
		print("lanci: %d" %(i))
		
		
	
	
		peers_list=[]
		for peer in data:
			raw=peer["addr"].split(":")
			addr=raw[0]
			if(addr not in peers_list):
				peers_list.append(addr)

		
		timestamp=time.time()
		date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')		#timestamp human readible
		csv_dict[timestamp]=peers_list
			
		#ordino il dizionario per timestamp
		csv_dict = collections.OrderedDict(sorted(csv_dict.items()))
		writer=csv.writer(f)
		writer.writerow([timestamp,peers_list])
#		duplicate_keys=[]
	
			

		time.sleep(TARGET)

		#faccio un backup ogni ora (ovviamente non voglio il salvataggio iniziale quando il file e' vuoto)
		if((i%11)==0 and i!=0):
			f.close()
			filename_backup="./"+date_input+"_backup/"+date+".txt"
			os.makedirs(os.path.dirname(filename_backup), exist_ok=True)
			copyfile(filename,filename_backup)
	f.close()
	
	   
		
	

	
