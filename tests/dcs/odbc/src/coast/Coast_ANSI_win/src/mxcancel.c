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

#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include <string.h>
#ifdef unixcli
	#include <pthread.h>
#else
	#include <process.h>
#endif
#include "basedef.h"
#include "common.h"
#include "log.h"

#define NUMBER_STMT		3

typedef struct thread_args_t
{
	int				id;
	SQLHANDLE 		henv;
	SQLHANDLE 		hdbc;
	SQLHANDLE		hstmt;
	int				type;	//0: Execdirect; 1: prepare&execute
	int				mode;	//0: Get kill before thread end; 1: thread runs until end
	char			*CancelThreadStr;
} thread_args;

void get_all_errors(SQLHANDLE henv, SQLHANDLE hdbc, SQLHANDLE hstmt, char *message_buf)
{             
	char		buf[MAX_STRING_SIZE];
	char		State[STATE_SIZE];
	RETCODE		returncode;

	strcpy(message_buf,"");
	returncode = SQLError((SQLHANDLE)henv, (SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLCHAR*)State, NULL, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
	while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO)){
		strcat(message_buf,"\nState: ");
		strcat(message_buf,State);
		strcat(message_buf,"\nError: ");
		strcat(message_buf,buf);

		State[STATE_SIZE-1]=NULL_STRING;
		returncode = SQLError((SQLHANDLE)henv, (SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLCHAR*)State, NULL, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
	}
	returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)hdbc, (SQLHANDLE)NULL, (SQLCHAR*)State, NULL, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
	while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO)){
		strcat(message_buf,"\nState: ");
		strcat(message_buf,State);
		strcat(message_buf,"\nError: ");
		strcat(message_buf,buf);

		State[STATE_SIZE-1]=NULL_STRING;
		returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)hdbc, (SQLHANDLE)NULL, (SQLCHAR*)State, NULL, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
	}
	returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLHANDLE)hstmt, (SQLCHAR*)State, NULL, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
	while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO)){
		strcat(message_buf,"\nState: ");
		strcat(message_buf,State);
		strcat(message_buf,"\nError: ");
		strcat(message_buf,buf);

		State[STATE_SIZE-1]=NULL_STRING;
		returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLHANDLE)hstmt, (SQLCHAR*)State, NULL, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
	}
}

void *exec_thread(void *dummy)
{
	TEST_DECLARE;
	RETCODE			returncode;
	SQLHANDLE 		henv;
	SQLHANDLE 		hdbc;
	SQLHANDLE		hstmt;
	char			t[64];
	int c = 1;
	thread_args *my_args = (thread_args *)dummy;
	memset(t, 0, sizeof(t));
 
	henv = my_args->henv;
	hdbc = my_args->hdbc;
	hstmt = my_args->hstmt;

	TESTCASE_BEGIN("Exec thread started\n");

	if (my_args->type == 0)	//Execdirect
	{
		LogMsg(LINEBEFORE,"exec_thread(%d): before SQLExecDirect(), at line %d\n", my_args->id, __LINE__);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)my_args->CancelThreadStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			Sleep(1000*my_args->id);
			LogMsg(ERRMSG,"exec_thread(%d): expected: SQL_SUCCESS, actual: %d, at line %d\n", my_args->id, returncode, __LINE__);
			TESTCASE_END;
			#ifdef unixcli
				pthread_exit(NULL);
			#else
				_endthread();
			#endif
			return NULL;
		}
	}
	else 	//prepare&execute
	{
		LogMsg(LINEBEFORE,"exec_thread(%d): before SQLPrepare(), at line %d\n", my_args->id, __LINE__);
		returncode = SQLPrepare(hstmt,(SQLCHAR*)my_args->CancelThreadStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			Sleep(1000*my_args->id);
			LogMsg(ERRMSG,"exec_thread(%d): expected: SQL_SUCCESS, actual: %d, at line %d\n", my_args->id, returncode, __LINE__);
			TESTCASE_END;
			#ifdef unixcli
				pthread_exit(NULL);
			#else
				_endthread();
			#endif
			return NULL;
		}

		LogMsg(LINEBEFORE,"exec_thread(%d): before SQLExecute(), at line %d\n", my_args->id, __LINE__);
		returncode = SQLExecute(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
		{
			Sleep(1000*my_args->id);
			LogMsg(ERRMSG,"exec_thread(%d): expected: SQL_SUCCESS, actual: %d, at line %d\n", my_args->id, returncode, __LINE__);
			TESTCASE_END;
			#ifdef unixcli
				pthread_exit(NULL);
			#else
				_endthread();
			#endif
			return NULL;
		}
	}

	if (strnicmp(my_args->CancelThreadStr,"select",6) == 0) {
		LogMsg(LINEBEFORE,"exec_thread(%d): before SQLBindCol(), at line %d\n", my_args->id, __LINE__);
		returncode = SQLBindCol(hstmt, 1, SQL_C_CHAR, (SQLPOINTER)t, sizeof(t), NULL);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
		{
			LogMsg(ERRMSG,"exec_thread(%d): expected: SQL_SUCCESS, actual: %d, at line %d\n", my_args->id, returncode, __LINE__);
			TESTCASE_END;
			#ifdef unixcli
				pthread_exit(NULL);
			#else
				_endthread();
			#endif
			return NULL;
		}

		LogMsg(LINEBEFORE,"exec_thread(%d): before SQLFetch(), at line %d\n", my_args->id, __LINE__);
		returncode = SQL_SUCCESS;
		while (returncode == SQL_SUCCESS) {
			returncode = SQLFetch(hstmt);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
			{
				Sleep(1000*my_args->id);
				LogMsg(ERRMSG,"exec_thread(%d): expected: SQL_SUCCESS, actual: %d, at line %d\n", my_args->id , returncode, __LINE__);
				TESTCASE_END;
				#ifdef unixcli
					pthread_exit(NULL);
				#else
					_endthread();
				#endif
				return NULL;
				//break;
			}
			LogMsg(NONE,"==%s==", t);
			if (c == 100) break;
			c++;
		}
	}
 
	LogMsg(LINEBEFORE,"exec_thread(%d): before Thread exits. No one issue cancel, at line %d\n", my_args->id, __LINE__);

	if (my_args->mode == 0)	{
		TEST_FAILED;
	}
	else {
		TESTCASE_END;
	}

	#ifdef unixcli
		pthread_exit(NULL);
	#else
		_endthread();
	#endif
	return NULL;
}

void *cancel_thread(void *dummy)
{
	TEST_DECLARE;
	RETCODE			returncode;
	SQLHANDLE 		henv;
	SQLHANDLE 		hdbc;
	SQLHANDLE		hstmt;
	int				k = 0;
	BOOL			RepeatCancel = FALSE;

	thread_args *my_args = (thread_args *)dummy;
 
	henv = my_args->henv;
	hdbc = my_args->hdbc;
	hstmt = my_args->hstmt;

	TESTCASE_BEGIN("Cancel thread started\n");

	RepeatCancel = FALSE;
	k = 0;
	while ((RepeatCancel == FALSE) && (k < 20))
	{
		returncode = SQLCancel(hstmt);
		if (returncode == SQL_ERROR)
		{
			RepeatCancel = FindError("70100",henv,hdbc,hstmt);
			if (RepeatCancel == TRUE) {
				LogMsg(ERRMSG,"[70100][Operation Aborted] >> The data source was unable to process the cancel request.\n");
				TEST_FAILED;
			}
			else {
				LogMsg(NONE,"Unable to Cancel at this movement try again.\n");
			}
		}
		else {
			RepeatCancel = TRUE;
			LogMsg(NONE,"The cancel request for hstmt was successful. Thread id=%d\n", my_args->id);
		}
		k++;
	}

	TESTCASE_END;

	#ifdef unixcli
		pthread_exit(0);
	#else
		_endthread();
	#endif
	return NULL;
}

