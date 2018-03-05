# Secure-Shell-Network-Connectivity
Build a secure shell connection to routers from network that I built in GNS3.


-----Secure Shell is a "cryptographic network protocol" for operating network services securely over unsecured networks.-----

--This protocol is a home to various services like file transfer, web surfing, web chat, email cients, network data sharing  and various files and data operations. 

--SSH connects from a client applications such as putty. SSH can be used to send data, command, text and files to various clients. It can be run on different platforms such as Windows, Linux, and also to other devices that run Linux and have SSH server installed such as android, routers, switches, mac, iphone. 

--SSH is operated by connecting to a SSH server through the use of an ip address, port number, a username and a password or RSA key pair which is essentially a key that can unlock SSH server. RSA pair is unique and random and kept on the client ans server's individual machine. When you are connected to a SSH server , you are dropped to a shell. This shell could be a linux terminal or a windows command prompt shell where you can execute commands on the machine you are connected to.

-----Application --Secure Shell Connectivity

-- This application will use SSH to connect to the routers from the network that I built in GNS3 section and send the commands defined inside the file to each router.
-- The application will also collect the IP addresses of the routers from the dedicated file and log in to the devices using crdentials (username and password) stored in another file.
-- Furthermore this pyhton application will verify if each of these three files exits in our current directory and it will check the IP connectivity to each router via ICMP.
-- Also it will send the configuration commands to all the routers simultaneously using threading module.



----Executing process
-- first upgrade the configuration files to each routers using console from network created in GNS3.
-- run the python file SSH_Config.py in linux shell terminal.
-- first of all the program asks for the file stroing the IP addresses i.e. "ssh_ip.txt".
-- then it checks the connectivity to each of the routers and issues a message at the end.
-- second it asks for the file storing the credentials i.e. "ssh_userpass.txt" to use SSh connection for each routers.
-- Finally it asks for the file storing the commands i.e. "ssh_commands.txt" that we want to send to each router simultaneously.








