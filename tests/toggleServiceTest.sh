#!/bin/bash

if [ "$#" -ne "1" ];
then
echo "usage: ./toggleServiceTest.sh [ServiceToTest]"
else
sudo iptables -L > ~tmpforToggleServiceTestIPTables
python src/fireman.py -vi services > ~tmpforToggleServiceTestServices

#ADD service
python src/fireman.py -as $1

#Get results
sudo iptables -L > ~tmpforToggleServiceTestIPTables2
python src/fireman.py -vi services > ~tmpforToggleServiceTestServices2

#compare
echo "Test for Add IP RULES"
diff ~tmpforToggleServiceTestIPTables ~tmpforToggleServiceTestIPTables2

echo "Test for Add Services"
diff ~tmpforToggleServiceTestServices ~tmpforToggleServiceTestServices2

#remove Service
python src/fireman.py -rs $1

#get results
sudo iptables -L > ~tmpforToggleServiceTestIPTables3
python src/fireman.py -vi services > ~tmpforToggleServiceTestServices3

#compare
echo "Test for remove IP RULES"
diff ~tmpforToggleServiceTestIPTables3 ~tmpforToggleServiceTestIPTables2

echo "Test for remove Services"
diff ~tmpforToggleServiceTestServices3 ~tmpforToggleServiceTestServices2

#compare final
echo "Comparing start and end (should be identical) IP RULES"
diff ~tmpforToggleServiceTestIPTables3 ~tmpforToggleServiceTestIPTables

echo "Comparing start and end (should be identical) Services"
diff ~tmpforToggleServiceTestServices3 ~tmpforToggleServiceTestServices

rm ~tmpforToggleServiceTestIPTables
rm ~tmpforToggleServiceTestServices
rm ~tmpforToggleServiceTestIPTables2
rm ~tmpforToggleServiceTestServices2
rm ~tmpforToggleServiceTestIPTables3
rm ~tmpforToggleServiceTestServices3
fi

