<p align="center">
<img src="https://raw.github.com/catmanjan/fireman/master/fireman.png" />
</p>

fireman
=======
python based responsive firewall manager

build
-----
```
python fireman.py
```

stretch goals
-------------
* Expand functionality of rule model to include other features supported by iptables, including conditional throttling, etc.
* Enhanced network support.
* Use journal parsing instead of polling to determine service status.

dependencies
------------
```
sudo yum install python-xmltodict
sudo yum install python-daemon
sudo yum install python-enum
```

For building RPM package with setup.py:
```
sudo yum install @development-tools
sudo yum install fedora-packager
```
