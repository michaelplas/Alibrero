import telnetlib
import datetime
import time
import re

# ophalen bestand ip lijst
with open('ip.txt') as fh:
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
        match = pattern.search(line)
        if match:
            lst2.append(match[0])
        else:
            print("")

    if ip not in lst2:
        print("Current ip: " + ip)
        try:
            tn = telnetlib.Telnet(ip)
        except TimeoutError:
            print("Timeout has been reached at " + ip + ". Skipping for now.")
            logging = open("../Resources/Logging/logging.txt", "a+")
            logging.write("\n" + ip + " Timeout. " + str(datetime.datetime.now()))
            continue
        except IOError:
            print("Cannot update " + ip + ". Skipping for now.")
            logging = open("../Resources/Logging/logging.txt", "a+")
            logging.write("\n" + ip + " Failed. " + str(datetime.datetime.now()))
            continue

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
        tn.read_sb_data().decode('ascii')
        time.sleep(1)
        tn.write(b"./blup.sh\n")
        #tn_read = tn.read_all()
        #print(repr(tn_read))
        #tn.read
        time.sleep(1)
        print(tn.read_sb_data().decode('ascii'))
        tn.write(b"exit\n")
        tn.read_all()
        print(tn.read_all())  # .decode('ascii'))

        # toevoegen aan lijst met geupdate albireos
        ipdone = open("ipsdone.txt", "a+")
        ipdone.write(ip + "\n")

        # logging
        logging = open("../Resources/Logging/logging.txt", "a+")
        logging.write("\n" + ip + " Success " + str(datetime.datetime.now()))

    else:
        print(ip + " is al gedaan")