import subprocess
import os

def execute(rules):
    filename = "my-iptables.xml"
    text_file = open(filename, "w")
    text_file.write(rules)
    text_file.close()
    xsltproc = subprocess.Popen(["xsltproc", "iptables.xslt", filename], stdout=subprocess.PIPE)
    subprocess.call(["iptables-restore"], stdin=xsltproc.stdout)
    xsltproc.wait()
    os.remove(filename)
