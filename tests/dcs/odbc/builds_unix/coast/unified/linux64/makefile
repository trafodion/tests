# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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


# DEFINES
C = g++ 
CC = $(C)
LINK = $(CC)
LINK2 = g++ 
CLEANUP = $(OBJ)/*.o ./*.char run.sh env.sh 
EXENAME = coast
SRCDIR = ../../../../src/coast/coast_unified/src
LIBPATH = ../../../../drivers_unix/linux64
INCLUDE = -I. -I$(SRCDIR) -I$(LIBPATH) 
OBJ=./obj
TSTOBJS =$(SRCDIR)/afcon.o \
	$(SRCDIR)/afenv.o \
	$(SRCDIR)/allochandle.o \
	$(SRCDIR)/alocstmt.o \
	$(SRCDIR)/bindcol.o \
	$(SRCDIR)/bindpara.o \
	$(SRCDIR)/browse.o \
	$(SRCDIR)/closecursor.o \
	$(SRCDIR)/COAST.o \
	$(SRCDIR)/colpriv.o \
	$(SRCDIR)/columns.o \
	$(SRCDIR)/common.o \
	$(SRCDIR)/connect.o \
	$(SRCDIR)/copydesc.o \
	$(SRCDIR)/datasrc.o \
	$(SRCDIR)/desparam.o \
	$(SRCDIR)/diagrec.o \
	$(SRCDIR)/drivers.o \
	$(SRCDIR)/drvconn.o \
	$(SRCDIR)/endtran.o \
	$(SRCDIR)/error.o \
	$(SRCDIR)/execdir.o \
	$(SRCDIR)/execute.o \
	$(SRCDIR)/fetch.o \
	$(SRCDIR)/fetchscroll.o \
	$(SRCDIR)/forkeys.o \
	$(SRCDIR)/getdata.o \
	$(SRCDIR)/getdescrec.o \
	$(SRCDIR)/getdiagfield.o \
	$(SRCDIR)/getfunc.o \
	$(SRCDIR)/getinfo.o \
	$(SRCDIR)/gettypei.o \
	$(SRCDIR)/getoptw.o \
	$(SRCDIR)/gettypeiR18.o \
	$(SRCDIR)/hash2.o \
	$(SRCDIR)/largeblock.o \
	$(SRCDIR)/infostats.o \
	$(SRCDIR)/log.o \
	$(SRCDIR)/moreres.o \
	$(SRCDIR)/mxcancel.o \
	$(SRCDIR)/mxcolatt.o \
	$(SRCDIR)/mxcolattr3.o \
	$(SRCDIR)/mxdescfields.o \
	$(SRCDIR)/mxdescol.o \
	$(SRCDIR)/MXProc.o \
	$(SRCDIR)/MXProcCol.o \
	$(SRCDIR)/mxputdata.o \
	$(SRCDIR)/mxresgov.o \
	$(SRCDIR)/natsql.o \
	$(SRCDIR)/numpar.o \
	$(SRCDIR)/numres.o \
	$(SRCDIR)/PartialDateTimeInput.o \
	$(SRCDIR)/PartialDateTimeOutput.o \
	$(SRCDIR)/prepare.o \
	$(SRCDIR)/prikeys.o \
	$(SRCDIR)/QueryID.o \
	$(SRCDIR)/rowcount.o \
	$(SRCDIR)/setenv.o \
	$(SRCDIR)/setgetco.o \
	$(SRCDIR)/setgetconnattr.o \
	$(SRCDIR)/setgetcu.o \
	$(SRCDIR)/setgetst.o \
	$(SRCDIR)/setstmtattr.o \
	$(SRCDIR)/specol.o \
	$(SRCDIR)/sqlbindcolinterval.o \
	$(SRCDIR)/sqlbindcolVer3.o \
	$(SRCDIR)/sqlbindparameterver3.o \
	$(SRCDIR)/sqlbindparaminterval.o \
	$(SRCDIR)/sqldescribecolver3.o \
	$(SRCDIR)/SQLExtendedFetch.o \
	$(SRCDIR)/sqlgetdatainterval.o \
	$(SRCDIR)/sqlgetdataver3.o \
	$(SRCDIR)/sqlgetinfover3.o \
	$(SRCDIR)/sqlmoreresultsver3.o \
	$(SRCDIR)/stat.o \
	$(SRCDIR)/tables.o \
	$(SRCDIR)/tabpriv.o \
	$(SRCDIR)/transact.o \
	$(SRCDIR)/windows.o

LINKOBJS =$(OBJ)/afcon.o \
	$(OBJ)/afenv.o \
	$(OBJ)/allochandle.o \
	$(OBJ)/alocstmt.o \
	$(OBJ)/bindcol.o \
	$(OBJ)/bindpara.o \
	$(OBJ)/browse.o \
	$(OBJ)/closecursor.o \
	$(OBJ)/COAST.o \
	$(OBJ)/colpriv.o \
	$(OBJ)/columns.o \
	$(OBJ)/common.o \
	$(OBJ)/connect.o \
	$(OBJ)/copydesc.o \
	$(OBJ)/datasrc.o \
	$(OBJ)/desparam.o \
	$(OBJ)/diagrec.o \
	$(OBJ)/drivers.o \
	$(OBJ)/drvconn.o \
	$(OBJ)/endtran.o \
	$(OBJ)/error.o \
	$(OBJ)/execdir.o \
	$(OBJ)/execute.o \
	$(OBJ)/fetch.o \
	$(OBJ)/fetchscroll.o \
	$(OBJ)/forkeys.o \
	$(OBJ)/getdata.o \
	$(OBJ)/getdescrec.o \
	$(OBJ)/getdiagfield.o \
	$(OBJ)/getfunc.o \
	$(OBJ)/getinfo.o \
	$(OBJ)/getoptw.o \
	$(OBJ)/gettypei.o \
	$(OBJ)/gettypeiR18.o \
	$(OBJ)/hash2.o \
	$(OBJ)/largeblock.o \
	$(OBJ)/infostats.o \
	$(OBJ)/log.o \
	$(OBJ)/moreres.o \
	$(OBJ)/mxcancel.o \
	$(OBJ)/mxcolatt.o \
	$(OBJ)/mxcolattr3.o \
	$(OBJ)/mxdescfields.o \
	$(OBJ)/mxdescol.o \
	$(OBJ)/MXProc.o \
	$(OBJ)/MXProcCol.o \
	$(OBJ)/mxputdata.o \
	$(OBJ)/mxresgov.o \
	$(OBJ)/natsql.o \
	$(OBJ)/numpar.o \
	$(OBJ)/numres.o \
	$(OBJ)/PartialDateTimeInput.o \
	$(OBJ)/PartialDateTimeOutput.o \
	$(OBJ)/prepare.o \
	$(OBJ)/QueryID.o \
	$(OBJ)/prikeys.o \
	$(OBJ)/rowcount.o \
	$(OBJ)/setenv.o \
	$(OBJ)/setgetco.o \
	$(OBJ)/setgetconnattr.o \
	$(OBJ)/setgetcu.o \
	$(OBJ)/setgetst.o \
	$(OBJ)/setstmtattr.o \
	$(OBJ)/specol.o \
	$(OBJ)/sqlbindcolinterval.o \
	$(OBJ)/sqlbindcolVer3.o \
	$(OBJ)/sqlbindparameterver3.o \
	$(OBJ)/sqlbindparaminterval.o \
	$(OBJ)/sqldescribecolver3.o \
	$(OBJ)/SQLExtendedFetch.o \
	$(OBJ)/sqlgetdatainterval.o \
	$(OBJ)/sqlgetdataver3.o \
	$(OBJ)/sqlgetinfover3.o \
	$(OBJ)/sqlmoreresultsver3.o \
	$(OBJ)/stat.o \
	$(OBJ)/tables.o \
	$(OBJ)/tabpriv.o \
	$(OBJ)/transact.o \
	$(OBJ)/windows.o

SINGLE = $(SRCDIR)/$(OJ).o

CFLAGS = -Dunixcli -g -w -Wno-missing-braces -D_$(MODE) -D_$(VER) -D_HASH2 # -fshort-wchar -D__SQLWCHAR_ISSHORT 
CXXFLAGS = -Dunixcli -g -w -Wno-missing-braces -D_$(MODE) -D_$(VER) -D_HASH2 # -fshort-wchar -D__SQLWCHAR_ISSHORT 

LIBS = -L$(LIBPATH) -ltrafodbc64 -lpthread -lz -licuucNv44 -licudataNv44

all: $(TSTOBJS)
	mv -f *.o $(OBJ)
	$(LINK2) $(LIBS) $(LINKOBJS) $(INCLUDE) -o $(EXENAME)
	rm -Rf $(CLEANUP)
#ln -f -s $(SRCDIR)/charset_ascii.char ./charset_auto_generated_ascii.char
	ln -f -s $(SRCDIR)/charset_auto_generated_ascii.char ./charset_auto_generated_ascii.char
	ln -f -s $(SRCDIR)/charset_auto_generated_gbk.char ./charset_auto_generated_gbk.char
	ln -f -s $(SRCDIR)/charset_auto_generated_gb2.char ./charset_auto_generated_gb2.char
	ln -f -s $(SRCDIR)/charset_auto_generated_sjis.char ./charset_auto_generated_sjis.char
	ln -f -s ../../../common/TRAFDSN_ANSI ./TRAFDSN
	ln -f -s ../../common/run.sh ./run.sh
	echo "export ODBCTEST_DSN=TDM_Default_DataSource" >> env.sh
	echo "export ODBCTEST_USER=userid" >> env.sh
	echo "export ODBCTEST_PASS=password" >> env.sh
	echo "export ODBCTEST_CHARSET=ASCII" >> env.sh
	echo "export ODBCTEST_OS=linux64" >> env.sh
	chmod -R 777 *	

link:
	$(LINK2) $(LIBS) $(LINKOBJS) $(INCLUDE) -o $(EXENAME)
	
clean:
	rm -Rf $(CLEANUP) coast

.cpp.o:
	$(CC) $(CXXFLAGS) $(INCLUDE) -c $< 
.c.o:
	$(CC) $(CFLAGS) $(INCLUDE) -c $< 
	
b1: $(SINGLE)
	mv -f $(OJ).o $(OBJ)/$(OJ).o
	$(LINK2) $(LIBS) $(LINKOBJS) $(INCLUDE) -o $(EXENAME)
	
