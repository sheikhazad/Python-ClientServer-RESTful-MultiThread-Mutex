
import socket
# pickle module for data Serialisation/De-serialisation
import pickle
import sys
from _thread import *
import threading

import CryptoRestAPI as rest

# sl = Global Container variable to store accumulated int array from multiple clients
sl = rest.sl

# To protect global variable sl from data racing
sl_lock = rest.sl_lock


# Function to communicate with TCP Clients
def tcp_thread_func(connection):
    while True:

        try:

            # Receive data from client (in our case, client send in Byte Stream form)
            data = connection.recv(1024)
            if not data:
                print('Server: No data received, closing connection from client, waiting for new client request...\n')
                break

            # De-Serialise Byte stream data from client into array list
            int_arr = pickle.loads(data)
            print('\nServer: New int array received from Client, Size:', len(int_arr), 'Array:', int_arr)

            # Add received int array from client to global sortedList variable sl in sorted order
            sl_lock.acquire()

            for i in int_arr:
                sl.add(i)

            print('Server: Processed sorted array in Server, New Size:', len(sl), 'New Array:', sl)

            # Serialise sorted sl into Byte stream before sending to client
            data_stream = pickle.dumps(sl)

            sl_lock.release()

            # Send back sorted integer list to client
            # Sending data across socket can take time, so better release lock before sending as data in sl is already protected
            connection.sendall(data_stream)

        except IOError as err:
            errno, strerror = err.args
            print("I/O error({0}): {1}".format(errno, strerror))

        except ValueError:
            print("Could not convert data to an integer.")

        except:
            print("Unexpected error:", sys.exc_info()[0])
            print('Exception thrown while handling data and receive/send across socket, continue to wait for next data from client..')

        finally:
            # Release lock if only already acquired and not released yet
            if sl_lock.acquire(False):
                sl_lock.release()

    # connection will be closed when requested from client
    connection.close()


# Function to start REST API
def thread_rest_func():
    # REST Server port = 12345
    # TCP Socket Server port = 6000

    # <--------------------ENABLE DOCKER CONTAINER ----------------------------------------------------->
    # By default, Flask server is only accessible from the localhost.
    # In case of starting server from docker, the container is the localhost (not your/my machine),
    # and browser requests are originating from outside the container.
    # setting host='0.0.0.0' or localhost parameter will not make the server accessible from external IPs.
    # So, you need to get the ip address (192.168.99.100) of the docker as explained in Instructions.txt
    # and enter on your browser e.g. http://192.168.99.100:12345/add_value
    # -------------------------------------------------------------------------------------------------->
    # However when running the server in local machine terminal (say Pycharm Terminal),
    # enter http://localhost:12345/add_value on your browser
    rest.app.run(debug=True, use_reloader=False, host="0.0.0.0", port=12345)


def main():
    # Run REST API to enable client from Web
    thread_rest_api = threading.Thread(target=thread_rest_func)
    thread_rest_api.start()

    host = "localhost"
    # REST Server port = 12345
    # TCP Socket Server port = 6000
    port = 6000

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Avoid bind() exception: OSError: [WinError 10048] Address already in use
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print('Server: Bind socket to host=', host, 'port=', port)
        sock.bind((host, port))


        # put the socket in listening mode
        sock.listen(5)
        print("Server: Socket is listening...")

    except socket.error:
        print('Socket Creation Failed, Exiting...')
        sys.exit(1)

    # Forever loop - will accept multiple clients
    while True:

        try:
            # Accept connection from client
            connection, address = sock.accept()

            print('Server: New connection received to host :', address[0], ' and port :', address[1])

            # Start a new thread for each client connection
            start_new_thread(tcp_thread_func, (connection,))

        except socket.error:
            print('TCP Server: Socket connection request from client failed, Continuing to listen for clients...')

        except:
            print('TCP Server: Exception thrown while Socket connection request from client and starting thread')
            print('Continuing to listen for clients...')

    # socket will never be closed, server will run always
    # sock.close()


if __name__ == '__main__':
    main()