/*
---------------------------------------------------------
   TestMXSQLCancel
---------------------------------------------------------
*/
PassFail TestMXSQLCancel(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE			returncode;
	SQLHANDLE 		henv;
	SQLHANDLE 		hdbc;
	SQLHANDLE		hstmt;
	SQLHANDLE		hstmt_array[NUMBER_STMT];
	char			Heading[MAX_STRING_SIZE];
	char			*CancelStr[] = 
						{
							"--",	//"insert into testcancel3 (c1) select x.c1 from testcancel1 x, testcancel2 y, testcancel1 z where x.c1 + y.c1 + z.c1 < 70",
							"--",	//"update testcancel3 set c1 = (select x.c1 from testcancel1 x, testcancel2 y, testcancel1 z where x.c1 + y.c1 + z.c1 = 30)",
							"--",	//"select x.c1 from testcancel1 x, testcancel2 y, testcancel1 z where x.c1 + y.c1 + z.c1 < 70",
							"--",	//"delete from testcancel3 where c1 in (select x.c1 from testcancel1 x, testcancel2 y, testcancel1 z where x.c1 + y.c1 + z.c1 = 30)",
							"endloop",
							"--",	//"insert into testcancel4 (c1) select x.c1 from testcancel1 x, testcancel2 y, testcancel1 z where x.c1 + y.c1 + z.c1 < 70",
							"--",	//"select count(*) from testcancel3"
						};

	char			*CancelStrA[] = 
						{
							"--",	//"insert into testcancel3 (c1) select x.c1 from testcancel1 x, testcancel2 y, testcancel1 z where x.c1 + y.c1 + z.c1 < 70",
							"--",	//"insert into testcancel4 (c1) select x.c1 from testcancel1 x, testcancel2 y, testcancel1 z where x.c1 + y.c1 + z.c1 < 70",
							"--",	//"select x.c1 from testcancel1 x, testcancel2 y, testcancel1 z where x.c1 + y.c1 + z.c1 < 70",
							"--",	//"select count(*) from testcancel3",
							"--",	//"select count(*) from testcancel4",
							"endloop"
						};

	char			*CancelStrForNeedData[] = 
						{
							"--",	//"insert into testcancel3 (c1) values (?)",
							"--",	//"update testcancel3 set c1=? where c1=10",
							"--",	//"select c1 from testcancel3 where c1=?",
							"--",	//"delete from testcancel3 where c1=?",
							"endloop"
						};

	char			*CancelThreadStr[] = 
						{
							"--",	//"insert into testcancel3 (c1) select x.c1 from testcancel1 x, testcancel2 y, testcancel1 z where x.c1 + y.c1 + z.c1 < 70",
							"--",	//"update testcancel3 set c1 = (select count(*) from testcancel1 x, testcancel2 y, testcancel1 z where x.c1 + y.c1 + z.c1 = 30)",
							"--",	//"select count(x.c1) from testcancel1 x, testcancel2 y, testcancel1 z where x.c1 + y.c1 + z.c1 < 70",
							"--",	//"delete from testcancel3 where c1 in (select x.c1 from testcancel1 x, testcancel2 y, testcancel1 z where x.c1 + y.c1 + z.c1 = 30)",
							"endloop"
						};

	char			*DrpTab[4];
	char			*CrtTab[4];
	char			*InsTab[4];
	char			*SelTab[2];

	char			buf[MAX_STRING_SIZE];
	char			State[STATE_SIZE];
	int				i = 0, j = 0, k = 0, l = 0, n=0, s=0;
	BOOL			RepeatCancel = FALSE;
	SQLLEN			InValue = SQL_DATA_AT_EXEC, RowCount;
	thread_args		t_args, t_args1;
	char			message_buf[1024];
	SQLRETURN		rc = 0;		
	#ifdef unixcli
		pthread_t	t[NUMBER_STMT];
	#else
		HANDLE		handle[NUMBER_STMT];
	#endif	

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLCancel", charset_file);
	if (var_list == NULL) return FAILED;

	CancelStr[0] = var_mapping("SQLCancel_CancelStr_0", var_list);
	CancelStr[1] = var_mapping("SQLCancel_CancelStr_1", var_list);
	CancelStr[2] = var_mapping("SQLCancel_CancelStr_2", var_list);
	CancelStr[3] = var_mapping("SQLCancel_CancelStr_3", var_list);
	CancelStr[5] = var_mapping("SQLCancel_CancelStr_5", var_list);
	CancelStr[6] = var_mapping("SQLCancel_CancelStr_6", var_list);

	CancelStrA[0] = var_mapping("SQLCancel_CancelStrA_0", var_list);
	CancelStrA[1] = var_mapping("SQLCancel_CancelStrA_1", var_list);
	CancelStrA[2] = var_mapping("SQLCancel_CancelStrA_2", var_list);
	CancelStrA[3] = var_mapping("SQLCancel_CancelStrA_3", var_list);
	CancelStrA[4] = var_mapping("SQLCancel_CancelStrA_4", var_list);

	CancelStrForNeedData[0] = var_mapping("SQLCancel_CancelStrForNeedData_0", var_list);
	CancelStrForNeedData[1] = var_mapping("SQLCancel_CancelStrForNeedData_1", var_list);
	CancelStrForNeedData[2] = var_mapping("SQLCancel_CancelStrForNeedData_2", var_list);
	CancelStrForNeedData[3] = var_mapping("SQLCancel_CancelStrForNeedData_3", var_list);

	CancelThreadStr[0] = var_mapping("SQLCancel_CancelThreadStr_0", var_list);
	CancelThreadStr[1] = var_mapping("SQLCancel_CancelThreadStr_1", var_list);
	CancelThreadStr[2] = var_mapping("SQLCancel_CancelThreadStr_2", var_list);
	CancelThreadStr[3] = var_mapping("SQLCancel_CancelThreadStr_3", var_list);

	DrpTab[0] = var_mapping("SQLCancel_DrpTab_0", var_list);
	DrpTab[1] = var_mapping("SQLCancel_DrpTab_1", var_list);
	DrpTab[2] = var_mapping("SQLCancel_DrpTab_2", var_list);
	DrpTab[3] = var_mapping("SQLCancel_DrpTab_3", var_list);

	CrtTab[0] = var_mapping("SQLCancel_CrtTab_0", var_list);
	CrtTab[1] = var_mapping("SQLCancel_CrtTab_1", var_list);
	CrtTab[2] = var_mapping("SQLCancel_CrtTab_2", var_list);
	CrtTab[3] = var_mapping("SQLCancel_CrtTab_3", var_list);

	InsTab[0] = var_mapping("SQLCancel_InsTab_0", var_list);
	InsTab[1] = var_mapping("SQLCancel_InsTab_1", var_list);
	InsTab[2] = var_mapping("SQLCancel_InsTab_2", var_list);
	InsTab[3] = var_mapping("SQLCancel_InsTab_3", var_list);

	SelTab[0] = var_mapping("SQLCancel_SelTab_0", var_list);
	SelTab[1] = var_mapping("SQLCancel_SelTab_1", var_list); 

//====================================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLCancel | SQLCancel | mxcancel.c\n");
	TEST_INIT;

	TESTCASE_BEGIN("Initialization for SQLCancel Tests\n");
	if(!FullConnect(pTestInfo)){
		LogMsg(NONE,"Unable to connect\n");
		TEST_FAILED;
		TEST_RETURN;
	}
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[0],SQL_NTS);	// cleanup
	SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[1],SQL_NTS);	// cleanup
	SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[2],SQL_NTS);	// cleanup
	SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[3],SQL_NTS);	// cleanup
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[0],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[1],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[2],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[3],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTab[0], SQL_NTS);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLExecute(hstmt);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTab[1], SQL_NTS);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	for (i = 0; i < 9; i++)
	{
		returncode = SQLExecute(hstmt);
		if (returncode != SQL_SUCCESS)
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
	}

	returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTab[2], SQL_NTS);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLExecute(hstmt);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTab[3], SQL_NTS);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	for (i = 0; i < 4; i++)
	{
		returncode = SQLExecute(hstmt);
		if (returncode != SQL_SUCCESS)
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
	}

	TESTCASE_END;	//end creates and inserts

        //1) 10-100621-1254: Incorrect error message after invoking SQLCancel
        //2) 10-100621-1255: Subsequent calls to SQLExecDirect after SQLCancel return in error
        //For both problems, SQL_ASYNC_ENABLE was ON which is rarely used by client applications.
        //So there is very less chance that these problems are visible in customer environment.
        //The fix would be risky for the time being since we only have two more SUTs

