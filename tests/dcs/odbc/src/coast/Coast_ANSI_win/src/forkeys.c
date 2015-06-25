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
 	char				Heading[MAX_HEADING_SIZE];
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	CHAR				TQualifier[NAME_LEN],TOwner[NAME_LEN];
	CHAR				*Output[NUM_OUTPUTS_PK],*Results[NUM_OUTPUTS_PK];
	SQLLEN				OutputLen[NUM_OUTPUTS_PK] = {NAME_LEN,NAME_LEN,NAME_LEN,NAME_LEN,NAME_LEN,NAME_LEN}; 
    int failedFlag = 0;

	CHAR	*ColType[] = {" char(10)",
						" varchar(10)",
						" decimal(10,5)",
						" numeric(10,5)",
						" smallint",
						" integer",
						" bigint",
						" date",
						" time",
						" timestamp",
						" bit",		// loops ends here for MX since it doesn't support this datatypes.
						" tinyint",
						" binary(10)",
						" varbinary(10)",
						" numeric(19,0)",						//for bignum
						" numeric(19,6)",						//for bignum
						" numeric(128,0)",						//for bignum
						" numeric(128,128)",					//for bignum
						" numeric(127,64)",						//for bignum
						" numeric(10,5) unsigned",				//for bignum
						" numeric(18,5) unsigned",				//for bignum
						" numeric(30,10) unsigned",				//for bignum
						"endloop"
					};

	CHAR	*ColName[6];
	char	*TableNames[] = {"","","","endloop"};
	char	*keyName;
    char    tempTabName[MAX_NOS_SIZE];
	
	CHAR	ColStr[MAX_NOS_SIZE], KeyStr[MAX_NOS_SIZE], CreateTbl[MAX_NOS_SIZE],END_LOOP[10];
	int	i = 0, j = 0, k = 0, l = 0, m = 0;

	struct {
		char tab1[NAME_LEN];
		char tab2[NAME_LEN];
	} displayBuf; 

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLForeignKeys", charset_file);
	if (var_list == NULL) return FAILED;

	//print_list(var_list);
	ColName[0] = var_mapping("SQLForeignKeys_ColName_1", var_list);
	ColName[1] = var_mapping("SQLForeignKeys_ColName_2", var_list);
	ColName[2] = var_mapping("SQLForeignKeys_ColName_3", var_list);
	ColName[3] = var_mapping("SQLForeignKeys_ColName_4", var_list);
	ColName[4] = var_mapping("SQLForeignKeys_ColName_5", var_list);
	ColName[5] = var_mapping("SQLForeignKeys_ColName_6", var_list);

    // Remember to free these pointers after done
    sprintf(tempTabName,"\"%s_%s\"",var_mapping("SQLForeignKeys_TableNames_1", var_list),pTestInfo->Schema);
	TableNames[0] = strdup(tempTabName);
    sprintf(tempTabName,"\"%s_%s\"",var_mapping("SQLForeignKeys_TableNames_2", var_list),pTestInfo->Schema);
	TableNames[1] = strdup(tempTabName);
    sprintf(tempTabName,"\"%s_%s\"",var_mapping("SQLForeignKeys_TableNames_3", var_list),pTestInfo->Schema);
	TableNames[2] = strdup(tempTabName);

	keyName = var_mapping("SQLForeignKeys_keyName_1", var_list);
