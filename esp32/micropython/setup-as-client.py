f=open("main.py","w")
f.write("import network\n")
f.write("sta_if = network.WLAN(network.STA_IF)\n")
f.write("sta_if.active(True)\n")
f.write('sta_if.connect("accesspoint", "password")\n')
f.write("import uftpd\n")
f.close()
import webrepl_setup
