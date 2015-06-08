export LD_LIBRARY_PATH=/home/squser1/lnxdrvr
g++ connect_test.cpp -L/home/squser1/lnxdrvr -I/home/squser1/lnxdrvr -lhpodbc64 -o connect_test
#./connect_test -d TDM_Default_DataSource -u sql_user -p redhat06