//====================================================================================================================
/* sq: This was commented out in the UNICODE version.  Do the same
for the ANSI version. */
#if 0
	printf("Test SQLCancel with ASYNC mode, one hstmt\n");
	TESTCASE_BEGIN("Test Positive Functionality of SQLCancel with ASYNC mode, one hstmt\n");
	returncode = SQLSetStmtOption(hstmt,SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_ON);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOption"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	TESTCASE_END;	//end initialization

	for(j = 0; j < 2; j++)
	{
		i = 0;
		while(_stricmp(CancelStr[i],"endloop") != 0)
		{
			returncode = SQLSetStmtOption(hstmt,SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_ON);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOption"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}

			if (j == 0)
			{
				sprintf(Heading,"Test Positive Functionality of SQLCancel after doing execdirect on the folowing SQL stmt\n%s\n",CancelStr[i]);
				TESTCASE_BEGIN(Heading);
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)CancelStr[i],strlen(CancelStr[i]));
				if(!CHECKRC(SQL_STILL_EXECUTING,returncode,"SQLExecDirect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
			}
			else
			{
				sprintf(Heading,"Test Positive Functionality of SQLCancel after doing prepare & execute on the following SQL stmt\n%s\n",CancelStr[i]);
				TESTCASE_BEGIN(Heading);
				do
				{
					returncode = SQLPrepare(hstmt,(SQLCHAR*)CancelStr[i],strlen(CancelStr[i]));
					if((returncode != SQL_STILL_EXECUTING) && (returncode != SQL_SUCCESS))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
				}
				while (returncode == SQL_STILL_EXECUTING);
				returncode = SQLExecute(hstmt);
				if(!CHECKRC(SQL_STILL_EXECUTING,returncode,"SQLExecute"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
			}
			if (returncode == SQL_STILL_EXECUTING)
			{
				RepeatCancel = FALSE;
				k = 0;
				while ((RepeatCancel == FALSE) && (k < 20))
				{
					returncode = SQLCancel(hstmt);
					if (returncode == SQL_ERROR) {
						RepeatCancel = FindError("70100",henv,hdbc,hstmt);
						if (RepeatCancel == TRUE) {
							LogMsg(ERRMSG,"[70100][Operation Aborted] >> The data source was unable to process the cancel request.\n");
							TEST_FAILED;
						}
						else {
							LogMsg(NONE,"Unable to Cancel at this moment try again.\n");
						}
					}
					else {
						RepeatCancel = TRUE;
						LogMsg(NONE,"The cancel request was successful.\n");
					}
					k++;
				}

				if (j == 0)	{
					do {
						returncode = SQLExecDirect(hstmt,(SQLCHAR*)CancelStr[i],strlen(CancelStr[i]));
					}
					while (returncode == SQL_STILL_EXECUTING);
				}
				else {
					do {
						returncode = SQLExecute(hstmt);
					}
					while (returncode == SQL_STILL_EXECUTING);
				}
				Sleep(5000);
				switch(returncode)
				{
					// SQL statement completed normally before SQLCancel could stop it
					case SQL_SUCCESS:
						LogMsg(NONE,"SQL statement completed normally before SQLCancel could stop it\n");
						if ( i == 2)
						{
							// read in all the records
							l = 0;
							do
							{
								returncode = SQLFetch(hstmt);
								if (returncode == SQL_STILL_EXECUTING)
								{
									RepeatCancel = FALSE;
									k = 0;
									while ((RepeatCancel == FALSE) && (k < 20))
									{
										returncode = SQLCancel(hstmt);
										if (returncode == SQL_ERROR)
										{
											RepeatCancel = FindError("70100",henv,hdbc,hstmt);
											if (RepeatCancel == TRUE)
											{
												LogMsg(ERRMSG,"[70100][Operation Aborted] >> The data source was unable to process the cancel request.\n");
												TEST_FAILED;
											}
											else
											{
												LogMsg(NONE,"Unable to Cancel at this movement try again.\n");
											}
										}
										else
										{
											RepeatCancel = TRUE;
											LogMsg(NONE,"The cancel request after SQLFetch was successful.\n");
										}
										k++;
									}
									do
									{
										returncode = SQLFetch(hstmt);
										LogMsg(NONE,"SQL_STILL_EXECUTING SQLFetch.\n");
									}
									while (returncode == SQL_STILL_EXECUTING);
								}
								l++;
							}
							while ((returncode == SQL_SUCCESS) && (l < 1));
							returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, hstmt, (SQLCHAR*)State, NULL, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLError"))
							{
								LogAllErrors(henv,hdbc,hstmt);
								TEST_FAILED;
							}

							if(strcmp(State,"08S01")!=0)
							{
								LogMsg(LINEBEFORE+ERRMSG+SHORTTIMESTAMP,"SQLExecDirect: Expected: 08S01  Actual: %s\n",State);
								LogMsg(NONE,"   File: %s   Line: %d\n",__FILE__,__LINE__);
								LogMsg(NONE,"   Should have received a 'comm link failure' (08S01) error.\n");
								LogMsg(NONE,"   but COAST got the following error:\n");
								LogMsg(LINEAFTER,"   (%s) %s\n",State,buf);
								LogAllErrors(henv,hdbc,hstmt);
								TEST_FAILED;
							}
							else
							{
								LogMsg(NONE,"Successfully Canceled the SQL operation.\n");
								LogMsg(NONE,"(%s) %s\n",State,buf);
								//make sure it was an 'end of data' error that kicked us out of the while loop
								if(!CHECKRC(SQL_NO_DATA_FOUND,returncode,"SQLFetch")) 
								{
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
								}
							}
						}
						break;
					// Check that error was because statement was cancelled
					case SQL_ERROR:
						get_all_errors(henv, hdbc, hstmt, message_buf);

						if (strstr(message_buf,"COMMUNICATION LINK FAILURE") == NULL &&
							strstr(message_buf,"OPERATION CANCELLED") == NULL &&
							strstr(message_buf,"Communication link failure") == NULL &&
							strstr(message_buf,"Operation cancelled") == NULL)
						{
							/*LogMsg(LINEBEFORE+ERRMSG+SHORTTIMESTAMP,"SQLExecDirect: Expected: 08S01  Actual: %s\n",State);
							LogMsg(NONE,"   File: %s   Line: %d\n",__FILE__,__LINE__);
							LogMsg(NONE,"   Should have received an 'operation cancelled' (08S01) error.\n");
							LogMsg(NONE,"   but COAST got the following error:\n");
							LogMsg(LINEAFTER,"%s\n",buf); */
							LogMsg(LINEBEFORE+ERRMSG+SHORTTIMESTAMP,"Should have received an 'operation cancelled' (08S01) error but:");
							LogMsg(LINEAFTER,"%s\n", message_buf);
							TEST_FAILED;
						}
						else
						{
							LogMsg(NONE,"Successfully Canceled the SQL operation.\n");
							LogMsg(NONE,"%s\n",message_buf);

							returncode = SQLSetStmtOption(hstmt,SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_OFF);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOption"))
							{
								LogAllErrors(henv,hdbc,hstmt);
								TEST_FAILED;
								TEST_RETURN;
							}

							LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Checking if MXOSRVR is still alive\n");
							returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTab[0],SQL_NTS);
							if(returncode != SQL_ERROR)
							{
								LogMsg(ERRMSG,"Expected: SQL_ERROR, actual: %d, at line=%d\n", returncode, __LINE__);
								TEST_FAILED;
							}
							LogAllErrors(henv,hdbc,hstmt);

							LogMsg(LINEBEFORE+SHORTTIMESTAMP,"MSOCRVR is killed. Need to reconnect for the next test\n");
							//When operation is cancel successfully, MXOSRVR is filled. Need to reconnect for the next test

							SQLFreeStmt(hstmt,SQL_CLOSE);
							SQLFreeStmt(hstmt,SQL_UNBIND);
							FullDisconnect(pTestInfo);

							if(!FullConnect(pTestInfo)){
								LogMsg(NONE,"Unable to connect after SQLCancel is issued and MXOSRVR is killed!\n");
								TEST_FAILED;
								TEST_RETURN;
							}
							henv = pTestInfo->henv;
 							hdbc = pTestInfo->hdbc;
 							hstmt = (SQLHANDLE)pTestInfo->hstmt;
						   	
							returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
 							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
							{
								LogAllErrors(henv,hdbc,hstmt);
								TEST_FAILED;
								TEST_RETURN;
							}
						}
						break;

					default:
						LogMsg(LINEBEFORE+ERRMSG+SHORTTIMESTAMP,
									"SQLExecDirect: Expected: SQL_SUCCESS or SQL_ERROR  Actual: %s\n",
									ReturncodeToChar(returncode,buf));
						LogMsg(NONE,"   File: %s   Line: %d\n",__FILE__,__LINE__);
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				//SQLFreeStmt(hstmt,SQL_CLOSE);
				//SQLFreeStmt(hstmt,SQL_UNBIND);
				TESTCASE_END;
			}

			//Verifying data
			TESTCASE_BEGIN("Verifying data ...\n");
			//printf("%s\n", CancelStr[6]);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)CancelStr[6],SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			RowCount = 0;
			returncode = SQLBindCol(hstmt, 1, SQL_C_LONG, &RowCount, 0, NULL);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TESTCASE_END;
			}
			returncode = SQLFetch(hstmt);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}

			if (RowCount != 0) {
				LogMsg(ERRMSG, "On successfuly SQLCanel, data must be cleaned up. But we found value %d in there. At line=%d\n", RowCount, __LINE__);
				TEST_FAILED;
			}
			else {
				LogMsg(LINEAFTER, "Verify data passed: expected RowCount: 0, actual RowCount=%d\n", RowCount);
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_UNBIND);

			i++;
		}
	}
	
