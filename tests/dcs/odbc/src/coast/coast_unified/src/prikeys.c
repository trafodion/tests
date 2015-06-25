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

#define NAME_LEN				300
#define NUM_OUTPUTS_PK	6

/*
---------------------------------------------------------
   TestSQLPrimaryKeys
---------------------------------------------------------
*/
PassFail TestSQLPrimaryKeys(TestInfo *pTestInfo, int MX_MP_SPECIFIC)
{                  
	TEST_DECLARE;
 	TCHAR			Heading[MAX_HEADING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	TCHAR			TQualifier[NAME_LEN],TOwner[NAME_LEN],TName[NAME_LEN];
	TCHAR			*Output[NUM_OUTPUTS_PK],*Results[NUM_OUTPUTS_PK];
	SQLLEN			OutputLen[NUM_OUTPUTS_PK] = {NAME_LEN,NAME_LEN,NAME_LEN,NAME_LEN,NAME_LEN,NAME_LEN};

	struct
	{
		TCHAR			*ColName;
		TCHAR			*ColType;
	} Columns[] = {
							{_T("--"),_T(" char(10) CHARACTER SET ISO88591")},
							{_T("--"),_T(" varchar(10) CHARACTER SET ISO88591")},
							{_T("--"),_T(" long varchar(10) CHARACTER SET ISO88591")},
							{_T("--"),_T(" char(10) CHARACTER SET UCS2")},
							{_T("--"),_T(" varchar(10) CHARACTER SET UCS2")},
							{_T("--"),_T(" long varchar(10) CHARACTER SET UCS2")},
							{_T("--"),_T(" char(10) CHARACTER SET UTF8")},
							{_T("--"),_T(" varchar(10) CHARACTER SET UTF8")},
							{_T("--"),_T(" long varchar(10) CHARACTER SET UTF8")},
							{_T("--"),_T(" decimal(10,5)")},
							{_T("--"),_T(" numeric(10,5)")},
							{_T("--"),_T(" numeric(19,0)")},			//for bignum
							{_T("--"),_T(" numeric(19,6)")},			//for bignum
							{_T("--"),_T(" numeric(128,0)")},			//for bignum
							{_T("--"),_T(" numeric(128,128)")},			//for bignum
							{_T("--"),_T(" numeric(127,64)")},		//for bignum
							{_T("--"),_T(" numeric(10,5) unsigned")},	//for bignum
							{_T("--"),_T(" numeric(18,5) unsigned")},	//for bignum
							{_T("--"),_T(" numeric(30,10) unsigned")},	//for bignum
							{_T("--"),_T(" smallint")},
							{_T("--"),_T(" integer")},
							{_T("--"),_T(" bigint")},
							{_T("--"),_T(" date")},
							{_T("--"),_T(" time")},
							{_T("--"),_T(" timestamp")},
							{_T("--"),_T(" bit")},	// loops ends here for MX since ity doesn't support this datatypes.
							{_T("--"),_T(" tinyint")},
							{_T("--"),_T(" binary(10)")},
							{_T("--"),_T(" varbinary(10)")},
							{_T("--"),_T("endloop")}
						};

	TCHAR			*TableStr[3];

	TCHAR			ColStr[MAX_NOS_SIZE], KeyStr[MAX_NOS_SIZE], CreateTbl[MAX_NOS_SIZE],END_LOOP[10];
	int				i = 0, j = 0, k = 0;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLPrimaryKeys"), charset_file);
	if (var_list == NULL) return FAILED;

	Columns[0].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_1"), var_list);
	Columns[1].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_2"), var_list);
	Columns[2].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_3"), var_list);
	Columns[3].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_4"), var_list);
	Columns[4].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_5"), var_list);
	Columns[5].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_6"), var_list);
	Columns[6].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_7"), var_list);
	Columns[7].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_8"), var_list);
	Columns[8].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_9"), var_list);
	Columns[9].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_10"), var_list);
	Columns[10].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_11"), var_list);
	Columns[11].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_12"), var_list);
	Columns[12].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_13"), var_list);
	Columns[13].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_14"), var_list);
	Columns[14].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_15"), var_list);
	Columns[15].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_16"), var_list);
	Columns[16].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_17"), var_list);
	Columns[17].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_18"), var_list);
	Columns[18].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_19"), var_list);
	Columns[19].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_20"), var_list);
	Columns[20].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_21"), var_list);
	Columns[21].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_22"), var_list);
	Columns[22].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_23"), var_list);
	Columns[23].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_24"), var_list);
	Columns[24].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_25"), var_list);
	Columns[25].ColName = var_mapping(_T("SQLPrimaryKeys_Columns_26"), var_list);

	TableStr[0] = var_mapping(_T("SQLPrimaryKeys_TableStr_1"), var_list);
	TableStr[1] = var_mapping(_T("SQLPrimaryKeys_TableStr_2"), var_list);
	TableStr[2] = var_mapping(_T("SQLPrimaryKeys_TableStr_3"), var_list);

//========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => MX Specific SQLPrimaryKeys.\n"));
	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLPrimaryKeys tests\n");
	if(!FullConnect(pTestInfo))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
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
	TESTCASE_END;	//end of setup

	_tcscpy(ColStr,_T(""));
	_tcscpy(KeyStr,_T(""));
	_tcscpy(END_LOOP,_T(""));

	Results[0] = (TCHAR *)malloc(NAME_LEN);
	_tcscpy(Results[0],pTestInfo->Catalog);		
	Results[1] = (TCHAR *)malloc(NAME_LEN);
	_tcscpy(Results[1],pTestInfo->Schema);
	Results[2] = (TCHAR *)malloc(NAME_LEN);
	_tcscpy(Results[2],TableStr[2]);
	Results[3] = (TCHAR *)malloc(NAME_LEN);
	_tcscpy(Results[3],_T(""));
	Results[4] = (TCHAR *)malloc(NAME_LEN);
	_tcscpy(Results[4],_T(""));
	Results[5] = (TCHAR *)malloc(NAME_LEN);
	_tcscpy(Results[5],TableStr[2]);
	_tcscpy(END_LOOP,_T(" bit"));			// needs a space to match
	_tcscpy(TQualifier,Results[0]);
	_tcscpy(TOwner,Results[1]);
	_tcscpy(TName,Results[2]);
	
	while (_tcsicmp(Columns[i].ColType,END_LOOP) != 0)
	{
		SQLExecDirect(hstmt,(SQLTCHAR*) (SQLTCHAR *)TableStr[1],SQL_NTS);
		if (i > 0)
		{
			_tcscat(ColStr,_T(","));
			_tcscat(KeyStr,_T(","));
		}
		_tcscat(ColStr,Columns[i].ColName);
		_tcscat(ColStr,Columns[i].ColType);
		_tcscat(ColStr,_T(" not null"));
		_tcscat(KeyStr,Columns[i].ColName);
		_tcscpy(CreateTbl,_T(""));
		_tcscat(CreateTbl,TableStr[0]);
		_tcscat(CreateTbl,_T("("));
		_tcscat(CreateTbl,ColStr);
		_tcscat(CreateTbl,_T(", primary key("));
		_tcscat(CreateTbl,KeyStr);
		_tcscat(CreateTbl,_T("))"));

		_stprintf(Heading,_T("Test Positive Functionality of SQLPrimaryKeys for "));
		_tcscat(Heading,CreateTbl);
		_tcscat(Heading,_T("\n"));
		TESTCASE_BEGINW(Heading);

		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CreateTbl,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		else
		{
			LogMsg(NONE,_T("SQLPrimaryKeys: create table with primary key %s\n"),KeyStr);
			if (_tcslen(TQualifier) > 0)
				returncode = SQLPrimaryKeys(hstmt,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TName,(SWORD)_tcslen(TName));
			else
				returncode = SQLPrimaryKeys(hstmt,NULL,0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TName,(SWORD)_tcslen(TName));
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrimaryKeys"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				for (j = 0; j < NUM_OUTPUTS_PK-1; j++)
				{
					Output[j] = (TCHAR *)malloc(NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(j+1),SQL_C_TCHAR,Output[j],NAME_LEN,&OutputLen[j]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
				}
				k = 0;
				while (returncode == SQL_SUCCESS)
				{
					returncode = SQLFetch(hstmt);
					if((returncode!=SQL_NO_DATA_FOUND) &&(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						if (returncode == SQL_SUCCESS)
						{
							LogMsg(NONE,_T("Comparing results\n"));
							for (j = 0; j < NUM_OUTPUTS_PK-1; j++)
							{
								if (j == 3)
								{
									if (MX_MP_SPECIFIC == MX_SPECIFIC)
										if (cwcscmp(Output[j],Columns[k].ColName,TRUE) != 0)
										{
											TEST_FAILED;	
											LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched\n"),Columns[k].ColName,Output[j]);
										}
								}
								else if (j == 4)
								{
									_itot(k+1,Results[j],10);
									if (_tcsicmp(Output[j],Results[j]) != 0)
									{
										TEST_FAILED;	
										LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched\n"),Results[j],Output[j]);
									}
								}
								else
								{
									//if (!(_tcscmp(Results[j], _T("TRAFODION"))))
									if (!(_tcscmp(Results[j], _T("TRAFODION"))))
									{
										if (_tcsicmp(Output[j],Results[j]) != 0)
										{
											TEST_FAILED;	
											LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched\n"),Results[j],Output[j]);
										}
									}
								}
							}
						}
					}
					if (returncode == SQL_SUCCESS) 
						k++;
				}
				for (j = 0; j < NUM_OUTPUTS_PK-1; j++)free(Output[j]);
				if(k == 0)
				{
					TEST_FAILED;
					LogMsg(ERRMSG,_T("No Data Found => Atleast one row should be fetched\n"));
				}
			}
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);
		}
		SQLExecDirect(hstmt,(SQLTCHAR*)(SQLTCHAR *)TableStr[1],SQL_NTS);
		i++;
		TESTCASE_END;
	}
	_tcscpy(ColStr,_T(""));
	_tcscpy(KeyStr,_T(""));
	_tcscpy(CreateTbl,_T(""));
	for (j = 0; j < NUM_OUTPUTS_PK; j++)
	{
		free(Results[j]);
	}

//========================================================================================================

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLPrimaryKeys.\n"));

	free_list(var_list);

	TEST_RETURN;
}
