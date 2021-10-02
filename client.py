import ipfshttpclient
import csv
import os

from ipfshttpclient.exceptions import ConnectionError
from urllib3.exceptions import NewConnectionError
from ipfshttpclient.exceptions import TimeoutError, ErrorResponse, ConnectionError
from requests.exceptions import HTTPError, ConnectionError as rConnectionError

column_names = ['Name', 'Hash', 'Size']

def add_files(init_file: str, *files, database='database.csv', ip: str='172.17.0.2', port: int=5001):
	"""
   A method used to add a list of files to a specific IPFS network
   
   __Attributes__
   ---------------   
	1) init_file: An initial file to be recorded.
   2) files: A collection of files contains at least one file you want to add.
   3) database: A csv file used to record the files already added to the network so far.
   4) ip: the node IP exists in an IPFS network.
   5) port: the port used to connect to that specific node -> 5001 by default -> get a look at the documentation.
      @Link https://docs.ipfs.io/how-to/configure-node/#addresses-api
      It's is also available to use 8080/tcp
         
   >>> add_file('test.txt', 'recorder.csv', '192.168.0.1', 5001)
         {"Name": 'test.txt', "Hash": QmbBzNiWyxr1hurr576inrQyxHmL2aHFQ6pVf47ZzzGooW, "Size": 44}
	"""	
	print('openning connection to the specific ipfs client...')
	client = ipfshttpclient.Client('/ip4/' + ip + '/tcp/' + str(port))
	logs = []
	try:
		logs.append(client.add(init_file))
		for file in files:
			logs.append(client.add(file))
	except TypeError as typeError:
		print(typeError)
	except NameError as nameerror:
		print(nameerror)
	except NewConnectionError as connectionError:
		print(connectionError)
	except rConnectionError as cnc:
		print(cnc)
	else:
		# starting to write LOGs for our database.
		try:
			print('Trying to open %s...' %database)
			db = open(database, 'a+t')
		except IOError as io:	
			print(io)
		else:
			writer = csv.DictWriter(db, fieldnames=column_names)
			if os.path.getsize(database) == 0: writer.writeheader()
			for row in logs:
				writer.writerow(row.as_json())
			db.close()
			print('Writing Logs to %s succeded...' %database)
	finally:   
		client.close()
		print('Connection closed succeseded...')
		print('Terminated!')

def add_dir(dir__: str, database='database.csv', ip: str='172.17.0.2', port: int=5001):
	"""
   A method used to add a list of files to a specific IPFS network
   
   Parameters
   -----------   
   1) dir__: An initial file to be recorded.
   2) database: A csv file used to record the files already added to the network so far.
   3) ip: the node IP exists in an IPFS network.
   4) port: the port used to connect to that specific node -> 5001 by default -> get a look at the documentation.
      @Link https://docs.ipfs.io/how-to/configure-node/#addresses-api
      It's is also available to use 8080/tcp
         
   >>> add_file('test.txt', 'recorder.csv', '192.168.0.1', 5001)
         {"Name": 'test.txt', "Hash": QmbBzNiWyxr1hurr576inrQyxHmL2aHFQ6pVf47ZzzGooW, "Size": 44}
	"""
	print('openning connection to the specific ipfs client...')
	client = ipfshttpclient.Client('/ip4/' + ip + '/tcp/' + str(port))
	try:
		logs = client.add(dir__, recursive=True, pin=True)
	except TypeError as typeError:
		print(typeError)
	except NameError as nameerror:
		print(nameerror)
	except NewConnectionError as connectionError:
		print(connectionError)
	except rConnectionError as cnc:
		print(cnc)
	else:
      # starting to write LOGs for our database.
		try:
			print('Trying to open %s...' %database)
			db = open(database, 'a+t')
		except IOError as io:
			print(io)
		else:
			writer = csv.DictWriter(db, fieldnames=column_names)
			if os.path.getsize(database) == 0: writer.writeheader()
			for row in logs:
				writer.writerow(row.as_json())
			db.close()
			print('Writing Logs to %s succeded...' %database)
	finally:
		client.close()
		print('Connection closed succeseded...')
		print('Terminated!')

