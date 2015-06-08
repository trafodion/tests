export PATH=/opt/hp/squser1/opencart/php/bin:$PATH
export LD_LIBRARY_PATH=/opt/hp/squser1/opencart/lnxdrvr
export ODBC_HOME=/opt/hp/squser1/opencart/lnxdrvr
export CPPFLAGS="-I$ODBC_HOME/include"; 
export CUSTOM_ODBC_LIBS="-L$ODBC_HOME -lhpodbc64"
