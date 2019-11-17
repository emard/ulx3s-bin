f=open("main.py","w")
f.write("import network\n")
f.write("ap_if = network.WLAN(network.AP_IF)\n")
f.write("ap_if.active(True)\n")
f.write('ap_if.config(essid="accesspoint", password="password")\n')
f.write("import uftpd\n")
import webrepl_setup
