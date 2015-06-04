#!/bin/bash
#
# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@
#
#------------------------------------------------------------------------------------
# @(#) config.sh
#
# PURPOSE:
#    Configure tests for Python Unittest Framework testing
#
#------------------------------------------------------------------------------------
#

export BASE_DIR=`dirname $0`
export DRVR_TAR_LOC=""
export DSN=""
export ODBCHOME="${ODBCHOME:-/usr}"
export ODBCHOME_LIB="${ODBCHOME}/lib64"
export ODBC_SHARED_LIB="libtrafodbc_drvr64.so"
export ODBC_TRACE="Off"
export DB_CATALOG="TRAFODION"
export DB_SCHEMA="SOMESCHEMA"
export DB_USER="SOMEUSER"
export DB_ROLE=""
export DB_PASSWORD="SOMEPASSWORD"
export DBROOT_USER="SOMEUSER"
export DBROOT_ROLE=""
export DBROOT_PASSWORD="SOMEPASSWORD"
export DB_TYPE="Trafodion"
export DB_UNICODE_TYPE='AppUnicodeType=utf16'
export DB_CERT=''
export PRINT_FILE_CONTENTS="false"
export CLEANUP_FILES="false"
export CONFIG_ODBC="true"
export T4JDBC_CLASSPATH='t4jdbc_classpath='
export NCI_CLASSPATH="hpdci_classpath="
export HPDCI_CLASS="hpdci_class=org.trafodion.ci.UserInterface"
export LOG_DIR=""
export LIBROOT=""
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.51.x86_64}"
export PYODBC_URL="http://dl.bintray.com/alchen99/python/pyodbc-3.0.7.1-unsupported.zip"
export PYPYODBC_URL="http://dl.bintray.com/alchen99/python/pypyodbc-1.3.3.1-unsupported.zip"
if [ "$BASE_DIR" = "." ]; then BASE_DIR=$(pwd); fi


function Program_Help {
    echo ""
    echo "Description: Configure for Python Unittest Framework test suite(s)"
    echo "Usage:       $0 -d <dsn> [OPTIONS]"
    echo ""
    echo "NOTE: If BOTH the -O and the -t option is NOT used then it's assumed the directory $BASE_DIR/odbc_driver has the appropriate ODBC driver installed."
    echo ""
    echo "Options:"
    echo "  -O                       Do NOT configure ODBC"
    echo "  -y <type>                Database type. (Default is Trafodion)"
    echo "  -c <catalog>             Database catalog name to use. (Default is TRAFODION)"
    echo "  -s <schema>              Database schema name to use. (Default is SOMESCHEMA) "
    echo "  -u <user>                Database user name. (Default is SOMEUSER)"
    echo "  -r <user_role>           Database user role."
    echo "  -p <password>            Database user password. (Default is SOMEPASSWORD)"
    echo "  -U <dbroot user>         DBROOT user name. (Default is SOMEUSER)"
    echo "  -R <dbroot user_role>    DBROOT user role."
    echo "  -P <dbroot password>     DBROOT user password. (Default is SOMEPASSWORD)"
    echo "  -d <dsn>                 DSN to connect to           : <Fully_Qualified_Domain_Name_Of_Machine_OR_IP>:<Port>"
    echo "  -t <tar_location>        If tar file exists locally  : /ABSOLUTE_PATH_TO/<ODBC_driver_Filename>.tar.gz"
    echo "                           If tar file exists remotely : scp:jenkins@downloads.trafodion.org:/ABSOLUTE_PATH_TO/<ODBC_driver_Filename>.tar.gz"
    echo "                                                         scp:downloads.trafodion.org:/ABSOLUTE_PATH_TO/<ODBC_driver_Filename>.tar.gz"
    echo "                                                         http://downloads.trafodion.org/<ODBC_driver_Filename>.tar.gz"
    echo "  -o <odbchome>            Driver Manager Home directory. Sets environment variable ODBCHOME. (Default is $ODBCHOME)"
    echo "  -L <odbchome_lib>        Driver Manager library directory. (Default is $ODBCHOME_LIB)"
    echo "  -T                       Set Driver Manager trace ON! (Default is OFF)"
    echo "  -j <java_home>           Java Home directory. Sets environment variable JAVA_HOME. (Default is $JAVA_HOME)"
    echo "  -J <jdbc_classpath>      /ABSOLUTE_PATH_TO/jdbcT4.jar"
    echo "  -N <hpdci_classpath>     /ABSOLUTE_PATH_TO/trafci.jar"
    echo "  -G <log_directory>       Log/Results Direcotry"
    echo "  -S <libroot>             Directory where library files are located. i.e. SPJs"
    echo "  -z                       Cleanup all files in this directory excluding .testrepository subdirectory."
    echo "                           NOTE: This option CANNOT be used with any other options"
    echo "  -v                       Echo contents of configured files"
    echo "  -h                       Print this usage message"
    echo ""
    exit
}

