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

#define NAME_LEN		300
#define NUM_OUTPUTS_PK	14

/*
---------------------------------------------------------
   TestSQLForeignKeys
---------------------------------------------------------
*/
PassFail TestMXSQLForeignKeys(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
 	TCHAR				Heading[MAX_HEADING_SIZE];
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	TCHAR				TQualifier[NAME_LEN],TOwner[NAME_LEN];
	TCHAR				*Output[NUM_OUTPUTS_PK],*Results[NUM_OUTPUTS_PK];
	SQLLEN				OutputLen[NUM_OUTPUTS_PK] = {NAME_LEN,NAME_LEN,NAME_LEN,NAME_LEN,NAME_LEN,NAME_LEN}; 
    int failedFlag = 0;

	TCHAR	*ColType[] = {_T(" char(10) CHARACTER SET ucs2"),
						_T(" varchar(10) CHARACTER SET ucs2"),
						_T(" long varchar(10) CHARACTER SET ucs2"),
						_T(" char(10) CHARACTER SET UCS2"),
						_T(" varchar(10) CHARACTER SET UCS2"),
						_T(" long varchar(10) CHARACTER SET UCS2"),
						_T(" decimal(10,5)"),
						_T(" numeric(10,5)"),
						_T(" numeric(19,0)"),						//for bignum
						_T(" numeric(19,6)"),						//for bignum
						_T(" numeric(128,0)"),						//for bignum
						_T(" numeric(128,128)"),					//for bignum
						_T(" numeric(127,64)"),						//for bignum
						_T(" numeric(10,5) unsigned"),				//for bignum
						_T(" numeric(18,5) unsigned"),				//for bignum
						_T(" numeric(30,10) unsigned"),				//for bignum
						_T(" smallint"),
						_T(" integer"),
						_T(" bigint"),
						_T(" date"),
						_T(" time"),
						_T(" timestamp"),
						_T(" bit"),		// loops ends here for MX since it doesn't support this datatypes.
						_T(" tinyint"),
						_T(" binary(10)"),
						_T(" varbinary(10)"),
						_T("endloop")
					};

	TCHAR	*ColName[6];
	TCHAR	*TableNames[] = {_T(""),_T(""),_T(""),_T("endloop")};
	TCHAR	*keyName;
	
	TCHAR	ColStr[MAX_NOS_SIZE], KeyStr[MAX_NOS_SIZE], CreateTbl[MAX_NOS_SIZE],END_LOOP[10];
	int	i = 0, j = 0, k = 0, l = 0, m = 0;

	struct {
		TCHAR tab1[NAME_LEN];
		TCHAR tab2[NAME_LEN];
	} displayBuf; 

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLForeignKeys"), charset_file);
	if (var_list == NULL) return FAILED;

	//print_list(var_list);
	ColName[0] = var_mapping(_T("SQLForeignKeys_ColName_1"), var_list);
	ColName[1] = var_mapping(_T("SQLForeignKeys_ColName_2"), var_list);
	ColName[2] = var_mapping(_T("SQLForeignKeys_ColName_3"), var_list);
	ColName[3] = var_mapping(_T("SQLForeignKeys_ColName_4"), var_list);
	ColName[4] = var_mapping(_T("SQLForeignKeys_ColName_5"), var_list);
	ColName[5] = var_mapping(_T("SQLForeignKeys_ColName_6"), var_list);

	TableNames[0] = var_mapping(_T("SQLForeignKeys_TableNames_1"), var_list);
	TableNames[1] = var_mapping(_T("SQLForeignKeys_TableNames_2"), var_list);
	TableNames[2] = var_mapping(_T("SQLForeignKeys_TableNames_3"), var_list);

	keyName = var_mapping(_T("SQLForeignKeys_keyName_1"), var_list);
//========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => MX Specific SQLForeignKeys.\n"));
	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLForeignKeys tests\n");
	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
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
	_tcscpy(END_LOOP,_T("endloop"));

	for (j = 0; j < NUM_OUTPUTS_PK; j++)
	{
		Results[j] = (TCHAR *)malloc(NAME_LEN);
	}
	_tcscpy(Results[0],pTestInfo->Catalog);		
	_tcscpy(Results[1],pTestInfo->Schema);
	_tcscpy(Results[4],pTestInfo->Catalog);		
	_tcscpy(Results[5],pTestInfo->Schema);
	_tcscpy(Results[9],_T("3"));		
	_tcscpy(Results[10],_T("3"));
	_tcscpy(Results[11],keyName);		
	_tcscpy(Results[12],keyName);
	_tcscpy(Results[13],_T("7"));
	_tcscpy(TQualifier,Results[0]);
	_tcscpy(TOwner,Results[1]);
	
	while (_tcsicmp(ColType[i],END_LOOP) != 0)
	{
		_stprintf(Heading,_T("Test Positive Functionality of SQLForeignKeys\n"));
		TESTCASE_BEGINW(Heading);
		j = 0;
		l = 0;
		while (_tcsicmp(TableNames[j],END_LOOP) != 0)
		{
			CreateTbl[0] = '\0';
			_stprintf(CreateTbl,_T("drop table %s cascade"),TableNames[j]);
			SQLExecDirect(hstmt,(SQLTCHAR*) CreateTbl,SQL_NTS);
			j++;
		}
		j = 0;
		while (_tcsicmp(TableNames[j],END_LOOP) != 0)
		{
			CreateTbl[0] = '\0';
			switch (j)
			{
				case 0:
                    // The  NO PARTITION is to help speed up this test on clustered systems with POS turned on.
					_stprintf(CreateTbl,_T("create table %s (%s %s not null not droppable, %s %s, primary key(%s)) NO PARTITION"),
							TableNames[j], ColName[0], ColType[i], ColName[1], ColType[i], ColName[0]);
					break;
				case 1:
                    // The  NO PARTITION is to help speed up this test on clustered systems with POS turned on.
					_stprintf(CreateTbl,_T("create table %s (%s %s not null not droppable, %s %s, primary key(%s), foreign key (%s) references %s(%s)) NO PARTITION"),
							TableNames[j], ColName[2], ColType[i], ColName[3], ColType[i], ColName[2], ColName[3], TableNames[j-1], ColName[0]);
					break;
				case 2:
                    // The  NO PARTITION is to help speed up this test on clustered systems with POS turned on.
					_stprintf(CreateTbl,_T("create table %s (%s %s not null not droppable, %s %s, primary key(%s), foreign key (%s) references %s(%s)) NO PARTITION"),
							TableNames[j], ColName[4], ColType[i], ColName[5], ColType[i], ColName[4], ColName[5], TableNames[j-1], ColName[2]);
					break;
			}

			LogMsg(NONE, _T("%s\n"), CreateTbl);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CreateTbl,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
                if(!failedFlag) // We only want to report 1 failure.
				    TEST_FAILED;
                failedFlag = 1;
				l = 1;
				break;
			}
			j++;
		}
        
		if (l == 0)
		{
			for (m = 0; m < 5; m++)
			{
				TESTCASE_BEGIN("");
				switch (m)
				{
					case 0:
						if (_tcslen(TQualifier) == 0)
							returncode = SQLForeignKeys(hstmt,NULL,0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[0],(SWORD)_tcslen(TableNames[0]),NULL,0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),'\0',0);
						else
							returncode = SQLForeignKeys(hstmt,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[0],(SWORD)_tcslen(TableNames[0]),(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),'\0',0);
						_tcscpy(Results[2],TableNames[0]);
						_tcscpy(Results[3], ColName[0]);
						_tcscpy(Results[6],TableNames[1]);
						_tcscpy(Results[7], ColName[3]);
						LogMsg(NONE, _T("m:%d SQLForeignKeys(hstmt, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d)\n"), m,
										TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),TableNames[0],_tcslen(TableNames[0]),
										TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),_T("<empty>"),0);

						break;
					case 1:
						if (_tcslen(TQualifier) == 0)
							returncode = SQLForeignKeys(hstmt,NULL,0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[1],(SWORD)_tcslen(TableNames[1]),NULL,0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),'\0',0);
						else
							returncode = SQLForeignKeys(hstmt,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[1],(SWORD)_tcslen(TableNames[1]),(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),'\0',0);
						_tcscpy(Results[2],TableNames[1]);
						_tcscpy(Results[3], ColName[2]);
						_tcscpy(Results[6],TableNames[2]);
						_tcscpy(Results[7], ColName[5]);
						LogMsg(NONE, _T("m:%d SQLForeignKeys(hstmt, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d)\n"), m,
										TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),TableNames[1],_tcslen(TableNames[1]),
										TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),_T("<empty>"),0);
						break;
					case 2:
						if (_tcslen(TQualifier) == 0)
							returncode = SQLForeignKeys(hstmt,NULL,0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),'\0',0,NULL,0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[1],(SWORD)_tcslen(TableNames[1]));
						else
							returncode = SQLForeignKeys(hstmt,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),'\0',0,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[1],(SWORD)_tcslen(TableNames[1]));
						//_stprintf(Heading,"SQLForeignKeys(hstmt,%s,%d,%s,%d,<empty>,0,%s,%d,%s,%d,%s,%d)\n",TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),TableNames[1],_tcslen(TableNames[1]));
						//LogMsg(NONE,Heading);
						_tcscpy(Results[2],TableNames[0]);
						_tcscpy(Results[3], ColName[0]);
						_tcscpy(Results[6],TableNames[1]);
						_tcscpy(Results[7], ColName[3]);
						LogMsg(NONE, _T("m:%d SQLForeignKeys(hstmt, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d)\n"), m,
										TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),_T("<empty>"),0,
										TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),TableNames[1],_tcslen(TableNames[1]));
						break;
					case 3:
						if (_tcslen(TQualifier) == 0)
							returncode = SQLForeignKeys(hstmt,NULL,0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),'\0',0,NULL,0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[2],(SWORD)_tcslen(TableNames[2]));
						else
							returncode = SQLForeignKeys(hstmt,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),'\0',0,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[2],(SWORD)_tcslen(TableNames[2]));
						//_stprintf(Heading,"SQLForeignKeys(hstmt,%s,%d,%s,%d,<empty>,0,%s,%d,%s,%d,%s,%d)\n",TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),TableNames[2],_tcslen(TableNames[2]));
						//LogMsg(NONE,Heading);
						_tcscpy(Results[2],TableNames[1]);
						_tcscpy(Results[3], ColName[2]);
						_tcscpy(Results[6],TableNames[2]);
						_tcscpy(Results[7], ColName[5]);
						LogMsg(NONE, _T("m:%d SQLForeignKeys(hstmt, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d)\n"), m,
										TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),_T("<empty>"),0,
										TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),TableNames[2],_tcslen(TableNames[2]));
						break;
					case 4:
                        removeQuotes(TableNames[0],displayBuf.tab1);
                        removeQuotes(TableNames[1],displayBuf.tab2);
						if (_tcslen(TQualifier) == 0)
							returncode = SQLForeignKeys(hstmt,NULL, 0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)displayBuf.tab1,(SWORD)_tcslen(displayBuf.tab1),
															  NULL, 0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)displayBuf.tab2,(SWORD)_tcslen(displayBuf.tab2));
						else
							returncode = SQLForeignKeys(hstmt,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)displayBuf.tab1,(SWORD)_tcslen(displayBuf.tab1),
															  (SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)displayBuf.tab2,(SWORD)_tcslen(displayBuf.tab2));
                            /*returncode = SQLForeignKeys(hstmt,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[0],(SWORD)_tcslen(TableNames[0]),
															  (SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[1],(SWORD)_tcslen(TableNames[1]));*/
						LogMsg(NONE, _T("m:%d SQLForeignKeys(hstmt, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d)\n"), m,
															TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),displayBuf.tab1,_tcslen(displayBuf.tab1),
															TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),displayBuf.tab2,_tcslen(displayBuf.tab2));
						_tcscpy(Results[2],TableNames[0]);
						_tcscpy(Results[3], ColName[0]);
						_tcscpy(Results[6],TableNames[1]);
						_tcscpy(Results[7], ColName[3]);
						break;
					case 5:
						if (_tcslen(TQualifier) == 0)
							returncode = SQLForeignKeys(hstmt,NULL,0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[2],(SWORD)_tcslen(TableNames[2]),NULL,0,(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[3],(SWORD)_tcslen(TableNames[3]));
						else
							returncode = SQLForeignKeys(hstmt,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[2],(SWORD)_tcslen(TableNames[2]),(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TableNames[3],(SWORD)_tcslen(TableNames[3]));
						_tcscpy(Results[2],TableNames[0]);
						_tcscpy(Results[3], ColName[0]);
						_tcscpy(Results[6],TableNames[1]);
						_tcscpy(Results[7], ColName[3]);
						LogMsg(NONE, _T("m:%d SQLForeignKeys(hstmt, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d)\n"), m,
										TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),TableNames[2],_tcslen(TableNames[2]),
										TQualifier,_tcslen(TQualifier),TOwner,_tcslen(TOwner),TableNames[3],_tcslen(TableNames[3]));
						break;
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLForeignKeys"))
				{
                    if(!failedFlag)
						TEST_FAILED;
                    failedFlag = 1;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (j = 0; j < NUM_OUTPUTS_PK; j++)
					{
						Output[j] = (TCHAR *)malloc(NAME_LEN);
						OutputLen[j] = NAME_LEN;
						returncode = SQLBindCol(hstmt,(SWORD)(j+1),SQL_C_TCHAR,Output[j],NAME_LEN,&OutputLen[j]);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
						{
                            if(!failedFlag)
							    TEST_FAILED;
                            failedFlag = 1;
							LogAllErrors(henv,hdbc,hstmt);
						}
					}
					k = 0;
					while (returncode == SQL_SUCCESS)
					{
						returncode = SQLFetch(hstmt);
						if((returncode!=SQL_NO_DATA_FOUND) &&(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
						{
                            if(!failedFlag)
							    TEST_FAILED;
                            failedFlag = 1;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (returncode == SQL_SUCCESS)
							{
								LogMsg(LINEBEFORE,_T("Comparing results\n"));
								for (j = 0; j < NUM_OUTPUTS_PK; j++)
								{
									_itot(k+1,Results[8],10);
									//if ((_tcscmp(Output[j], _T("TRAFODION")) != 0) && (_tcslen(Results[j]) != 0))
									if ((_tcscmp(Output[j], _T("TRAFODION")) != 0) && (_tcslen(Results[j]) != 0))
									{
										if (cstrncmp(Results[j],Output[j],TRUE,_tcslen(Results[j])) == 0)
										{
											LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),Results[j],Output[j]);
										}	
										else
										{
											if(!failedFlag)
												TEST_FAILED;	
											failedFlag = 1;
											LogMsg(ERRMSG,_T("Result id=%d: expect: %s and actual: %s are not matched (m:%d j:%d) at line: %d\n"),j,Results[j],Output[j],m,j,__LINE__);
										}
									}
								}
							}
						}
						if (returncode == SQL_SUCCESS) 
							k++;
					}
					for (j = 0; j < NUM_OUTPUTS_PK; j++) free(Output[j]);
					if(k == 0)
					{
						TEST_FAILED;
						_stprintf (Heading, _T("m=%d"),m);
						LogMsg(NONE, Heading);
						LogMsg(ERRMSG,_T("No Data Found => Atleast one row should be fetched %d\n"), __LINE__);
					}
					else {
						TESTCASE_END;
					}
				}
				SQLFreeStmt(hstmt,SQL_UNBIND);
				SQLFreeStmt(hstmt,SQL_CLOSE);
			}
		}
		j = 0;
		while (_tcsicmp(TableNames[j],END_LOOP) != 0)
		{
			CreateTbl[0] = '\0';
			_stprintf(CreateTbl,_T("drop table %s cascade"),TableNames[j]);
			SQLExecDirect(hstmt,(SQLTCHAR*) CreateTbl,SQL_NTS);
			j++;
		}
		i++;
		TESTCASE_END;
        failedFlag = 0;
	}
	_tcscpy(ColStr,_T(""));
	_tcscpy(KeyStr,_T(""));
	_tcscpy(CreateTbl,_T(""));
	for (j = 0; j < NUM_OUTPUTS_PK; j++)
	{
		free(Results[j]);
	}

//========================================================================================================

	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLForeignKeys.\n"));
	free_list(var_list);
	TEST_RETURN;
}
