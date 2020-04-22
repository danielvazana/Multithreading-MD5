import hashlib
import threading
import multiprocessing
import socket

found = False
Server_md5 = ""
Number = 0


def make_md5(string):
	result = hashlib.md5(string.encode())
	return str(result.hexdigest())


def check_number_to_md5(num1, num2):
	"""The Function gets a range and checks every number if it's the md5"""
	global found
	global Number
	for number in range(num1, num2 + 1):
		if found:
			break
		elif make_md5(str(number)) == Server_md5:
			found = True
			Number = number
			break


def client_waits_to_message_and_look_for_md5(my_socket):
	"""The Function that waits for a range from the server and then splits it by the number of the cores and gives to every thread diffrent range to work on. At the end of the work sends the number if the number is found, and 'Not Found' if the number was not found"""
	global found
	global Server_md5
	global Number
	cpu_count = multiprocessing.cpu_count()
	start_details = my_socket.recv(1024).decode()
	if start_details == 'found':
		print('found')
		quit()
	Server_md5 = start_details.split(':')[0]
	range_end = int(start_details.split(':')[1].split(',')[1])
	range_start = int(start_details.split(':')[1].split(',')[0])
	print(str(range_start) + ' - ' + str(range_end))
	list_threads = []
	for number in range(range_start, range_end, int(range_end / cpu_count)):
		t = threading.Thread(target=check_number_to_md5, args=(number, number + int(range_end / cpu_count)))
		list_threads.append(t)
		t.start()
	for thread in list_threads:
		thread.join()
	if found:
		my_socket.send(bytes(str(Number), 'utf-8'))
		print('I found ' + str(Number))
	else:
		my_socket.send(bytes('Not found', 'utf-8'))
		print('not found now')
		client_waits_to_message_and_look_for_md5(my_socket)


def main():
	my_socket = socket.socket()
	my_socket.connect(('127.0.0.1', 8080))
	client_waits_to_message_and_look_for_md5(my_socket)


if __name__ == "__main__":
	main()
