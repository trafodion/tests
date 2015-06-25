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
#define NUM_TABLE_OUTPUTS		8
#define REM_LEN					254									 
#define TabType_LEN				30
#define	RGB_MAX_LEN				50
#define STR_LEN					128+1    //added to test SQLBindCols and SQLFetch
#define TOTALATTRIBS			18

/*
---------------------------------------------------------
TestSQLTables()
Tests the SQLTables function in ODBC, also tests wildcard
syntax of parser.
---------------------------------------------------------
*/

PassFail TestMXSQLTables (TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	char			Heading[MAX_HEADING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt, hstmt1;
	CHAR			TableQualifier[NAME_LEN],TableOwner[NAME_LEN],Remark[REM_LEN],*TableStr;
	CHAR			oTableQualifier[NAME_LEN];
	CHAR			oTableOwner[NAME_LEN];
	CHAR			oTableName[NAME_LEN];
	CHAR			oTableType[NAME_LEN];
	CHAR			oRemark[REM_LEN];
	SQLLEN			oTableQualifierlen,oTableOwnerlen,oTableNamelen,oTableTypelen,oRemarklen;

	int				cols, iatt;
	SWORD numOfCols = 0;
	SWORD pcbDesc;
	SQLLEN pfDesc;
	CHAR cn[TabType_LEN];
	SWORD cl;
	SWORD st;
	SQLULEN cp;
	SWORD cs, cnull;
	CHAR rgbDesc[RGB_MAX_LEN];
	CHAR *CharOutput[12];
	SQLLEN stringlength;
	struct
	{
		CHAR		*TableName;
		CHAR		*TableType;
		CHAR		*TableTypeIn;
	} Table[] = {
							{"--"	,"TABLE"	,""},
							{"--"	,"TABLE"	,"TABLE"},
							{"--"	,"TABLE"	,"TABLE,VIEW,SYSTEM TABLE"}, 
							{"--"	,"TABLE"	,"TABLE,SYSTEM TABLE,VIEW"},
							{"--"	,"TABLE"	,"TABLE,VIEW,SYSTEM TABLE,SYNONYM,MV,MVG"},
							{"--"	,"VIEW","VIEW"},
							{"--"	,"VIEW","TABLE,VIEW,SYSTEM TABLE"},
							{"--"	,"MATERIALIZED VIEW",""}, 
							{"--"	,"MATERIALIZED VIEW","MV"},
							{"--"	,"SYNONYM",""}, 
							{"--"	,"SYNONYM","SYNONYM"},
							{"endloop",}
					};

	struct
	{
		CHAR		*TabQua;
		CHAR		*TabOwner;
		CHAR		*TabName;
		CHAR		*TabType;
		int			changedSchema;
	} TableWC[] = 
						{		
							{SQL_ALL_CATALOGS	,""					,"--"	,""						,-1},		//0
							{""					,SQL_ALL_SCHEMAS	,"--"	,""						,-1},		//1
							{""					,""					,"--"	,SQL_ALL_TABLE_TYPES	,-1},		//2
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//3
							{pTestInfo->Catalog	,SQL_ALL_SCHEMAS	,"--"	,SQL_ALL_TABLE_TYPES	,-1},		//4
							{pTestInfo->Catalog	,SQL_ALL_SCHEMAS	,"--"	,SQL_ALL_TABLE_TYPES	,-1},		//5
							{pTestInfo->Catalog	,SQL_ALL_SCHEMAS	,"--"	,"TABLE"				,-1},		//6
							{pTestInfo->Catalog	,SQL_ALL_SCHEMAS	,"--"	,SQL_ALL_TABLE_TYPES	,-1},		//7
							{pTestInfo->Catalog	,SQL_ALL_SCHEMAS	,"--"	,SQL_ALL_TABLE_TYPES	,-1},		//8
							{pTestInfo->Catalog	,SQL_ALL_SCHEMAS	,"--"	,"TABLE"				,-1},		//9
							{pTestInfo->Catalog	,"--"				,"--"	,"TABLE"				,1},		//10
							{pTestInfo->Catalog	,"--"				,"--"	,"TABLE"				,1},		//11
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//12
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//13
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,SQL_ALL_TABLE_TYPES	,-1},		//14
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//15
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//16
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//17
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//18
							{pTestInfo->Catalog	,SQL_ALL_SCHEMAS	,"--"	,SQL_ALL_TABLE_TYPES	,-1},		//19
							{pTestInfo->Catalog	,SQL_ALL_SCHEMAS	,"--"	,"TABLE"				,-1},		//20
							{pTestInfo->Catalog	,SQL_ALL_SCHEMAS	,"--"	,"TABLE"				,-1},		//21
							{pTestInfo->Catalog	,"--"				,"--"	,"TABLE"				,1},		//22
							{pTestInfo->Catalog	,SQL_ALL_SCHEMAS	,"--"	,"TABLE"				,-1},		//23
							{pTestInfo->Catalog	,"--"				,"--"	,"TABLE"				,1},		//24
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//25
							{pTestInfo->Catalog	,"--"				,"--"	,"TABLE"				,1},		//26
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"VIEW"					,-1},		//27
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//28
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,SQL_ALL_TABLE_TYPES	,-1},		//29
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//30
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"VIEW"					,-1},		//31
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//32
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//33
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//34
							{"NULL"				,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//35
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//36
							{pTestInfo->Catalog	,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//37
							{"NULL"				,"--"				,"--"	,"TABLE"				,0},		//38
							{"NULL"				,pTestInfo->Schema	,"--"	,"TABLE"				,-1},		//39
							{"NULL"				,"NULL"				,"--"	,"TABLE"				,-1},		//40
							{pTestInfo->Catalog	,"--"				,"--"	,SQL_ALL_TABLE_TYPES	,0},		//41
							{pTestInfo->Catalog	,"--"				,"--"	,SQL_ALL_TABLE_TYPES	,0},		//42
							{pTestInfo->Catalog	,"--"				,"--"	,SQL_ALL_TABLE_TYPES	,2},		//43
							{"endloop",}
						};	

	struct
	{
		CHAR		*TabQua;
		SWORD		TabQuaLen;
		CHAR		*TabOwner;
		SWORD		TabOwnerLen;
		CHAR		*TabName;
		SWORD		TabNameLen;
		CHAR		*TabType;
		SWORD		TabTypeLen;
	} TableWC2[] = {		// wild cards from here
							{pTestInfo->Catalog, (SWORD)-1, pTestInfo->Schema,(SWORD)-1, "--",(SWORD)-1, "", (SWORD)-1},
							//{pTestInfo->Catalog, (SWORD)4, pTestInfo->Schema,(SWORD)2, "OBJECTS",(SWORD)2, "", (SWORD)2},
							//{pTestInfo->Catalog, (SWORD)3, pTestInfo->Schema,(SWORD)7, "OBJECTS",(SWORD)3, "", (SWORD)0},
							{"endloop",}
						};
	//attributes for columns added for negative testing
	UWORD DescrType[] = 
				{
					SQL_COLUMN_AUTO_INCREMENT,SQL_COLUMN_CASE_SENSITIVE,SQL_COLUMN_COUNT,
					SQL_COLUMN_DISPLAY_SIZE,SQL_COLUMN_LENGTH,SQL_COLUMN_MONEY,
					SQL_COLUMN_NULLABLE,SQL_COLUMN_PRECISION,SQL_COLUMN_SCALE,
					SQL_COLUMN_SEARCHABLE,SQL_COLUMN_TYPE,SQL_COLUMN_UNSIGNED,
					SQL_COLUMN_UPDATABLE,SQL_COLUMN_NAME,SQL_COLUMN_TYPE_NAME,
					SQL_COLUMN_OWNER_NAME,SQL_COLUMN_QUALIFIER_NAME,SQL_COLUMN_TABLE_NAME,
					SQL_COLUMN_LABEL
				};

    struct {
        char cat[STR_LEN];
        char sch[STR_LEN];
        char tab[STR_LEN];
        char typ[STR_LEN];
    } displayBuf;
	
	int	i = 0, k = 0, NullValue = 0;
	char tmpSchema[129];
	char schemaList[3][256];
	int myInd=1;
	int len = strlen(pTestInfo->Schema);

	CHAR *CrtCol[] = { "--", "--" };
	CHAR *DrpTab[] = { "--", "--", "--"};
	CHAR *CrtTab[] = { "--", "--", "--"};

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLTables", charset_file);
	if (var_list == NULL) return FAILED;

	Table[0].TableName = var_mapping("SQLTables_Table_TableName_0", var_list);
	Table[1].TableName = var_mapping("SQLTables_Table_TableName_1", var_list);
	Table[2].TableName = var_mapping("SQLTables_Table_TableName_2", var_list);
	Table[3].TableName = var_mapping("SQLTables_Table_TableName_3", var_list);
	Table[4].TableName = var_mapping("SQLTables_Table_TableName_4", var_list);
	Table[5].TableName = var_mapping("SQLTables_Table_TableName_5", var_list);
	Table[6].TableName = var_mapping("SQLTables_Table_TableName_6", var_list);
	Table[7].TableName = var_mapping("SQLTables_Table_TableName_7", var_list);
	Table[8].TableName = var_mapping("SQLTables_Table_TableName_8", var_list);
	Table[9].TableName = var_mapping("SQLTables_Table_TableName_9", var_list);
	Table[10].TableName = var_mapping("SQLTables_Table_TableName_10", var_list);
	
	TableWC[10].TabOwner = var_mapping("SQLTables_TableWC_TabOwner_10", var_list);
	TableWC[11].TabOwner = var_mapping("SQLTables_TableWC_TabOwner_11", var_list);
	TableWC[22].TabOwner = var_mapping("SQLTables_TableWC_TabOwner_22", var_list);
	TableWC[24].TabOwner = var_mapping("SQLTables_TableWC_TabOwner_24", var_list);
	TableWC[26].TabOwner = var_mapping("SQLTables_TableWC_TabOwner_26", var_list);
	TableWC[38].TabOwner = var_mapping("SQLTables_TableWC_TabOwner_38", var_list);
	TableWC[41].TabOwner = var_mapping("SQLTables_TableWC_TabOwner_10", var_list);
	TableWC[42].TabOwner = var_mapping("SQLTables_TableWC_TabOwner_41", var_list);
	TableWC[43].TabOwner = var_mapping("SQLTables_TableWC_TabOwner_43", var_list);

	TableWC[0].TabName = var_mapping("SQLTables_TableWC_TabName_0", var_list);
	TableWC[1].TabName = var_mapping("SQLTables_TableWC_TabName_1", var_list);
	TableWC[2].TabName = var_mapping("SQLTables_TableWC_TabName_2", var_list);
	TableWC[3].TabName = var_mapping("SQLTables_TableWC_TabName_3", var_list);
	TableWC[4].TabName = var_mapping("SQLTables_TableWC_TabName_4", var_list);
	TableWC[5].TabName = var_mapping("SQLTables_TableWC_TabName_5", var_list);
	TableWC[6].TabName = var_mapping("SQLTables_TableWC_TabName_6", var_list);
	TableWC[7].TabName = var_mapping("SQLTables_TableWC_TabName_7", var_list);
	TableWC[8].TabName = var_mapping("SQLTables_TableWC_TabName_8", var_list);
	TableWC[9].TabName = var_mapping("SQLTables_TableWC_TabName_9", var_list);
	TableWC[10].TabName = var_mapping("SQLTables_TableWC_TabName_10", var_list);
	TableWC[11].TabName = var_mapping("SQLTables_TableWC_TabName_11", var_list);
	TableWC[12].TabName = var_mapping("SQLTables_TableWC_TabName_12", var_list);
	TableWC[13].TabName = var_mapping("SQLTables_TableWC_TabName_13", var_list);
	TableWC[14].TabName = var_mapping("SQLTables_TableWC_TabName_14", var_list);
	TableWC[15].TabName = var_mapping("SQLTables_TableWC_TabName_15", var_list);
	TableWC[16].TabName = var_mapping("SQLTables_TableWC_TabName_16", var_list);
	TableWC[17].TabName = var_mapping("SQLTables_TableWC_TabName_17", var_list);
	TableWC[18].TabName = var_mapping("SQLTables_TableWC_TabName_18", var_list);
	TableWC[19].TabName = var_mapping("SQLTables_TableWC_TabName_19", var_list);
	TableWC[20].TabName = var_mapping("SQLTables_TableWC_TabName_20", var_list);
	TableWC[21].TabName = var_mapping("SQLTables_TableWC_TabName_21", var_list);
	TableWC[22].TabName = var_mapping("SQLTables_TableWC_TabName_22", var_list);
	TableWC[23].TabName = var_mapping("SQLTables_TableWC_TabName_23", var_list);
	TableWC[24].TabName = var_mapping("SQLTables_TableWC_TabName_24", var_list);
	TableWC[25].TabName = var_mapping("SQLTables_TableWC_TabName_25", var_list);
	TableWC[26].TabName = var_mapping("SQLTables_TableWC_TabName_26", var_list);
	TableWC[27].TabName = var_mapping("SQLTables_TableWC_TabName_27", var_list);
	TableWC[28].TabName = var_mapping("SQLTables_TableWC_TabName_28", var_list);
	TableWC[29].TabName = var_mapping("SQLTables_TableWC_TabName_29", var_list);
	TableWC[30].TabName = var_mapping("SQLTables_TableWC_TabName_30", var_list);
	TableWC[31].TabName = var_mapping("SQLTables_TableWC_TabName_31", var_list);
	TableWC[32].TabName = var_mapping("SQLTables_TableWC_TabName_32", var_list);
	TableWC[33].TabName = var_mapping("SQLTables_TableWC_TabName_33", var_list);
	TableWC[34].TabName = var_mapping("SQLTables_TableWC_TabName_34", var_list);
	TableWC[35].TabName = var_mapping("SQLTables_TableWC_TabName_35", var_list);
	TableWC[36].TabName = var_mapping("SQLTables_TableWC_TabName_36", var_list);
	TableWC[37].TabName = var_mapping("SQLTables_TableWC_TabName_37", var_list);
	TableWC[38].TabName = var_mapping("SQLTables_TableWC_TabName_38", var_list);
	TableWC[39].TabName = var_mapping("SQLTables_TableWC_TabName_39", var_list);
	TableWC[40].TabName = var_mapping("SQLTables_TableWC_TabName_40", var_list);
	TableWC[41].TabName = var_mapping("SQLTables_TableWC_TabName_41", var_list);
	TableWC[42].TabName = var_mapping("SQLTables_TableWC_TabName_42", var_list);
	TableWC[43].TabName = var_mapping("SQLTables_TableWC_TabName_43", var_list);

	TableWC2[0].TabName = var_mapping("SQLTables_TableWC2_TabName_0", var_list);

	CrtCol[0] = var_mapping("SQLTables_CrtCol_0", var_list);
	CrtCol[1] = var_mapping("SQLTables_CrtCol_1", var_list);

	DrpTab[0] = var_mapping("SQLTables_DrpTab_0", var_list);
	DrpTab[1] = var_mapping("SQLTables_DrpTab_1", var_list);
	DrpTab[2] = var_mapping("SQLTables_DrpTab_2", var_list);

	CrtTab[0] = var_mapping("SQLTables_CrtTab_0", var_list);
	CrtTab[1] = var_mapping("SQLTables_CrtTab_1", var_list);
	CrtTab[2] = var_mapping("SQLTables_CrtTab_2", var_list);
//===========================================================================================================
	myInd = len - 2;
	if (len>5) myInd=4;

	strncpy (schemaList[0],pTestInfo->Schema,myInd);
	schemaList[0][myInd]='%';schemaList[0][myInd+1]='\0';
	strncpy (schemaList[1],pTestInfo->Schema,myInd+1);
	schemaList[1][myInd+1]='%';schemaList[1][myInd+2]='\0';

    if(isCharSet==TRUE) {
        sprintf(tmpSchema, "\"SQLTABLES_%s\"", pTestInfo->Schema);
        sprintf(schemaList[2], pTestInfo->Schema);
    }
    else {
	    sprintf(tmpSchema, "SQLTABLES_%s", pTestInfo->Schema);
	    strupr(tmpSchema);

        len = 0; myInd = 0;
	    // Be careful with this when using 2-byte encoding
	    do {
		    if (pTestInfo->Schema[myInd] == '_')
			    schemaList[2][len++] = '\\';
		    schemaList[2][len++] = pTestInfo->Schema[myInd];
	    } while (pTestInfo->Schema[myInd++] != '\0');
    }

    LogMsg(NONE,"%s %s %s\n", schemaList[0], schemaList[1], schemaList[2]);

//======================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => MX SPECIFIC SQLTables | SQLTables | tables.c\n");

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLTables tests\n");
	// for ODBC 3.0
	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,"Unable to connect as ODBC3.0 application.\n");
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else
	{
		LogMsg(NONE,"Allocate a stmt handle successfully.\n");
	}

   TESTCASE_END;

	if (returncode == SQL_SUCCESS)
	{
        sprintf(Heading,"drop schema %s.%s cascade",pTestInfo->Catalog,tmpSchema);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)Heading, SQL_NTS);
        sprintf(Heading,"create schema %s.%s",pTestInfo->Catalog,tmpSchema);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)Heading, SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

        sprintf(Heading,"set schema %s.%s",pTestInfo->Catalog,tmpSchema);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)Heading, SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		strcpy(TableQualifier,pTestInfo->Catalog);
		strcpy(TableOwner, tmpSchema);
		strcpy(Remark,"");
		TableStr = (char *)malloc(MAX_NOS_SIZE);

		i = 0;
		while (_stricmp(Table[i].TableName,"endloop") != 0) // cleanup 
		{
			strcpy(TableStr,"");
			strcat(TableStr,"drop ");
			strcat(TableStr,Table[i].TableType);
			strcat(TableStr," ");
			strcat(TableStr,Table[i].TableName);
			strcat(TableStr," cascade");
			LogMsg(NONE,"Cleanup: %s\n",TableStr);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*) TableStr,SQL_NTS);
			i++;
		}
		
		i = 0;
		while (_stricmp(Table[i].TableName,"endloop") != 0)
		{
			strcpy(TableStr,"");
			strcat(TableStr,"create ");
			strcat(TableStr,Table[i].TableType);
			strcat(TableStr," ");
			strcat(TableStr,Table[i].TableName);
			if (_stricmp(Table[i].TableType,"VIEW") == 0) {
				strcat(TableStr,CrtCol[1]);
				strcat(TableStr, Table[0].TableName);
			}
			else if (_stricmp(Table[i].TableType,"MATERIALIZED VIEW") == 0) {
				strcat(TableStr, " REFRESH ON REQUEST INITIALIZE ON REFRESH ");
				strcat(TableStr,CrtCol[1]);
				strcat(TableStr, Table[0].TableName); 
			}
			else if (_stricmp(Table[i].TableType,"SYNONYM") == 0) {
				strcat(TableStr, " FOR ");
				strcat(TableStr, Table[0].TableName);
			}
			else
			{
				strcat(TableStr,CrtCol[0]);
			}
		
			sprintf(Heading,"SQLTables: Test %d: using the following table create command=> \n",i);
			strcat(Heading,TableStr);
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
				LogMsg(NONE,"Created table successfully.\n");
			}

			if(isCharSet) {
				returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_TRUE,0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr(SQL_ATTR_METADATA_ID"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
			
			if (returncode == SQL_SUCCESS)
			{
				if (strlen(TableQualifier) > 0)
					returncode = SQLTables(hstmt,(SQLCHAR*)TableQualifier,(SWORD)strlen(TableQualifier),(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)Table[i].TableName,(SWORD)strlen(Table[i].TableName),(SQLCHAR*)Table[i].TableTypeIn,(SWORD)strlen(Table[i].TableTypeIn));
				else
					returncode = SQLTables(hstmt,NULL,(SWORD)strlen(TableQualifier),(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)Table[i].TableName,(SWORD)strlen(Table[i].TableName),(SQLCHAR*)Table[i].TableTypeIn,(SWORD)strlen(Table[i].TableTypeIn));
				
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTables"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					LogMsg(NONE,"Call to SQLTables() executed successfully.\n");
					
					strcpy(oTableQualifier,"");
					strcpy(oTableOwner,"");
					strcpy(oTableName,"");
					strcpy(oTableType,"");
					strcpy(oRemark,"");
					returncode=SQLBindCol(hstmt,1,SQL_C_CHAR,oTableQualifier,NAME_LEN,&oTableQualifierlen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")){
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
						}
				   returncode=SQLBindCol(hstmt,2,SQL_C_CHAR,oTableOwner,NAME_LEN,&oTableOwnerlen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")){
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
						}
					returncode=SQLBindCol(hstmt,3,SQL_C_CHAR,oTableName,NAME_LEN,&oTableNamelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")){
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
						}
				   returncode=SQLBindCol(hstmt,4,SQL_C_CHAR,oTableType,NAME_LEN,&oTableTypelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")){
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
						}
					returncode=SQLBindCol(hstmt,5,SQL_C_CHAR,oRemark,NAME_LEN,&oRemarklen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")){
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
						}

					k = 0;
					while (returncode == SQL_SUCCESS)
					{
						returncode = SQLFetch(hstmt);
						if((returncode != SQL_NO_DATA_FOUND)&&(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
						{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
						}
						else if (returncode == SQL_SUCCESS)
						{
							if (strlen(TableQualifier) == 0)
							{
								strcpy(TableQualifier, pTestInfo->Catalog);
							}
							if ((_stricmp(TableQualifier,oTableQualifier) == 0) 
								&& (cstrcmp(TableOwner,oTableOwner,TRUE,isCharSet) == 0) 
								&& (cstrcmp(Table[i].TableName,oTableName,TRUE,isCharSet) == 0) 
								&& (_strnicmp(Table[i].TableType,oTableType,strlen(Table[i].TableType)) == 0) 
								&& (_stricmp(Remark,oRemark) == 0))
							{
								//LogMsg(NONE,"TableQualifier expect: '%s' and actual: '%s' are matched\n",(SQLCHAR*)TableQualifier,oTableQualifier);
								//LogMsg(NONE,"TableOwner expect: '%s' and actual: '%s' are matched\n",(SQLCHAR*)TableOwner,oTableOwner);
								//LogMsg(NONE,"TableName expect: '%s' and actual: '%s' are matched\n",(SQLCHAR*)Table[i].TableName,oTableName);
								//LogMsg(NONE,"TableType expect: '%s' and actual: '%s' are matched\n",Table[i].TableType,oTableType);
								//LogMsg(NONE,"Remark expect: '%s' and actual: '%s' are matched\n",Remark,oRemark);
							}	
							else
							{
								TEST_FAILED;	
								if (_stricmp(TableQualifier,oTableQualifier) != 0)
									LogMsg(ERRMSG,"TableQualifier expect: '%s' and actual: '%s' are not matched\n",(SQLCHAR*)TableQualifier,oTableQualifier);
								if (cstrcmp(TableOwner,oTableOwner,TRUE,isCharSet) != 0) 
									LogMsg(ERRMSG,"TableOwner expect: '%s' and actual: '%s' are not matched\n",(SQLCHAR*)TableOwner,oTableOwner);
								if (cstrcmp(Table[i].TableName,oTableName,TRUE,isCharSet) != 0) 
									LogMsg(ERRMSG,"TableName expect: '%s' and actual: '%s' are not matched\n",(SQLCHAR*)Table[i].TableName,oTableName);
								if (_strnicmp(Table[i].TableType,oTableType,10) != 0) 
									LogMsg(ERRMSG,"TableType expect: '%s' and actual: '%s' are not matched\n",Table[i].TableType,oTableType);
								if (_stricmp(Remark,oRemark) != 0) 
									LogMsg(ERRMSG,"Remark expect: '%s' and actual: '%s' are not matched\n",Remark,oRemark);
							}

							k++;
						}
					}//End while loop

					if(k != 1)
					{
						TEST_FAILED;
						LogMsg(ERRMSG,"Only one row should be fetched, the actual number of rows fetched: %d\n", k);
					} else {
						LogMsg(NONE, "Number of rows fetched: %d\n", k);
					}
				}
				SQLFreeStmt(hstmt,SQL_UNBIND);
				SQLFreeStmt(hstmt,SQL_CLOSE);
			}
			TESTCASE_END;
			i++;
		}
//		i = 0;
//		while (_stricmp(Table[i].TableName,"endloop") != 0) // cleanup
//		{
//			strcpy(TableStr,"");
//			strcat(TableStr,"drop ");
//			strcat(TableStr,Table[i].TableType);
//			strcat(TableStr," ");
//			strcat(TableStr,Table[i].TableName);
//			SQLExecDirect(hstmt,(SQLCHAR*) TableStr,SQL_NTS);
//			i++;
//		}

        sprintf(Heading,"drop schema %s.%s cascade",pTestInfo->Catalog,tmpSchema);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)Heading, SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		if (isCharSet) {
			sprintf(Heading,"set schema %s.\"%s\"",pTestInfo->Catalog,pTestInfo->Schema);
		}
		else {
			sprintf(Heading,"set schema %s.%s",pTestInfo->Catalog,pTestInfo->Schema);
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)Heading, SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

//======================================================================================================
		sprintf(Heading,"Setting up Table & view to test SQLTables for wildcard options => \n");
		strcat(Heading,"\n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[0],SQL_NTS);
		SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[1],SQL_NTS);
		SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[2],SQL_NTS);
		LogMsg(NONE,"%s\n", CrtTab[0]);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[0],SQL_NTS);

		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		else
		{
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[1],SQL_NTS);
			LogMsg(NONE,"%s\n", CrtTab[1]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			else
			{
				LogMsg(NONE,"setting up tables & views executed successfully.\n");
				TESTCASE_END;
			}
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[2],SQL_NTS);
		LogMsg(NONE,"%s\n", CrtTab[2]);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		i = 0;
		while (_stricmp(TableWC[i].TabQua,"endloop") != 0)
		{
			if(TableWC[i].changedSchema == -1)
				sprintf(Heading,"Test Positive Functionality of SQLTables for following wildcard options => \n"
				" TableQualifier: %s\n TableOwner: %s\n TableName: %s\n TableType: %s\n",
				printSymbol(TableWC[i].TabQua,displayBuf.cat),
                printSymbol(TableWC[i].TabOwner,displayBuf.sch),
				printSymbol(TableWC[i].TabName,displayBuf.tab),
                printSymbol(TableWC[i].TabType,displayBuf.typ));
			else
				sprintf(Heading,"Test Positive Functionality of SQLTables for following wildcard options => \n"
				" TableQualifier: %s\n TableOwner: %s\n TableName: %s\n TableType: %s\n",
				printSymbol(TableWC[i].TabQua,displayBuf.cat),
                schemaList[TableWC[i].changedSchema],
				printSymbol(TableWC[i].TabName,displayBuf.tab),
                printSymbol(TableWC[i].TabType,displayBuf.typ));

			TESTCASE_BEGIN(Heading);
			NullValue = 0;

			returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_FALSE,0);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr(SQL_ATTR_METADATA_ID"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}

			if (_stricmp(TableWC[i].TabType,"NULL") == 0)
			{
				TableWC[i].TabType = NULL;
				NullValue = 1;
				returncode = SQLTables(hstmt,NULL,0,NULL,0,NULL,0,NULL,0);
			}
			else if (_stricmp(TableWC[i].TabName,"NULL") == 0)
			{
				TableWC[i].TabName = NULL;
				NullValue = 1;
				returncode = SQLTables(hstmt,NULL,0,NULL,0,NULL,0,(SQLCHAR*)TableWC[i].TabType,(SWORD)strlen(TableWC[i].TabType));
			}
			else if (_stricmp(TableWC[i].TabOwner,"NULL") == 0)
			{
				TableWC[i].TabOwner = NULL;
				NullValue = 1;
				returncode = SQLTables(hstmt,NULL,0,NULL,0,(SQLCHAR*)removeQuotes(TableWC[i].TabName,displayBuf.tab),(SWORD)strlen(displayBuf.tab),(SQLCHAR*)TableWC[i].TabType,(SWORD)strlen(TableWC[i].TabType));
			}
			else if (_stricmp(TableWC[i].TabQua,"NULL") == 0)
			{
				TableWC[i].TabQua = NULL;
				NullValue = 1;
				if (TableWC[i].changedSchema == -1)
					returncode = SQLTables(hstmt,NULL,0,(SQLCHAR*)TableWC[i].TabOwner,(SWORD)strlen(TableWC[i].TabOwner),(SQLCHAR*)removeQuotes(TableWC[i].TabName,displayBuf.tab),(SWORD)strlen(displayBuf.tab),(SQLCHAR*)TableWC[i].TabType,(SWORD)strlen(TableWC[i].TabType));
				else
					returncode = SQLTables(hstmt,NULL,0,(SQLCHAR*)schemaList[TableWC[i].changedSchema],(SWORD)strlen(schemaList[TableWC[i].changedSchema]),(SQLCHAR*)removeQuotes(TableWC[i].TabName,displayBuf.tab),(SWORD)strlen(displayBuf.tab),(SQLCHAR*)TableWC[i].TabType,(SWORD)strlen(TableWC[i].TabType));
			}
			else
			{
				if (TableWC[i].changedSchema == -1)
					returncode = SQLTables(hstmt,(SQLCHAR*)TableWC[i].TabQua,(SWORD)strlen(TableWC[i].TabQua),(SQLCHAR*)TableWC[i].TabOwner,(SWORD)strlen(TableWC[i].TabOwner),(SQLCHAR*)removeQuotes(TableWC[i].TabName,displayBuf.tab),(SWORD)strlen(displayBuf.tab),(SQLCHAR*)TableWC[i].TabType,(SWORD)strlen(TableWC[i].TabType));
				else
					returncode = SQLTables(hstmt,(SQLCHAR*)TableWC[i].TabQua,(SWORD)strlen(TableWC[i].TabQua),(SQLCHAR*)schemaList[TableWC[i].changedSchema],(SWORD)strlen(schemaList[TableWC[i].changedSchema]),(SQLCHAR*)removeQuotes(TableWC[i].TabName,displayBuf.tab),(SWORD)strlen(displayBuf.tab),(SQLCHAR*)TableWC[i].TabType,(SWORD)strlen(TableWC[i].TabType));
			}

			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTables"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				LogMsg(NONE,"Call to SQLTables() executed successfully.\n");
				strcpy(oTableQualifier,"");
				strcpy(oTableOwner,"");
				strcpy(oTableName,"");
				strcpy(oTableType,"");
				strcpy(oRemark,"");
				returncode=SQLBindCol(hstmt,1,SQL_C_CHAR,oTableQualifier,NAME_LEN,&oTableQualifierlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,2,SQL_C_CHAR,oTableOwner,NAME_LEN,&oTableOwnerlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,3,SQL_C_CHAR,oTableName,NAME_LEN,&oTableNamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,4,SQL_C_CHAR,oTableType,NAME_LEN,&oTableTypelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,5,SQL_C_CHAR,oRemark,NAME_LEN,&oRemarklen);
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
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
					if (returncode == SQL_SUCCESS)
						k++;
				}
				if(k == 0)
				{
					TEST_FAILED;
					LogMsg(ERRMSG,"No Data Found => Atleast one row should be fetched\n");
                } else {
                    LogMsg(NONE, "Number of rows fetched: %d\n", k);
                }
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			i++;
			TESTCASE_END;
		}
		free(TableStr);
	}