def display(cid: str, ip: str='172.17.0.2', port: int=5001):
	"""
	A function used display the contenet of a specific file given its CID

	Parameters
	-----------
	1) cid: the CID of the fille needed to be manipulated.
	2) ip: the node IP exists in an IPFS network.
	3) port: the port used to connect to that specific node -> 5001 by default -> get a look at the documentation.
			@Link https://docs.ipfs.io/how-to/configure-node/#addresses-api
			It's is also available to use 8080/tcp
	"""
	client = ipfshttpclient.Client('/ip4/' + ip + '/tcp/' + str(port), timeout=60)
	try:
		out = client.cat(cid)
	except NewConnectionError as connectionError:
		print(connectionError)
	except rConnectionError as cnc:
		print(cnc)	
	except TimeoutError as te:
		print(te)
	except HTTPError as e:
		print(e)
	except ErrorResponse as er:
		print('This Contenet ID %s corresponds to a direcory so the contenet can\'t be displayed.'%cid)
	else:
		print(out)
	finally:
		client.close()

def get(cid: str, target_path: str = '.',  ip: str='172.17.0.2', port: int=5001):
	"""
	A method used to get the file or the directory corresponding to the given CID.
	
	Parameters
	-----------
	1) cid: the id of the needed file or folder.
	2) target_path: the working path to save the file/folder into.
	3) ip: the node IP exists in an IPFS network.
 	4) port: the port used to connect to that specific node -> 5001 by default -> get a look at the documentation.
 			@Link https://docs.ipfs.io/how-to/configure-node/#addresses-api
 	 		It's is also available to use 8080/tcp
	"""
	client = ipfshttpclient.Client('/ip4/' + ip + '/tcp/' + str(port), timeout=60)
	try:
		print('start connection...')
		client.get(cid, target_path)
	except NewConnectionError as connectionError:
		print(connectionError)
	except rConnectionError as cnc:
		print(cnc)
	except TimeoutError as te:
		print('This CID %s maybe not valid'%cid)
		print(te)
	except PermissionError as p:
		print(p)
	finally:
		client.close()
		print('Done!')

def get_hashes(*cids: str, target: str='all', ip: str='172.17.0.2', port: int=5001):
	"""
	A function used to print all the hashes recorded so far or manipulate specific subset of them
	
	Parameters
	-----------
	1) cids: the CIDs of the content to be listed
	2) target: type of pin
	3) ip: the node IP exists in an IPFS network.
	4) port: the port used to connect to that specific node -> 5001 by default -> get a look at the documentation.
			@Link https://docs.ipfs.io/how-to/configure-node/#addresses-api
			It's is also available to use 8080/tcp
	

	Returns
	-------- 
	A dictionary of all the recorded pinned hashes within a specific client
	"""
	client = ipfshttpclient.Client('/ip4/' + ip + '/tcp/' + str(port), timeout=60)
	try:
		if len(cids) == 0:
			out = client.pin.ls(type=target).as_json()['Keys']
		else:
			out = []
			for cid in cids:
				out.append(client.pin.ls(cid, type=target).as_json()['Keys'])
	except NewConnectionError as connectionError:
		print(connectionError)
	except TimeoutError as te:
		print(te)
	except PermissionError as pe:
		print(pe)
	except ConnectionError as conc:
		print(conc)
		print('Check the node\'s ip and port....')
	except rConnectionError as rce:
		print(rce)
	except ErrorResponse as er:
		print(er)
	except HTTPError as e:
		print(e)
	else:
		if type(out) == list:
			out = {k: v for single in out for k, v in single.items()}
		client.close()
		return out
	finally:
		client.close()

def remove(cid: str, ip: str='172.17.0.2', port: int=5001):
	"""
	This function used to unpin a specific file or folder from the pinned list
	
	Parameters
	-----------
	1) cid: the contenet id to be removed from the pin lise
	2) recursive: indicates if the cid corresponds to a file or folder (True -> folder, False -> file)
	3) ip: the node IP exists in an IPFS network.
	4) port: the port used to connect to that specific node -> 5001 by default -> get a look at the documentation.
        	@Link https://docs.ipfs.io/how-to/configure-node/#addresses-api
     		It's is also available to use 8080/tcp
	
	"""
	client = ipfshttpclient.Client('/ip4/' + ip + '/tcp/' + str(port), timeout=60)
	try:
		out = client.pin.rm(cid)
	except ErrorResponse as er:
		print(er)
	except NewConnectionError as ce:	
		print(ce)
	except ConnectionError as cnc:
		print(cnc)
	except HTTPError as e:
		print('Check the type of the pinned content.')
	except TimeoutError as te:
		print(te)
	except PermissionError as p:
		print(p, 'The process has been terminated!', sep='\n')
	else:
		print('%s deleted sucessfully...' %cid)
	finally:
		client.close()
