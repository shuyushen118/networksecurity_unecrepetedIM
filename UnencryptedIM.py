import socket
import sys
import select
import argparse

#server program
def s():
    HOST =''
    PORT = 9999
    #create an INET, STREAMing socket
    listen_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #set to reuse address
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #bind socket to an address
    listen_socket.bind((HOST, PORT))
    #listen for connections made to socket, 10 is the maxium que connection 
    listen_socket.listen(10)
    #empty socket
    client_socket = []
    #infinite loop for reciving signal 
    while True:
        #list store keyboardinput and established connection 
        inputs = [sys.stdin,listen_socket]+client_socket
        #using select to store data and not blocking communication
        read_list, write_list, error = select.select(inputs,[],[])
        for r in read_list:
            #a new connection established
            if r is listen_socket:
                conn,addr = r.accept()
                #add new connection to the client socket list
                client_socket.append(conn)
                #send new message
            #moniter is there any input from the keyboard
            elif r is sys.stdin:
                #message enter from keyboard, sending message
                msg = sys.stdin.readline()
                conn.send(msg)
                sys.stdout.flush()
            #no message input then waiting for incoming message from client
            else:
                msg = conn.recv(1024)
                sys.stdout.write(msg)
                sys.stdout.flush()


#client program
def c():
##    print ("in the client")
    HOST =''
    PORT =9999
    #create an INET, STREAMing socket
    connect_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connect_socket.connect((HOST,PORT))
    while True:
        #list store any keyboard input and coming message
        inputs = [sys.stdin, connect_socket]
        read_list, write_list, error = select.select(inputs,[],[])
        for r in read_list:
            #a new connection established and message is comming in
            if r is connect_socket:
                msg = r.recv(1024)
                sys.stdout.write (msg)
                sys.stdout.flush()
            #keyboard entered, ready to send message 
            elif r is sys.stdin:
                outgoing_message = sys.stdin.readline()
                connect_socket.send(outgoing_message)
                sys.stdout.flush()

#main
#get command line argument and decide which function to run
##print 'Number of arguments:', len(sys.argv),'arguments.'
argv_1 = sys.argv[1]
if argv_1 == "--s":
    s()
elif argv_1 == "--c":
    c()