//========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => MX Specific SQLForeignKeys | SQLForeignKeys | forkeys.c\n");
	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLForeignKeys tests\n");
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
	TESTCASE_END;	//end of setup

	strcpy(ColStr,"");
	strcpy(KeyStr,"");
	strcpy(END_LOOP,"endloop");

	for (j = 0; j < NUM_OUTPUTS_PK; j++)
	{
		Results[j] = (char *)malloc(NAME_LEN);
	}
	strcpy(Results[0],pTestInfo->Catalog);		
	strcpy(Results[1],pTestInfo->Schema);
	strcpy(Results[4],pTestInfo->Catalog);		
	strcpy(Results[5],pTestInfo->Schema);
	strcpy(Results[9],"3");		
	strcpy(Results[10],"3");
	strcpy(Results[11],keyName);		
	strcpy(Results[12],keyName);
	strcpy(Results[13],"7");
	strcpy(TQualifier,Results[0]);
	strcpy(TOwner,Results[1]);
	
	while (_stricmp(ColType[i],END_LOOP) != 0)
	{
		sprintf(Heading,"Test Positive Functionality of SQLForeignKeys\n");
		TESTCASE_BEGIN(Heading);
		j = 0;
		l = 0;
		while (_stricmp(TableNames[j],END_LOOP) != 0)
		{
			CreateTbl[0] = '\0';
			sprintf(CreateTbl,"drop table %s cascade",TableNames[j]);
			SQLExecDirect(hstmt,(SQLCHAR*) CreateTbl,SQL_NTS);
			j++;
		}
		j = 0;
		while (_stricmp(TableNames[j],END_LOOP) != 0)
		{
			CreateTbl[0] = '\0';
			switch (j)
			{
				case 0:
                    // The  NO PARTITION is to help speed up this test on clustered systems with POS turned on.
					sprintf(CreateTbl,"create table %s (%s %s not null not droppable, %s %s, primary key(%s)) NO PARTITION",
							TableNames[j], ColName[0], ColType[i], ColName[1], ColType[i], ColName[0]);
					break;
				case 1:
                    // The  NO PARTITION is to help speed up this test on clustered systems with POS turned on.
					sprintf(CreateTbl,"create table %s (%s %s not null not droppable, %s %s, primary key(%s), foreign key (%s) references %s(%s)) NO PARTITION",
							TableNames[j], ColName[2], ColType[i], ColName[3], ColType[i], ColName[2], ColName[3], TableNames[j-1], ColName[0]);
					break;
				case 2:
                    // The  NO PARTITION is to help speed up this test on clustered systems with POS turned on.
					sprintf(CreateTbl,"create table %s (%s %s not null not droppable, %s %s, primary key(%s), foreign key (%s) references %s(%s)) NO PARTITION",
							TableNames[j], ColName[4], ColType[i], ColName[5], ColType[i], ColName[4], ColName[5], TableNames[j-1], ColName[2]);
					break;
			}

			//LogMsg(NONE, "%s\n", CreateTbl);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)CreateTbl,SQL_NTS);
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
				TESTCASE_BEGIN(NULL);
				switch (m)
				{
					case 0:
						if (strlen(TQualifier) == 0)
							returncode = SQLForeignKeys(hstmt,NULL,0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TableNames[0],(SWORD)strlen(TableNames[0]),NULL,0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),'\0',0);
						else
							returncode = SQLForeignKeys(hstmt,(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TableNames[0],(SWORD)strlen(TableNames[0]),(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),'\0',0);
						strcpy(Results[2],TableNames[0]);
						strcpy(Results[3], ColName[0]);
						strcpy(Results[6],TableNames[1]);
						strcpy(Results[7], ColName[3]);
						break;
					case 1:
						if (strlen(TQualifier) == 0)
							returncode = SQLForeignKeys(hstmt,NULL,0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TableNames[1],(SWORD)strlen(TableNames[1]),NULL,0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),'\0',0);
						else
							returncode = SQLForeignKeys(hstmt,(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TableNames[1],(SWORD)strlen(TableNames[1]),(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),'\0',0);
						strcpy(Results[2],TableNames[1]);
						strcpy(Results[3], ColName[2]);
						strcpy(Results[6],TableNames[2]);
						strcpy(Results[7], ColName[5]);
						break;
					case 2:
						if (strlen(TQualifier) == 0)
							returncode = SQLForeignKeys(hstmt,NULL,0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),'\0',0,NULL,0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TableNames[1],(SWORD)strlen(TableNames[1]));
						else
							returncode = SQLForeignKeys(hstmt,(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),'\0',0,(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TableNames[1],(SWORD)strlen(TableNames[1]));
						//sprintf(Heading,"SQLForeignKeys(hstmt,%s,%d,%s,%d,<empty>,0,%s,%d,%s,%d,%s,%d)\n",TQualifier,strlen(TQualifier),TOwner,strlen(TOwner),TQualifier,strlen(TQualifier),TOwner,strlen(TOwner),TableNames[1],strlen(TableNames[1]));
						//LogMsg(NONE,Heading);
						strcpy(Results[2],TableNames[0]);
						strcpy(Results[3], ColName[0]);
						strcpy(Results[6],TableNames[1]);
						strcpy(Results[7], ColName[3]);
						break;
					case 3:
						if (strlen(TQualifier) == 0)
							returncode = SQLForeignKeys(hstmt,NULL,0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),'\0',0,NULL,0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TableNames[2],(SWORD)strlen(TableNames[2]));
						else
							returncode = SQLForeignKeys(hstmt,(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),'\0',0,(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TableNames[2],(SWORD)strlen(TableNames[2]));
						//sprintf(Heading,"SQLForeignKeys(hstmt,%s,%d,%s,%d,<empty>,0,%s,%d,%s,%d,%s,%d)\n",TQualifier,strlen(TQualifier),TOwner,strlen(TOwner),TQualifier,strlen(TQualifier),TOwner,strlen(TOwner),TableNames[2],strlen(TableNames[2]));
						//LogMsg(NONE,Heading);
						strcpy(Results[2],TableNames[1]);
						strcpy(Results[3], ColName[2]);
						strcpy(Results[6],TableNames[2]);
						strcpy(Results[7], ColName[5]);
						break;
					case 4:
                        removeQuotes(TableNames[0],displayBuf.tab1);
                        removeQuotes(TableNames[1],displayBuf.tab2);
						if (strlen(TQualifier) == 0)
							returncode = SQLForeignKeys(hstmt,NULL, 0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)displayBuf.tab1,(SWORD)strlen(displayBuf.tab1),
															  NULL, 0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)displayBuf.tab2,(SWORD)strlen(displayBuf.tab2));
						else
							returncode = SQLForeignKeys(hstmt,(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)displayBuf.tab1,(SWORD)strlen(displayBuf.tab1),
															  (SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)displayBuf.tab2,(SWORD)strlen(displayBuf.tab2));
                            //LogMsg(NONE, "SQLForeignKeys(hstmt, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d, %s, %d)\n", 
															//TQualifier,strlen(TQualifier),TOwner,strlen(TOwner),displayBuf.tab1,strlen(displayBuf.tab1),
															//TQualifier,strlen(TQualifier),TOwner,strlen(TOwner),displayBuf.tab2,strlen(displayBuf.tab2));
						strcpy(Results[2],TableNames[0]);
						strcpy(Results[3], ColName[0]);
						strcpy(Results[6],TableNames[1]);
						strcpy(Results[7], ColName[3]);
						break;
					case 5:
						if (strlen(TQualifier) == 0)
							returncode = SQLForeignKeys(hstmt,NULL,0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TableNames[2],(SWORD)strlen(TableNames[2]),NULL,0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TableNames[3],(SWORD)strlen(TableNames[3]));
						else
							returncode = SQLForeignKeys(hstmt,(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TableNames[2],(SWORD)strlen(TableNames[2]),(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TableNames[3],(SWORD)strlen(TableNames[3]));
						strcpy(Results[2],TableNames[0]);
						strcpy(Results[3], ColName[0]);
						strcpy(Results[6],TableNames[1]);
						strcpy(Results[7], ColName[3]);
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
						Output[j] = (char *)malloc(NAME_LEN);
						returncode = SQLBindCol(hstmt,(SWORD)(j+1),SQL_C_CHAR,Output[j],NAME_LEN,&OutputLen[j]);
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
								LogMsg(LINEBEFORE,"Comparing results\n");
								for (j = 0; j < NUM_OUTPUTS_PK; j++)
								{
									_itoa(k+1,Results[8],10);
									if ((strcmp(Output[j], pTestInfo->Catalog) != 0) && (strlen(Results[j]) != 0))
									{
										if (cstrncmp(Results[j],Output[j],TRUE,isCharSet,strlen(Results[j])) == 0)
										{
											//LogMsg(NONE,"expect: %s and actual: %s are matched\n",Results[j],Output[j]);
										}	
										else
										{
                                            if (cstrncmp(Results[j],Output[j],TRUE,TRUE,strlen(Results[j])) != 0) {
											    if(!failedFlag)
												    TEST_FAILED;	
											    failedFlag = 1;
											    LogMsg(ERRMSG,"Result id=%d: expect: %s and actual: %s are not matched at line: %d\n",j,Results[j],Output[j],__LINE__);
                                            }    
                                        }
									}
								}
							}
						}
						if (returncode == SQL_SUCCESS) 
							k++;
					}
					for (j = 0; j < NUM_OUTPUTS_PK; j++)free(Output[j]);
					if(k == 0)
					{
						TEST_FAILED;
						sprintf (Heading, "m=%d",m);
						LogMsg(NONE, Heading);
						LogMsg(ERRMSG,"No Data Found => Atleast one row should be fetched %d\n", __LINE__);
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
		while (_stricmp(TableNames[j],END_LOOP) != 0)
		{
			CreateTbl[0] = '\0';
			sprintf(CreateTbl,"drop table %s cascade",TableNames[j]);
			SQLExecDirect(hstmt,(SQLCHAR*) CreateTbl,SQL_NTS);
			j++;
		}
		i++;
		TESTCASE_END;
        failedFlag = 0;
	}
	strcpy(ColStr,"");
	strcpy(KeyStr,"");
	strcpy(CreateTbl,"");
	for (j = 0; j < NUM_OUTPUTS_PK; j++)
	{
		free(Results[j]);
	}

//========================================================================================================

	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLForeignKeys.\n");
    free(TableNames[0]);
    free(TableNames[1]);
    free(TableNames[2]);
	free_list(var_list);
	TEST_RETURN;
}
