#coding=utf8
import os
import re

feature_file = "./feature.csv"
app = "WeChat"
protocol = "6"

def hex2int(hex):
	ret = 0
	a = hex[0]
	b = hex[1]
	if a == "a":
		ret += 16*10
	elif a == "b":
		ret += 16*11
	elif a == "c":
		ret += 16*12
	elif a == "d":
		ret += 16*13
	elif a == "e":
		ret += 16*14
	elif a == "f":
		ret += 16*15
	else:
		ret += 16*int(a)

	if b == "a":
		ret += 10
	elif b == "b":
		ret += 11
	elif b == "c":
		ret += 12
	elif b == "d":
		ret += 13
	elif b == "e":
		ret += 14
	elif b == "f":
		ret += 15
	else:
		ret += int(b)

	return ret


def main():
	#f = open(feature_file,"a")
	pcaps = os.listdir("./")
	for pcap in pcaps:
		cmd_count_streams = "tshark -r %s -q -z conv,tcp|wc -l"%pcap
		num = int(os.popen(cmd_count_streams).read()) - 6
		for i in range(num):
			line = ""
			cmd_get_info = "tshark -r %s -q -z follow,tcp,hex,%d"%(pcap,i)
			info = os.popen(cmd_get_info).read()
			a = info.split("\n\t")
			b = a[0].split("\n")
			node0 = b[4].split(":",1)[1].replace(" ","").split(":")
			node0_ip = node0[0]
			node0_port = node0[1]
			node1 = b[5].split(":",1)[1].replace(" ","").split(":")
			node1_ip = node1[0]
			node1_port = node1[1]
			bytes16 = b[6].split( )[1:17]
			line = node0_ip+","+node0_port+","+node1_ip+","+node1_port+","+protocol+","+"%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d"%(hex2int(bytes16[0]),hex2int(bytes16[1]),hex2int(bytes16[2]),hex2int(bytes16[3]),hex2int(bytes16[4]),hex2int(bytes16[5]),hex2int(bytes16[6]),hex2int(bytes16[7]),hex2int(bytes16[8]),hex2int(bytes16[9]),hex2int(bytes16[10]),hex2int(bytes16[11]),hex2int(bytes16[12]),hex2int(bytes16[13]),hex2int(bytes16[14]),hex2int(bytes16[15]))+","+app+"\n"
			print(line)




	#f.close()


if __name__ == '__main__':
	main()