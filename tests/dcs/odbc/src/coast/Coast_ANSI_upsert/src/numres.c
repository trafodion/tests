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

/*
---------------------------------------------------------
   TestSQLNumResultsCol
---------------------------------------------------------
*/
PassFail TestSQLNumResultCols(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
  	char			Heading[MAX_STRING_SIZE];
	RETCODE			returncode;
	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	SWORD			col;
	CHAR			*ExecDirStr[] = {"--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"};
	char			*TestCase[] = {
						"after preparing stmt ",
						"after preparing & executing stmt ",
						"after preparing, executing & fetching stmt ",
						"after execdirect stmt ",
						"after execdirect & fetching stmt ",
						"after preparing param stmt ",
						"after preparing & binding stmt ",
						"after preparing, binding & executing stmt ",
						"after preparing, binding, executing & fetching stmt "
					};
	int				lend = 9, iend = 5;
	SQLUSMALLINT	i = 0, l = 0;
	int				expcol[] = {1,2,6,9,2};
	SQLLEN			cbIn = SQL_NTS;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLNumResultCols", charset_file);
	if (var_list == NULL) return FAILED;

	ExecDirStr[0] = var_mapping("SQLNumResultCols_ExecDirStr_0", var_list);
	ExecDirStr[1] = var_mapping("SQLNumResultCols_ExecDirStr_1", var_list);
	ExecDirStr[2] = var_mapping("SQLNumResultCols_ExecDirStr_2", var_list);
	ExecDirStr[3] = var_mapping("SQLNumResultCols_ExecDirStr_3", var_list);
	ExecDirStr[4] = var_mapping("SQLNumResultCols_ExecDirStr_4", var_list);
	ExecDirStr[5] = var_mapping("SQLNumResultCols_ExecDirStr_5", var_list);
	ExecDirStr[6] = var_mapping("SQLNumResultCols_ExecDirStr_6", var_list);
	ExecDirStr[7] = var_mapping("SQLNumResultCols_ExecDirStr_7", var_list);
	ExecDirStr[8] = var_mapping("SQLNumResultCols_ExecDirStr_8", var_list);
	ExecDirStr[9] = var_mapping("SQLNumResultCols_ExecDirStr_9", var_list);
	ExecDirStr[10] = var_mapping("SQLNumResultCols_ExecDirStr_10", var_list);
	ExecDirStr[11] = var_mapping("SQLNumResultCols_ExecDirStr_11", var_list);
	ExecDirStr[12] = var_mapping("SQLNumResultCols_ExecDirStr_12", var_list);
	ExecDirStr[13] = var_mapping("SQLNumResultCols_ExecDirStr_13", var_list);
	ExecDirStr[14] = var_mapping("SQLNumResultCols_ExecDirStr_14", var_list);
	ExecDirStr[15] = var_mapping("SQLNumResultCols_ExecDirStr_15", var_list);
	ExecDirStr[16] = var_mapping("SQLNumResultCols_ExecDirStr_16", var_list);
	ExecDirStr[17] = var_mapping("SQLNumResultCols_ExecDirStr_17", var_list);
	ExecDirStr[18] = var_mapping("SQLNumResultCols_ExecDirStr_18", var_list);
	ExecDirStr[19] = var_mapping("SQLNumResultCols_ExecDirStr_19", var_list);

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLNumResultcols | SQLNumResultCols | numres.c\n");

	TEST_INIT;
	   
	TESTCASE_BEGIN("Setup for SQLNumResultCols tests\n");

	if(!FullConnect(pTestInfo)){
		LogMsg(NONE,"Unable to connect\n");
		TEST_FAILED;
		TEST_RETURN;
		}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}
	TESTCASE_END; // end of setup

	for (l = 0; l < lend; l++){
		for (i = 0; i < iend; i++){
			//==================================================================================
			sprintf(Heading,"Test Positive Functionality of SQLNumResultCols ");
			strcat(Heading, TestCase[l]);
			strcat(Heading, ExecDirStr[i+iend+iend+iend]);
			strcat(Heading, "\n");
			TESTCASE_BEGIN(Heading);
			if ((i != (iend-1)) && (l < 5)){
				SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i],SQL_NTS); /* cleanup */
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend],SQL_NTS); /* create table */
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					}
				else{
					returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend],SQL_NTS); /* insert into table */
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
						}
					else{
						switch( l ) {
							case 0:
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
									}
								break;
							case 1 :
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
									}
								else{
									returncode = SQLExecute(hstmt);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
										}
									}
								break;
							case 2 :
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
									}
								else{
									returncode = SQLExecute(hstmt);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
										}
									else{
										returncode = SQLFetch(hstmt);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")){
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
											}
										}
									}
								break;
							case 3 :
								returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
									}
								break;
							case 4 :
								returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
									}
								else{
									returncode = SQLFetch(hstmt);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")){
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
										}
									}
								break;
							}
						if (returncode == SQL_SUCCESS){
							returncode = SQLNumResultCols(hstmt, &col);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultCols")){
								LogAllErrors(henv,hdbc,hstmt);
								TEST_FAILED;
								}
							if (col == expcol[i])
								{
									LogMsg(NONE,"expect: %d and actual: %d are matched\n",expcol[i], col);
								}	
							else
								{
									TEST_FAILED;	
									LogMsg(NONE,"expect: %d and actual: %d are not matched\n",expcol[i], col);
								}
							}
							SQLFreeStmt(hstmt,SQL_CLOSE);
							SQLExecDirect(hstmt,(SQLCHAR*) ExecDirStr[i],SQL_NTS); /* cleanup */
						}
					}
				}
			else if ((i == (iend-1)) && (l >= 5)){
				SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i],SQL_NTS); /* cleanup */
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend],SQL_NTS); /* create table */
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					}
				else{
					returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend],SQL_NTS); /* insert into table */
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
						}
					else{
						switch( l ){
							case 5 :
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
									}
								break;
							case 6 :
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
									}
								else{
									returncode = SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_CHAR,SQL_INTEGER,0,0,(SQLPOINTER)"10",300,&cbIn);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindparameter")){
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
										}
									else{
										returncode = SQLBindParameter(hstmt,2,SQL_PARAM_INPUT,SQL_C_CHAR,SQL_INTEGER,0,0,(SQLPOINTER)"20",300,&cbIn);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter")){
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
											}
										}
									}
								break;
							case 7 :
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
									}
								else{
									returncode = SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_CHAR,SQL_INTEGER,0,0,(SQLPOINTER)"10",300,&cbIn);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindparameter")){
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
										}
									else{
										returncode = SQLBindParameter(hstmt,2,SQL_PARAM_INPUT,SQL_C_CHAR,SQL_INTEGER,0,0,(SQLPOINTER)"20",300,&cbIn);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter")){
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
											}
										else{
											returncode = SQLExecute(hstmt);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
												}
											}
										}
									}
								break;
						    case 8 :
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
									LogAllErrors(henv,hdbc,hstmt);
									TEST_FAILED;
									}
								else{
									returncode = SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_CHAR,SQL_INTEGER,0,0,(SQLPOINTER)"10",300,&cbIn);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindparameter")){
										LogAllErrors(henv,hdbc,hstmt);
										TEST_FAILED;
										}
									else{
										returncode = SQLBindParameter(hstmt,2,SQL_PARAM_INPUT,SQL_C_CHAR,SQL_INTEGER,0,0,(SQLPOINTER)"20",300,&cbIn);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter")){
											LogAllErrors(henv,hdbc,hstmt);
											TEST_FAILED;
											}
										else{
											returncode = SQLExecute(hstmt);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
												LogAllErrors(henv,hdbc,hstmt);
												TEST_FAILED;
												}
											else{
												returncode = SQLFetch(hstmt);
												if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")){
													LogAllErrors(henv,hdbc,hstmt);
													TEST_FAILED;
													}
												}
											}
										}
									}
								break;
							}
						if (returncode == SQL_SUCCESS){
								returncode = SQLNumResultCols(hstmt, &col);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultCols"))
								{
									TEST_FAILED;
									LogAllErrors(henv,hdbc,hstmt);
								}
								if (col == expcol[i])
								{
									LogMsg(NONE,"expect: %d and actual: %d are matched\n",expcol[i], col);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(NONE,"expect: %d and actual: %d are not matched\n",expcol[i], col);
								}
							}
							SQLFreeStmt(hstmt,SQL_CLOSE);
							SQLExecDirect(hstmt,(SQLCHAR*) ExecDirStr[i],SQL_NTS); /* cleanup */
						}
					}
				}
			TESTCASE_END;
			} /* iend loop */
		} /* lend loop */
	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLNumResultcols.\n");
	free_list(var_list);
	TEST_RETURN;
}