//====================================================================================================================
	returncode = SQLSetStmtOption(hstmt,SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_OFF);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOption"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	for (s=0; s<2; s++) {
		if (s == 0) {//statement level
			printf("Test SQLCancel with ASYNC mode, multiple hstmt, statement level\n");
			TESTCASE_BEGIN("Test Positive Functionality of SQLCancel with ASYNC mode at statement level, multiple hstmt\n");
		}
		else {//connection level
			printf("Test SQLCancel with ASYNC mode, multiple hstmt, connection level\n");
			TESTCASE_BEGIN("Test Positive Functionality of SQLCancel with ASYNC mode at connection level, multiple hstmt\n");
			returncode = SQLSetConnectOption(hdbc,SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_ON);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
		}

		for(n = 0; n < 3; n++)
		{
#ifndef unixcli
				LogMsg(LINEBEFORE+SHORTTIMESTAMP+LINEAFTER,"Testing Cancel hstmt%d in the queue, MSOSRVR has to die\n", n+1);
				printf("Testing Cancel hstmt%d in the queue, MSOSRVR has to die\n", n+1);
#else
			if (n == 0) {
				LogMsg(LINEBEFORE+SHORTTIMESTAMP+LINEAFTER,"Testing Cancel hstmt%d in the queue, MSOSRVR has to die\n", n+1);
				printf("Testing Cancel hstmt%d in the queue, MSOSRVR has to die\n", n+1);
			}
			else {
				LogMsg(LINEBEFORE+SHORTTIMESTAMP+LINEAFTER,"Testing Cancel hstmt%d in the queue, MSOSRVR has to be alive\n", n+1);		
				printf("Testing Cancel hstmt%d in the queue, MSOSRVR has to be alive\n", n+1);		
			}
#endif
			for(j = 0; j < 2; j++)
			{
				for (i=0; i<NUMBER_STMT; i++) {
					returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt_array[i]);	
 					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
					{
						LogAllErrors(henv,hdbc,hstmt_array[i]);
						TEST_FAILED;
						TEST_RETURN;
					}
				}
				if (s == 0) {
					for (i=0; i<NUMBER_STMT; i++) {
						returncode = SQLSetStmtOption(hstmt_array[i],SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_ON);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOption"))
						{
							LogAllErrors(henv,hdbc,hstmt_array[i]);
							TEST_FAILED;
							TEST_RETURN;
						}
					}
				}

				if (s == 1) {
					returncode = SQLSetStmtOption(hstmt,SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_OFF);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOption"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
						TEST_RETURN;
					}
				}

				returncode = SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[2],SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[3],SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[2],SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[3],SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}

				TESTCASE_END;

				if (j == 0)
				{
					sprintf(Heading,"Test Positive Functionality of SQLCancel after doing execdirect\n");
					TESTCASE_BEGIN(Heading);

					for (i=0; i<NUMBER_STMT; i++) {
						LogMsg(NONE,"hstmt%d: %s\n", i+1, CancelStrA[i]);
						returncode = SQLExecDirect(hstmt_array[i],(SQLCHAR*)CancelStrA[i],strlen(CancelStrA[i]));
						if(!CHECKRC(SQL_STILL_EXECUTING,returncode,"SQLExecDirect"))
						{
							LogAllErrors(henv,hdbc,hstmt_array[i]);
							TEST_FAILED;
						}
					}
				}
				else
				{
					sprintf(Heading,"Test Positive Functionality of SQLCancel after doing prepare & execute on the following SQL stmt\n");
					TESTCASE_BEGIN(Heading);

					for (i=0; i<NUMBER_STMT; i++) {
						LogMsg(NONE,"hstmt%d: %s\n", i+1, CancelStrA[i]);
						do
						{
							returncode = SQLPrepare(hstmt_array[i],(SQLCHAR*)CancelStrA[i],strlen(CancelStrA[i]));
							if((returncode != SQL_STILL_EXECUTING) && (returncode != SQL_SUCCESS))
							{
								LogAllErrors(henv,hdbc,hstmt_array[i]);
								TEST_FAILED;
							}
						}
						while (returncode == SQL_STILL_EXECUTING);
					}

					for (i=0; i<NUMBER_STMT; i++) {
						returncode = SQLExecute(hstmt_array[i]);
						if(!CHECKRC(SQL_STILL_EXECUTING,returncode,"SQLExecute"))
						{
							LogAllErrors(henv,hdbc,hstmt_array[i]);
							TEST_FAILED;
						}
					}
				}

				//Doing SQLCancel here
				if (j == 0) {
					returncode = SQLExecDirect(hstmt_array[n],(SQLCHAR*)CancelStrA[n],strlen(CancelStrA[n]));
					if(!CHECKRC(SQL_STILL_EXECUTING,returncode,"SQLExecDirect"))
					{
						LogAllErrors(henv,hdbc,hstmt_array[n]);
						TEST_FAILED;
						TEST_RETURN;
					}
				}
				else {
					returncode = SQLExecute(hstmt_array[n]);
					if(!CHECKRC(SQL_STILL_EXECUTING,returncode,"SQLExecute"))
					{
						LogAllErrors(henv,hdbc,hstmt_array[n]);
						TEST_FAILED;
						TEST_RETURN;
					}
				}

				RepeatCancel = FALSE;
				k = 0;
				while ((RepeatCancel == FALSE) && (k < 20))
				{
					returncode = SQLCancel(hstmt_array[n]);
					if (returncode == SQL_ERROR)
					{
						RepeatCancel = FindError("70100",henv,hdbc,hstmt_array[n]);
						if (RepeatCancel == TRUE) {
							LogMsg(ERRMSG,"[70100][Operation Aborted] >> The data source was unable to process the cancel request.\n");
							TEST_FAILED;
						}
						else {
							LogMsg(NONE,"Unable to Cancel at this moment try again. Try: %d\n", k+1);
						}
					}
					else {
						RepeatCancel = TRUE;
						LogMsg(NONE,"The cancel request was successful.\n");
					}
					k++;
				}

				if (j == 0) {
					do {
						returncode = SQLExecDirect(hstmt_array[n],(SQLCHAR*)CancelStrA[n],strlen(CancelStrA[n]));
					} while (returncode == SQL_STILL_EXECUTING);
				}
				else {
					do {
						returncode = SQLExecute(hstmt_array[n]);
					} while (returncode == SQL_STILL_EXECUTING);
				}
				switch(returncode)
				{
					// SQL statement completed normally before SQLCancel could stop it
					case SQL_SUCCESS:
						LogMsg(NONE,"===========>>>> HAVE TO CHECK BACK THIS CASE\n");
						if ( i == 2)
						{
							// read in all the records
							l = 0;
							do
							{
								returncode = SQLFetch(hstmt_array[n]);
								if (returncode == SQL_STILL_EXECUTING)
								{
									RepeatCancel = FALSE;
									k = 0;
									while ((RepeatCancel == FALSE) && (k < 20))
									{
										returncode = SQLCancel(hstmt_array[n]);
										if (returncode == SQL_ERROR)
										{
											RepeatCancel = FindError("70100",henv,hdbc,hstmt_array[n]);
											if (RepeatCancel == TRUE)
											{
												LogMsg(ERRMSG,"[70100][Operation Aborted] >> The data source was unable to process the cancel request.\n");
												TEST_FAILED;
											}
											else
											{
												LogMsg(NONE,"Unable to Cancel at this movement try again.\n");
											}
										}
										else
										{
											RepeatCancel = TRUE;
											LogMsg(NONE,"The cancel request was successful.\n");
										}
		//										Sleep(10);
										k++;
									}
									do
									{
										returncode = SQLFetch(hstmt_array[n]);
										LogMsg(NONE,"SQL_STILL_EXECUTING SQLFetch.\n");
		//										Sleep(500);
									}
									while (returncode == SQL_STILL_EXECUTING);
								}
								l++;
							}
							while ((returncode == SQL_SUCCESS) && (l < 1));
							returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, hstmt_array[n], (SQLCHAR*)State, NULL, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLError"))
							{
								LogAllErrors(henv,hdbc,hstmt_array[n]);
								TEST_FAILED;
							}

							if(strcmp(State,"08S01")!=0)
							{
								LogMsg(LINEBEFORE+ERRMSG+SHORTTIMESTAMP,"SQLExecDirect: Expected: 08S01  Actual: %s\n",State);
								LogMsg(NONE,"   File: %s   Line: %d\n",__FILE__,__LINE__);
								LogMsg(NONE,"   Should have received a 'comm link failure' (08S01) error.\n");
								LogMsg(NONE,"   but TOAST got the following error:\n");
								LogMsg(LINEAFTER,"   (%s) %s\n",State,buf);
								LogAllErrors(henv,hdbc,hstmt_array[n]);
								TEST_FAILED;
							}
							else
							{
								LogMsg(NONE,"Successfully Canceled the SQL operation.\n");
								LogMsg(NONE,"(%s) %s\n",State,buf);
								//make sure it was an 'end of data' error that kicked us out of the while loop
								if(!CHECKRC(SQL_NO_DATA_FOUND,returncode,"SQLFetch")) 
								{
									LogAllErrors(henv,hdbc,hstmt_array[n]);
									TEST_FAILED;
								}
							}
						}
						break;
					// Check that error was because statement was cancelled
					case SQL_ERROR:
						get_all_errors(henv,hdbc,hstmt_array[n],message_buf);

						if (strstr(message_buf,"COMMUNICATION LINK FAILURE") == NULL &&
							strstr(message_buf,"OPERATION CANCELLED") == NULL &&
							strstr(message_buf,"Communication link failure") == NULL &&
							strstr(message_buf,"Operation cancelled") == NULL)
		//						if(strcmp(State,"08S01")!=0)
						{
							LogMsg(LINEBEFORE+ERRMSG+SHORTTIMESTAMP,"SQLExecDirect: Expected: 08S01  Actual: %s\n",State);
							LogMsg(NONE,"   File: %s   Line: %d\n",__FILE__,__LINE__);
							LogMsg(NONE,"   Should have received an 'operation cancelled' (08S01) error.\n");
							LogMsg(NONE,"   but TOAST got the following error:\n");
							LogMsg(LINEAFTER,"%s\n",message_buf);
							TEST_FAILED;
						}
						else
						{
							LogMsg(NONE,"Successfully Canceled the SQL operation, on hstmt%d.\n", n+1);
							LogMsg(LINEBEFORE+SHORTTIMESTAMP+LINEAFTER,"%s\n",message_buf);
						}
						break;

					default:
						LogMsg(LINEBEFORE+ERRMSG+SHORTTIMESTAMP,
									"SQLExecDirect: Expected: SQL_SUCCESS or SQL_ERROR  Actual: %s\n",
									ReturncodeToChar(returncode,buf));
						LogMsg(NONE,"   File: %s   Line: %d\n",__FILE__,__LINE__);
						LogAllErrors(henv,hdbc,hstmt_array[n]);
						TEST_FAILED;
				}//End switch for hstmt

