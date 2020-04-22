import socket
import hashlib
import threading
import random

list_clients = [] # List of customers' sockets
found = False # Is the number found
number = str(random.randint(0, 9999999)) # The number we encrypt
md5 = str(hashlib.md5(number.encode()).hexdigest()) # The number after the encryption
current_range = 0 # The beginning of the range we are increasing every time is a fixed number
add_to_range = 100000 # The range over which each client works and we increase our current range with the help of it
dict_client_to_range = {} # A dictionary the key is the client and the value is the range he is working on, so that if the client logs off we can save his range to another client
list_ranges_left = [] # A list of ranges that were supposed to work on them but the clients disconnected


def wait_for_message(client):
	global md5
	try:
		message = client.recv(1024).decode()
	except:
		# The client is disconnected, and we are erase him from our lists and dictionaries and save his range for other client
		list_ranges_left.append[dict_client_to_range[client]]
		list_clients.remove(client)
		del dict_client_to_range[client]
		quit()
	if message == 'Not found':
		if len(list_ranges_left) > 0: # Check if there is an rage left by a disconnected client and if so give it to our client
			range_to_send = list_ranges_left[0]
			list_ranges_left.remove(range_to_send)
			client.send(bytes(md5 + ':' + str(range_to_send) + ',' + str(range_to_send + add_to_range), 'utf-8'))
		else: # Give a new range to our client
			global current_range
			client.send(bytes(md5 + ':' + str(current_range) + ',' + str(current_range + add_to_range), 'utf-8'))
			current_range += add_to_range
			thread = threading.Thread(target=wait_for_message, args=(client,))
			thread.start()
			thread.join()
	elif message == '': # The client is disconnected, and we are erase him from our lists and dictionaries and save his range for other client
		if cient in dict_client_to_range:
			list_ranges_left.append[dict_client_to_range[client]]
			list_clients.remove(client)
			del dict_client_to_range[client]
		quit()
	else: # Our client has found the requested number and we inform all other clients
		print('The Number is : ' + message)
		global found
		found = True
		for client in list_clients:
			try:
				client.send(bytes('found ' + message, 'utf-8'))
			except:
				pass
		quit()


def add_clients(server_socket):
	global current_range
	global found
	while not found:
		(client_socket, client_adrass) = server_socket.accept()
		list_clients.append(client_socket) # Adds the client to our list
		if len(list_ranges_left) > 0: # Check if there is an rage left by a disconnected client and if so give it to our client
			range_to_send = list_ranges_left[0]
			list_ranges_left.remove(range_to_send)
			client.send(bytes(md5 + ':' + str(range_to_send) + ',' + str(range_to_send + add_to_range), 'utf-8'))
			dict_client_to_range.update({client_socket: range_to_send})
		else: # Give a new range to our client
			dict_client_to_range.update({client_socket: current_range})
			client_socket.send(bytes(md5 + ':' + str(current_range) + ',' + str(current_range + add_to_range), 'utf-8'))
			current_range += add_to_range
		thread = threading.Thread(target=wait_for_message, args=(client_socket,))
		thread.start()
	quit()


def main():
	global md5
	global number
	print('The md5 is ' + md5 + ' to the number ' + str(number))
	server_socket = socket.socket()
	server_socket.bind(('0.0.0.0', 8080))
	server_socket.listen(200000)
	add_clients(server_socket)
	threading.Thread(target=add_clients, args=(server_socket,)).start()


if __name__ == '__main__':
	main()
