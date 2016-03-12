import nmap
import socket
import socket
import fcntl
import struct
import sys
import xml.etree.ElementTree as ET

IFACE = 'eth0'
IP = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
NM = nmap.PortScanner()
DBLIST = ['DB/nvdcve-2.0-2002.xml','DB/nvdcve-2.0-2003.xml','DB/nvdcve-2.0-2004.xml','DB/nvdcve-2.0-2005.xml','DB/nvdcve-2.0-2007.xml','DB/nvdcve-2.0-2008.xml','DB/nvdcve-2.0-2009.xml','DB/nvdcve-2.0-2010.xml','DB/nvdcve-2.0-2011.xml','DB/nvdcve-2.0-2012.xml','DB/nvdcve-2.0-2013.xml','DB/nvdcve-2.0-2014.xml','DB/nvdcve-2.0-2015.xml']

host = []
protocol = []
port = []
name = []
state = []
product = []
extrainfo = []
reason = []
version = []
conf = []
cpe = []
uniqueIPs = set()
foundCPE = dict()

#returns something like "255.255.255.0"
def get_netmask(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s',ifname))[20:24])

#takes in something like "255.255.255.0" and returns, for this example, "24"
def get_netmask_num(net):
	if net == "255.255.0.0":
		return 16
	elif net == "255.255.128.0":
		return 17
	elif net == "255.255.192.0":
		return 18
	elif net == "255.255.224.0":
		return 19
	elif net == "255.255.240.0":
		return 20
	elif net == "255.255.248.0":
		return 21
	elif net == "255.255.252.0":
		return 22
	elif net == "255.255.254.0":
		return 23
	elif net == "255.255.255.0":
		return 24
	elif net == "255.255.255.128":
		return 25
	elif net == "255.255.255.192":
		return 26
	elif net == "255.255.255.224":
		return 27
	elif net == "255.255.255.240":
		return 28
	elif net == "255.255.255.248":
		return 29
	elif net == "255.255.255.252":
		return 30
	else:
		return 0

#Sorts through a given csv file and assigns the data to different variables
def assignStats(csv):
	for line in csv:
		if len(line) > 10: #if there's actually for the host scanned (it exists)
			#host[i],protocol[i],port[i],name[i],state[i],product[i],extrainfo[i],reason[i],version[i],conf[i],cpe[i] = line.split(';')
			a,b,c,d,e,f,g,h,j,k,l = line.split(';')
			if len(a)>7: #so it ignores the header csv stuff
				host.append(str(a.split())[2:-2])
				protocol.append(str(b.split())[2:-2])
				port.append(str(c.split())[2:-2])
				name.append(str(d.split())[2:-2])
				state.append(str(e.split())[2:-2])
				product.append(str(f.split())[2:-2])
				extrainfo.append(str(g.split())[2:-2])
				reason.append(str(h.split())[2:-2])
				version.append(str(j.split())[2:-2])
				conf.append(str(k.split())[2:-2])
				cpe.append(str(l.split())[2:-2])
				uniqueIPs.add(str(a.split())[2:-2])

#Goes through all of the DB files to see if it can find one that matches the given CPE
def searchForCPE(cpe, root):
	rootLvl=0
	product=0
	for val in root:
		for val2 in root[rootLvl][1]:
			if cpe.strip() == root[rootLvl][1][product].text:
				return rootLvl
			product=product+1
		rootLvl=rootLvl+1
		product=0
	return -1

#Goes through the CPEs to find vulnerability levels by comparing them to the DBLIST
def referenceDB(cpe):
	result = ""
	if cpe in foundCPE: #quick search to see if the cpe has been already found. If so, return its associated vulnerability level
		result = str(foundCPE[cpe])
	else:
		found = False
		for DB in DBLIST:
			tree = ET.parse(DB)
			root = tree.getroot()
			num = searchForCPE(cpe, root) #search for given CPE in the DB
			if num != -1:
				vulnLvl = root[num][5][0][0].text
				result = str(vulnLvl)
				foundCPE[cpe] = vulnLvl #Create dictionary item of cpe and the vulnerability level associated with it
				found = True
				break
		if not found:
			result = "NOT FOUND"
	return result



#time to start doing things!
print "\nNetwork Interface: " + IFACE
print "IP Address: " + IP

#F=fist things first, we have the IP, but we need to now get the subnet mask that it lies on
subnet_mask = get_netmask_num(get_netmask(IFACE))
print "Subnet Mask: " + str(subnet_mask) + "\n"


#time to separate the IP in order to append the subnet_mask
f,s,t,l = IP.split('.') #separates IP by .
ipScannableRange = f+'.'+s+'.'+t+'.0/'+str(subnet_mask) #get IP subnet (192.168.1) + '.0'


print "Let\'s scan the hosts!"
NM.scan(ipScannableRange,arguments='-sV -T4 -F') #ping scan


#this gets our results of the scan in a beautiful csv style format
csv = NM.csv().split('\n')


#time to sort through the csv and assign all the important information
assignStats(csv)


#alright! Now we have all the cool information. Let's print out the different IPs that we found. Easy enough:
for item in uniqueIPs:
	print "IP: " + item


#now it's time to get into more of the guts. We're going to associate the CPEs for each of the unique IPs and find some vulnerability levels
for ip in uniqueIPs: #go through all the unique IPs
	print "=====RESULTS FOR IP " + ip + "====="
	i = 0
	for item in host: #go through all the IPs
		if ip == item: #if the unique IP is found in the list of all IPs
			if len(cpe[i])>4: #if there's a reported cpe
				print "Port: " + port[i]
				print "Name: " + name[i]
				print "CPE: "  + cpe[i]
				print "Vulnerability Level: " + referenceDB(cpe[i]) #search the DB files to find the vulnerability level. (can take awhile)
				print ""
		i+=1
	print ""