function Cleanup_Files {
  echo "INFO: Cleaning up all files in $BASE_DIR except .testrepository subdirectory"
  cd "$BASE_DIR"
  rm *.ini 2>/dev/null
  rm env.sh 2>/dev/null
  rm *.trc 2>/dev/null
  find . -name "*.pyc" -exec rm -f {} \;
  rm -rf .tox 2>/dev/null
  rm -rf odbc_driver 2>/dev/null
  echo ""
} # end function Cleanup_Files

function Download_Install_Driver {
  # function expects driver to be installed @ $BASE_DIR/odbc_driver
  cd "$BASE_DIR/odbc_driver"
  mkdir tmp
  cd tmp

  # downloads and untars odbc driver installer to tmp directory
  if [ -f "$DRVR_TAR_LOC" ]
  then
    # tar file is located locally
    tar xvf "$DRVR_TAR_LOC"
  elif [ $(echo "$DRVR_TAR_LOC" | egrep -c '^scp:') -eq 1 ]
  then
    # fetch tar file via scp
    scp ${DRVR_TAR_LOC##scp:} .
    tar xvf ${DRVR_TAR_LOC##*\/}
  elif [ $(echo "$DRVR_TAR_LOC" | egrep -c '^http:') -eq 1 ]
  then
    # fetch file via wget
    wget ${DRVR_TAR_LOC}
    tar xvf ${DRVR_TAR_LOC##*\/}
  else
    # unknown option
    echo ""
    echo "ERROR: Do not know how to fetch driver from $DRVR_TAR_LOC. Please check to make sure you are using absolute paths."
    echo ""
    exit 1
  fi

  cd PkgTmp

  # run odbc driver installer
  ./install.sh <<- EOF
YES
$BASE_DIR/odbc_driver
$BASE_DIR/odbc_driver
$BASE_DIR/odbc_driver
$BASE_DIR/odbc_driver
EOF

  # list odbc_driver directory
  echo ""
  echo "INFO: ODBC Driver has been installed and configured"
  if [ "$PRINT_FILE_CONTENTS" = "true" ]
  then
    echo "INFO: Contents of $BASE_DIR/odbc_driver"
    echo ""
    ls "$BASE_DIR/odbc_driver"
  fi
  echo ""
} # end Download_Install_Driver function

function Setup_ODBC_Config {
  cd "$BASE_DIR"

  # set up odbcinst.ini
  sed -e "s%TEMPLATE_PATH_TO_DRIVER%$BASE_DIR/odbc_driver%g" -e "s%TEMPLATE_ODBC_SHARED_LIB%$ODBC_SHARED_LIB%g" -e "s%TEMPLATE_TRACE_FLAG%$ODBC_TRACE%g" -e "s/TEMPLATE_DBTYPE/$DB_TYPE/g" .odbcinst.ini.tmpl > odbcinst.ini
  echo ""
  echo "INFO: File odbcinst.ini has been configured"
  if [ "$PRINT_FILE_CONTENTS" = "true" ]
  then
    echo "INFO: Contents of odbcinst.ini"
    echo ""
    cat odbcinst.ini
  fi
  echo ""

  # set up odbc.ini
  sed -e "s/TEMPLATE_CATALOG/$DB_CATALOG/g" -e "s/TEMPLATE_SCHEMA/$DB_SCHEMA/g" -e "s/TEMPLATE_DSN/$DSN/g" -e "s/TEMPLATE_DBTYPE/$DB_TYPE/g" -e "s%TEMPLATE_DB_CERT%$DB_CERT%g" -e "s/TEMPLATE_UNICODE_TYPE/$DB_UNICODE_TYPE/g" .odbc.ini.tmpl > odbc.ini
  echo ""
  echo "INFO: File odbc.ini has been configured"
  if [ "$PRINT_FILE_CONTENTS" = "true" ]
  then
    echo "INFO: Contents of odbc.ini"
    echo ""
    cat odbc.ini
  fi
  echo ""
} # end Setup_ODBC_Config function

function Setup_PythonFW_Config {
  cd "$BASE_DIR"

  # set up env.sh
  if [ "$CONFIG_ODBC" = "true" ]
  then
    sed -e "s%TEMPLATE_ODBC_LIB%$BASE_DIR/odbc_driver:$ODBCHOME_LIB%g" -e "s%TEMPLATE_ODBC_HOME%$ODBCHOME%g" -e "s%TEMPLATE_ODBC_SYS_INI%$BASE_DIR%g" .env.sh.tmpl > .env.sh.tmpl.1
  else
    sed -e "/TEMPLATE_ODBC_LIB/d" -e "/TEMPLATE_ODBC_HOME/d" -e "/TEMPLATE_ODBC_SYS_INI/d" -e '/export ODBCINI.*/d' -e '/export ODBCINST.*/d' .env.sh.tmpl > .env.sh.tmpl.1
  fi

  if [ -n "$DB_CERT" ]
  then
    sed -e "s/TEMPLATE_UNICODE_TYPE/$DB_UNICODE_TYPE/g" -e "s%TEMPLATE_DB_CERT%$DB_CERT%g" .env.sh.tmpl.1 > env.sh
  else
    sed -e "s/TEMPLATE_UNICODE_TYPE/$DB_UNICODE_TYPE/g" -e '/export TEMPLATE_DB_CERT/d' .env.sh.tmpl.1 > env.sh
  fi
  rm .env.sh.tmpl.1
  echo ""
  echo "INFO: File env.sh has been configured"
  if [ "$PRINT_FILE_CONTENTS" = "true" ]
  then
    echo "INFO: Contents of env.sh"
    echo ""
    cat env.sh
  fi
  echo ""

  # set up config.ini
  sed -e "s/TEMPLATE_CATALOG/$DB_CATALOG/g" -e "s/TEMPLATE_SCHEMA/$DB_SCHEMA/g" -e "s/TEMPLATE_DSN/$DSN/g" -e "s/TEMPLATE_USER/$DB_USER/g" -e "s/TEMPLATE_ROLE/$DB_ROLE/g" -e "s/TEMPLATE_PASSWORD/$DB_PASSWORD/g" -e "s/TEMPLATE_DBROOTUSER/$DBROOT_USER/g" -e "s/TEMPLATE_DBROOTROLE/$DBROOT_ROLE/g" -e "s/TEMPLATE_DBROOTPASSWORD/$DBROOT_PASSWORD/g" -e "s%TEMPLATE_JDBC%$T4JDBC_CLASSPATH%g" -e "s%TEMPLATE_HPDCICLASS%$HPDCI_CLASS%g" -e "s%TEMPLATE_HPDCI%$NCI_CLASSPATH%g" -e "s%TEMPLATE_LOG_DIR%$LOG_DIR%g" -e "s%TEMPLATE_LIBROOT%$LIBROOT%g" .config.ini.tmpl > config.ini

  echo ""
  echo "INFO: File config.ini has been configured"
  if [ "$PRINT_FILE_CONTENTS" = "true" ]
  then
    echo "INFO: Contents of config.ini"
    echo ""
    cat config.ini
  fi
  echo ""

  # set up tox.ini
  if [ "$CONFIG_ODBC" = "true" ]
  then
    sed -e "s%TEMPLATE_ODBC_HOME%$ODBCHOME%g" -e "s%TEMPLATE_ODBC_LIB%$BASE_DIR/odbc_driver:$ODBCHOME_LIB%g" -e "s%TEMPLATE_PYODBC%$PYODBC_URL%g" -e "s%TEMPLATE_PYPYODBC%$PYPYODBC_URL%g" .tox.ini.tmpl > .tox.ini.tmpl.1
  else
    sed -e "/TEMPLATE_ODBC_HOME/d" -e "/TEMPLATE_ODBC_LIB/d" -e '/ODBCSYSINI/d' -e '/ODBCINST/d' -e '/ODBCINI/d' -e "/TEMPLATE_PYODBC/d" -e "/TEMPLATE_PYPYODBC/d" .tox.ini.tmpl > .tox.ini.tmpl.1
  fi

  if [ -n "$DB_CERT" ]
  then
    sed -e "s%TEMPLATE_JAVA_HOME%$JAVA_HOME%g" -e "s/TEMPLATE_UNICODE_TYPE/$DB_UNICODE_TYPE/g" -e "s%TEMPLATE_DB_CERT%$DB_CERT%g" .tox.ini.tmpl.1 > .tox.ini.tmpl.2
  else
    sed -e "s%TEMPLATE_JAVA_HOME%$JAVA_HOME%g" -e "s/TEMPLATE_UNICODE_TYPE/$DB_UNICODE_TYPE/g" -e '/TEMPLATE_DB_CERT/d' .tox.ini.tmpl.1 > .tox.ini.tmpl.2
  fi

  # check to see if http_proxy set in the environment
  PROXY_INFO=""
  PROXY_INFO="$(env | egrep 'http_proxy=' | cut -d'=' -f2)"
  if [ -z "$PROXY_INFO" ]
  then
    sed -e '/TEMPLATE_HTTP_PROXY/d' -e '/TEMPLATE_HTTPS_PROXY/d' -e '/TEMPLATE_FTP_PROXY/d' .tox.ini.tmpl.2 > tox.ini
  else
    sed -e "s%TEMPLATE_HTTP_PROXY%http_proxy=$PROXY_INFO%g" -e "s%TEMPLATE_HTTPS_PROXY%https_proxy=$PROXY_INFO%g" -e "s%TEMPLATE_FTP_PROXY%ftp_proxy=$PROXY_INFO%g" .tox.ini.tmpl.2 > tox.ini
    echo "" >> env.sh
    echo "export http_proxy=$PROXY_INFO" >> env.sh
    echo "export https_proxy=$PROXY_INFO" >> env.sh
    echo "export ftp_proxy=$PROXY_INFO" >> env.sh
  fi
  rm .tox.ini.tmpl.1 .tox.ini.tmpl.2

  echo "INFO: File tox.ini has been configured"
  if [ "$PRINT_FILE_CONTENTS" = "true" ]
  then
    echo "INFO: Contents of tox.ini"
    echo ""
    cat tox.ini
  fi
  echo ""
} # end Setup_PythonFW_Config function


#----------
# Main
#----------

# Process command line arguments
if [ $# -eq 0 ]
then
  Program_Help
  exit 1
else
  while getopts c:d:G:o:L:p:P:r:R:s:t:u:U:y:N:S:j:J:TvzO opt
  do
    case "$opt" in
      c) # catalog
         DB_CATALOG="$OPTARG"
         ;;
      d) # DSN
         DSN="$OPTARG"
         ;;
      G) # log / results directory
         T_LOG_DIR="$OPTARG"
         if [ "${T_LOG_DIR:0:1}" = "/" ]
         then
           # if log directory parameter is given and starts with / then assume it's the absolute path
           LOG_DIR="$T_LOG_DIR"
         else
           # assume relative path
           LOG_DIR=`readlink -f $BASE_DIR/$T_LOG_DIR`
         fi
         ;;
      j) # JAVA_HOME
         JAVA_HOME="$OPTARG"
         ;;
      J) # JDBC classpath
         T4JDBC_CLASSPATH="t4jdbc_classpath=$OPTARG"
         ;;
      L) # ODBCHOME library
         ODBCHOME_LIB="$OPTARG"
         ;;
      N) # HPDCI classpath
         NCI_CLASSPATH="hpdci_classpath=$OPTARG"
         ;;
      o) # ODBCHOME
         ODBCHOME="$OPTARG"
         ;;
      O) # do NOT configure ODBC
         CONFIG_ODBC="false"
         ;;
      p) # Database user's password
         DB_PASSWORD="$OPTARG"
         ;;
      P) # Dbroot user's password
         DBROOT_PASSWORD="$OPTARG"
         ;;
      r) # Database User Role
         DB_ROLE="$OPTARG"
         ;;
      R) # Dbroot User Role
         DBROOT_ROLE="$OPTARG"
         ;;
      s) # Database Schema
         DB_SCHEMA="$OPTARG"
         ;;
      S) # library root directory
         T_LIBROOT="$OPTARG"
         if [ "${T_LIBROOT:0:1}" = "/" ]
         then
           # if log directory parameter is given and starts with / then assume it's the absolute path
           LIBROOT="$T_LIBROOT"
         else
           # assume relative path
           LIBROOT=`readlink -f $BASE_DIR/$T_LIBROOT`
         fi
         ;;
      T) # ODBC Driver trace ON
         ODBC_TRACE="On"
         ;;
      t) # ODBC Driver tar file location
         DRVR_TAR_LOC="$OPTARG"
         ;;
      u) # Database user
         DB_USER="$OPTARG"
         ;;
      U) # Dbroot user
         DBROOT_USER="$OPTARG"
         ;;
      y) # Database type
         DB_TYPE="$OPTARG"
         if [ "$DB_TYPE" != "Trafodion" ]; then
           echo 'ERROR: Invalid database type!  The following are valid database types : Trafodion.'
           exit 1
         fi
         ;;
      v) # print contents of files configured
         PRINT_FILE_CONTENTS="true"
         ;;
      z) # clean up all files except .testrepository subdirectory
         Cleanup_Files
         exit 0
         ;;
     \?) # Unknown option
         Program_Help
         exit 1
         ;;
    esac
  done