//=========================================================================================

	TESTCASE_BEGIN("SQLTables: Negative test with NULL handle.\n");

	hstmt1 = (SQLHANDLE)NULL;
	i = 0;
	returncode = SQLTables(hstmt1,(SQLCHAR*)TableWC[i].TabQua,(SWORD)strlen(TableWC[i].TabQua),(SQLCHAR*)TableWC[i].TabOwner,(SWORD)strlen(TableWC[i].TabOwner),(SQLCHAR*)TableWC[i].TabName,(SWORD)strlen(TableWC[i].TabName),(SQLCHAR*)TableWC[i].TabType,(SWORD)strlen(TableWC[i].TabType));
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLTables"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("SQLTables: Negative test with invalid arg lengths.\n");
	i = 0;
	while (_stricmp(TableWC2[i].TabQua,"endloop") != 0)
	{
		returncode = SQLTables(hstmt,(SQLCHAR*)TableWC2[i].TabQua,TableWC2[i].TabQuaLen,(SQLCHAR*)TableWC2[i].TabOwner,TableWC2[i].TabOwnerLen,(SQLCHAR*)TableWC2[i].TabName,TableWC2[i].TabNameLen,(SQLCHAR*)TableWC2[i].TabType,TableWC2[i].TabTypeLen);
		if(!CHECKRC(SQL_ERROR,returncode,"SQLTables"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		i++;
	}
	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("Testing SQLColAttribute, SQLDescribeCol, SQLBindCol and SQLFetch functions for catalog names.\n");

    if(isCharSet) {
		returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_FALSE,0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr(SQL_ATTR_METADATA_ID"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
	}

	for(i = 0; i < 5; i++)
	{
		returncode = SQLTables(hstmt,(SQLCHAR*)TableWC[i].TabQua,(SWORD)strlen(TableWC[i].TabQua),(SQLCHAR*)TableWC[i].TabOwner,(SWORD)strlen(TableWC[i].TabOwner),(SQLCHAR*)TableWC[i].TabName,(SWORD)strlen(TableWC[i].TabName),(SQLCHAR*)TableWC[i].TabType,(SWORD)strlen(TableWC[i].TabType));
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumns"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		returncode = SQLNumResultCols(hstmt, &numOfCols);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultsCol"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG,"Test failed while executing call for SQLNUMRESULTSCOL");
			LogAllErrors(henv,hdbc,hstmt);
		}
		for(cols = 0; cols < numOfCols; cols++)
		{
			returncode = SQLDescribeCol(hstmt,(SWORD)(cols+1),(SQLCHAR*)cn,TabType_LEN,&cl,&st,&cp,&cs,&cnull);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDescribeCol"))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,"Test failed while executing call for SQLDESCRIBECOL of column");
				LogAllErrors(henv,hdbc,hstmt);
			}
			CharOutput[cols] = (char *)malloc(STR_LEN);
			for (iatt = 0; iatt <= TOTALATTRIBS; iatt++)
			{
				strcpy(rgbDesc,"");
				pcbDesc = 0;
				pfDesc = 0;
				returncode = SQLColAttributes(hstmt,(SWORD)(cols+1),DescrType[iatt],(SQLCHAR*)rgbDesc,STR_LEN,&pcbDesc,&pfDesc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColAttribute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
			returncode = SQLBindCol(hstmt,(SWORD)(cols+1),SQL_C_CHAR,(SQLCHAR*)CharOutput[cols],STR_LEN,&stringlength);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,"Test failed while executing call for SQLBindCols of column : %d.\n",cols);
				LogAllErrors(henv,hdbc,hstmt);
			}
		}

		k = 0;
		while (returncode == SQL_SUCCESS)
		{
			returncode = SQLFetch(hstmt);
			if((returncode!=SQL_NO_DATA_FOUND) && (!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			if (returncode == SQL_SUCCESS)
				k++;
		}
		if(k == 0)
		{
            sprintf(Heading,"\n"
				" TableQualifier: %s\n TableOwner: %s\n TableName: %s\n TableType: %s\n",
				printSymbol(TableWC[i].TabQua,displayBuf.cat),
                printSymbol(TableWC[i].TabOwner,displayBuf.sch),
				printSymbol(TableWC[i].TabName,displayBuf.tab),
                printSymbol(TableWC[i].TabType,displayBuf.typ));
            LogMsg(NONE,Heading);
			TEST_FAILED;
			LogMsg(ERRMSG,"No Data Found => Atleast one row should be fetched\n");
		} else {
            LogMsg(NONE, "Number of rows fetched: %d\n", k);
        }

		for(cols = 0; cols < numOfCols; cols++)
		{
			free(CharOutput[cols]);
		}
		TESTCASE_END;
	}

	// Clean up
	SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[0],SQL_NTS);
	SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[1],SQL_NTS);
	SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[2],SQL_NTS);

//=========================================================================================

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLTables.\n");
	free_list(var_list);
	TEST_RETURN;
}
