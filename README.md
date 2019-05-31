# Python-ClientServer-RESTful-MultiThread-Mutex
This project use some advanced features of Python like:
1. TCP/IP Client-Server by using socket
2. Server exposed to RSTFUL webservice using Flask
3. Multi-threading
4. Locking mechanism etc.
5. Server part (without Socket Client)  is packed in DOCKER.


Attached Files: 

1. Problem description file which explains purpose of this project (Suggested to read this first before seeing code)

2. Server part (without Socket Client)  is packed in docker, which means it can be run and test RESTful API.  Repository is:

https://cloud.docker.com/repository/registry-1.docker.io/sheikhazad2/crypto-tcp-rest-server

3. Attached Test result by running TCP Server/REST/TCP Client/Web browser on Pycharm Python Terminal. Also attached REST API test on docker.

4. Code are in 3 files:
   i)   CryptoServer.py         -  (Server executable - [ Contains code for TCP server + REST API ])
   ii)  CryptoRestAPI.py        -  (REST API called by i) 
   iii) CryptoTCPClient.py      -  (TCP Client executable )
   iv) Instructions.txt
   v) TestResult-REST-Browser-TCP-Client.PNG   - (Test Result)



HOW TO RUN:
Follow instructions given in file - Instruction.txt