fi

# null out all variables related to ODBC 
if [ "$CONFIG_ODBC" = "false" ]
then
  ODBCHOME_LIB=""
  ODBCHOME=""
  DRVR_TAR_LOC=""
  DB_CERT=""
  sed -i '/^https:\/\/github\.com\/.*\/pyodbc.*/d' $BASE_DIR/test-requirements.txt                       # remove pyodbc from test-requirements
  sed -i '/^https:\/\/github\.com\/.*\/pypyodbc.*/d' $BASE_DIR/test-requirements.txt                     # remove pypyodbc from test-requirements
else
  # fix up pyodbc in test-requirements file
  if [ $(egrep -c 'http://dl.bintray.com/.*/pyodbc.*' $BASE_DIR/test-requirements.txt) -lt 1 ]
  then
    echo "$PYODBC_URL" >> $BASE_DIR/test-requirements.txt
  elif [ $(egrep -c 'http://dl.bintray.com/.*/pyodbc.*' $BASE_DIR/test-requirements.txt) -gt 1 ]
  then
    sed -i '/^http:\/\/dl\.bintray\.com\/.*\/pyodbc.*/d' $BASE_DIR/test-requirements.txt                 # remove pyodbc from test-requirements
    echo "$PYODBC_URL" >> $BASE_DIR/test-requirements.txt                                                # add pyodbc back to test-requirements
  fi

  # fix up pypyodbc in test-requirements file
  if [ $(egrep -c 'http://dl.bintray.com/.*/pypyodbc.*' $BASE_DIR/test-requirements.txt) -lt 1 ]
  then
    echo "$PYPYODBC_URL" >> $BASE_DIR/test-requirements.txt
  elif [ $(egrep -c 'http://dl.bintray.com/.*/pypyodbc.*' $BASE_DIR/test-requirements.txt) -gt 1 ]
  then
    sed -i '/^http:\/\/dl\.bintray\.com\/.*\/pypyodbc.*/d' $BASE_DIR/test-requirements.txt               # remove pypyodbc from test-requirements
    echo "$PYPYODBC_URL" >> $BASE_DIR/test-requirements.txt                                              # add pypyodbc back to test-requirements
  fi