#ifndef unixcli
				//MXOSRVR has to die, all hstmt have to fail
				for (i=0; i<NUMBER_STMT; i++) {
					if (i == n) continue;

					LogMsg(NONE,"Check the connection status of hstmt%d.\n", i+1);
					if (j == 0)	{
						do {
							returncode = SQLExecDirect(hstmt_array[i],(SQLCHAR*)CancelStrA[i],strlen(CancelStrA[i]));
						} while (returncode == SQL_STILL_EXECUTING);
					}
					else {
						do {
							returncode = SQLExecute(hstmt_array[i]);
						} while (returncode == SQL_STILL_EXECUTING);
					}
					if(!CHECKRC(SQL_ERROR,returncode,"SQLExecute"))
					{
						TEST_FAILED;
					}
					LogAllErrors(henv,hdbc,hstmt_array[i]);
				}
#else
				if (n == 0) { //MXOSRVR has to die, all hstmt have to fail
					for (i=1; i<NUMBER_STMT; i++) {
						LogMsg(NONE,"Check the connection status of hstmt%d.\n", i+1);
						if (j == 0)	{
							do {
								returncode = SQLExecDirect(hstmt_array[i],(SQLCHAR*)CancelStrA[i],strlen(CancelStrA[i]));
							} while (returncode == SQL_STILL_EXECUTING);
						}
						else {
							do {
								returncode = SQLExecute(hstmt_array[i]);
							} while (returncode == SQL_STILL_EXECUTING);
						}
						if(!CHECKRC(SQL_ERROR,returncode,"SQLExecute"))
						{
							TEST_FAILED;
						}
						LogAllErrors(henv,hdbc,hstmt_array[i]);
					}
				}
				else { //MXOSRVR has to be alive, all the remaining hstmts have to pass
					for (i=0; i<NUMBER_STMT; i++) {
						if (i == n) continue;

						LogMsg(NONE,"Check the connection status of hstmt%d.\n", i+1);
						if (j == 0)	{
							do {
								returncode = SQLExecDirect(hstmt_array[i],(SQLCHAR*)CancelStrA[i],strlen(CancelStrA[i]));
							} while (returncode == SQL_STILL_EXECUTING);
						}
						else {
							do {
								returncode = SQLExecute(hstmt_array[i]);
							} while (returncode == SQL_STILL_EXECUTING);
						}
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
						{
							LogAllErrors(henv,hdbc,hstmt_array[i]);
							TEST_FAILED;
						}

						//Validate the data
						returncode = SQLRowCount(hstmt_array[i], &RowCount);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLRowCount"))
						{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
						}
						if (i != 2) {
							if (RowCount != 4194304) {
								TEST_FAILED;
								LogMsg(ERRMSG,"Expect rowcount: 4194304, actual rowcount: %d\n", RowCount);
							}
							else {
								LogMsg(LINEBEFORE+LINEAFTER,"Expect rowcount: 4194304, actual rowcount: %d\n", RowCount);
							}
						}
						else {
							if (RowCount != 0) {
								LogMsg(ERRMSG,"Expect rowcount: 0, actual rowcount: %d\n", RowCount);
								TEST_FAILED;
							}
							else {
								LogMsg(LINEBEFORE+LINEAFTER,"Expect rowcount: 0, actual rowcount: %d\n", RowCount);
							}
						}
					}
				}
