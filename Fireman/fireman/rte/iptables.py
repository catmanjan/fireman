import subprocess
import os

def execute(rules):
    """ Takes an xml string following iptables-xml specification and adds the
        rules to iptables
        (str) -> None
    """
    # temporary file saved to hold xml
    filename = "my-iptables.xml"
    # xsltproc needs a file to read
    text_file = open(filename, "w")
    # save the xml string to a file
    text_file.write(rules)
    text_file.close()
    # use iptables.xslt to transform the xml file to iptables commands
    xsltproc = subprocess.Popen(["xsltproc", "iptables.xslt",
                                filename], stdout=subprocess.PIPE)
    # execute iptables rules using iptables-restore
    subprocess.call(["iptables-restore"], stdin=xsltproc.stdout)
    xsltproc.wait()
    # remove the file
    os.remove(filename)
