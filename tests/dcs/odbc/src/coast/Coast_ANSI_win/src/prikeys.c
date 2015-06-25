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
 	char			Heading[MAX_HEADING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	CHAR			TQualifier[NAME_LEN],TOwner[NAME_LEN],TName[NAME_LEN];
	CHAR			*Output[NUM_OUTPUTS_PK],*Results[NUM_OUTPUTS_PK];
	SQLLEN			OutputLen[NUM_OUTPUTS_PK] = {NAME_LEN,NAME_LEN,NAME_LEN,NAME_LEN,NAME_LEN,NAME_LEN};

	struct
	{
		CHAR			*ColName;
		CHAR			*ColType;
	} Columns[] = {
							{"--"," char(10)"},
							{"--"," varchar(10)"},
							{"--"," decimal(10,5)"},
							{"--"," numeric(10,5)"},
							{"--"," smallint"},
							{"--"," integer"},
							{"--"," bigint"},
							{"--"," date"},
							{"--"," time"},
							{"--"," timestamp"},
							{"--"," bit"},	// loops ends here for MX since ity doesn't support this datatypes.
							{"--"," tinyint"},
							{"--"," binary(10)"},
							{"--"," varbinary(10)"},
							{"--"," numeric(19,0)"},			//for bignum
							{"--"," numeric(19,6)"},			//for bignum
							{"--"," numeric(128,0)"},			//for bignum
							{"--"," numeric(128,128)"},			//for bignum
							{"--"," numeric(127,64)"},			//for bignum
							{"--"," numeric(10,5) unsigned"},	//for bignum
							{"--"," numeric(18,5) unsigned"},	//for bignum
							{"--"," numeric(30,10) unsigned"},	//for bignum
							{"--","endloop"}
						};

	CHAR			*TableStr[3];

	CHAR			ColStr[MAX_NOS_SIZE], KeyStr[MAX_NOS_SIZE], CreateTbl[MAX_NOS_SIZE],END_LOOP[10];
	int				i = 0, j = 0, k = 0;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLPrimaryKeys", charset_file);
	if (var_list == NULL) return FAILED;

	Columns[0].ColName = var_mapping("SQLPrimaryKeys_Columns_1", var_list);
	Columns[1].ColName = var_mapping("SQLPrimaryKeys_Columns_2", var_list);
	Columns[2].ColName = var_mapping("SQLPrimaryKeys_Columns_3", var_list);
	Columns[3].ColName = var_mapping("SQLPrimaryKeys_Columns_4", var_list);
	Columns[4].ColName = var_mapping("SQLPrimaryKeys_Columns_5", var_list);
	Columns[5].ColName = var_mapping("SQLPrimaryKeys_Columns_6", var_list);
	Columns[6].ColName = var_mapping("SQLPrimaryKeys_Columns_7", var_list);
	Columns[7].ColName = var_mapping("SQLPrimaryKeys_Columns_8", var_list);
	Columns[8].ColName = var_mapping("SQLPrimaryKeys_Columns_9", var_list);
	Columns[9].ColName = var_mapping("SQLPrimaryKeys_Columns_10", var_list);
	Columns[10].ColName = var_mapping("SQLPrimaryKeys_Columns_11", var_list);
	Columns[11].ColName = var_mapping("SQLPrimaryKeys_Columns_12", var_list);
	Columns[12].ColName = var_mapping("SQLPrimaryKeys_Columns_13", var_list);
	Columns[13].ColName = var_mapping("SQLPrimaryKeys_Columns_14", var_list);
	Columns[14].ColName = var_mapping("SQLPrimaryKeys_Columns_15", var_list);
	Columns[15].ColName = var_mapping("SQLPrimaryKeys_Columns_16", var_list);
	Columns[16].ColName = var_mapping("SQLPrimaryKeys_Columns_17", var_list);
	Columns[17].ColName = var_mapping("SQLPrimaryKeys_Columns_18", var_list);
	Columns[18].ColName = var_mapping("SQLPrimaryKeys_Columns_19", var_list);
	Columns[19].ColName = var_mapping("SQLPrimaryKeys_Columns_20", var_list);
	Columns[20].ColName = var_mapping("SQLPrimaryKeys_Columns_21", var_list);
	Columns[21].ColName = var_mapping("SQLPrimaryKeys_Columns_22", var_list);

	TableStr[0] = var_mapping("SQLPrimaryKeys_TableStr_1", var_list);
	TableStr[1] = var_mapping("SQLPrimaryKeys_TableStr_2", var_list);
	TableStr[2] = var_mapping("SQLPrimaryKeys_TableStr_3", var_list);

//========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => MX Specific SQLPrimaryKeys | SQLPrimaryKeys | prikeys.c\n");
	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLPrimaryKeys tests\n");
	if(!FullConnect(pTestInfo))
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
	TESTCASE_END;	//end of setup

	strcpy(ColStr,"");
	strcpy(KeyStr,"");
	strcpy(END_LOOP,"");

	Results[0] = (char *)malloc(NAME_LEN);
	strcpy(Results[0],pTestInfo->Catalog);		
	Results[1] = (char *)malloc(NAME_LEN);
	strcpy(Results[1],pTestInfo->Schema);
	Results[2] = (char *)malloc(NAME_LEN);
	strcpy(Results[2],TableStr[2]);
	Results[3] = (char *)malloc(NAME_LEN);
	strcpy(Results[3],"");
	Results[4] = (char *)malloc(NAME_LEN);
	strcpy(Results[4],"");
	Results[5] = (char *)malloc(NAME_LEN);
	strcpy(Results[5],TableStr[2]);
	strcpy(END_LOOP," bit");			// needs a space to match
	strcpy(TQualifier,Results[0]);
	strcpy(TOwner,Results[1]);
	strcpy(TName,Results[2]);
	
	while (_stricmp(Columns[i].ColType,END_LOOP) != 0)
	{
		SQLExecDirect(hstmt,(SQLCHAR*) (SQLCHAR *)TableStr[1],SQL_NTS);
		if (i > 0)
		{
			strcat(ColStr,",");
			strcat(KeyStr,",");
		}
		strcat(ColStr,Columns[i].ColName);
		strcat(ColStr,Columns[i].ColType);
		strcat(ColStr," not null");
		strcat(KeyStr,Columns[i].ColName);
		strcpy(CreateTbl,"");
		strcat(CreateTbl,TableStr[0]);
		strcat(CreateTbl,"(");
		strcat(CreateTbl,ColStr);
		strcat(CreateTbl,", primary key(");
		strcat(CreateTbl,KeyStr);
		strcat(CreateTbl,"))");

		sprintf(Heading,"Test Positive Functionality of SQLPrimaryKeys for ");
		strcat(Heading,CreateTbl);
		strcat(Heading,"\n");
		TESTCASE_BEGIN(Heading);

		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CreateTbl,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		else
		{
			LogMsg(NONE,"SQLPrimaryKeys: create table with primary key %s\n",KeyStr);
			if (strlen(TQualifier) > 0)
				returncode = SQLPrimaryKeys(hstmt,(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TName,(SWORD)strlen(TName));
			else
				returncode = SQLPrimaryKeys(hstmt,NULL,0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TName,(SWORD)strlen(TName));
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrimaryKeys"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				for (j = 0; j < NUM_OUTPUTS_PK-1; j++)
				{
					Output[j] = (char *)malloc(NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(j+1),SQL_C_CHAR,Output[j],NAME_LEN,&OutputLen[j]);
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
							LogMsg(NONE,"Comparing results\n");
							for (j = 0; j < NUM_OUTPUTS_PK-1; j++)
							{
								if (j == 3)
								{
									if (MX_MP_SPECIFIC == MX_SPECIFIC)
										if (cstrcmp(Output[j],Columns[k].ColName,TRUE,isCharSet) != 0)
										{
											TEST_FAILED;	
											LogMsg(ERRMSG,"expect: %s and actual: %s are not matched\n",Columns[k].ColName,Output[j]);
										}
								}
								else if (j == 4)
								{
									_itoa(k+1,Results[j],10);
									if (_stricmp(Output[j],Results[j]) != 0)
									{
										TEST_FAILED;	
										LogMsg(ERRMSG,"expect: %s and actual: %s are not matched\n",Results[j],Output[j]);
									}
								}
								else
								{
									if (!(strcmp(Results[j], "TRAFODION")))
									{
										if (_stricmp(Output[j],Results[j]) != 0)
										{
											TEST_FAILED;	
											LogMsg(ERRMSG,"expect: %s and actual: %s are not matched\n",Results[j],Output[j]);
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
					LogMsg(ERRMSG,"No Data Found => Atleast one row should be fetched\n");
				}
			}
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);
		}
		SQLExecDirect(hstmt,(SQLCHAR*)(SQLCHAR *)TableStr[1],SQL_NTS);
		i++;
		TESTCASE_END;
	}
	strcpy(ColStr,"");
	strcpy(KeyStr,"");
	strcpy(CreateTbl,"");
	for (j = 0; j < NUM_OUTPUTS_PK; j++)
	{
		free(Results[j]);
	}

//========================================================================================================

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLPrimaryKeys.\n");

	free_list(var_list);

	TEST_RETURN;
}
