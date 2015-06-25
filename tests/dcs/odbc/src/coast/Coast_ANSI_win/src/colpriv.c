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

/* sq: Need to make sure that the ID used here as SQ_GRANTEE is
 *           registered on the target system.  There is a script
 *           src/scripts/regLDAPuser.sql that can be obeyed from sqlci
 *           on the target, if the IDs have not been registered.
 */
/* sq */ #define SQ_GRANTEE "QAUSER_EXECS" /* "DB__ROOT" */
/* sq */ #define LDAP 1
#define NAME_LEN			128+1
#define NUM_OUTPUTS			8
#define REM_LEN				254
#define NUM_PATTERN			5
#define	NUM_PRIVILEGES		5

/*
---------------------------------------------------------
   MX Specific TestSQLColumnPrivileges
---------------------------------------------------------
*/
PassFail TestMXSQLColumnPrivileges( TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	char			Heading[MAX_HEADING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;

	char			TableQualifier[NAME_LEN],TableOwner[NAME_LEN],Is_Grantable[4];
	char			*TableStr;

	char			*TableName;
// sq	char			*Grantor;
/* sq new */ CHAR            Grantor[SQL_MAX_ROLENAME_LEN+2];
	char			oTableQualifier[NAME_LEN];  
	char			oTableOwner[NAME_LEN];
	char			oTableName[NAME_LEN];
	char			oColName[NAME_LEN];
	char			oGrantor[NAME_LEN]; 
	char			oGrantee[NAME_LEN];
	char			oPrivilege[NAME_LEN];
	char			oIs_Grantable[4];

	SQLLEN		oTableQualifierlen; 
	SQLLEN		oTableOwnerlen;
	SQLLEN		oTableNamelen;
	SQLLEN		oColNamelen;
	SQLLEN		oGrantorlen;
	SQLLEN		oGranteelen;
	SQLLEN		oPrivilegelen;
	SQLLEN		oIs_Grantablelen;

/* sq */	
	struct
	{
		char		*Col;
		char		*ColType;
		char		*Grantee;
		char		*Privilege;
	} TableCol[] = {
						{"--","char(10)",SQ_GRANTEE,"REFERENCES"},
						{"--","varchar(10)",SQ_GRANTEE,"UPDATE"},
						{"--","long varchar",SQ_GRANTEE,"REFERENCES"},
						{"--","decimal(10,5)",SQ_GRANTEE,"UPDATE"},
						{"--","numeric(10,5)",SQ_GRANTEE,"REFERENCES"},
						{"--","smallint",SQ_GRANTEE,"UPDATE"},
						{"--","integer",SQ_GRANTEE,"REFERENCES"},
						{"--","bigint",SQ_GRANTEE,"UPDATE"},
						{"--","real",SQ_GRANTEE,"REFERENCES"},
						{"--","float",SQ_GRANTEE,"UPDATE"},
						{"--","double precision",SQ_GRANTEE,"REFERENCES"},
						{"--","date",SQ_GRANTEE,"UPDATE"},
						{"--","time",SQ_GRANTEE,"REFERENCES"},
						{"--","timestamp",SQ_GRANTEE,"UPDATE"},
						{"--","numeric(19,0)",SQ_GRANTEE,"REFERENCES"},
						{"--","numeric(19,6)",SQ_GRANTEE,"REFERENCES"},
						{"--","numeric(128,0)",SQ_GRANTEE,"REFERENCES"},
						{"--","numeric(128,128)",SQ_GRANTEE,"REFERENCES"},
						{"--","numeric(10,5) unsigned",SQ_GRANTEE,"REFERENCES"},
						{"--","numeric(18,5) unsigned",SQ_GRANTEE,"REFERENCES"},
						{"--","numeric(30,10) unsigned",SQ_GRANTEE,"REFERENCES"},
						{"endloop",}
					};

	struct
	{
		char		*TabQua;
		char		*TabOwner;
		char		*TabName;
		char		*ColName;
		RETCODE		CheckCode;
	} ColumnWC[] = {								/* wild cards from here */
						{"--","--","--","--"},	// Have a row with all valid values here so that 
						{"--","--","--","--", SQL_ERROR}, 
						{"--","--","--","--", SQL_ERROR}, 
						{"--","--","--","--", SQL_SUCCESS}, 
						{"--","--","--","--", SQL_ERROR},
						{"--","--","--","--", SQL_SUCCESS},
						{"--","--","--","--", SQL_SUCCESS},
						{"--","--","--","--", SQL_SUCCESS},
						{"--","--","--","--", SQL_SUCCESS},
						{"--","--","--","--", SQL_SUCCESS},
						{"--","--","--","--", SQL_SUCCESS},
						{"--","--","--","--", SQL_SUCCESS},
						{"--","--","--","--", SQL_SUCCESS},
						{"--","--","--","--", SQL_SUCCESS},
						{"--","--","--","--", SQL_SUCCESS},
						{"--","--","--","--", SQL_SUCCESS},
						{"--","--","--","--", SQL_SUCCESS},
						{"--","--","--","--", SQL_SUCCESS},
						{"endloop",}
					};

	int	i = 0, k = 0;
//	DWORD	nSize;

    struct {
        char cat[NAME_LEN];
        char sch[NAME_LEN];
        char tab[NAME_LEN];
        char col[NAME_LEN];
    } displayBuf;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLColumnPrivileges", charset_file);
	if (var_list == NULL) return FAILED;

	TableName = var_mapping("SQLColumnPrivileges_TableName", var_list);
/* sq: In Sequset, we will call SQLGetConnectAttr() to get it later
 * after hdbc is established. */
/* sq	Grantor = var_mapping("SQLColumnPrivileges_Grantor", var_list);
*/
	TableCol[0].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_0", var_list);
	TableCol[1].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_1", var_list);
	TableCol[2].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_2", var_list);
	TableCol[3].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_3", var_list);
	TableCol[4].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_4", var_list);
	TableCol[5].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_5", var_list);
	TableCol[6].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_6", var_list);
	TableCol[7].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_7", var_list);
	TableCol[8].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_8", var_list);
	TableCol[9].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_9", var_list);
	TableCol[10].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_10", var_list);
	TableCol[11].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_11", var_list);
	TableCol[12].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_12", var_list);
	TableCol[13].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_13", var_list);
	TableCol[14].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_14", var_list);
	TableCol[15].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_15", var_list);
	TableCol[16].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_16", var_list);
	TableCol[17].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_17", var_list);
	TableCol[18].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_18", var_list);
	TableCol[19].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_19", var_list);
	TableCol[20].Col = var_mapping("SQLColumnPrivileges_TableCol_Col_20", var_list);

	ColumnWC[0].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_0", var_list);
    ColumnWC[0].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_0", var_list);
	ColumnWC[0].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_0", var_list);
	ColumnWC[0].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_0", var_list);

	ColumnWC[1].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_1", var_list);
	ColumnWC[1].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_1", var_list);
	ColumnWC[1].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_1", var_list);
	ColumnWC[1].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_1", var_list);

	ColumnWC[2].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_2", var_list);
	ColumnWC[2].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_2", var_list);
	ColumnWC[2].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_2", var_list);
	ColumnWC[2].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_2", var_list);

	ColumnWC[3].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_3", var_list);
	ColumnWC[3].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_3", var_list);
	ColumnWC[3].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_3", var_list);
	ColumnWC[3].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_3", var_list);

	ColumnWC[4].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_4", var_list);
	ColumnWC[4].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_4", var_list);
	ColumnWC[4].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_4", var_list);
	ColumnWC[4].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_4", var_list);

	ColumnWC[5].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_5", var_list);
	ColumnWC[5].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_5", var_list);
	ColumnWC[5].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_5", var_list);
	ColumnWC[5].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_5", var_list);

	ColumnWC[6].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_6", var_list);
	ColumnWC[6].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_6", var_list);
	ColumnWC[6].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_6", var_list);
	ColumnWC[6].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_6", var_list);

	ColumnWC[7].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_7", var_list);
	ColumnWC[7].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_7", var_list);
	ColumnWC[7].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_7", var_list);
	ColumnWC[7].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_7", var_list);

	ColumnWC[8].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_8", var_list);
	ColumnWC[8].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_8", var_list);
	ColumnWC[8].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_8", var_list);
	ColumnWC[8].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_8", var_list);

	ColumnWC[9].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_9", var_list);
	ColumnWC[9].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_9", var_list);
	ColumnWC[9].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_9", var_list);
	ColumnWC[9].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_9", var_list);

	ColumnWC[10].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_10", var_list);
	ColumnWC[10].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_10", var_list);
	ColumnWC[10].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_10", var_list);
	ColumnWC[10].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_10", var_list);

	ColumnWC[11].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_11", var_list);
	ColumnWC[11].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_11", var_list);
	ColumnWC[11].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_11", var_list);
	ColumnWC[11].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_11", var_list);

	ColumnWC[12].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_12", var_list);
	ColumnWC[12].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_12", var_list);
	ColumnWC[12].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_12", var_list);
	ColumnWC[12].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_12", var_list);

	ColumnWC[13].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_13", var_list);
	ColumnWC[13].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_13", var_list);
	ColumnWC[13].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_13", var_list);
	ColumnWC[13].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_13", var_list);

	ColumnWC[14].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_14", var_list);
	ColumnWC[14].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_14", var_list);
	ColumnWC[14].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_14", var_list);
	ColumnWC[14].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_14", var_list);

	ColumnWC[15].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_15", var_list);
	ColumnWC[15].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_15", var_list);
	ColumnWC[15].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_15", var_list);
	ColumnWC[15].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_15", var_list);

	ColumnWC[16].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_16", var_list);
	ColumnWC[16].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_16", var_list);
	ColumnWC[16].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_16", var_list);
	ColumnWC[16].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_16", var_list);

	ColumnWC[17].TabQua = var_mapping("SQLColumnPrivileges_ColumnWC_TabQua_17", var_list);
	ColumnWC[17].TabOwner = var_mapping("SQLColumnPrivileges_ColumnWC_TabOwner_17", var_list);
	ColumnWC[17].TabName = var_mapping("SQLColumnPrivileges_ColumnWC_TabName_17", var_list);
	ColumnWC[17].ColName = var_mapping("SQLColumnPrivileges_ColumnWC_ColName_17", var_list);

//=================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => MX Specific SQLColumnPrivileges | SQLColumnPriv | colpriv.c\n");

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLColumnPrivileges tests\n");
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

// SEAQUSET new
#ifdef LDAP
/*
        returncode = SQLGetConnectAttr(hdbc, (SQLINTEGER)SQL_ATTR_ROLENAME,
        (SQLCHAR*)Grantor, SQL_MAX_ROLENAME_LEN+2, (SQLINTEGER *) &oGrantorlen);
        if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetConnectAttr"))
        {
                LogAllErrors(henv,hdbc,hstmt);
                TEST_FAILED;
                TEST_RETURN;
        }
*/
/* hardcode it for now */ strcpy (Grantor, "DB__ROOT");
#else
        Grantor = var_mapping("SQLColumnPrivileges_Grantor", var_list);
#endif
// end of sq new

	TESTCASE_END; 
	returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_TRUE,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}// end of setup

	strcpy(TableQualifier,pTestInfo->Catalog);
	strcpy(TableOwner,pTestInfo->Schema);

	TableStr = (char *)malloc(MAX_NOS_SIZE);
	strcpy(Is_Grantable, "");

	i = 0;
	while (_stricmp(TableCol[i].Col,"endloop") != 0)
	{
		sprintf(TableStr,"drop table %s",TableName);
		SQLExecDirect(hstmt,(SQLCHAR*) TableStr,SQL_NTS);	//Clean up

		sprintf(TableStr, "create table %s (%s %s) no partition;",TableName,TableCol[i].Col,TableCol[i].ColType);
		sprintf(Heading,TableStr);
		strcat(Heading,"\n");

		TESTCASE_BEGIN(Heading);

		returncode = SQLExecDirect(hstmt,(SQLCHAR*)TableStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		else
		{
			TESTCASE_END;

			sprintf(TableStr,"GRANT %s ON %s TO \"%s\"",TableCol[i].Privilege,TableName,TableCol[i].Grantee);
			if ((i % 2) == 0)
				strcpy(Is_Grantable, "YES");
			else
				strcpy(Is_Grantable, "NO");
			if (_stricmp(Is_Grantable,"YES") == 0)
				strcat(TableStr, " WITH GRANT OPTION");

			sprintf(Heading,TableStr);
			strcat(Heading,"\n");
			TESTCASE_BEGIN(Heading);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)TableStr,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			TESTCASE_END;

			sprintf(Heading,"Test #%d:",i);
			TESTCASE_BEGIN(Heading);
			if (strlen(TableQualifier) == 0) {
				returncode = SQLColumnPrivileges(hstmt,NULL,0,(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)TableName,(SWORD)strlen(TableName),(SQLCHAR*)TableCol[i].Col,(SWORD)strlen(TableCol[i].Col));
				LogMsg(NONE,"SQLColPriv(hstmt,NULL,0,%s, %d, %s, %d, %s, %d)\n",  (SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)TableName,(SWORD)strlen(TableName),(SQLCHAR*)TableCol[i].Col,(SWORD)strlen(TableCol[i].Col));
			} else {
				returncode = SQLColumnPrivileges(hstmt,(SQLCHAR*)TableQualifier,(SWORD)strlen(TableQualifier),(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)TableName,(SWORD)strlen(TableName),(SQLCHAR*)TableCol[i].Col,(SWORD)strlen(TableCol[i].Col));
				LogMsg(NONE,"SQLColPriv(hstmt,%s ,%d ,%s, %d, %s, %d, %s, %d)\n", (SQLCHAR*)TableQualifier,(SWORD)strlen(TableQualifier),(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)TableName,(SWORD)strlen(TableName),(SQLCHAR*)TableCol[i].Col,(SWORD)strlen(TableCol[i].Col));
			}
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumnPrivileges"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			else
			{
				strcpy(oTableQualifier,"");
				strcpy(oTableOwner,"");
				strcpy(oTableName,"");
				strcpy(oColName,"");
				strcpy(oGrantor,"");
				strcpy(oGrantee,"");
				strcpy(oPrivilege,"");
				strcpy(oIs_Grantable,"");
				returncode = SQLBindCol(hstmt,1,SQL_C_CHAR,oTableQualifier,NAME_LEN,&oTableQualifierlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,2,SQL_C_CHAR,oTableOwner,NAME_LEN,&oTableOwnerlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,3,SQL_C_CHAR,oTableName,NAME_LEN,&oTableNamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}

				returncode = SQLBindCol(hstmt,4,SQL_C_CHAR,oColName,NAME_LEN,&oColNamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,5,SQL_C_CHAR,oGrantor,NAME_LEN,&oGrantorlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,6,SQL_C_CHAR,oGrantee,NAME_LEN,&oGranteelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				
				returncode = SQLBindCol(hstmt,7,SQL_C_CHAR,oPrivilege,NAME_LEN,&oPrivilegelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,8,SQL_C_CHAR,oIs_Grantable,NAME_LEN,&oIs_Grantablelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}

				do 
				{
					returncode = SQLFetch(hstmt);
				} while ((returncode == SQL_SUCCESS) &&
					(_stricmp(oGrantor,Grantor)));
				
				if((returncode!=SQL_NO_DATA_FOUND) && (!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				else if (returncode == SQL_SUCCESS)
				{
					sprintf(Heading,"\nSQLColumnPrivileges: compare results of columns fetched for following column \n");
					strcat(Heading,"The Column Name is "); 
					strcat(Heading,TableCol[i].Col);
					strcat(Heading,"\n");
					LogMsg(NONE,Heading);

					if (cstrcmp(TableQualifier,oTableQualifier,TRUE,isCharSet) == 0) {
						//LogMsg(NONE,"TableQualifier expect: %s and actual: %s are matched\n",TableQualifier,oTableQualifier);
					}
					else {
						LogMsg(ERRMSG,"TableQualifier expect: %s and actual: %s are not matched\n",TableQualifier,oTableQualifier);
						TEST_FAILED;	
					}

					if (cstrcmp(TableOwner,oTableOwner,TRUE,isCharSet) == 0) {
						//LogMsg(NONE,"TableOwner expect: %s and actual: %s are matched\n",TableOwner,oTableOwner);
					}
					else {
						LogMsg(ERRMSG,"TableOwner expect: %s and actual: %s are not matched\n",TableOwner,oTableOwner);
						TEST_FAILED;	
					}

					if(cstrcmp(TableName,oTableName,TRUE,isCharSet) == 0) {
						//LogMsg(NONE,"TableName expect: %s and actual: %s are matched\n",TableName,oTableName);
					}
					else {
						LogMsg(ERRMSG,"TableName expect: %s and actual: %s are not matched\n",TableName,oTableName);
						TEST_FAILED;	
					}

					if (cstrcmp(TableCol[i].Col,oColName,TRUE,isCharSet) == 0) {
						//LogMsg(NONE,"ColName expect: %s and actual: %s are matched\n",TableCol[i].Col,oColName);
					}
					else {
						LogMsg(ERRMSG,"ColName expect: %s and actual: %s are not matched\n",TableCol[i].Col,oColName);
						TEST_FAILED;	
					}

					if(_stricmp(oGrantor,Grantor) == 0) {
						//LogMsg(NONE,"Grantor expect: %s and actual: %s are matched\n",Grantor,oGrantor);
					}
					else {
						LogMsg(ERRMSG,"Grantor expect: %s and actual: %s are not matched\n",Grantor,oGrantor);
						TEST_FAILED;	
					}

					if (_stricmp(oGrantee,TableCol[i].Grantee) == 0) {
						//LogMsg(NONE,"Grantee expect: %s and actual: %s are matched\n",TableCol[i].Grantee,oGrantee);
					}
					else {
						LogMsg(ERRMSG,"Grantee expect: %s and actual: %s are not matched\n",TableCol[i].Grantee,oGrantee);
						TEST_FAILED;	
					}

					if (_stricmp(TableCol[i].Privilege,oPrivilege) == 0) {
						//LogMsg(NONE,"Privilege expect: %s and actual: %s are matched\n",TableCol[i].Privilege,oPrivilege);
					}
					else {
						LogMsg(ERRMSG,"Privilege expect: %s and actual: %s are not matched\n",TableCol[i].Privilege,oPrivilege);
						TEST_FAILED;	
					}

					if (_stricmp(Is_Grantable,oIs_Grantable) == 0) {
						//LogMsg(NONE,"Is_Grantable expect: %s and actual: %s are matched\n",Is_Grantable,oIs_Grantable);
					}
					else
					{
						LogMsg(ERRMSG,"Is_Grantable expect: %s and actual: %s are not matched\n",Is_Grantable,oIs_Grantable);
						TEST_FAILED;	
					}
				}
				else
				{
					LogMsg(ERRMSG,"No Data Found => Atleast one row should be fetched. line %d\n", __LINE__);
					TEST_FAILED;
				}
			}
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);
		}
		TESTCASE_END;

		strcpy(TableStr,"");
		sprintf(TableStr,"REVOKE %s ON %s FROM \"%s\"",TableCol[i].Privilege,TableName,TableCol[i].Grantee);
		sprintf(Heading,TableStr);
		strcat(Heading,"\n");

		TESTCASE_BEGIN(Heading);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)TableStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;
		sprintf(TableStr,"drop table %s",TableName);
		SQLExecDirect(hstmt,(SQLCHAR*) TableStr,SQL_NTS);
		i++;
	} 

//=======================================================================================

	returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_FALSE,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	i = 0;
	sprintf(TableStr,"drop table %s.%s.%s",ColumnWC[i].TabQua, ColumnWC[i].TabOwner, ColumnWC[i].TabName);
	SQLExecDirect(hstmt,(SQLCHAR*) TableStr,SQL_NTS);
	sprintf(TableStr,"drop schema %s.%s cascade",ColumnWC[i].TabQua, ColumnWC[i].TabOwner);
	SQLExecDirect(hstmt,(SQLCHAR*) TableStr,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
	}
	else
	{
		sprintf(TableStr,"create schema %s.%s",ColumnWC[i].TabQua, ColumnWC[i].TabOwner);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*) TableStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		else
		{
			sprintf(TableStr,"create table %s.%s.%s(%s char(10)) no partition;",ColumnWC[i].TabQua, ColumnWC[i].TabOwner, ColumnWC[i].TabName, ColumnWC[i].ColName);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*) TableStr,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
		}
	}
	if (returncode == SQL_SUCCESS) 
	{
		while (_stricmp(ColumnWC[i].TabQua,"endloop") != 0)
		{
            sprintf(Heading,"SQLColumnPrivileges: wildcard options => \n"
				" Table Qualifier: %s\n Table Owner: %s\n Table Name: %s\n Column Name: %s \n",
				printSymbol(ColumnWC[i].TabQua,displayBuf.cat),
                printSymbol(ColumnWC[i].TabOwner,displayBuf.sch),
				printSymbol(ColumnWC[i].TabName,displayBuf.tab),
                printSymbol(ColumnWC[i].ColName,displayBuf.col));
			TESTCASE_BEGIN(Heading);
			if (_stricmp(ColumnWC[i].TabQua,"NULL") == 0)
				ColumnWC[i].TabQua = NULL;
			if (_stricmp(ColumnWC[i].TabOwner,"NULL") == 0)
				ColumnWC[i].TabOwner = NULL;
			if (_stricmp(ColumnWC[i].TabName,"NULL") == 0)
				ColumnWC[i].TabName = NULL;

			if (ColumnWC[i].TabQua == NULL || ColumnWC[i].TabOwner == NULL || ColumnWC[i].TabName == NULL)
				returncode = SQLColumnPrivileges(hstmt,(SQLCHAR*)ColumnWC[i].TabQua,SQL_NTS,
                                                       (SQLCHAR*)ColumnWC[i].TabOwner,SQL_NTS,
                                                       (SQLCHAR*)ColumnWC[i].TabName,SQL_NTS,
                                                       (SQLCHAR*)removeQuotes(ColumnWC[i].ColName,displayBuf.col),SQL_NTS);
			else
				returncode = SQLColumnPrivileges(hstmt,(SQLCHAR*)ColumnWC[i].TabQua,(SWORD)strlen(ColumnWC[i].TabQua),
													   (SQLCHAR*)ColumnWC[i].TabOwner,(SWORD)strlen(ColumnWC[i].TabOwner),
                                                       (SQLCHAR*)removeQuotes(ColumnWC[i].TabName,displayBuf.tab),(SWORD)strlen(displayBuf.tab),
                                                       (SQLCHAR*)removeQuotes(ColumnWC[i].ColName,displayBuf.col),(SWORD)strlen(displayBuf.col));			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumnPrivileges"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				LogMsg(NONE,"SQLColumnPrivileges: SQLColumnPrivileges function call executed correctly.\n");
				strcpy(oTableQualifier,"");
				strcpy(oTableOwner,"");
				strcpy(oTableName,"");
				strcpy(oColName,"");
				strcpy(oGrantor,"");
				strcpy(oGrantee,"");
				strcpy(oPrivilege,"");
				strcpy(oIs_Grantable,"");
				returncode = SQLBindCol(hstmt,1,SQL_C_CHAR,oTableQualifier,NAME_LEN,&oTableQualifierlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				} 

				returncode = SQLBindCol(hstmt,2,SQL_C_CHAR,oTableOwner,NAME_LEN,&oTableOwnerlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,3,SQL_C_CHAR,oTableName,NAME_LEN,&oTableNamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}

				returncode = SQLBindCol(hstmt,4,SQL_C_CHAR,oColName,NAME_LEN,&oColNamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,5,SQL_C_CHAR,oGrantor,NAME_LEN,&oGrantorlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,6,SQL_C_CHAR,oGrantee,NAME_LEN,&oGranteelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				
				returncode = SQLBindCol(hstmt,7,SQL_C_CHAR,oPrivilege,NAME_LEN,&oPrivilegelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,8,SQL_C_CHAR,oIs_Grantable,NAME_LEN,&oIs_Grantablelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				k = 0;
				while (returncode == SQL_SUCCESS) 
				{
					returncode = SQLFetch(hstmt);
					if((returncode!=SQL_NO_DATA_FOUND) && (!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					if (returncode == SQL_SUCCESS)
						k++;
				}
				if(k == 0 && ColumnWC[i].CheckCode == SQL_SUCCESS)
				{
					TEST_FAILED;
					LogMsg(ERRMSG,"No Data Found => Atleast one row should be fetched line %d\n", __LINE__);
				} else {
                    LogMsg(NONE,"Number of rows fetched: %d\n", k);
                }
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			TESTCASE_END;
			i++;
		}
	}


	// Cleanup
	i = 0;
	sprintf(TableStr,"drop table %s.%s.%s",ColumnWC[i].TabQua, ColumnWC[i].TabOwner, ColumnWC[i].TabName);
	SQLExecDirect(hstmt,(SQLCHAR*) TableStr,SQL_NTS);
	sprintf(TableStr,"drop schema %s.%s cascade",ColumnWC[i].TabQua, ColumnWC[i].TabOwner);
	SQLExecDirect(hstmt,(SQLCHAR*) TableStr,SQL_NTS);

//==================================================================================================

	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => MX Specific SQLColumnPrivileges.\n");
	free(TableStr);
	free_list(var_list);
	TEST_RETURN;
}