#endif

				Sleep(5000);

				returncode = SQLSetStmtOption(hstmt,SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_OFF);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOption"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}

				LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Checking if MXOSRVR is still alive\n");
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTab[0],SQL_NTS);
#ifndef unixcli
				if(returncode!=SQL_ERROR)
				{
					LogMsg(ERRMSG,"Expected: SQL_ERROR, actual: %d, at line=%d\n", returncode, __LINE__);
					TEST_FAILED;
				}
				else {
#else
				if(returncode==SQL_SUCCESS || returncode==SQL_SUCCESS_WITH_INFO)
				{
					if (n == 0) {
						LogMsg(ERRMSG,"Expected: SQL_ERROR, actual: %d, at line=%d\n", returncode, __LINE__);
						TEST_FAILED;
					}
				}
				else {
					if (n != 0) {
						LogMsg(ERRMSG,"Expected: SQL_SUCCESS, actual: %d, at line=%d\n", returncode, __LINE__);
						TEST_FAILED;
					}
#endif

					LogAllErrors(henv,hdbc,hstmt);
					LogMsg(LINEBEFORE+SHORTTIMESTAMP,"MSOCRVR is killed. Need to reconnect for the next test\n");

					SQLFreeStmt(hstmt,SQL_CLOSE);
					SQLFreeStmt(hstmt,SQL_UNBIND);
					for (i=0; i<NUMBER_STMT; i++) {
						SQLFreeStmt(hstmt_array[i],SQL_CLOSE);
						SQLFreeStmt(hstmt_array[i],SQL_UNBIND);
					}
					FullDisconnect(pTestInfo);

					if(!FullConnect(pTestInfo)){
						LogMsg(NONE,"Unable to connect after SQLCancel is issued and MXOSRVR is killed!\n");
						TEST_FAILED;
						TEST_RETURN;
					}
					henv = pTestInfo->henv;
					hdbc = pTestInfo->hdbc;
					hstmt = (SQLHANDLE)pTestInfo->hstmt;
				   	
					returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
						TEST_RETURN;
					}

					for (i=0; i<NUMBER_STMT; i++) {
						returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt_array[i]);	
 						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
						{
							LogAllErrors(henv,hdbc,hstmt_array[i]);
							TEST_FAILED;
							TEST_RETURN;
						}
					}

					if (s == 1) {
						returncode = SQLSetConnectOption(hdbc,SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_ON);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
						{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
							TEST_RETURN;
						}
					}
				}

				SQLFreeStmt(hstmt,SQL_CLOSE);
				SQLFreeStmt(hstmt,SQL_UNBIND);
				for (i=0; i<NUMBER_STMT; i++) {
					SQLFreeStmt(hstmt_array[i],SQL_CLOSE);
					SQLFreeStmt(hstmt_array[i],SQL_UNBIND);
				}
				TESTCASE_END;
			}//End for j loop (for execdirect and prepare/execute)
		}//End for n loop
	}//End for s loop
	