fi

# Print out the options set
echo ""
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "@                                                                                                                     "
echo "@  DSN                                : $DSN"
echo "@  Database Type                      : $DB_TYPE"
echo "@  Database User                      : $DB_USER"
echo -n "@  Database User Role                 : "
if [ -z "$DB_ROLE" ]; then echo "Not needed"; else echo "$DB_ROLE"; fi
echo "@  Database Password                  : $DB_PASSWORD"
echo "@  Dbroot User                        : $DBROOT_USER"
echo -n "@  Dbroot User Role                    : "
if [ -z "$DBROOT_ROLE" ]; then echo "Not needed"; else echo "$DBROOT_ROLE"; fi
echo "@  Dbroot Password                    : $DBROOT_PASSWORD"
echo "@  Configuring for ODBC               : $CONFIG_ODBC"
echo -n "@  Driver Tar File Location           : "
if [ -z "$DRVR_TAR_LOC" ]; then echo "Not needed"; else echo "$DRVR_TAR_LOC"; fi
echo -n "@  Driver Manager Home Directory      : "
if [ -z "$ODBCHOME" ]; then echo "Not needed"; else echo "$ODBCHOME"; fi
echo -n "@  Driver Manager Library Directory   : "
if [ -z "$ODBCHOME_LIB" ]; then echo "Not needed"; else echo "$ODBCHOME_LIB"; fi
echo -n "@  JAVA HOME                          : "
if [ -z "$JAVA_HOME" ]; then echo "Not needed"; else echo "${JAVA_HOME}"; fi
echo -n "@  JDBC CLASSPATH                     : "
if [ -z "$T4JDBC_CLASSPATH" ]; then echo "Not needed"; else echo "${T4JDBC_CLASSPATH##*=}"; fi
echo -n "@  HP DCI CLASSPATH                   : "
if [ -z "$NCI_CLASSPATH" ]; then echo "Not needed"; else echo "${NCI_CLASSPATH##*=}"; fi
echo -n "@  Results/Log Directory              : "
if [ -z "$LOG_DIR" ]; then echo "Not needed"; else echo "$LOG_DIR"; fi
echo -n "@  Trafodion library root directory   : "
if [ -z "$LIBROOT" ]; then echo "Not needed"; else echo "$LIBROOT"; fi
echo "@                                                                                                                     "
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo ""

# clean up directory
Cleanup_Files

# check to see if odbc_driver directory exists
if [ "$CONFIG_ODBC" = "true" ]
then
  if [ ! -L "$BASE_DIR/odbc_driver/$ODBC_SHARED_LIB" -a -z "$DRVR_TAR_LOC" ]
  then
    echo ""
    echo "ERROR: Directory $BASE_DIR/odbc_driver has to contain the $DB_TYPE ODBC driver or the option -t <tar_location> has to be specified!"
    echo ""
    exit 1
  elif [ ! -L "$BASE_DIR/odbc_driver/$ODBC_SHARED_LIB" ]
  then
    cd "$BASE_DIR"
    rm -rf odbc_driver
    mkdir odbc_driver
    Download_Install_Driver
  fi
fi

# run setup
if [ "$CONFIG_ODBC" = "true" ]; then Setup_ODBC_Config; fi
Setup_PythonFW_Config

