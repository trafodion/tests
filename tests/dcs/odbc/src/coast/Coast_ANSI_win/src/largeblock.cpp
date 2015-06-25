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
#include "basedef.h"
#include "common.h"
#include "log.h"
#include "apitests.h"

#define MAX_SIZE_KEY				2048
#define	MAX_SIZE_KEY_UCS2			1024
#define MAX_SIZE_COL				32708
#define MAX_COL		 				20
#define MAX_FILENAME_LENGTH			256
#define MAX_SERVER_NAME_LENGTH		128
#define SQL_MAX_DB_NAME_LEN			60
#define MAX_STRING_SIZE				500
#define STATE_SIZE					6
#define OUT_CONN_STR				1024

#define EXEC_DIRECT					0
#define PREPARE_EXEC_FETCH			1
#define PREPARE_EXEC_EXNENDEDFETCH	2

#define T_SQLConnect				0
#define T_SQLDriverConnect			1

#ifndef _WM
#define DATE_FORMAT1 "2007-12-30"
#define DATE_FORMAT2 "2007-10-30"
#else
#define DATE_FORMAT1 "07/12/30"
#define DATE_FORMAT2 "07/10/30"
#endif

PassFail TestLargeBlock(TestInfo *pTestInfo)
{
	TEST_DECLARE;
	char				temp[MAX_SIZE_COL];
    char				keysize[18];
 	char				Heading[MAX_STRING_SIZE];
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	SQLUSMALLINT		FetchStatus;
	SQLULEN				FetchProcessed;
	SQLLEN				OutConnStrLen;
	int					loop, totalLen = 0, i, j=0, k;
	bool				failed = false;

	char				ld_input[MAX_SIZE_KEY+3];
    char				ld_input_half[MAX_SIZE_KEY+3];
	char				ld_output[MAX_SIZE_KEY+1];
    char				ld_output_half[MAX_SIZE_KEY+1];
	char				outValue[MAX_SIZE_KEY+1];
    char                datastr1[MAX_SIZE_KEY+3];      //"abcdefghij"
    char                datastr2[MAX_SIZE_KEY+3];      //"'abcdefghijklmnopqrstuvwxyz1234567890'"
    char                datastr3[MAX_SIZE_KEY+3];      //"abcdefghijk123432"
    char                datastr4[MAX_SIZE_KEY+3];      //"13453aabea__DEJKD"
	char*				sqlStmt;
    char*               whereClause;

	char	*DrpTable,*CrtTable,*InsTable,*SelTable,*UpdTable,*DelTable;

	struct _Row {
		CHAR		A[MAX_COL][MAX_SIZE_COL];
		SQLLEN		AInd[MAX_COL];
	} aRow;

	struct testStruct
	{
		int			size;
		char		*cols;
		char		*input[MAX_COL];
		char		*updatecols;
		char		*output[MAX_COL];
	} dataTypesMatrix[] = {
		{2, "--",	{ld_input,"'0123456789'"},		                "--",		{ld_output,datastr1}},
		{2, "--",	{ld_input,"'0123456789'"},		                "--",		{ld_output,datastr1}},
		{2, "--",	{ld_input,"1234.56789"},		                "--",		{ld_output,"9876.54321"}},
		{2, "--",	{ld_input,"5678.12345"},		                "--",		{ld_output,"1234.56785"}},
        {2, "--",	{ld_input,"5678.12345"},		                "--",		{ld_output,"1234.56785"}},
		{2, "--",	{ld_input,"-1234"},				                "--",		{ld_output,"-4321"}},
		{2, "--",	{ld_input,"6789"},				                "--",		{ld_output,"9876"}},
		{2, "--",	{ld_input,"-12345"},			                "--",		{ld_output,"-54321"}},
		{2, "--",	{ld_input,"56789"},				                "--",		{ld_output,"98765"}},
		{2, "--",	{ld_input,"12340"},				                "--",		{ld_output,"54321.0"}},
		{2, "--",	{ld_input,"12300"},				                "--",		{ld_output,"32100.0"}},
		{2, "--",	{ld_input,"12345670"},			                "--",		{ld_output,"76543210.0"}},
		{2, "--",	{ld_input,"{d '1993-12-30'}"},	                "--",		{ld_output,DATE_FORMAT1}},
		{2, "--",	{ld_input,"-9876543"},			                "--",		{ld_output,"-1234567"}},
		{2, "--",	{ld_input,"{t '11:45:23'}"},	                "--",		{ld_output,"12:15:20"}},
		{2, "--",	{ld_input,"{ts '1992-12-31 23:45:23.123456'}"}, "--",       {ld_output,"2007-12-30 12:15:20.123456"}},
		{3, "--",	{ld_input, ld_input, "123456.001"},	            "--",       {ld_output, ld_output, "654321.001"}},
		{4, "--",	{"123450", ld_input, "123456.001", ld_input},   "--",       {"123450", ld_output, "654321.001", ld_output}},
		{18,"--",	{ld_input,"'0123456789'","'0123456789'",ld_input,"1234.56789","5678.12345","-1234","6789","-12345","56789","12340",	"12300","12345670","{d '1993-12-30'}","{t '11:45:23'}","{ts '1992-12-31 23:45:23.123456'}","-9876543", "12345678.9012345678901234567890"},
			"--",   {ld_output,datastr1,datastr1,ld_output,"9876.54321","8765.12345","-4321","9876","-54321","98765","43210.0","32100.0","76543210.0",DATE_FORMAT2,"12:25:21","2007-10-30 12:25:21.123456", "-6563455", "-12345678.1234567890000000000000"}},
        //This section is for Bignum testing
        {2, "--",	{ld_input,"1234567890.12345678"},               "--",		{ld_output,"123456789.12345678"}},
        {2, "--",	{ld_input,"12345678901234567890.12345678901234567890123456789012345678901"}, 
            "--",   {ld_output,"-123456789012345678901234567890.123456789012345678901234567890123456789012345678901000"}},
		{2, "--", 
			{"-1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678",
			 "'1234567890'"},
			"--",
			{"-1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678",
			 "0123456"}
		},
		{2, "--",
			{"1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678",
			 "'1234567890'"},
			"--",
			{"1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678",
			 "0123456"}
		},
		{2, "--",
			{"'1234567890'",
			 "1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678"},
			"--",
			{"1234567890",
			 "1234567890123456789012345678901234567890.1234567890123456789012345678901234567890123456789012345678901234"}
		},
		{2, "--",
			{"'1234567890'",
			 "-1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678"},
			"--",
			{"1234567890",
             "-1234567890123456789012345678901234567890.1234567890123456789012345678901234567890123456789012345678901234"}
		},
		{2, "--",
			{"'1234567890'",
			 "1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678"},
			"--",
			{"1234567890",
			 "1234567890123456789012345678901234567890.1234567890123456789012345678901234567890123456789012345678901234"}
		},
		{7, "--",
			{"1234567.1234556789",
			 "12345678.1234567899",
			 "1234567890123456789",
			 "1234567890123456789012345678901234567890",
			 "1234567890123456789012345678901234567890.123456789012345678901234567890123456789",
			 "0.12345678901234567890123456789012345678901234567890123456789012345678901234567890",
			 "1234567.8901234567"},
			"--",
			{"1234567",
			 "12345678.1234500000",
			 "1234567890",
			 "123456789012345678901234567890123456789012345678901234.5678901234",
			 "12345678901234567890.1234567890000000000000000000000000000000000000000000000000000000",
#ifndef _WM
			 "0.12345678901234567890123456789012345678901234567890123456789000000000000000000000000000000000000000000000000000000000000000000000",
			 /*sq "0.1234567890" */"1234567.8901234567"
#else
			 ".12345678901234567890123456789012345678901234567890123456789000000000000000000000000000000000000000000000000000000000000000000000",
			 /*sq ".1234567890" */"1234567.8901234567"
#endif			
			}
		},
		{7, "--",
			{"-1234567.1234567899",
			 "-12345678.1234567899",
			 "-1234567890123456789",
			 "-1234567890123456789012345678901234567890",
			 "-1234567890123456789012345678901234567890.123456789012345678901234567890123456789",
			 "-0.12345678901234567890123456789012345678901",
			 "-1234567.8901234567"},
			"--",
			{"-1234567.1234567899000000000000000000000000000000000000000000000000000000",
			 "-12345678.1234500000",
			 "-1234567890",
			 "-12345678901234567890123456789012345678901234567890123456789012345678901234567890",
			 "-12345678901234567890.1234567890000000000000000000000000000000000000000000000000000000",
#ifndef _WM
			 "-0.12345678901234567890123456789012345678901234567890123456789000000000000000000000000000000000000000000000000000000000000000000000",
			 "-0.1234567890"
#else
			 "-.12345678901234567890123456789012345678901234567890123456789000000000000000000000000000000000000000000000000000000000000000000000",
			 "-.1234567890"
#endif
			}
		},
		{7, "--",
			{"0.12345678901234567899",
			 "-12345678.1234567899",
			 "1234567890123456789",
			 "-1234567890123456789012345678901234567890",
			 "1234567890123456789012345678901234567890.123456789012345678901234567890123456789",
			 "-0.12345678901234567890123456789012345678901",
			 "1234567.8901234567"},
			"--",
			{
#ifndef _WM
				"0.12345678901234567899000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
				"12345678.1234500000",
				"-1234567890",
				"12345678901234567890123456789012345678901234567890123456789012345678901234567890",
				"-12345678901234567890.1234567890000000000000000000000000000000000000000000000000000000",
				"0.12345678901234567890123456789012345678901234567890123456789000000000000000000000000000000000000000000000000000000000000000000000",
				"-0.1234567890"
#else
				".12345678901234567899000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
				"12345678.1234500000",
				"-1234567890",
				"12345678901234567890123456789012345678901234567890123456789012345678901234567890",
				"-12345678901234567890.1234567890000000000000000000000000000000000000000000000000000000",
				".12345678901234567890123456789012345678901234567890123456789000000000000000000000000000000000000000000000000000000000000000000000",
				"-.1234567890"
#endif		
			}
		},
		{10,"--",
			{"0.12345678901234567890",
			 "123.456789",
			 "1234567890",
			 "1234.567890",
			 "0.123456789",
			 "12345.6789012345",
			 "123456789012345600",
			 "123456789.012345600",
			 "0.123456789012345678",
			 "12.12345678901234567890"},
			"--",
			{
#ifndef _WM
				"0.12345678901234567890000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
				"123.456780",
				"1234567899",
				"1234.567899",
				"0.1234567890",
				"1234.6789012345",
				"1234567890123456",
				"12345678.012345600",
				"0.123456789012345670",
				"12.12345678901234567800"
#else
				".12345678901234567890000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
				"123.456780",
				"1234567899",
				"1234.567899",
				".1234567890",
				"1234.6789012345",
				"1234567890123456",
				"12345678.012345600",
				".123456789012345670",
				"12.12345678901234567800"
#endif
			}
		},
        {6, "--",	
               {ld_input,ld_input_half,ld_input,ld_input_half,datastr2,datastr2}, "--", 
               {ld_input,datastr3,datastr3,datastr3,datastr3,datastr3}
        },
        {6, "--",	
               {ld_input,ld_input_half,ld_input,ld_input_half,datastr2,datastr2}, "--", 
               {ld_output,ld_output_half,datastr4,ld_output_half,datastr4,datastr2}
        },
        {6, "--",	
               {ld_input,ld_input_half,ld_input,ld_input_half,datastr2,datastr2}, "--", 
               {ld_output,datastr3,ld_output,datastr3,datastr2,datastr3}
        },
		{
			9999,
		}
	};

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("LargeBlock", charset_file);
	if (var_list == NULL) return FAILED;

	DrpTable = var_mapping("LargeBlock_DrpTable", var_list);
	CrtTable = var_mapping("LargeBlock_CrtTable", var_list);
	InsTable = var_mapping("LargeBlock_InsTable", var_list);
	SelTable = var_mapping("LargeBlock_SelTable", var_list);
	UpdTable = var_mapping("LargeBlock_UpdTable", var_list);
	DelTable = var_mapping("LargeBlock_DelTable", var_list);

	if(isUCS2) {
		sprintf(keysize, "%d", MAX_SIZE_KEY_UCS2);
	} else {
		sprintf(keysize, "%d", MAX_SIZE_KEY);
	}

    i = 0;
    while(dataTypesMatrix[i].size != 9999) {
        if((i==16 || i==17) && isUCS2) {
            sprintf(temp,"LargeBlock_dataTypesMatrix_cols_%d_UCS2", i);
            dataTypesMatrix[i].cols = var_mapping((char*)temp, var_list);
        } else {
            sprintf(temp,"LargeBlock_dataTypesMatrix_cols_%d", i);
            dataTypesMatrix[i].cols = var_mapping((char*)temp, var_list);
        }
        sprintf(temp,"LargeBlock_dataTypesMatrix_updatecols_%d", i);
        dataTypesMatrix[i].updatecols = var_mapping((char*)temp, var_list);
        i++;
    }

    whereClause = var_mapping("LargeBlock_UpdTable_w", var_list);

    sprintf(datastr1,"'%s'",var_mapping("LargeBlock_datastr1", var_list));
    sprintf(datastr2,"'%s'",var_mapping("LargeBlock_datastr2", var_list));
/*SEAQUSET    sprintf(datastr3,"'%s'",var_mapping("LargeBlock_datastr3", var_list)); */
    sprintf(datastr3,"%s",var_mapping("LargeBlock_datastr3", var_list));
    sprintf(datastr4,"'%s'",var_mapping("LargeBlock_datastr4", var_list));

//=============================================================================================================================
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing feature =>LargeBlock | LargeBlock | largeblock.cpp\n");
	TEST_INIT;

	TESTCASE_BEGIN("Setup for LargeBlock tests\n");
	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
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

	//Generate large data
	j=0;
	if(isUCS2) j = MAX_SIZE_KEY_UCS2;
	else       j = MAX_SIZE_KEY;
	ld_input[0] = '\'';
	for (i=0; i<j; i++) {
		ld_input[i+1] = (char)(i%10 + 48);
		ld_output[i] = (char)(i%10 + 48);
	}
	ld_input[i+1] = '\'';
	ld_input[i+2] = '\0';
	ld_output[i] = '\0';

    if(isUCS2) {
        strncpy(ld_input_half,ld_input,i+3);
        strncpy(ld_output_half,ld_output,i+1);
    } else {
        strncpy(ld_input_half,ld_input,MAX_SIZE_KEY_UCS2+1);
        ld_input_half[MAX_SIZE_KEY_UCS2+1] = '\'';
        ld_input_half[MAX_SIZE_KEY_UCS2+2] = '\0';
        strncpy(ld_output_half,ld_output,MAX_SIZE_KEY_UCS2);
        ld_output_half[MAX_SIZE_KEY_UCS2] = '\0';
    }

    //LogMsg(NONE,"String in is %s\n",ld_input_half);
    //LogMsg(NONE,"String out is %s\n",ld_output_half);

	TESTCASE_END; // end of setup

	i=0;
	while (dataTypesMatrix[i].size != 9999) {
		SQLExecDirect(hstmt, (SQLCHAR*)DrpTable,SQL_NTS); //clean up

		for (loop=0; loop<=PREPARE_EXEC_EXNENDEDFETCH; loop++) {
			if (loop == EXEC_DIRECT)
				sprintf(Heading,"Test %d.a Positive functionality of LargeBlock by doing ExecDirect\n",i+1);
			else if (loop == PREPARE_EXEC_FETCH)
				sprintf(Heading,"Test %d.b Positive functionality of LargeBlock by doing Prepare/Execute/Fetch\n",i+1);
			else 
				sprintf(Heading,"Test %d.c Positive functionality of LargeBlock by doing Prepare/Execute/ExtendedFetch\n",i+1);
            TESTCASE_BEGIN(Heading);

			//Create table
			sqlStmt = (char *)malloc((strlen(CrtTable)+strlen(dataTypesMatrix[i].cols)+100)*sizeof(char));
			if (sqlStmt == NULL) {
				LogMsg(ERRMSG,"Error on malloc memory!");
				TEST_FAILED;
				TEST_RETURN;
			}
			sprintf(sqlStmt, "%s %s", CrtTable, dataTypesMatrix[i].cols);
			replace_str(sqlStmt,(char*)"$$$$",keysize);
            sprintf(temp,"%d",MAX_SIZE_KEY_UCS2);
            replace_str(sqlStmt,(char*)"****",temp);

			if (loop ==  EXEC_DIRECT) {
				returncode = SQLExecDirect(hstmt, (SQLCHAR*)sqlStmt,SQL_NTS);
                if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")) {
                    LogMsg(NONE,"The string is: %s\n",sqlStmt);
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }
			}
			else {
				returncode = SQLPrepare(hstmt, (SQLCHAR*)sqlStmt,SQL_NTS);
                if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")) {
                    LogMsg(NONE,"The string is: %s\n",sqlStmt);
					TEST_FAILED;
                    LogAllErrors(henv,hdbc,hstmt);
                }
				returncode = SQLExecute(hstmt);			
                if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")) {
                    LogMsg(NONE,"The string is: %s\n",sqlStmt);
					TEST_FAILED;
                    LogAllErrors(henv,hdbc,hstmt);
                }
			}
			free(sqlStmt);

			/**********************************************************************************/
			//Insert table
			if (dataTypesMatrix[i].size != 1) {
				for (j=0; j<dataTypesMatrix[i].size; j++) {
					totalLen += strlen(dataTypesMatrix[i].input[j]);
				}
				sqlStmt = (char *)malloc((strlen(InsTable)+totalLen+100)*sizeof(char));
				if (sqlStmt == NULL) {
					LogMsg(ERRMSG,"Error on malloc memory!");
					TEST_FAILED;
					TEST_RETURN;
				}
				sprintf(sqlStmt, "%s ( ", InsTable);
				for (j=0; j<dataTypesMatrix[i].size; j++) {
                    strcat(sqlStmt,dataTypesMatrix[i].input[j]);
                    if (j<dataTypesMatrix[i].size-1) {
						strcat(sqlStmt,",");
                        if(i>= 30 && i <= 32 && (j == 0 || j == 2 || j == 4))
                            strcat (sqlStmt,(char*)"_UCS2");
                    }
				}
				strcat(sqlStmt," )");
			}
			else {
				sqlStmt = (char *)malloc((strlen(InsTable)+strlen(dataTypesMatrix[i].input[0])+100)*sizeof(char));
				if (sqlStmt == NULL) {
					LogMsg(ERRMSG,"Error on malloc memory!");
					TEST_FAILED;
					TEST_RETURN;
				}
				sprintf(sqlStmt, "%s ( %s )", InsTable, dataTypesMatrix[i].input[0]);
			}

			LogMsg(LINEBEFORE,"INSERT ONTO TABLE ...\n");
			//LogMsg(LINEBEFORE,"%s\n", sqlStmt);
			if (loop ==  EXEC_DIRECT) {
				returncode = SQLExecDirect(hstmt, (SQLCHAR*)sqlStmt,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
                    LogMsg(NONE,"The string is: %s\n",sqlStmt);
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }
			}
			else {
				returncode = SQLPrepare(hstmt, (SQLCHAR*)sqlStmt,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
                    LogMsg(NONE,"The string is: %s\n",sqlStmt);
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }
				returncode = SQLExecute(hstmt);			
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
                    LogMsg(NONE,"The string is: %s\n",sqlStmt);
					LogMsg(ERRMSG,"SQLExecute. Expected: SQL_SUCCESS, actual: %d at line %d\n", returncode, __LINE__);
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
			}
			free(sqlStmt);

			/**********************************************************************************/
			//Update table
			sqlStmt = (char *)malloc((strlen(UpdTable)+strlen(dataTypesMatrix[i].updatecols)
									+strlen(dataTypesMatrix[i].input[0])+100)*sizeof(char));
			if (sqlStmt == NULL) {
				LogMsg(ERRMSG,"Error on malloc memory!");
				TEST_FAILED;
				TEST_RETURN;
			}
			sprintf(sqlStmt, "%s %s %s%s", UpdTable, dataTypesMatrix[i].updatecols, whereClause, dataTypesMatrix[i].input[0]);
			LogMsg(LINEBEFORE,"UPDATE TABLE ...\n");
			//LogMsg(LINEBEFORE,"%s\n", sqlStmt);

			if (loop ==  EXEC_DIRECT) {
				returncode = SQLExecDirect(hstmt, (SQLCHAR*)sqlStmt,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
                    LogMsg(NONE,"The string is: %s\n",sqlStmt);
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }
			}
			else {
				returncode = SQLPrepare(hstmt, (SQLCHAR*)sqlStmt,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
                    LogMsg(NONE,"The string is: %s\n",sqlStmt);
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }

				returncode = SQLExecute(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
                    LogMsg(NONE,"The string is: %s\n",sqlStmt);
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }
			}

			free(sqlStmt);
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);

			/**********************************************************************************/
			//Select table using different types of APIs
			if (loop != PREPARE_EXEC_EXNENDEDFETCH)
			{
				if (loop ==  EXEC_DIRECT) {
					LogMsg(LINEBEFORE,"Using EXEC_DIRECT, Test id=%d\n", i+1);
					returncode = SQLExecDirect(hstmt, (SQLCHAR*)SelTable,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
                        LogMsg(NONE,"The string is: %s\n",sqlStmt);
                        LogAllErrors(henv,hdbc,hstmt);				
                        TEST_FAILED;
                    }
				}
				else {
					LogMsg(LINEBEFORE,"Using PREPARE_EXEC, Test id=%d\n", i+1);
					returncode = SQLPrepare(hstmt, (SQLCHAR*)SelTable,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
                        LogMsg(NONE,"The string is: %s\n",sqlStmt);
                        LogAllErrors(henv,hdbc,hstmt);				
                        TEST_FAILED;
                    }

					returncode = SQLExecute(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
                        LogMsg(NONE,"The string is: %s\n",sqlStmt);
                        LogAllErrors(henv,hdbc,hstmt);				
                        TEST_FAILED;
                    }
				}

                //LogMsg(LINEBEFORE,"%s\n", SelTable);

				returncode = SQLFetch(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")){
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }

				if (returncode == SQL_SUCCESS_WITH_INFO) {
					LogAllErrors(henv,hdbc,hstmt);
				}

				failed = false;
				for (j = 0; j < dataTypesMatrix[i].size; j++)
				{  
					returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR, outValue, MAX_SIZE_KEY+1,&OutConnStrLen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						failed = true;
					}
					else
					{
						if (strcmp(dataTypesMatrix[i].output[j],outValue) != 0)
						{
                            if((strncmp(dataTypesMatrix[i].output[j],outValue,sizeof(dataTypesMatrix[i].output[j])) != 0) &&
                               (cstrcmp(dataTypesMatrix[i].output[j],outValue,FALSE,TRUE) != 0)) {
							        failed = true;
                                    LogMsg(ERRMSG,"expect: %s and actual: %s values of column %d are not matched at %d\n",dataTypesMatrix[i].output[j],outValue, j+1,__LINE__);
							} else {
                                //LogMsg(NONE,"expect: %s and actual: %s values of column %d\n",dataTypesMatrix[i].output[j],outValue);
                            }
						}
						else
						{
							//LogMsg(NONE,"expect: %s and actual: %s values of column %d are matched\n", dataTypesMatrix[i].output[j],outValue,j+1);
						}
					}
				}

				if (failed) {
					TEST_FAILED;
				}
			}
			else {
				SQLSetStmtOption(hstmt, SQL_CONCURRENCY, SQL_CONCUR_READ_ONLY);
				SQLSetStmtOption(hstmt, SQL_CURSOR_TYPE, SQL_CURSOR_FORWARD_ONLY);
				SQLSetStmtOption(hstmt, SQL_ROWSET_SIZE, 1);
				SQLSetStmtOption(hstmt, SQL_BIND_TYPE, sizeof(aRow));

				// Bind the parameters in row-wise fashion.
				for (j=0; j<dataTypesMatrix[i].size; j++) {
					returncode = SQLBindCol(hstmt, j+1, SQL_C_CHAR, &aRow.A[j], MAX_SIZE_KEY+1, &aRow.AInd[j]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
						TEST_FAILED;
				}

				// Execute the select statement.
				LogMsg(LINEBEFORE,"Using PREPARE_EXEC_EXNENDEDFETCH, Test id=%d\n", i+1);
				returncode = SQLExecDirect(hstmt, (SQLCHAR*)SelTable,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }

				returncode = SQL_SUCCESS;
				while (returncode != SQL_NO_DATA_FOUND || returncode == SQL_ERROR)
				{
					returncode = SQLExtendedFetch(hstmt, SQL_FETCH_NEXT, 1, &FetchProcessed, &FetchStatus);
					if (returncode == SQL_ERROR)
					{
                        LogMsg(ERRMSG,"SQLExtendedFetch, select table: %s\n",SelTable);
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
					if (returncode == SQL_NO_DATA_FOUND || returncode == SQL_ERROR) break;

					//Check to see which sets of parameters were processed successfully.
					for (k = 0; k < (int)FetchProcessed; k++) 
					{
						returncode = SQLSetPos(hstmt, k+1, SQL_POSITION, SQL_LOCK_UNLOCK);
						if (returncode == SQL_ERROR)
						{
							LogMsg(ERRMSG,"SQLSetPos, expected SQL_SUCCESS, actual : %d\n", returncode);
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
						}
					
						if (FetchStatus == SQL_ROW_SUCCESS || FetchStatus == SQL_ROW_SUCCESS_WITH_INFO) 
						{
							failed = false;
							for (j=0; j<dataTypesMatrix[i].size; j++) {
								if (aRow.AInd[j] == SQL_NULL_DATA) {
									LogMsg(ERRMSG,"Col SQL_NULL_DATA\n");
									failed = true;
									continue;
								}

								if (strcmp(dataTypesMatrix[i].output[j],aRow.A[j]) != 0)
								{
                                    if((strncmp(dataTypesMatrix[i].output[j],aRow.A[j],sizeof(dataTypesMatrix[i].output[j])) != 0) &&
                                       (cstrcmp(dataTypesMatrix[i].output[j],aRow.A[j],FALSE,TRUE) != 0)) {
							            failed = true;
							            LogMsg(ERRMSG,"expect: %s and actual: %s values of column %d are not matched at %d\n",dataTypesMatrix[i].output[j],aRow.A[j], j+1,__LINE__);
                                    } else {
                                        //LogMsg(NONE,"expect: %s and actual: %s values of column %d\n",dataTypesMatrix[i].output[j],aRow.A[j]);
                                    }
								}
								else
								{
									//LogMsg(NONE,"expect: %s and actual: %s values of column %d are matched\n", dataTypesMatrix[i].output[j],aRow.A[j],j+1);
								}
							}

							if (failed) {
								TEST_FAILED;
							}
						}
					}//End For loop
				}//End while loop
			}//End else
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);

			/**********************************************************************************/
			//Delete a row using Prepare/Execute
			sqlStmt = (char *)malloc((strlen(DelTable)+strlen(dataTypesMatrix[i].input[0])+100)*sizeof(char));
			if (sqlStmt == NULL) {
				LogMsg(ERRMSG,"Error on malloc memory!");
				TEST_FAILED;
				TEST_RETURN;
			}
			sprintf(sqlStmt, "%s", DelTable);
			strcat(sqlStmt,dataTypesMatrix[i].input[0]);

			LogMsg(LINEBEFORE,"DELETE FROM TABLE ...\n");
			//LogMsg(LINEBEFORE,"%s\n", sqlStmt);
			if (loop ==  EXEC_DIRECT) {
				returncode = SQLExecDirect(hstmt, (SQLCHAR*)sqlStmt,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }
			}
			else {
				returncode = SQLPrepare(hstmt, (SQLCHAR*)sqlStmt,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }

				returncode = SQLExecute(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }
			}
			free(sqlStmt);
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);

			/**********************************************************************************/
			//Drop table
			//LogMsg(LINEBEFORE,"%s\n", DrpTable);
			if (loop ==  EXEC_DIRECT) {
				returncode = SQLExecDirect(hstmt, (SQLCHAR*)DrpTable,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }
			}
			else {
				returncode = SQLPrepare(hstmt, (SQLCHAR*)DrpTable,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }

				returncode = SQLExecute(hstmt);			
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }
			}
            //LogMsg(LINEBEFORE,"%s\n", DrpTable);
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);
			TESTCASE_END;
		}//End for loop

		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLFreeStmt(hstmt,SQL_CLOSE);

		i++;
	}

//============================================================================================
	FullDisconnect3(pTestInfo);
	free_list(var_list);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => LargeBlock.\n");
	TEST_RETURN;
}