//====================================================================================================================
#endif /* sq */

	printf("Test SQLCancel for functions that need data\n");
	TESTCASE_BEGIN("Test Positive Functionality of SQLCancel for functions that need data.\n");
	returncode = SQLSetStmtOption(hstmt,SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_OFF);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtOption"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END;


	for(j = 0; j < 2; j++)
	{
		i = 0;
		while(_stricmp(CancelStrForNeedData[i],"endloop") != 0)
		{
			if (j == 0)
			{
				sprintf(Heading,"Test Positive Functionality of SQLCancel after doing execdirect on the folowing SQL stmt\n%s\n",CancelStrForNeedData[i]);
				TESTCASE_BEGIN(Heading);
				InValue = SQL_DATA_AT_EXEC;
				returncode = SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_LONG,SQL_INTEGER,10,0,NULL,0,&InValue);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)CancelStrForNeedData[i],strlen(CancelStrForNeedData[i]));
				if(!CHECKRC(SQL_NEED_DATA,returncode,"SQLExecDirect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
			}
			else
			{
				sprintf(Heading,"Test Positive Functionality of SQLCancel after doing prepare & execute on the following SQL stmt\n%s\n",CancelStrForNeedData[i]);
				TESTCASE_BEGIN(Heading);
				returncode = SQLPrepare(hstmt,(SQLCHAR*)CancelStrForNeedData[i],strlen(CancelStrForNeedData[i]));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				InValue = SQL_DATA_AT_EXEC;
				returncode = SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_LONG,SQL_INTEGER,10,0,NULL,0,&InValue);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				returncode = SQLExecute(hstmt);
				if(!CHECKRC(SQL_NEED_DATA,returncode,"SQLExecute"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
			}
//			Sleep(5000);
			RepeatCancel = FALSE;
			k = 0;
			while ((RepeatCancel == FALSE) && (k < 20))
			{
				returncode = SQLCancel(hstmt);
				if (returncode == SQL_ERROR)
				{
					RepeatCancel = FindError("70100",henv,hdbc,hstmt);
					if (RepeatCancel == TRUE)
					{
						LogMsg(ERRMSG,"[70100][Operation Aborted] >> The data source was unable to process the cancel request.\n");
						TEST_FAILED;
					}
					else
					{
						LogMsg(NONE,"Unable to Cancel at this movement try again.\n");
					}
				}
				else
				{
					RepeatCancel = TRUE;
					LogMsg(NONE,"The cancel request was successful.\n");
				}
//				Sleep(1000);
				k++;
			}
			if (j == 0)
			{
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)CancelStrForNeedData[i],strlen(CancelStrForNeedData[i]));
				if(!CHECKRC(SQL_NEED_DATA,returncode,"SQLExecDirect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
			}
			else
			{
				returncode = SQLExecute(hstmt);
				if(!CHECKRC(SQL_NEED_DATA,returncode,"SQLExecute"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
			}
			SQLCancel(hstmt);
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_UNBIND);
			TESTCASE_END;
			i++;
		}
	}
/* The Multi-thread cancelling test was badly written.  It has no coordination
 * between 2 threads and uses sleep() a lot.  The tests ofen fail because of
 * different client machine speed or target machine speed.  Comment them
 * out for now.
 */
#ifdef TEST_MULTITHREAD_CANCEL

//====================================================================================================================
	printf("Test SQLCancel for functions on another thread, single thread\n");
	TESTCASE_BEGIN("Test Positive Functionality of SQLCancel for functions on another thread.\n");
	
	//i=0: The function is canceled successfully. MXOSRVR has to die
	//i=1: The function is finished before issueing cancel. MXOSRVR should not die
	for (n=0; n<2; n++) {
		for(j = 0; j < 2; j++)
		{
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[2],SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[2],SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}

			i = 0;
			if (j == 0)
			{
				sprintf(Heading,"Test Positive Functionality of SQLCancel after doing execdirect on the folowing SQL stmt\n%s\n",CancelStrA[i]);
			}
			else
			{
				sprintf(Heading,"Test Positive Functionality of SQLCancel after doing prepare & execute on the following SQL stmt\n%s\n",CancelStrA[i]);
			}
			TESTCASE_BEGIN(Heading);

			t_args.id = i;
			t_args.henv = henv;
			t_args.hdbc = hdbc;
			t_args.hstmt = hstmt;
			t_args.CancelThreadStr = CancelStrA[i];
			t_args.type = j;
			t_args.mode = n;

			#ifdef unixcli
				rc = pthread_create(&t[i], NULL, exec_thread, &t_args);
				if (rc){
					LogMsg(ERRMSG,"ERROR: Could not create a new thread. pthread_create()return code: rc=%d\n", rc);
					TEST_FAILED;
					TEST_RETURN;
				}
				Sleep(3000);
			#else
				handle[i] = (HANDLE) _beginthread(exec_thread,0,&t_args); // create thread
				Sleep(3000);
			#endif

			if (n == 1) {
				#ifdef unixcli
					pthread_join(t[i], NULL);
				#else
					WaitForSingleObject(handle[i],INFINITE);
				#endif		
			}

			RepeatCancel = FALSE;
			k = 0;
			while ((RepeatCancel == FALSE) && (k < 20))
			{
				returncode = SQLCancel(hstmt);
				if (returncode == SQL_ERROR)
				{
					RepeatCancel = FindError("70100",henv,hdbc,hstmt);
					if (RepeatCancel == TRUE) {
						LogMsg(ERRMSG,"[70100][Operation Aborted] >> The data source was unable to process the cancel request.\n");
						TEST_FAILED;
					}
					else {
						LogMsg(NONE,"Unable to Cancel at this movement try again.\n");
					}
				}
				else {
					RepeatCancel = TRUE;
					LogMsg(NONE,"The cancel request for hstmt was successful.\n");
				}
				k++;
			}

			if (n == 0) {
				#ifdef unixcli
					pthread_join(t[i], NULL);
				#else
					WaitForSingleObject(handle[i],INFINITE);
				#endif
			}

			get_all_errors(henv,hdbc,hstmt,message_buf);

			if (n == 0) {
				if (strstr(message_buf,"COMMUNICATION LINK FAILURE") == NULL &&
					strstr(message_buf,"OPERATION CANCELLED") == NULL &&
					strstr(message_buf,"Communication link failure") == NULL &&
					strstr(message_buf,"Operation cancelled") == NULL)
				{
					LogMsg(LINEBEFORE+ERRMSG+SHORTTIMESTAMP,"SQLExecDirect: Expected: 08S01  Actual: %s\n",State);
					LogMsg(NONE,"   File: %s   Line: %d\n",__FILE__,__LINE__);
					LogMsg(NONE,"   Should have received an 'operation cancelled' (08S01) error.\n");
					LogMsg(NONE,"   but TOAST got the following error:\n");
					LogMsg(LINEAFTER,"%s\n",message_buf);
					TEST_FAILED;
				}
				else
				{
					LogMsg(NONE,"Successfully Canceled the SQL operation, on hstmt\n");
					LogMsg(LINEBEFORE+SHORTTIMESTAMP+LINEAFTER,"%s\n",message_buf);
				}
			}
			else {
				LogMsg(LINEBEFORE+SHORTTIMESTAMP+LINEAFTER,"I dont think we have any error message here.\n%s\n",message_buf);
			}

			LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Checking if MXOSRVR is still alive\n");
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTab[1],SQL_NTS);
			if(returncode != SQL_ERROR)
			{
				if (n == 0)	LogMsg(ERRMSG,"Expected: SQL_ERROR, actual: %d\n", returncode);
				else LogMsg(LINEBEFORE+SHORTTIMESTAMP,"MSOSRVR is still alive\n");
			}
			else {
				if (n == 1) {
					LogMsg(ERRMSG,"MXOSRVR has to be alive in this case. Since the function finished before cancel!");
					TEST_FAILED;
				}

				LogAllErrors(henv,hdbc,hstmt);
				
				SQLFreeStmt(hstmt,SQL_CLOSE);
				SQLFreeStmt(hstmt,SQL_UNBIND);

				//When operation is cancel successfully, MXOSRVR is filled. Need to reconnect for the next test
				LogMsg(LINEBEFORE+SHORTTIMESTAMP,"MSOSRVR is killed. Need to reconnect for the next test\n");
				if(!FullConnect(pTestInfo)){
					LogMsg(NONE,"Unable to connect after SQLCancel is issued and MXOSRVR is killed!\n");
					TEST_FAILED;
					TEST_RETURN;
				}
				henv = pTestInfo->henv;
				hdbc = pTestInfo->hdbc;
				hstmt = (SQLHANDLE)pTestInfo->hstmt;

				returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
			}

			//Verify the data
			LogMsg(LINEBEFORE+SHORTTIMESTAMP+LINEAFTER, "We are verifying the data after doing cancel.");

			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_UNBIND);

			returncode = SQLExecDirect(hstmt,(SQLCHAR*)CancelStrA[i+3],SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			returncode = SQLBindCol(hstmt, 1, SQL_C_LONG, &RowCount, 0, NULL);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TESTCASE_END;
			}
			returncode = SQLFetch(hstmt);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}

			LogMsg(LINEAFTER, "Data returns: %d\n", RowCount);
			if (n == 0) {
				if (RowCount != 0) {
					LogMsg(ERRMSG, "On successfuly SQLCanel, data must be cleaned up. But we found value %d in there.\n", RowCount);
				}
			}
			else {
				if (RowCount == 0) {
					LogMsg(ERRMSG, "Since the function finished before cancel, data must be in the table. But we have rowcount=%d\n", RowCount);
				}
			}

			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_UNBIND);
			TESTCASE_END;
		}//End j for loop
	}//End n for loop

	TESTCASE_END;

