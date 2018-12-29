#coding=utf8
import json
import os

logfile = "./com.tencent.xin.log"
dnsile = "./dns.log"
savefile = "./targets.log"
targets = {}
lines = ""
pcapfile = "wechat.pcap"

'''
kyes: length, protocol, time, dstIP, srcIP, dstPort, srcPort
'''

def main():
	dns_dict = {}
	cmd = "tshark -r %s -q -z \"hosts\""%pcapfile
	dns_list = os.popen(cmd).read().split('\n')
	for dns_item in dns_list:
		print(dns_item)
		try:
			tmp_item = dns_item.split('\t')
		except:
			continue
		if len(tmp_item) != 2:
			continue
		try:
			ttttt = dns_dict[tmp_item[1]]	
		except:
			dns_dict[tmp_item[1]] = []
		dns_dict[tmp_item[1]].append(tmp_item[0])
	counter = 0
	with open(dnsile,"a") as f:
		for dns_item in dns_dict.items():
			s = dns_item[0] + ":"
			for ip in dns_item[1]:
				s += ip+" "
				counter += 1
			f.write(s+"\n")
	print(counter)

	with open(logfile,"r") as f:
		lines = f.readlines()
	
	for line in lines:
		j = json.loads(line)
		target = ""
		if j["srcPort"] != "0":
			srcIP = ""
			try:
				srcIP = dns_dict[j["srcIP"]]
			except:
				target = "%s:%s:%s"%(j["protocol"],j["srcIP"],j["srcPort"])
			else:
				target = "%s:%s:%s"%(j["protocol"],srcIP,j["srcPort"])
		elif j["dstPort"] != "0":
			dstIP = ""
			try:
				dstIP = dns_dict[j["dstIP"]]
			except:
				target = "%s:%s:%s"%(j["protocol"],j["dstIP"],j["dstPort"])
			else:
				target = "%s:%s:%s"%(j["protocol"],dstIP,j["dstPort"])
		else:
			continue

		targets[target] = 0

	ts = targets.keys()
	with open(savefile,"a") as f:
		for t in ts:
			f.write(t+"\n")


if __name__ == '__main__':
	main()
