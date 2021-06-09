import telnetlib
import datetime
import time
import re

# ophalen bestand ip lijst
with open('iplist.txt') as fh:
    fstring = fh.readlines()
pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
lst = []
for line in fstring:
    lst.append(pattern.search(line)[0])
print(lst)

# ophalen tftp server
with open('../tftp.txt', 'r') as f:
    tftp = (f.read())
    print("Tftp server is: " + tftp)

user = "root"
password = ""
response = ""

for ip in lst:
    ipdone = open("ipsdone.txt", "r")

    pattern2 = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
    lst2 = []

    for line in ipdone:
        lst2.append(pattern.search(line)[0])
    if ip not in lst2:
        print("Current ip: " + ip)
        try:
            tn = telnetlib.Telnet(ip)
            response = "Connection successful. Updating now."
        except Exception:
            response = "Failed Connection. Skipping!."
            logging = open("Logging/logging.txt", "a+")
            logging.write("\n" + ip + " Failed " + str(datetime.datetime.now()))
        finally:
            print(response)

        # telnet verbinding inloggen
        tn.read_until(b"login: ")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
        time.sleep(1)
        ipdone.close()

        tn.write(b"tftp -gr  blup.sh " + tftp.encode('ascii') + b"\n")
        time.sleep(1)
        tn.write(b"chmod 0777 blup.sh\n")
        time.sleep(1)
        tn.write(b"echo tftphost=" + tftp.encode('ascii') + b" > /tmp/serverparams.conf\n")
        print(tn.read_sb_data().decode('ascii'))
        time.sleep(1)
        tn.write(b"./blup.sh\n")
        time.sleep(1)
        print(tn.read_sb_data().decode('ascii'))
        tn.write(b"exit\n")
        tn.read_all()  # .decode('ascii'))
        print("Updated")

        # toevoegen aan lijst met geupdate albireos
        ipdone = open("ipsdone.txt", "a+")
        ipdone.write(ip + "\n")

        # logging
        logging = open("Resources/Logging/logging.txt", "a+")
        logging.write("\n" + ip + " Success " + str(datetime.datetime.now()))

    else:
        print(ip + " is al gedaan")