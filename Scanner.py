try:
	import socket
except:
	print("[+] Erro ao importar a biblioteca Socket.")
try:
	import threading
except:
	print("[+] Erro ao importar a biblioteca threading")
try:
	from queue import Queue
except:
	print("[+] Erro ao importar a biblioteca queue")
try:
	import os
except:
	print("[+] Erro ao importar a biblioteca OS")
try:
	import argparse
except:
	print("[+] Erro ao importar a biblioteca argparse")

class portScanner():
	def Scanear(porta):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			conexao = s.connect((ip,porta))
			portasliberadas.append(porta)
			with print_lock:
				print('[+] Porta:',porta,'está aberta')
		except:
			if(args.verbose == True):
				print('[!] Porta:',porta,'está fechada')			
			else:
				pass
		
	def servicos(servicos):
		if(args.banner):
			pass
		else:
			print("[+] Para mostrar os banner, ative a opção -b.")
			print("[+] Saindo...")
			exit()
		s = socket.socket()
		conexao = s.connect((ip,servicos))
		banner = s.recv(1024)
		banner = banner.decode()
		banner = banner.replace("b''", "")
		banner = banner.replace("\n", "")
		banner = banner.replace("\r", "")
		banner = banner.replace("220", "")
		banner = banner.replace("["+ip+"]", "")
		banner = socket.getservbyport(servicos, 'tcp')
		with print_lock:
			print("Banner da porta",servicos,":",banner)
def banner():
	print("""
	Olá! =)
	""")
def threader():
	while True:
		worker = q.get()
		portScanner.Scanear(worker)
		q.task_done()
def threaderservicos():
	while True:
		worker = q.get()
		portScanner.servicos(worker)
		q.task_done()
if __name__ == "__main__":
	print_lock = threading.Lock()
	global portasliberadas
	portasliberadas = []
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--ip", help="Adiciona um IP Alvo")
	parser.add_argument("-v", "--verbose",action="store_true", help="Liga o modo verbose" )
	parser.add_argument("-b", "--banner",action="store_true", help="Liga o exploit para ver Versões" )
	parser.add_argument("-r", "--range1", type=int, help="Adiciona o range inicial")
	parser.add_argument("-f", "--range2", type=int, help="Adiciona o range final")
	args = parser.parse_args()

	os.system('cls')
	banner()
	if(args.ip):
		ip = (args.ip)
		print("[+] Sumário de opções escolhidas por você:")
		print("[!] Alvo: -i", args.ip)
		if(args.verbose):
			print("[!] Método Verbose: -v")
		else:
			pass
		if(args.banner):
			print("[!] Ver versões: -b")
		else:
			pass
		print("[!] Range inicial: ", args.range1)
		print("[!] Range inicial: ", args.range2)
		if(args.range1 > args.range2):
			os.system('cls')
			print("[+] O Argumento r deve ser menor que o argumento f")
			print("Saindo...")
			exit()
		else:
			pass
		print("------------------------------------------")
	else:
		print("[+] Por favor, utilize argumentos.")
		print("[+] Ex1: python PorScanner -i 127.0.0.1 -v -r 20 -f 1450")
		print("[+] Ex1: python PorScanner -i 127.0.0.1 -r 10 -f 147")
		print("[+] Utilize python PortScanner -h para ver as opções em datalhes.")


	q = Queue()
	for x in range(100):
		t = threading.Thread(target = threader)
		t.daemon = True
		t.start()
	for worker in range(args.range1,args.range2):
		q.put(worker)
	q.join()
	print("Iniciando grabbing....")
	q = Queue()
	for x in range(100):
		t = threading.Thread(target = threaderservicos)
		t.daemon = True
		t.start()
	for worker in portasliberadas:
		q.put(worker)
	q.join()
