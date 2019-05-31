import socket
import random
# pickle module for data Serialisation/De-Serialisation
import pickle
import os
import sys


def main():
    # <------------Establish connection to TCP-Server ----------->
    # local host IP address = '127.0.0.1'
    # host = '127.0.0.1'
    # <--------------------ENABLE DOCKER CONTAINER ----------------------------------------------------->
    # In case of running server/client from docker, the container is the localhost (not our machine),
    # Setting host='0.0.0.0' or '127.0.0.1' or localhost parameter will not make the server accessible
    # as docker container is running on different IP.
    # So, you need to get the ip address (say 192.168.99.100) of the docker as explained in Instructions.txt
    # and set it as environment variable IP_ADDR e.g. IP_ADDR=192.168.99.100
    # <-------------------- WHEN RUN ON LOCAL MACHINE -------------------------------------------------->
    # Set User Environment variable: IP_ADDR=localhost
    # -------------------------------------------------------------------------------------------------->
    host = ""
    try:
        # host = "localhost"
        host = os.environ["IP_ADDR"]
    except KeyError:
        print('IP Address missing, Set environment variable IP_ADDR with IP Address in which server is running, See Instructions.txt')
        print('1. If running from local machine, set User Environment Variable IP_ADDR=localhost')
        print('2. If running from docker container, see IP address with command <docker-machine ip> and pass with run command,')
        print("For example, docker run --name cryptoServer -e IP_ADDR='192.168.99.100' -p 12345:12345 azad-crypto-server")

        sys.exit(1)

    # Port on which connection is to be established
    port = 6000

    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to server on local machine
        print('TCP-Client: host=', host, 'port=', port)
        s.connect((host, port))

        while True:

            try:
                # <------------ Generate Random array to be sent to server ----------->
                arr = []
                # Generate random size between 10 and 20
                random_size = random.randint(10, 20)

                for i in range(0, random_size):
                    arr.append(random.randint(0, 100))
                print('TCP Client: Random array to be sent to Server, Size:', str(random_size), ' Array:', str(arr))

                # <------------ Send random int array to TCP-Server ----------->
                # Serialise (convert) the array to byte stream before sending to server
                data_stream = pickle.dumps(arr)
                print('DEBUG:data_stream', data_stream)
                # Send serialised byte stream to server
                s.sendall(data_stream)

                # Sorted accumulated byte stream received from TCP-Server
                data = s.recv(1024)
                print('DEBUG:data', data)

                # De-Serialise (Re-convert) the byte stream into array after receiving from server
                sorted_int_arr = pickle.loads(data)

                print('TCP Client: Received from Server, New Size:', len(sorted_int_arr), 'New Sorted Array:', sorted_int_arr)

                yes_no = input('\nClient: Do you want to send more data to Server? (y/n) : ')
                if yes_no == 'y':
                    continue
                else:
                    break
            except:
                print('TCP Client: Exception thrown while processing data to be sent to server, processing next data...')

    except socket.error:
        print('TCP Client: Socket Creation Failed, Check if TCP Server has been started, then start client again...')

    finally:
        # Close the connection to TCP-Server
        s.close()


if __name__ == '__main__':
    main()