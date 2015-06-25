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
#define NUM_OUTPUTS		8
#define NUM_SCOPE		3
#define NUM_NULL		2
#define NUM_COLTYPE		2

/*
---------------------------------------------------------
   TestSQLSpecialColumns
---------------------------------------------------------
*/

PassFail TestSQLSpecialColumns(TestInfo *pTestInfo, int MX_MP_SPECIFIC)
{                  
	TEST_DECLARE;
 	char			Heading[MAX_HEADING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	CHAR			TQualifier[NAME_LEN],TOwner[NAME_LEN],TName[NAME_LEN];
	UWORD			fColType[NUM_COLTYPE] = {SQL_BEST_ROWID,SQL_ROWVER};
	UWORD			Scope[NUM_SCOPE] = {SQL_SCOPE_CURROW,SQL_SCOPE_TRANSACTION,SQL_SCOPE_SESSION};
	UWORD			Nullable[NUM_NULL] = {SQL_NO_NULLS,SQL_NULLABLE};
	CHAR			ocname[MAX_COLUMN_NAME],octype[MAX_COLUMN_NAME];
	SWORD			oscope,ocdatatype,ocsca,ocpc;
	SDWORD			ocprec,oclen;		
	SQLLEN			oscopelen,ocnamelen,ocdatatypelen,octypelen,ocpreclen,oclenlen,ocscalen,ocpclen;

	struct
	{
		CHAR		*ColName;
		SWORD		ColDataType;
		CHAR		*ColTypeName;
		CHAR		*ColTypeOutput;
		CHAR		*ColTypeLen;
		SDWORD		ColPrec;
		SWORD		ColSca;
		SDWORD		ColLen;
	} Columns[] = {
							{"--",SQL_CHAR,"char","CHAR","(10)",10,0,10},
							{"--",SQL_VARCHAR,"varchar","VARCHAR","(10)",10,0,10},
							{"--",SQL_DECIMAL,"decimal","DECIMAL SIGNED","(10,5)",10,5,12},
							{"--",SQL_NUMERIC,"numeric","NUMERIC SIGNED","(10,5)",10,5,12},
							{"--",SQL_SMALLINT,"smallint","SMALLINT SIGNED","",5,0,2},
							{"--",SQL_INTEGER,"integer","INTEGER SIGNED","",10,0,4},
							{"--",SQL_BIGINT,"bigint","BIGINT SIGNED","",19,0,20},
							{"--",SQL_DATE,"date","DATE","",10,0,6},
							{"--",SQL_TIME,"time","TIME","",8,0,6},
							{"--",SQL_TIMESTAMP,"timestamp","TIMESTAMP","",26,6,16},
							{"--",SQL_BIT,"bit","BIT","",1,1,0},
							{"--",SQL_TINYINT,"tinyint","TINYINT","",3,0,2},
							{"-",SQL_BINARY,"binary","BINARY","(10)",10,0,10},
							{"--",SQL_VARBINARY,"varbinary","VARBINARY","(10)",10,0,10},
							{"--",SQL_NUMERIC,"numeric","NUMERIC SIGNED","(19,0)",19,0,21},				//Bignum
							{"--",SQL_NUMERIC,"numeric","NUMERIC SIGNED","(19,6)",19,6,21},				//Bignum
							{"--",SQL_NUMERIC,"numeric","NUMERIC SIGNED","(128,0)",128,0,130},			//Bignum
							{"--",SQL_NUMERIC,"numeric","NUMERIC SIGNED","(128,128)",128,128,130},		//Bignum
							{"--",SQL_NUMERIC,"numeric","NUMERIC SIGNED","(128,64)",128,64,130},			//Bignum
							{"--",SQL_NUMERIC,"numeric","NUMERIC UNSIGNED","(10,5) unsigned",10,5,12},		//Bignum
							{"--",SQL_NUMERIC,"numeric","NUMERIC UNSIGNED","(18,5) unsigned",18,5,20},		//Bignum
							{"--",SQL_NUMERIC,"numeric","NUMERIC UNSIGNED","(30,10) unsigned",30,10,32},	//Bignum							
							{"",0,"endloop","",0,0,0,0}
						};

	CHAR	*TableStr[4];
	CHAR	ColStr[MAX_NOS_SIZE], KeyStr[MAX_NOS_SIZE], CreateTbl[MAX_NOS_SIZE],END_LOOP[10];
	int		i = 0, k = 0,ct = 0, s = 0, t = 0, n = 0, psc = 1;
    BOOL    found = FALSE;
	char *charNameUCS2 = "WIDE CHARACTER";
	char *varcharNameUCS2 = "WIDE VARCHAR";

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLSpecialColumns", charset_file);
	if (var_list == NULL) return FAILED;

	//print_list(var_list);
	Columns[0].ColName = var_mapping("SQLSpecialColumns_Columns_1", var_list);
	Columns[1].ColName = var_mapping("SQLSpecialColumns_Columns_2", var_list);
	Columns[2].ColName = var_mapping("SQLSpecialColumns_Columns_3", var_list);
	Columns[3].ColName = var_mapping("SQLSpecialColumns_Columns_4", var_list);
	Columns[4].ColName = var_mapping("SQLSpecialColumns_Columns_5", var_list);
	Columns[5].ColName = var_mapping("SQLSpecialColumns_Columns_6", var_list);
	Columns[6].ColName = var_mapping("SQLSpecialColumns_Columns_7", var_list);
	Columns[7].ColName = var_mapping("SQLSpecialColumns_Columns_8", var_list);
	Columns[8].ColName = var_mapping("SQLSpecialColumns_Columns_9", var_list);
	Columns[9].ColName = var_mapping("SQLSpecialColumns_Columns_10", var_list);
	Columns[10].ColName = var_mapping("SQLSpecialColumns_Columns_11", var_list);
	Columns[11].ColName = var_mapping("SQLSpecialColumns_Columns_12", var_list);
	Columns[12].ColName = var_mapping("SQLSpecialColumns_Columns_13", var_list);
	Columns[13].ColName = var_mapping("SQLSpecialColumns_Columns_14", var_list);
	Columns[14].ColName = var_mapping("SQLSpecialColumns_Columns_15", var_list);
	Columns[15].ColName = var_mapping("SQLSpecialColumns_Columns_16", var_list);
	Columns[16].ColName = var_mapping("SQLSpecialColumns_Columns_17", var_list);
	Columns[17].ColName = var_mapping("SQLSpecialColumns_Columns_18", var_list);
	Columns[18].ColName = var_mapping("SQLSpecialColumns_Columns_19", var_list);
	Columns[19].ColName = var_mapping("SQLSpecialColumns_Columns_20", var_list);
	Columns[20].ColName = var_mapping("SQLSpecialColumns_Columns_21", var_list);
	Columns[21].ColName = var_mapping("SQLSpecialColumns_Columns_22", var_list);

	TableStr[0] = var_mapping("SQLSpecialColumns_TableStr_1", var_list);
	TableStr[1] = var_mapping("SQLSpecialColumns_TableStr_2", var_list);
	TableStr[2] = var_mapping("SQLSpecialColumns_TableStr_3", var_list);
	TableStr[3] = var_mapping("SQLSpecialColumns_TableStr_4", var_list);

//=========================================================================================

	if(isUCS2) {
		LogMsg(NONE,"Setup for UCS2 mode testing: ColPrec has to be doubled\n");

		i = 0;
		while(stricmp(Columns[i].ColTypeName,"endloop") != 0) {
			if (Columns[i].ColDataType == SQL_CHAR){
				//Columns[i].ColDataType = SQL_WCHAR;
				//Columns[i].ColTypeOutput = charNameUCS2;
				Columns[i].ColPrec *= 2;  //--> This is in character, no need to double
				Columns[i].ColLen *= 2;
			}
			else if (Columns[i].ColDataType == SQL_VARCHAR) {
				//Columns[i].ColDataType = SQL_WVARCHAR;
				//Columns[i].ColTypeOutput = varcharNameUCS2;
				Columns[i].ColPrec *= 2;  //--> This is in character, no need to double
				Columns[i].ColLen *= 2;
			}
			else if (Columns[i].ColDataType == SQL_LONGVARCHAR)	{
				//Columns[i].ColDataType = SQL_WLONGVARCHAR;
				//Columns[i].ColTypeOutput = varcharNameUCS2;
				Columns[i].ColPrec *= 2;  //--> This is in character, no need to double
				Columns[i].ColLen *= 2;
			}
			i++;
		}
		i = 0;
	}

//=========================================================================================

	if (MX_MP_SPECIFIC == MX_SPECIFIC)
		LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => MX Specific SQLSpecialColumns | SQLSpecialColumns | specol.c\n");
	else
		LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => MP Specific SQLSpecialColumns | SQLSpecialColumns | specol.c\n");
	
	TEST_INIT;
	TESTCASE_BEGIN("Setup for SQLSpecialColumns tests\n");

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
	TESTCASE_END;

	strcpy(ColStr,"");
	strcpy(KeyStr,"");
	strcpy(END_LOOP,"");
	strcpy(TName,TableStr[2]);

	if (MX_MP_SPECIFIC == MX_SPECIFIC)
	{
		strcpy(TQualifier,pTestInfo->Catalog);
		strcpy(TOwner,pTestInfo->Schema);
		strcpy(END_LOOP,"bit");
	}
	else
	{
		strcpy(TQualifier,"");
		strcpy(TOwner,pTestInfo->UserID);
		strcpy(END_LOOP,"endloop");
	}

	while (_stricmp(Columns[i].ColTypeName,END_LOOP) != 0)
	{
		SQLExecDirect(hstmt,(SQLCHAR*) (SQLCHAR *)TableStr[1],SQL_NTS); // cleanup
		if (i > 0)
		{
			strcat(ColStr,",");
			strcat(KeyStr,",");
		}
		strcat(ColStr,Columns[i].ColName);
		strcat(ColStr," ");
		strcat(ColStr,Columns[i].ColTypeName);
		strcat(ColStr,Columns[i].ColTypeLen);
		strcat(ColStr," not null");
		strcat(KeyStr,Columns[i].ColName);
		strcpy(CreateTbl,"");
		strcat(CreateTbl,TableStr[0]);
		strcat(CreateTbl,"(");
		strcat(CreateTbl,ColStr);
		strcat(CreateTbl,", primary key(");
		strcat(CreateTbl,KeyStr);
		strcat(CreateTbl,"))");

		sprintf(Heading,"Test Positive Functionality of SQLSpecialColumns for this table:\n");
		strcat(Heading,CreateTbl);
		strcat(Heading,"\n");
		TESTCASE_BEGIN(Heading);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CreateTbl,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		else{
			if (strlen(TQualifier) > 0)
				returncode = SQLSpecialColumns(hstmt,fColType[ct],(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TName,(SWORD)strlen(TName),Scope[s],Nullable[n]);
			else
				returncode = SQLSpecialColumns(hstmt,fColType[ct],NULL,0,(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TName,(SWORD)strlen(TName),Scope[s],Nullable[n]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSpecialColumns")){
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
				}
			else{
				oscope = 0;
				strcpy(ocname,"");
				ocdatatype = 0;
				strcpy(octype,"");
				ocprec = 0;
				oclen = 0;
				ocsca = 0;
				ocpc = 0;
				SQLBindCol(hstmt,1,SQL_C_SHORT,&oscope,0,&oscopelen);
			    SQLBindCol(hstmt,2,SQL_C_CHAR,ocname,MAX_COLUMN_NAME,&ocnamelen);
				SQLBindCol(hstmt,3,SQL_C_SHORT,&ocdatatype,0,&ocdatatypelen);
				SQLBindCol(hstmt,4,SQL_C_CHAR,octype,MAX_COLUMN_NAME,&octypelen);
				SQLBindCol(hstmt,5,SQL_C_LONG,&ocprec,0,&ocpreclen);
				SQLBindCol(hstmt,6,SQL_C_LONG,&oclen,0,&oclenlen);
				SQLBindCol(hstmt,7,SQL_C_SHORT,&ocsca,0,&ocscalen);
				SQLBindCol(hstmt,8,SQL_C_SHORT,&ocpc,0,&ocpclen);

				k = 0;
				while (returncode == SQL_SUCCESS){
					returncode = SQLFetch(hstmt);
					if((returncode!=SQL_NO_DATA_FOUND)
							&&(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))){
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
						}
					else{
						if (returncode == SQL_SUCCESS){
							if (MX_MP_SPECIFIC == MX_SPECIFIC)
							{
								psc = SQL_PC_NOT_PSEUDO;
							}
							else
							{
								psc = 1;
							}
							LogMsg(NONE,"Comparing results for SQLSpecialColumns\n");
                            t = 0;
                            found = FALSE;
                            while(strcmp(Columns[t].ColTypeName,(char*)"endloop")!=0) {
                                if(cstrcmp(ocname, Columns[t].ColName,TRUE,isCharSet) == 0) {
							        if ((oscope == Scope[s]) 
								        && (ocdatatype == Columns[t].ColDataType) 
								        //&& (_strnicmp(octype,Columns[t].ColTypeName,strlen(Columns[t].ColTypeName)) == 0) 
								        && (stricmp(octype,Columns[t].ColTypeOutput) == 0) 
								        && (ocprec == Columns[t].ColPrec) 
								        && (oclen == Columns[t].ColLen) 
								        && (ocsca == Columns[t].ColSca) 
								        && (ocpc == (SWORD)psc)){
								        /*
								        LogMsg(NONE,"Scope expect: %d and actual: %d are matched\n",Scope[s],oscope);
								        LogMsg(NONE,"colname expect: %s and actual: %s are matched\n",Columns[t].ColName,ocname);
								        LogMsg(NONE,"ColDataType expect: %d and actual: %d are matched\n",Columns[t].ColDataType,ocdatatype);
								        LogMsg(NONE,"ColTypeName expect: %s and actual: %s are matched\n",Columns[t].ColTypeName,octype);
								        LogMsg(NONE,"ColPrec expect: %d and actual: %d are matched\n",Columns[t].ColPrec,ocprec);
								        LogMsg(NONE,"ColLen expect: %d and actual: %d are matched\n",Columns[t].ColLen,oclen);
								        LogMsg(NONE,"ColScale expect: %d and actual: %d are matched\n",Columns[t].ColSca,ocsca);
								        LogMsg(NONE,"ColPseudoCol expect: %d and actual: %d are matched\n\n",(SWORD)psc,ocpc);
								        */
							        } else {
							            TEST_FAILED;	
							            if (oscope != Scope[s]) 
								            LogMsg(ERRMSG,"Scope expect: %d and actual: %d are not matched\n",Scope[t],oscope);
							            if (ocdatatype != Columns[t].ColDataType) 
								            LogMsg(ERRMSG,"ColDataType expect: %d and actual: %d are not matched\n",Columns[t].ColDataType,ocdatatype);
							            if (_stricmp(octype,Columns[t].ColTypeName) != 0) 
								            LogMsg(ERRMSG,"ColTypeName expect: %s and actual: %s are not matched\n",Columns[t].ColTypeOutput,octype);
							            if (ocprec != Columns[t].ColPrec) 
								            LogMsg(ERRMSG,"ColPrec expect: %d and actual: %d are not matched\n",Columns[t].ColPrec,ocprec);
							            if (oclen != Columns[t].ColLen) 
								            LogMsg(ERRMSG,"ColLen expect: %d and actual: %d are not matched\n",Columns[t].ColLen,oclen);
							            if (ocsca != Columns[t].ColSca) 
								            LogMsg(ERRMSG,"ColScale expect: %d and actual: %d are not matched\n",Columns[t].ColSca,ocsca);
							            if (ocpc != (SWORD)psc)
								            LogMsg(ERRMSG,"ColPseudoCol expect: %d and actual: %d are not matched\n\n",(SWORD)psc,ocpc);
						            }
                                    found = TRUE;
                                    break;
                                } else {
                                    t++;
                                }
                            }
                            if(!found) {
                                TEST_FAILED;
                                LogMsg(ERRMSG,"Unexpected returned data: %s\n", ocname);
                            }
						}
                    }
					if (returncode == SQL_SUCCESS)
						k++;
					} // end while
					if(k == 0)
					{
						TEST_FAILED;
						LogMsg(ERRMSG,"No Data Found => Atleast one row should be fetched\n");
					}
				}
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);
			}
			SQLExecDirect(hstmt,(SQLCHAR*) (SQLCHAR *)TableStr[1],SQL_NTS);
		i++;
		TESTCASE_END;
		}  // end while

	//========================================================================================================

	sprintf(Heading,"SQLSpecialColumns: Negative test with NULL handle\n");
	TESTCASE_BEGIN(Heading);

	hstmt = (SQLHANDLE)NULL;
	strcpy(TQualifier,"");
	strcpy(TOwner,pTestInfo->UserID);
	strcpy(TName,TableStr[3]);
	i = 0;

	returncode = SQLSpecialColumns(hstmt,fColType[i],(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TName,(SWORD)strlen(TName),Scope[i],Nullable[i]);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLSpecialColumns"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

	//========================================================================================================

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLSpecialColumns.\n");
	free_list(var_list);
	TEST_RETURN;
}
