/**
  @@@ START COPYRIGHT @@@

  (C) Copyright 2015 Hewlett-Packard Development Company, L.P.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  @@@ END COPYRIGHT @@@
*/

// Endure.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdlib.h>
#ifdef __linux
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/wait.h>
#define Sleep usleep
#else
#include <windows.h>
#include <winbase.h>
#endif

int main(int argc, char* argv[])
{
	//dsn, uid, pwd, num of minutes, number of clients (this many connect/ddl/dml clients will be spawned)

	char dsn[50];
	char uid[50];
	char pwd[50];
	char connstr[200];

	unsigned int numMinutes;
	unsigned int numConnClients, numDDLClients, numDMLClients, numPoolClients;
	unsigned int i;
	unsigned int j = 0;
	unsigned int numTables;

#ifdef __linux
	int m;
	pid_t pid;
	pid_t *pid_list;
	int pid_idx=0;
	char *my_argv[9];
#else
	char ProcCrtStr[1000];
	STARTUPINFO	si;
	PROCESS_INFORMATION	pi;
#endif

	if (argc < 4)
	{
		puts ("Usage: endure <dsn> <uid> <pwd> <number of minutes> <#conn clients> <#DDL clients> <#DML clients> <#Pooling clients>\n");
		puts ("<dsn> : Required. Data Source to be used\n");
		puts ("<uid> : Required. User ID to be used\n");
		puts ("<pwd> : Required. Password\n");
		puts ("<number of minutes> : Optional. clients will be run for this duration, Default 10 mins\n");
		puts ("<number of Connect/Disconnect clients> : Optional. This many Connect clients will be spawned. Default is 5.\n");
		puts ("<number of DDL clients> : Optional. This many DDL clients will be spawned. Default is 5.\n");
		puts ("<number of DML clients> : Optional. This many DML clients will be spawned. Default is 5.\n");
        puts ("<number of Pooling clients> : Optional. This many connection clients with ConnectionPooling option will be spawned. Default is 5.\n");
		return 0;
	}

	strcpy(dsn, argv[1]);
	strcpy(uid, argv[2]);
	strcpy(pwd, argv[3]);
	numMinutes = 10;
	numConnClients = 5;
	numDDLClients = 5;
	numDMLClients = 5;
    numPoolClients = 5;
	if (argc >= 5)
	{
		numMinutes = atoi(argv[4]);
		if (argc >= 6)
		{
			numConnClients = atoi(argv[5]);
			if (argc >= 7)
			{
				numDDLClients = atoi(argv[6]);
				if (argc >= 8)
				{
					numDMLClients = atoi(argv[7]);
                    if(argc >= 9) {
                        numPoolClients = atoi(argv[8]);
                    }
				}
			}
		}
	}

#ifdef __linux
	pid_list = (pid_t *) malloc (sizeof(pid_t) * 
                           (numConnClients+numDDLClients+
                            numDMLClients+numPoolClients));
#endif

	sprintf(connstr,"DSN=%s;UID=%s;PWD=%s;",dsn, uid, pwd);

	numTables = 2;

	// DDL Clients
	for (i = 0; i < numDDLClients; i++)
	{
        if(numDDLClients == 0)
            break;

#ifdef __linux
		pid = fork();
		if (pid == 0)
		{
			for(m = 0; m < 8; m++)
				my_argv[m] = (char *) malloc (50);
			/* child process */
			sprintf (my_argv[0], "./clientscale");
			sprintf (my_argv[1], "%d", numMinutes);
			sprintf (my_argv[2], "%d", j+1);
			sprintf (my_argv[3], "%s", connstr);
			sprintf (my_argv[4], "DDL");
			sprintf (my_argv[5], "%d", i+1);
			sprintf (my_argv[6], "%d", numDDLClients);
			sprintf (my_argv[7], "%d", numTables);
			my_argv[8] = 0;
			execv("./clientscale", my_argv);
			/* the code will come here only when execv fails */
			printf ("ERROR: execv(clientscale) failed for DDL "
                                "errno %d: %s\n", errno, strerror(errno));
			fflush (stdout);
			exit (-1); /* only if exec fails */
		}
		else
		{
			/* pid !=0 parent process */
			/* I don't think we need to wait for the child to
			 * exit here. 
			 */
			/* waitpid (pid, 0, 0); */	
			pid_list[pid_idx++]=pid;
			j++;
			sleep (3);
		}
#else
		memset(&si, 0, sizeof(si));
		si.cb = sizeof(si);
		sprintf(ProcCrtStr,"clientScale %d %d %s DDL %d %d %d", numMinutes, j+1, connstr, i+1, numDDLClients, numTables);
		CreateProcess(NULL, ProcCrtStr, NULL, NULL, TRUE, CREATE_NEW_CONSOLE, NULL, NULL, &si, &pi);
		j++;
		Sleep(3000);
#endif
	}
	
	// DML Clients
	for (i = 0; i < numDMLClients; i++)
	{
        if(numDMLClients == 0)
            break;
#ifdef __linux
                pid = fork();
                if (pid == 0)
                {
                        for(m = 0; m < 8; m++)
                                my_argv[m] = (char *) malloc (50);
                        /* child process */
                        sprintf (my_argv[0], "./clientscale");
                        sprintf (my_argv[1], "%d", numMinutes);
                        sprintf (my_argv[2], "%d", j+1);
                        sprintf (my_argv[3], "%s", connstr);
                        sprintf (my_argv[4], "DML");
                        sprintf (my_argv[5], "%d", i+1);
                        sprintf (my_argv[6], "%d", numDMLClients);
                        sprintf (my_argv[7], "%d", numTables);
                        my_argv[8] = 0;
                        execv("./clientscale", my_argv);
                        /* the code will come here only when execv fails */
                        printf ("ERROR: execv(clientscale) failed for DDL "
                                "errno %d: %s\n", errno, strerror(errno));
                        fflush (stdout);
                        exit (-1); /* only if exec fails */
                }
                else
                {
                        /* pid !=0 parent process */
                        /* I don't think we need to wait for the child to
                         * exit here.
                         */
                        /* waitpid (pid, 0, 0); */
                        pid_list[pid_idx++]=pid;
                        j++;
                        sleep (3);
                }
#else
		memset(&si, 0, sizeof(si));
		si.cb = sizeof(si);
		sprintf(ProcCrtStr,"clientScale %d %d %s DML %d %d %d", numMinutes, j+1, connstr, i+1, numDMLClients, numTables);
		CreateProcess(NULL, ProcCrtStr, NULL, NULL, TRUE, CREATE_NEW_CONSOLE, NULL, NULL, &si, &pi);
		j++;
		Sleep(3000);
#endif
	}

    // Connection Pooling Clients
    for (i = 0; i < numPoolClients; i++)
	{
        if(numPoolClients == 0)
            break;
#ifdef __linux
                pid = fork();
                if (pid == 0)
                {
                        for(m = 0; m < 8; m++)
                                my_argv[m] = (char *) malloc (50);
                        /* child process */
                        sprintf (my_argv[0], "./clientscale");
                        sprintf (my_argv[1], "%d", numMinutes);
                        sprintf (my_argv[2], "%d", j+1);
                        sprintf (my_argv[3], "%s", connstr);
                        sprintf (my_argv[4], "POOLING");
                        sprintf (my_argv[5], "%d", i+1);
                        sprintf (my_argv[6], "%d", numConnClients);
                        sprintf (my_argv[7], "%d", numTables);
                        my_argv[8] = 0;
                        execv("./clientscale", my_argv);
                        /* the code will come here only when execv fails */
                        printf ("ERROR: execv(clientscale) failed for DDL "
                                "errno %d: %s\n", errno, strerror(errno));
                        fflush (stdout);
                        exit (-1); /* only if exec fails */
                }
                else
                {
                        /* pid !=0 parent process */
                        /* I don't think we need to wait for the child to
                         * exit here.
                         */
                        /* waitpid (pid, 0, 0); */
                        pid_list[pid_idx++]=pid;
                        j++;
                        sleep (3);
                }
#else
		memset(&si, 0, sizeof(si));
		si.cb = sizeof(si);
		sprintf(ProcCrtStr,"clientScale %d %d %s POOLING %d %d %d", numMinutes, j+1, connstr, i+1, numConnClients, numTables);
		CreateProcess(NULL, ProcCrtStr, NULL, NULL, TRUE, CREATE_NEW_CONSOLE, NULL, NULL, &si, &pi);
		j++;
		Sleep(3000);
#endif
	}

	// Connect and Disconnect Clients
#ifdef __linux
	sleep (5);
#else
	Sleep(5000);
#endif
	for (i = 0; i < numConnClients; i++)
	{
        if(numConnClients == 0)
            break;
#ifdef __linux
                pid = fork();
                if (pid == 0)
                {
                        for(m = 0; m < 8; m++)
                                my_argv[m] = (char *) malloc (50);
                        /* child process */
                        sprintf (my_argv[0], "./clientscale");
                        sprintf (my_argv[1], "%d", numMinutes);
                        sprintf (my_argv[2], "%d", j+1);
                        sprintf (my_argv[3], "%s", connstr);
                        sprintf (my_argv[4], "CONNECTION");
                        sprintf (my_argv[5], "%d", i+1);
                        sprintf (my_argv[6], "%d", numConnClients);
                        sprintf (my_argv[7], "%d", numTables);
                        my_argv[8] = 0;
                        execv("./clientscale", my_argv);
                        /* the code will come here only when execv fails */
                        printf ("ERROR: execv(clientscale) failed for DDL "
                                "errno %d: %s\n", errno, strerror(errno));
                        fflush (stdout);
                        exit (-1); /* only if exec fails */
                }
                else
                {
                        /* pid !=0 parent process */
                        /* I don't think we need to wait for the child to
                         * exit here.
                         */
                        /* waitpid (pid, 0, 0); */
                        pid_list[pid_idx++]=pid;
                        j++;
                        sleep (3);
                }
#else
		memset(&si, 0, sizeof(si));
		si.cb = sizeof(si);
		sprintf(ProcCrtStr,"clientScale %d %d %s CONNECTION %d %d %d", numMinutes, j+1, connstr, i+1, numConnClients, numTables);
		CreateProcess(NULL, ProcCrtStr, NULL, NULL, TRUE, CREATE_NEW_CONSOLE, NULL, NULL, &si, &pi);
		j++;
		Sleep(3000);
#endif
	}

#ifdef __linux
	/* Now wait for all childen to finish */
	for (m = 0; m < (numConnClients+numDDLClients+
                        numDMLClients+numPoolClients); m++)
	  waitpid (pid_list[m], 0, 0);
#endif

	return 0;
}

