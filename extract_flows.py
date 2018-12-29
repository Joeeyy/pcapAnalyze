#coding=utf8
import os
import re

extracted_flows_dir = "./extracted_flows/"
targets_path = "./targets.log"
targets = []
pcap_path = "./wechat.pcap"

def main():
	if not os.path.isdir(extracted_flows_dir):
		os.mkdir(extracted_flows_dir)

	with open(targets_path,"r") as f:
		targets = f.readlines()

	for target in targets:
		name = ""
		print(target)
		target = target.replace("\n","")
		tmp = target.split(":")
		protocol = tmp[0]
		ip_or_dn = tmp[1]
		port = tmp[2]

		re_result = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_or_dn)
		rule = ""
		if re_result:
			rule = "ip.addr==%s&&tcp.port==%s"%(ip_or_dn,port)
			name = ip_or_dn
		else:
			if ip_or_dn[0] == "[":
				ip_list = ip_or_dn[1:-1].replace("\'","").split(", ")
				for ip in ip_list:
					if ip == ip_list[-1]:
						rule += "(ip.addr==%s&&tcp.port==%s)"%(ip,port)
					else:
						rule += "(ip.addr==%s&&tcp.port==%s)||"%(ip,port)
				name = "["+ip_list[0]+"]"
			else:
				rule = "(ip.src_host==%s||ip.dst_host==%s)&&tcp.port==%s"%(ip_or_dn,ip_or_dn,port)
				name = ip_or_dn

		save_file = extracted_flows_dir + "%s_%s.pcap"%(name,port)
		cmd = "tshark -r %s -2 -R \"%s\" -w %s"%(pcap_path, rule, save_file)
		print(cmd)
		os.system(cmd)

if __name__ == '__main__':
	main()