//====================================================================================================================
	printf("Test SQLCancel for functions on another thread, multiple thread\n");
	TESTCASE_BEGIN("Test Positive Functionality of SQLCancel for functions on another thread.\n");
	
	//i=0: The function is canceled successfully. MXOSRVR has to die
	//i=1: The function is finished before issueing cancel. MXOSRVR should not die
	for (n=0; n<1; n++) {
		for(j = 0; j < 2; j++)
		{
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[2],SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[2],SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}

			i = 0;
			if (j == 0)
			{
				sprintf(Heading,"Test Positive Functionality of SQLCancel after doing execdirect on the folowing SQL stmt\n%s\n",CancelStrA[i]);
			}
			else
			{
				sprintf(Heading,"Test Positive Functionality of SQLCancel after doing prepare & execute on the following SQL stmt\n%s\n",CancelStrA[i]);
			}
			TESTCASE_BEGIN(Heading);

			t_args.id = i;
			t_args.henv = henv;
			t_args.hdbc = hdbc;
			t_args.hstmt = hstmt;
			t_args.CancelThreadStr = CancelStrA[i];
			t_args.type = j;
			t_args.mode = n;

			t_args1.id = i+1;
			t_args1.henv = henv;
			t_args1.hdbc = hdbc;
			t_args1.hstmt = hstmt;
			t_args1.CancelThreadStr = CancelStrA[i];
			t_args1.type = j;
			t_args1.mode = n;

			#ifdef unixcli
				rc = pthread_create(&t[i], NULL, exec_thread, &t_args);
				if (rc){
					LogMsg(ERRMSG,"ERROR: Could not create a new exec_thread. pthread_create()return code: rc=%d\n", rc);
					TEST_FAILED;
					TEST_RETURN;
				}
				Sleep(3000);

				rc = pthread_create(&t[i+1], NULL, cancel_thread, &t_args1);
				if (rc){
					LogMsg(ERRMSG,"ERROR: Could not create a new cancel_thread. pthread_create()return code: rc=%d\n", rc);
					TEST_FAILED;
					TEST_RETURN;
				}
				pthread_join(t[i+1], NULL);
				pthread_join(t[i], NULL);
			#else
				handle[i] = (HANDLE) _beginthread(exec_thread,0,&t_args); // create thread
				Sleep(3000);

				handle[i+1] = (HANDLE) _beginthread(cancel_thread,0,&t_args1); // create thread
				WaitForSingleObject(handle[i+1],INFINITE);
				WaitForSingleObject(handle[i],INFINITE);
			#endif

			get_all_errors(henv,hdbc,hstmt,message_buf);

			if (n == 0) {
				if (strstr(message_buf,"COMMUNICATION LINK FAILURE") == NULL &&
					strstr(message_buf,"OPERATION CANCELLED") == NULL &&
					strstr(message_buf,"Communication link failure") == NULL &&
					strstr(message_buf,"Operation cancelled") == NULL)
				{
					LogMsg(LINEBEFORE+ERRMSG+SHORTTIMESTAMP,"SQLExecDirect: Expected: 08S01  Actual: %s\n",State);
					LogMsg(NONE,"   File: %s   Line: %d\n",__FILE__,__LINE__);
					LogMsg(NONE,"   Should have received an 'operation cancelled' (08S01) error.\n");
					LogMsg(NONE,"   but TOAST got the following error:\n");
					LogMsg(LINEAFTER,"%s\n",message_buf);
					TEST_FAILED;
				}
				else
				{
					LogMsg(NONE,"Successfully Canceled the SQL operation, on hstmt\n");
					LogMsg(LINEBEFORE+SHORTTIMESTAMP+LINEAFTER,"%s\n",message_buf);
				}
			}
			else {
				LogMsg(LINEBEFORE+SHORTTIMESTAMP+LINEAFTER,"I dont think we have any error message here.\n%s\n",message_buf);
			}

			LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Checking if MXOSRVR is still alive\n");
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTab[1],SQL_NTS);
			if(returncode != SQL_ERROR)
			{
				if (n == 0)	LogMsg(ERRMSG,"Expected: SQL_ERROR, actual: %d\n", returncode);
				else LogMsg(LINEBEFORE+SHORTTIMESTAMP,"MSOSRVR is still alive\n");
			}
			else {
				if (n == 1) {
					LogMsg(ERRMSG,"MXOSRVR has to be alive in this case. Since the function finished before cancel!");
					TEST_FAILED;
				}

				LogAllErrors(henv,hdbc,hstmt);
				
				SQLFreeStmt(hstmt,SQL_CLOSE);
				SQLFreeStmt(hstmt,SQL_UNBIND);

				//When operation is cancel successfully, MXOSRVR is filled. Need to reconnect for the next test
				LogMsg(LINEBEFORE+SHORTTIMESTAMP,"MSOSRVR is killed. Need to reconnect for the next test\n");
				if(!FullConnect(pTestInfo)){
					LogMsg(NONE,"Unable to connect after SQLCancel is issued and MXOSRVR is killed!\n");
					TEST_FAILED;
					TEST_RETURN;
				}
				henv = pTestInfo->henv;
				hdbc = pTestInfo->hdbc;
				hstmt = (SQLHANDLE)pTestInfo->hstmt;

				returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
			}

			//Verify the data
			LogMsg(LINEBEFORE+SHORTTIMESTAMP+LINEAFTER, "We are verifying the data after doing cancel.");

			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_UNBIND);

			returncode = SQLExecDirect(hstmt,(SQLCHAR*)CancelStrA[i+3],SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			returncode = SQLBindCol(hstmt, 1, SQL_C_LONG, &RowCount, 0, NULL);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TESTCASE_END;
			}
			returncode = SQLFetch(hstmt);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}

			LogMsg(LINEAFTER, "Data returns: %d\n", RowCount);
			if (n == 0) {
				if (RowCount != 0) {
					LogMsg(ERRMSG, "On successfuly SQLCanel, data must be cleaned up. But we found value %d in there.\n", RowCount);
				}
			}
			else {
				if (RowCount == 0) {
					LogMsg(ERRMSG, "Since the function finished before cancel, data must be in the table. But we have rowcount=%d\n", RowCount);
				}
			}

			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_UNBIND);
			TESTCASE_END;
		}//End j for loop
	}//End n for loop

	TESTCASE_END;
#endif /* TEST_MULTITHREAD_CANCEL */
//====================================================================================================================
	SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[0],SQL_NTS);	// cleanup
	SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[1],SQL_NTS);	// cleanup
	SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[2],SQL_NTS);	// cleanup
	FullDisconnect(pTestInfo);
	LogMsg(LINEBEFORE+SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLCancel.\n");
	free_list(var_list);
	TEST_RETURN;
}
//tt
