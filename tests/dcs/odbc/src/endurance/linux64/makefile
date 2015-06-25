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
C = gcc 
CC = $(C)
LINK = $(CC)
LINK2 = g++ 
CLEANUP = ./*.o 
LIBPATH = ../lnxdrvr
INCLUDE = -I. -I../lnxdrvr

CFLAGS = -D_UNIX -Dunixcli -g -Wno-deprecated

LIBS = -L$(LIBPATH) -ltrafodbc64 -lpthread -lz -licuucNv44 -licudataNv44

all: endure clientscale

endure: endure.cpp
	$(LINK2) $(LIBS) $(INCLUDE) -o endure endure.cpp
	rm -Rf $(CLEANUP)
	chmod -R 777 *	

clientscale: clientscale.cpp
	$(LINK2) $(LIBS) $(INCLUDE) -o clientscale clientscale.cpp
	rm -Rf $(CLEANUP)
	chmod -R 777 *	

clean:
	rm -Rf $(CLEANUP) endure
	rm -Rf $(CLEANUP) clientscale

.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDE) -c $< 
.c.o:
	$(CC) $(CFLAGS) $(INCLUDE) -c $<
