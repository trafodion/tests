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

/* modified test for Launchpad bug 1323835 */
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"


#define NAME_LEN	300
#define NUM_OUTPUTS	8
#define REM_LEN		254
#define NUM_PATTERN	5
#define ACCESS_MODE 2
#define COLNAME_LEN	128+1
#define	RGB_MAX_LEN	50
#define STR_LEN     128+1    //added to test SQLBindCols and SQLFetch

/*
---------------------------------------------------------
   TestSQLColumns for MX Specific (file is columns.c)
---------------------------------------------------------
*/
PassFail TestMXSQLColumns( TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	char		Heading[MAX_HEADING_SIZE];
 	RETCODE		returncode;
 	SQLHANDLE 	henv;
 	SQLHANDLE 	hdbc;
 	SQLHANDLE	hstmt, hstmt1;
	CHAR		TableQualifier[NAME_LEN],TableOwner[NAME_LEN],TableName[NAME_LEN],*TableColStr,*TableStr;
	CHAR		ColInput[NAME_LEN] = "%";
	CHAR		*ColNull[] = {" not null", ""," not null"};
	CHAR		oTableQualifier[NAME_LEN];
	CHAR		oTableOwner[NAME_LEN];
	CHAR		oTableName[NAME_LEN];
	CHAR		oColName[NAME_LEN];
	SWORD		oColDataType;
	CHAR		oColTypeName[NAME_LEN];
	SDWORD		oColPrec;
	SDWORD		oColLen;
	SWORD		oColScale;
	SWORD		oColRadix;
	SWORD		oColNullable;
	CHAR		oRemark[REM_LEN];
	SQLLEN		oTableQualifierlen; //  
	SQLLEN		oTableOwnerlen;
	SQLLEN		oTableNamelen;
	SQLLEN		oColNamelen;
	SQLLEN		oColDataTypelen;
	SQLLEN		oColTypeNamelen;
	SQLLEN		oColPreclen;
	SQLLEN		oColLenlen;
	SQLLEN		oColScalelen;
	SQLLEN		oColRadixlen;
	SQLLEN		oColNullablelen;
	SQLLEN		oRemarklen;

	int cols;
	int	iatt;
	int totatt = 18;
	SWORD numOfCols = 0;
	SWORD pcbDesc;
	SQLLEN pfDesc; //  
	CHAR cn[COLNAME_LEN];
	SWORD cl;
	SWORD st;
	SQLULEN cp; //  
	SWORD cs, cnull;
	CHAR rgbDesc[RGB_MAX_LEN];
	CHAR *CharOutput[40];
	SQLLEN stringlength; //  
	CHAR *TabName;
	CHAR *MVSName[3];

	struct
	{
		CHAR *CrtTab;
		CHAR *DrpTab;
	} TableOps[] = {
		{"--", "--"},	//for normal table
		{"--", "--"},	//for wildcard
		{"--", "--"},	//for view
		{"--", "--"},	//for materialized view
		{"--", "--"}	//for synonym
	};
	
	struct
	{
		UWORD		fOption;
		SQLULEN	vParamInt[ACCESS_MODE];
	} ConnectOption = {	SQL_ACCESS_MODE,
						SQL_MODE_READ_WRITE,
						SQL_MODE_READ_ONLY,
										};
	
	struct
	{
		CHAR		*ColName;
		SWORD		ColDataType;
		CHAR		*ColTypeName;
		CHAR		*ColTypePrec;
		CHAR		*ColTypeOutput;
		SDWORD		ColPrec;												
		SDWORD		ColLen;
		SWORD		ColScale;
		SWORD		ColRadix;
		SWORD		ColNullable;
		CHAR		*Remark;
	} TableCol[] = {
							{"--",SQL_CHAR,"char","(10)","CHAR",10,10,0,0,SQL_NULLABLE,"CHARACTER  CHARACTER SET ISO88591"},
							{"--",SQL_VARCHAR,"varchar","(10)","VARCHAR",10,10,0,0,SQL_NULLABLE,"VARCHAR  CHARACTER SET ISO88591"},
							{"--",SQL_LONGVARCHAR,"long varchar","","LONG VARCHAR",2000,2000,0,0,SQL_NULLABLE,"VARCHAR  CHARACTER SET ISO88591"},
							{"--",SQL_DECIMAL,"decimal","(10,5)","DECIMAL SIGNED",10,12,5,10,SQL_NULLABLE,"SIGNED DECIMAL "},
							{"--",SQL_DECIMAL,"decimal","(5,2) unsigned","DECIMAL UNSIGNED",5,7,2,10,SQL_NULLABLE,"UNSIGNED DECIMAL "},
							{"--",SQL_NUMERIC,"numeric","(10,5)","NUMERIC SIGNED",10,12,5,10,SQL_NULLABLE,"SIGNED NUMERIC "},
							{"--",SQL_NUMERIC,"numeric","(5,2) unsigned","NUMERIC UNSIGNED",5,7,2,10,SQL_NULLABLE,"UNSIGNED NUMERIC "},
							{"--",SQL_SMALLINT,"smallint","","SMALLINT SIGNED",5,2,0,10,SQL_NULLABLE,"SIGNED SMALLINT "},
							{"--",SQL_SMALLINT,"smallint"," unsigned","SMALLINT UNSIGNED",5,2,0,10,SQL_NULLABLE,"UNSIGNED SMALLINT "},
							{"--",SQL_INTEGER,"integer","","INTEGER SIGNED",10,4,0,10,SQL_NULLABLE,"SIGNED INTEGER "},
							{"--",SQL_INTEGER,"integer"," unsigned","INTEGER UNSIGNED",10,4,0,10,SQL_NULLABLE,"UNSIGNED INTEGER "},
							{"--",SQL_BIGINT,"bigint","","BIGINT SIGNED",19,20,0,10,SQL_NULLABLE,"SIGNED LARGEINT "},
							{"--",SQL_REAL,"real","","REAL",22,4,0,2,SQL_NULLABLE,"REAL "},
							{"--",SQL_FLOAT,"float","","FLOAT",54,8,0,2,SQL_NULLABLE,"FLOAT "},
							{"--",SQL_DOUBLE,"double precision","","DOUBLE PRECISION",54,8,0,2,SQL_NULLABLE,"DOUBLE "},
							{"--",SQL_DATE,"date","","DATE",10,6,0,0,SQL_NULLABLE,"DATE "},
							{"--",SQL_TIME,"time","","TIME",8,6,0,0,SQL_NULLABLE,"TIME (0)"},
							{"--",SQL_TIMESTAMP,"timestamp","","TIMESTAMP",26,16,6,0,SQL_NULLABLE,"TIMESTAMP (6)"},
							{"--",SQL_NUMERIC,"numeric","(19,0)","NUMERIC SIGNED",19,21,0,10,SQL_NULLABLE,"SIGNED NUMERIC "},
							{"--",SQL_NUMERIC,"numeric","(19,6)","NUMERIC SIGNED",19,21,6,10,SQL_NULLABLE,"SIGNED NUMERIC "},
							{"--",SQL_NUMERIC,"numeric","(60,30)","NUMERIC SIGNED",60,62,30,10,SQL_NULLABLE,"SIGNED NUMERIC "},
							{"--",SQL_NUMERIC,"numeric","(128,0)","NUMERIC SIGNED",128,130,0,10,SQL_NULLABLE,"SIGNED NUMERIC "},
							{"--",SQL_NUMERIC,"numeric","(128,128)","NUMERIC SIGNED",128,130,128,10,SQL_NULLABLE,"SIGNED NUMERIC "},
							{"--",SQL_NUMERIC,"numeric","(10,5) unsigned","NUMERIC UNSIGNED",10,12,5,10,SQL_NULLABLE,"UNSIGNED NUMERIC "},
							{"--",SQL_NUMERIC,"numeric","(18,5) unsigned","NUMERIC UNSIGNED",18,20,5,10,SQL_NULLABLE,"UNSIGNED NUMERIC "},
							{"--",SQL_NUMERIC,"numeric","(30,10) unsigned","NUMERIC UNSIGNED",30,32,10,10,SQL_NULLABLE,"UNSIGNED NUMERIC "},
							{"endloop",}
						};

	struct
	{
		CHAR		*TabQua;
		CHAR		*TabOwner;
		CHAR		*TabName;
		CHAR		*ColName;
	} ColumnWC[] = {								// wild cards from here --26
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							// testing NULL values
							// Anything with a NULL value for catalog or schema will
							// fail if someting other than default system cat/sch specified
							// because it defaults to what was specifed by the user
							// so for now these have been commented out :-(  this needs
							// to be recoded to deal with this.
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,"%","--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--","--"},
							{"endloop",}
						};

	// same table but with inaccurate lengths added for negative testing
	struct
	{
		CHAR		*TabQua;
		SWORD		TabQuaLen;
		CHAR		*TabOwner;
		SWORD		TabOwnerLen;
		CHAR		*TabName;
		SWORD		TabNameLen;
		CHAR		*ColName;
		SWORD		ColNameLen;
	} ColumnWC2[] = {								/* wild cards from here */
							{pTestInfo->Catalog, (SWORD)-1, pTestInfo->Schema,(SWORD)-1, "",(SWORD)-1, "", (SWORD)-1},
							{"endloop",}
						};

	struct
	{
		CHAR		*TabQua;
		CHAR		*TabOwner;
		CHAR		*TabName;
		CHAR		*ColName;
	} ColumnWC3[] = {								// wild cards from here
							{"--","--","--","--"},
							{"--","--","--","--"},
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



	int	i = 0, k = 0, j = 0, t = 0, NullValue = 0;
	char *charUCS2 = "CHARACTER  CHARACTER SET UCS2";
	char *varcharUCS2 = "VARCHAR  CHARACTER SET UCS2";
	char *charNameUCS2 = "WIDE CHARACTER";
	char *varcharNameUCS2 = "WIDE VARCHAR";
	char *longvarcharNameUCS2 = "WIDE LONG VARCHAR";

    struct {
        char cat[STR_LEN];
        char sch[STR_LEN];
        char tab[STR_LEN];
        char col[STR_LEN];
    } displayBuf;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLColumns", charset_file);
	if (var_list == NULL) return FAILED;
//================Modified for Longvarchar Changes===========================================================
if(!pTestInfo->bLongOn)
{
	 SWORD ColDataType = SQL_VARCHAR;
	 char *ColTypeName = "varchar";
	 char *ColTypePrec = "(2000)";
	 char *ColTypeOutput = "VARCHAR";
	 SDWORD ColPrec = 2000;
	 SDWORD ColLen = 2000;
	 SWORD ColScale = 0;
	 SWORD ColRadix = 0;
	 SWORD ColNullable = SQL_NULLABLE;
	 char *Remark = "VARCHAR  CHARACTER SET ISO88591";

	 TableCol[2].ColTypeName = ColTypeName;
	 TableCol[2].ColDataType = ColDataType;
	 TableCol[2].ColTypePrec = ColTypePrec;
	 TableCol[2].ColTypeOutput = ColTypeOutput;
	 TableCol[2].ColPrec = ColPrec;
	 TableCol[2].ColScale = ColScale;
	 TableCol[2].ColRadix = ColRadix;
	 TableCol[2].Remark = Remark;
}
//================Modified for Longvarchar Changes===========================================================
	TableCol[0].ColName = var_mapping("SQLColumns_TableCol_ColName_0", var_list);
	TableCol[1].ColName = var_mapping("SQLColumns_TableCol_ColName_1", var_list);
	TableCol[2].ColName = var_mapping("SQLColumns_TableCol_ColName_2", var_list);
	TableCol[3].ColName = var_mapping("SQLColumns_TableCol_ColName_3", var_list);
	TableCol[4].ColName = var_mapping("SQLColumns_TableCol_ColName_4", var_list);
	TableCol[5].ColName = var_mapping("SQLColumns_TableCol_ColName_5", var_list);
	TableCol[6].ColName = var_mapping("SQLColumns_TableCol_ColName_6", var_list);
	TableCol[7].ColName = var_mapping("SQLColumns_TableCol_ColName_7", var_list);
	TableCol[8].ColName = var_mapping("SQLColumns_TableCol_ColName_8", var_list);
	TableCol[9].ColName = var_mapping("SQLColumns_TableCol_ColName_9", var_list);
	TableCol[10].ColName = var_mapping("SQLColumns_TableCol_ColName_10", var_list);
	TableCol[11].ColName = var_mapping("SQLColumns_TableCol_ColName_11", var_list);
	TableCol[12].ColName = var_mapping("SQLColumns_TableCol_ColName_12", var_list);
	TableCol[13].ColName = var_mapping("SQLColumns_TableCol_ColName_13", var_list);
	TableCol[14].ColName = var_mapping("SQLColumns_TableCol_ColName_14", var_list);
	TableCol[15].ColName = var_mapping("SQLColumns_TableCol_ColName_15", var_list);
	TableCol[16].ColName = var_mapping("SQLColumns_TableCol_ColName_16", var_list);
	TableCol[17].ColName = var_mapping("SQLColumns_TableCol_ColName_17", var_list);
	TableCol[18].ColName = var_mapping("SQLColumns_TableCol_ColName_18", var_list);
	TableCol[19].ColName = var_mapping("SQLColumns_TableCol_ColName_19", var_list);
	TableCol[20].ColName = var_mapping("SQLColumns_TableCol_ColName_20", var_list);
	TableCol[21].ColName = var_mapping("SQLColumns_TableCol_ColName_21", var_list);
	TableCol[22].ColName = var_mapping("SQLColumns_TableCol_ColName_22", var_list);
	TableCol[23].ColName = var_mapping("SQLColumns_TableCol_ColName_23", var_list);
	TableCol[24].ColName = var_mapping("SQLColumns_TableCol_ColName_24", var_list);
	TableCol[25].ColName = var_mapping("SQLColumns_TableCol_ColName_25", var_list);

	ColumnWC[0].TabName = var_mapping("SQLColumns_ColumnWC_TabName_0", var_list);
	ColumnWC[0].ColName = var_mapping("SQLColumns_ColumnWC_ColName_0", var_list);
	ColumnWC[1].TabName = var_mapping("SQLColumns_ColumnWC_TabName_1", var_list);
	ColumnWC[1].ColName = var_mapping("SQLColumns_ColumnWC_ColName_1", var_list);
	ColumnWC[2].TabName = var_mapping("SQLColumns_ColumnWC_TabName_2", var_list);
	ColumnWC[2].ColName = var_mapping("SQLColumns_ColumnWC_ColName_2", var_list);
	ColumnWC[3].TabName = var_mapping("SQLColumns_ColumnWC_TabName_3", var_list);
	ColumnWC[3].ColName = var_mapping("SQLColumns_ColumnWC_ColName_3", var_list);
	ColumnWC[4].TabName = var_mapping("SQLColumns_ColumnWC_TabName_4", var_list);
	ColumnWC[4].ColName = var_mapping("SQLColumns_ColumnWC_ColName_4", var_list);
	ColumnWC[5].TabName = var_mapping("SQLColumns_ColumnWC_TabName_5", var_list);
	ColumnWC[5].ColName = var_mapping("SQLColumns_ColumnWC_ColName_5", var_list);
	ColumnWC[6].TabName = var_mapping("SQLColumns_ColumnWC_TabName_6", var_list);
	ColumnWC[6].ColName = var_mapping("SQLColumns_ColumnWC_ColName_6", var_list);
	ColumnWC[7].TabName = var_mapping("SQLColumns_ColumnWC_TabName_7", var_list);
	ColumnWC[7].ColName = var_mapping("SQLColumns_ColumnWC_ColName_7", var_list);
	ColumnWC[8].TabName = var_mapping("SQLColumns_ColumnWC_TabName_8", var_list);
	ColumnWC[8].ColName = var_mapping("SQLColumns_ColumnWC_ColName_8", var_list);
	ColumnWC[9].TabName = var_mapping("SQLColumns_ColumnWC_TabName_9", var_list);
	ColumnWC[9].ColName = var_mapping("SQLColumns_ColumnWC_ColName_9", var_list);
	ColumnWC[10].TabName = var_mapping("SQLColumns_ColumnWC_TabName_10", var_list);
	ColumnWC[10].ColName = var_mapping("SQLColumns_ColumnWC_ColName_10", var_list);
	ColumnWC[11].TabName = var_mapping("SQLColumns_ColumnWC_TabName_11", var_list);
	ColumnWC[11].ColName = var_mapping("SQLColumns_ColumnWC_ColName_11", var_list);
	ColumnWC[12].TabName = var_mapping("SQLColumns_ColumnWC_TabName_12", var_list);
	ColumnWC[12].ColName = var_mapping("SQLColumns_ColumnWC_ColName_12", var_list);
	ColumnWC[13].TabName = var_mapping("SQLColumns_ColumnWC_TabName_13", var_list);
	ColumnWC[13].ColName = var_mapping("SQLColumns_ColumnWC_ColName_13", var_list);
	ColumnWC[14].TabName = var_mapping("SQLColumns_ColumnWC_TabName_14", var_list);
	ColumnWC[14].ColName = var_mapping("SQLColumns_ColumnWC_ColName_14", var_list);

	ColumnWC[15].TabName = var_mapping("SQLColumns_ColumnWC_TabName_15", var_list);
	ColumnWC[15].ColName = var_mapping("SQLColumns_ColumnWC_ColName_15", var_list);
	ColumnWC[16].TabName = var_mapping("SQLColumns_ColumnWC_TabName_16", var_list);
	ColumnWC[16].ColName = var_mapping("SQLColumns_ColumnWC_ColName_16", var_list);
	ColumnWC[17].TabName = var_mapping("SQLColumns_ColumnWC_TabName_17", var_list);
	ColumnWC[17].ColName = var_mapping("SQLColumns_ColumnWC_ColName_17", var_list);
	ColumnWC[18].TabName = var_mapping("SQLColumns_ColumnWC_TabName_18", var_list);
	ColumnWC[18].ColName = var_mapping("SQLColumns_ColumnWC_ColName_18", var_list);
	ColumnWC[19].TabName = var_mapping("SQLColumns_ColumnWC_TabName_19", var_list);
	ColumnWC[19].ColName = var_mapping("SQLColumns_ColumnWC_ColName_19", var_list);
	ColumnWC[20].TabName = var_mapping("SQLColumns_ColumnWC_TabName_20", var_list);
	ColumnWC[20].ColName = var_mapping("SQLColumns_ColumnWC_ColName_20", var_list);
	ColumnWC[21].TabName = var_mapping("SQLColumns_ColumnWC_TabName_21", var_list);
	ColumnWC[21].ColName = var_mapping("SQLColumns_ColumnWC_ColName_21", var_list);
	ColumnWC[22].TabName = var_mapping("SQLColumns_ColumnWC_TabName_22", var_list);
	ColumnWC[22].ColName = var_mapping("SQLColumns_ColumnWC_ColName_22", var_list);
	ColumnWC[23].TabName = var_mapping("SQLColumns_ColumnWC_TabName_23", var_list);
	ColumnWC[23].ColName = var_mapping("SQLColumns_ColumnWC_ColName_23", var_list);
	ColumnWC[24].TabName = var_mapping("SQLColumns_ColumnWC_TabName_24", var_list);
	ColumnWC[24].ColName = var_mapping("SQLColumns_ColumnWC_ColName_24", var_list);
	ColumnWC[25].TabName = var_mapping("SQLColumns_ColumnWC_TabName_25", var_list);
	ColumnWC[25].ColName = var_mapping("SQLColumns_ColumnWC_ColName_25", var_list);

	ColumnWC2[0].TabName = var_mapping("SQLColumns_ColumnWC2_TabName_0", var_list);
	ColumnWC2[0].ColName = var_mapping("SQLColumns_ColumnWC2_ColName_0", var_list);

	ColumnWC3[0].TabName = var_mapping("SQLColumns_ColumnWC3_TabName_0", var_list);
	ColumnWC3[0].ColName = var_mapping("SQLColumns_ColumnWC3_ColName_0", var_list);
	ColumnWC3[1].TabName = var_mapping("SQLColumns_ColumnWC3_TabName_1", var_list);
	ColumnWC3[1].ColName = var_mapping("SQLColumns_ColumnWC3_ColName_1", var_list);

	TabName    = var_mapping("SQLColumns_TableName", var_list);
	MVSName[0] = var_mapping("SQLColumns_ViewName", var_list);
	MVSName[1] = var_mapping("SQLColumns_MVName", var_list);
	MVSName[2] = var_mapping("SQLColumns_SynonymName", var_list);

	TableOps[0].CrtTab = var_mapping("SQLColumns_TableOps_CrtTab_0", var_list);
	TableOps[0].DrpTab = var_mapping("SQLColumns_TableOps_DrpTab_0", var_list);
	TableOps[1].CrtTab = var_mapping("SQLColumns_TableOps_CrtTab_1", var_list);
	TableOps[1].DrpTab = var_mapping("SQLColumns_TableOps_DrpTab_1", var_list);
	TableOps[2].CrtTab = var_mapping("SQLColumns_TableOps_CrtTab_2", var_list);
	TableOps[2].DrpTab = var_mapping("SQLColumns_TableOps_DrpTab_2", var_list);
	TableOps[3].CrtTab = var_mapping("SQLColumns_TableOps_CrtTab_3", var_list);
	TableOps[3].DrpTab = var_mapping("SQLColumns_TableOps_DrpTab_3", var_list);
	TableOps[4].CrtTab = var_mapping("SQLColumns_TableOps_CrtTab_4", var_list);
	TableOps[4].DrpTab = var_mapping("SQLColumns_TableOps_DrpTab_4", var_list);

//=========================================================================================

	if(isUCS2) {
		LogMsg(NONE,"Setup for UCS2 mode testing: ColPrec has to be doubled\n");

		i = 0;
		while(stricmp(TableCol[i].ColName,"endloop") != 0) {
			if((TableCol[i].ColDataType == SQL_CHAR) ||
				(TableCol[i].ColDataType == SQL_VARCHAR) ||
				(TableCol[i].ColDataType == SQL_LONGVARCHAR))
			{
				TableCol[i].ColPrec *= 2;    //--> This is in character, so no need to double
				TableCol[i].ColLen *= 2;

				if(TableCol[i].ColDataType == SQL_CHAR) {
				//	TableCol[i].ColDataType = SQL_WCHAR;
				//	TableCol[i].ColTypeOutput = charNameUCS2;
					TableCol[i].Remark = charUCS2;
				}
				else if (TableCol[i].ColDataType == SQL_VARCHAR) {
				//	TableCol[i].ColDataType = SQL_WVARCHAR;
				//	TableCol[i].ColTypeOutput = varcharNameUCS2;
					TableCol[i].Remark = varcharUCS2;
				}
				else {
				//	TableCol[i].ColDataType = SQL_WLONGVARCHAR;
				//	TableCol[i].ColTypeOutput = longvarcharNameUCS2;
					TableCol[i].Remark = varcharUCS2;
				}
			}
			i++;
		}
		i = 0;
	}

//=========================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => MX Specific SQLColumns | SQLColumns | columns.c\n");

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLColumns tests\n");

	if(!FullConnectWithOptions(pTestInfo,CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,"Unable to connect\n");
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
/*	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);*/
        returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	TESTCASE_END;  // end of setup

//=========================================================================================

	strcpy(TableQualifier,pTestInfo->Catalog);
	strcpy(TableOwner,pTestInfo->Schema);
	TableColStr = (char *)malloc(MAX_NOS_SIZE);
	TableStr = (char *)malloc(MAX_NOS_SIZE);
	for (j = 0; j < ACCESS_MODE; j++)
	{
		i = 0;
		strcpy(TableName,TabName);
		strcpy(TableColStr,"");
		while (_stricmp(TableCol[i].ColName,"endloop") != 0)
		{
			if ( i > 0) strcat(TableColStr,",");
			strcat(TableColStr, TableCol[i].ColName);
			strcat(TableColStr," ");
			strcat(TableColStr, TableCol[i].ColTypeName);
			strcat(TableColStr, TableCol[i].ColTypePrec);
			strcat(TableColStr, ColNull[TableCol[i].ColNullable]);
			strcpy(TableStr, TableOps[0].CrtTab);
			strcat(TableStr, TableColStr);
			strcat(TableStr,") no partition");
			sprintf(Heading,"Test create table =>");
			strcat(Heading,TableStr);
			strcat(Heading,"\n");
			TESTCASE_BEGIN(Heading);
			returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);  
                        SQLExecDirect(hstmt,(SQLCHAR*)TableOps[0].DrpTab,SQL_NTS);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)TableStr,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			else
			{
				TESTCASE_END;
				sprintf(Heading,"SQLColumns: Test #%d \n",i);
				//strcat(Heading,TableStr);
				//strcat(Heading,"\n");
				TESTCASE_BEGIN(Heading);
				// LP 
				LogMsg(NONE, "SQLSetConnectOption(SQL_ACCESS_MODE,%d)\n", ConnectOption.vParamInt[j]);
				returncode = SQLSetConnectOption((SQLHANDLE)hdbc,ConnectOption.fOption,ConnectOption.vParamInt[j]);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				if (strlen(TableQualifier) > 0) {
                    LogMsg(NONE,"SQLColumns(hstmt,%s,%d,%s,%d,%s,%d,%s,%d)\n",(SQLCHAR*)TableQualifier,(SWORD)strlen(TableQualifier),(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)TableName,(SWORD)strlen(TableName),(SQLCHAR*)ColInput,(SWORD)strlen(ColInput));
					returncode = SQLColumns(hstmt,(SQLCHAR*)TableQualifier,(SWORD)strlen(TableQualifier),(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)TableName,(SWORD)strlen(TableName),(SQLCHAR*)ColInput,(SWORD)strlen(ColInput));
				}
				else {
                    LogMsg(NONE,"SQLColumns(hstmt,%s,%d,%s,%d,%s,%d,%s,%d)\n",(SQLCHAR*)"NULL",(SWORD)0,(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)TableName,(SWORD)strlen(TableName),(SQLCHAR*)ColInput,(SWORD)strlen(ColInput));
					returncode = SQLColumns(hstmt,NULL,0,(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)TableName,(SWORD)strlen(TableName),(SQLCHAR*)ColInput,(SWORD)strlen(ColInput));
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumns"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				else
				{
					LogMsg(NONE,"SQLColumns: SQLColumns function call executed correctly.\n");
					strcpy(oTableQualifier,"");
					strcpy(oTableOwner,"");
					strcpy(oTableName,"");
					strcpy(oColName,"");
					oColDataType = 0;
					strcpy(oColTypeName,"");
					oColPrec = 0;
					oColLen = 0;
					oColScale = 0;
					oColRadix = 0;
					oColNullable = 0;
					strcpy(oRemark,"");
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
					returncode = SQLBindCol(hstmt,5,SQL_C_SHORT,&oColDataType,0,&oColDataTypelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,6,SQL_C_CHAR,oColTypeName,NAME_LEN,&oColTypeNamelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,7,SQL_C_LONG,&oColPrec,0,&oColPreclen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,8,SQL_C_LONG,&oColLen,0,&oColLenlen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,9,SQL_C_SHORT,&oColScale,0,&oColScalelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,10,SQL_C_SHORT,&oColRadix,0,&oColRadixlen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,11,SQL_C_SHORT,&oColNullable,0,&oColNullablelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,12,SQL_C_CHAR,oRemark,REM_LEN,&oRemarklen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					k = 0;
					while (returncode == SQL_SUCCESS)
					{
						strcpy(oTableQualifier,"");
						strcpy(oTableOwner,"");
						strcpy(oTableName,"");
						strcpy(oColName,"");
						oColDataType = 0;
						strcpy(oColTypeName,"");
						oColPrec = 0;
						oColLen = 0;
						oColScale = 0;
						oColRadix = 0;
						oColNullable = 0;
						strcpy(oRemark,"");
						returncode = SQLFetch(hstmt);
						if((returncode!=SQL_NO_DATA_FOUND) && (!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
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
							if ((cstrcmp(TableQualifier,oTableQualifier,TRUE,isCharSet) == 0) 
								&& (cstrcmp(TableOwner,oTableOwner,TRUE,isCharSet) == 0) 
								&& (cstrcmp(TableName,oTableName,TRUE,isCharSet) == 0) 
								&& (cstrcmp(TableCol[k].ColName,oColName,TRUE,isCharSet) == 0) 
								&& (TableCol[k].ColDataType == oColDataType) 
								&& (_strnicmp(oColTypeName,TableCol[k].ColTypeOutput,strlen(oColTypeName)) == 0) 
								&& (TableCol[k].ColPrec == oColPrec)
								&& (TableCol[k].ColLen == oColLen)
								&& (TableCol[k].ColScale == oColScale)
								&& (TableCol[k].ColRadix == oColRadix)
								&& (TableCol[k].ColNullable == oColNullable)
								&& (_stricmp(TableCol[k].Remark,oRemark) == 0))
							{
								//LP Traf
								LogMsg(NONE,"TableQualifier expect: %s and actual: %s are matched\n",TableQualifier,oTableQualifier);
								LogMsg(NONE,"TableOwner expect: %s and actual: %s are matched\n",TableOwner,oTableOwner);
								LogMsg(NONE,"TableName expect: %s and actual: %s are matched\n",TableName,oTableName);
								LogMsg(NONE,"ColName expect: %s and actual: %s are matched\n",TableCol[k].ColName,oColName);
								LogMsg(NONE,"ColDataType expect: %d and actual: %d are matched\n",TableCol[k].ColDataType,oColDataType);
								LogMsg(NONE,"ColTypeName expect: %s and actual: %s are matched\n",TableCol[k].ColTypeOutput,oColTypeName);
								LogMsg(NONE,"ColPrec expect: %d and actual: %d are matched\n",TableCol[k].ColPrec,oColPrec);
								LogMsg(NONE,"ColLen expect: %d and actual: %d are matched\n",TableCol[k].ColLen,oColLen);
								LogMsg(NONE,"ColScale expect: %d and actual: %d are matched\n",TableCol[k].ColScale,oColScale);
								LogMsg(NONE,"ColRadix expect: %d and actual: %d are matched\n",TableCol[k].ColRadix,oColRadix);
								LogMsg(NONE,"ColNullable expect: %d and actual: %d are matched\n",TableCol[k].ColNullable,oColNullable);
								LogMsg(NONE,"Remark expect: %s and actual: %s are matched\n",TableCol[k].Remark,oRemark);
							}	
							else
							{
                                sprintf(Heading,"\nSQLColumns: compare results of columns fetched for following column \n");
							    strcat(Heading,"The Column Name is "); 
							    strcat(Heading,TableCol[k].ColName);
							    strcat(Heading," and column type is ");
							    strcat(Heading,TableCol[k].ColTypeName);
							    strcat(Heading,"\n");
							    LogMsg(NONE,Heading);
								TEST_FAILED;	
								if (cstrcmp(TableQualifier,oTableQualifier,TRUE,isCharSet) != 0)
									LogMsg(ERRMSG,"TableQualifier expect: %s and actual: %s are not matched\n",TableQualifier,oTableQualifier);
								if (cstrcmp(TableOwner,oTableOwner,TRUE,isCharSet) != 0) 
									LogMsg(ERRMSG,"TableOwner expect: %s and actual: %s are not matched\n",TableOwner,oTableOwner);
								if (cstrcmp(TableName,oTableName,TRUE,isCharSet) != 0) 
									LogMsg(ERRMSG,"TableName expect: %s and actual: %s are not matched\n",TableName,oTableName);
								if (cstrcmp(TableCol[k].ColName,oColName,TRUE,isCharSet) != 0) 
									LogMsg(ERRMSG,"ColName expect: %s and actual: %s are not matched\n",TableCol[k].ColName,oColName);
								if (TableCol[k].ColDataType != oColDataType) 
									LogMsg(ERRMSG,"ColDataType expect: %d and actual: %d are not matched\n",TableCol[k].ColDataType,oColDataType);
								if (_strnicmp(oColTypeName,TableCol[k].ColTypeOutput,strlen(oColTypeName)) != 0) 
									LogMsg(ERRMSG,"ColTypeName expect: %s and actual: %s are not matched\n",TableCol[k].ColTypeOutput,oColTypeName);
								if (TableCol[k].ColPrec != oColPrec)
									LogMsg(ERRMSG,"ColPrec expect: %d and actual: %d are not matched\n",TableCol[k].ColPrec,oColPrec);
								if (TableCol[k].ColLen != oColLen)
									LogMsg(ERRMSG,"ColLen expect: %d and actual: %d are not matched\n",TableCol[k].ColLen,oColLen);
								if (TableCol[k].ColScale != oColScale)
									LogMsg(ERRMSG,"ColScale expect: %d and actual: %d are not matched\n",TableCol[k].ColScale,oColScale);
								if (TableCol[k].ColRadix != oColRadix)
									LogMsg(ERRMSG,"ColRadix expect: %d and actual: %d are not matched\n",TableCol[k].ColRadix,oColRadix);
								if (TableCol[k].ColNullable != oColNullable)
									LogMsg(ERRMSG,"ColNullable expect: %d and actual: %d are not matched\n",TableCol[k].ColNullable,oColNullable);
								if (_stricmp(TableCol[k].Remark,oRemark) != 0)
									LogMsg(ERRMSG,"Remark expect: %s and actual: %s are not matched\n",TableCol[k].Remark,oRemark);
							}
						k++;
						}
					}
					SQLFreeStmt(hstmt,SQL_UNBIND);
					SQLFreeStmt(hstmt,SQL_CLOSE);
					if(k == 0)
					{
						TEST_FAILED;
						LogMsg(ERRMSG,"No Data Found => At least one row should be fetched(1)\n");
					} else {
                        LogMsg(NONE,"Number of rows fetched: %d\n", k);
                    }
				}
				TESTCASE_END;
			}
			returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
			SQLExecDirect(hstmt,(SQLCHAR*)TableOps[0].DrpTab,SQL_NTS);
			i++;
		}

		//Testing view, materialized view and synonym
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)TableStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		i = 2;
		while (i<5)
		{
			strcpy(TableName,MVSName[i-2]);
			sprintf(Heading,"Test create table =>");
			strcat(Heading,TableOps[i].CrtTab);
			strcat(Heading,"\n");
			TESTCASE_BEGIN(Heading);
			returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
			SQLExecDirect(hstmt,(SQLCHAR*)TableOps[i].DrpTab,SQL_NTS);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)TableOps[i].CrtTab,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			else
			{
				TESTCASE_END;
				sprintf(Heading,"SQLColumns: Test #%d \n",i);
				TESTCASE_BEGIN(Heading);
				returncode = SQLSetConnectOption((SQLHANDLE)hdbc,ConnectOption.fOption,ConnectOption.vParamInt[j]);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				if (strlen(TableQualifier) > 0) {
					returncode = SQLColumns(hstmt,(SQLCHAR*)TableQualifier,(SWORD)strlen(TableQualifier),(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)TableName,(SWORD)strlen(TableName),(SQLCHAR*)ColInput,(SWORD)strlen(ColInput));
					//LogMsg(NONE,"SQLColumns(hstmt,%s,%d,%s,%d,%s,%d,%s,%d)\n",(SQLCHAR*)TableQualifier,(SWORD)strlen(TableQualifier),(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)TableName,(SWORD)strlen(TableName),(SQLCHAR*)ColInput,(SWORD)strlen(ColInput));
				}
				else {
					returncode = SQLColumns(hstmt,NULL,0,(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)TableName,(SWORD)strlen(TableName),(SQLCHAR*)ColInput,(SWORD)strlen(ColInput));
					//LogMsg(NONE,"SQLColumns(hstmt,%s,%d,%s,%d,%s,%d,%s,%d)\n",(SQLCHAR*)"NULL",(SWORD)0,(SQLCHAR*)TableOwner,(SWORD)strlen(TableOwner),(SQLCHAR*)TableName,(SWORD)strlen(TableName),(SQLCHAR*)ColInput,(SWORD)strlen(ColInput));
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumns"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				else
				{
					LogMsg(NONE,"SQLColumns: SQLColumns function call executed correctly.\n");
					strcpy(oTableQualifier,"");
					strcpy(oTableOwner,"");
					strcpy(oTableName,"");
					strcpy(oColName,"");
					oColDataType = 0;
					strcpy(oColTypeName,"");
					oColPrec = 0;
					oColLen = 0;
					oColScale = 0;
					oColRadix = 0;
					oColNullable = 0;
					strcpy(oRemark,"");
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
					returncode = SQLBindCol(hstmt,5,SQL_C_SHORT,&oColDataType,0,&oColDataTypelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,6,SQL_C_CHAR,oColTypeName,NAME_LEN,&oColTypeNamelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,7,SQL_C_LONG,&oColPrec,0,&oColPreclen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,8,SQL_C_LONG,&oColLen,0,&oColLenlen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,9,SQL_C_SHORT,&oColScale,0,&oColScalelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,10,SQL_C_SHORT,&oColRadix,0,&oColRadixlen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,11,SQL_C_SHORT,&oColNullable,0,&oColNullablelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,12,SQL_C_CHAR,oRemark,REM_LEN,&oRemarklen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					k = 0;
					while (returncode == SQL_SUCCESS)
					{
						strcpy(oTableQualifier,"");
						strcpy(oTableOwner,"");
						strcpy(oTableName,"");
						strcpy(oColName,"");
						oColDataType = 0;
						strcpy(oColTypeName,"");
						oColPrec = 0;
						oColLen = 0;
						oColScale = 0;
						oColRadix = 0;
						oColNullable = 0;
						strcpy(oRemark,"");
						returncode = SQLFetch(hstmt);
						if((returncode!=SQL_NO_DATA_FOUND) && (!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
						{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
						}
						else if (returncode == SQL_SUCCESS)
						{
							sprintf(Heading,"\nSQLColumns: compare results of columns fetched for following column \n");
							strcat(Heading,"The Column Name is "); 
							strcat(Heading,TableCol[k].ColName);
							strcat(Heading," and column type is ");
							strcat(Heading,TableCol[k].ColTypeName);
							strcat(Heading,"\n");
							LogMsg(NONE,Heading);
							if (strlen(TableQualifier) == 0)
							{
								strcpy(TableQualifier, "TRAFODION");
							}
							if ((cstrcmp(TableQualifier,oTableQualifier,TRUE,isCharSet) == 0) 
								&& (cstrcmp(TableOwner,oTableOwner,TRUE,isCharSet) == 0) 
								&& (cstrcmp(TableName,oTableName,TRUE,isCharSet) == 0) 
								&& (cstrcmp(TableCol[k].ColName,oColName,TRUE,isCharSet) == 0) 
								&& (TableCol[k].ColDataType == oColDataType) 
								&& (_strnicmp(oColTypeName,TableCol[k].ColTypeOutput,strlen(oColTypeName)) == 0) 
								&& (TableCol[k].ColPrec == oColPrec)
								&& (TableCol[k].ColLen == oColLen)
								&& (TableCol[k].ColScale == oColScale)
								&& (TableCol[k].ColRadix == oColRadix)
								&& (TableCol[k].ColNullable == oColNullable)
								&& (_stricmp(TableCol[k].Remark,oRemark) == 0))
							{
								//LogMsg(NONE,"TableQualifier expect: %s and actual: %s are matched\n",TableQualifier,oTableQualifier);
								//LogMsg(NONE,"TableOwner expect: %s and actual: %s are matched\n",TableOwner,oTableOwner);
								//LogMsg(NONE,"TableName expect: %s and actual: %s are matched\n",TableName,oTableName);
								//LogMsg(NONE,"ColName expect: %s and actual: %s are matched\n",TableCol[k].ColName,oColName);
								//LogMsg(NONE,"ColDataType expect: %d and actual: %d are matched\n",TableCol[k].ColDataType,oColDataType);
								//LogMsg(NONE,"ColTypeName expect: %s and actual: %s are matched\n",TableCol[k].ColTypeOutput,oColTypeName);
								//LogMsg(NONE,"ColPrec expect: %d and actual: %d are matched\n",TableCol[k].ColPrec,oColPrec);
								//LogMsg(NONE,"ColLen expect: %d and actual: %d are matched\n",TableCol[k].ColLen,oColLen);
								//LogMsg(NONE,"ColScale expect: %d and actual: %d are matched\n",TableCol[k].ColScale,oColScale);
								//LogMsg(NONE,"ColRadix expect: %d and actual: %d are matched\n",TableCol[k].ColRadix,oColRadix);
								//LogMsg(NONE,"ColNullable expect: %d and actual: %d are matched\n",TableCol[k].ColNullable,oColNullable);
								//LogMsg(NONE,"Remark expect: %s and actual: %s are matched\n",TableCol[k].Remark,oRemark);
							}	
							else
							{
								TEST_FAILED;	
								if (cstrcmp(TableQualifier,oTableQualifier,TRUE,isCharSet) != 0)
									LogMsg(ERRMSG,"TableQualifier expect: %s and actual: %s are not matched\n",TableQualifier,oTableQualifier);
								if (cstrcmp(TableOwner,oTableOwner,TRUE,isCharSet) != 0) 
									LogMsg(ERRMSG,"TableOwner expect: %s and actual: %s are not matched\n",TableOwner,oTableOwner);
								if (cstrcmp(TableName,oTableName,TRUE,isCharSet) != 0) 
									LogMsg(ERRMSG,"TableName expect: %s and actual: %s are not matched\n",TableName,oTableName);
								if (cstrcmp(TableCol[k].ColName,oColName,TRUE,isCharSet) != 0) 
									LogMsg(ERRMSG,"ColName expect: %s and actual: %s are not matched\n",TableCol[k].ColName,oColName);
								if (TableCol[k].ColDataType != oColDataType) 
									LogMsg(ERRMSG,"ColDataType expect: %d and actual: %d are not matched\n",TableCol[k].ColDataType,oColDataType);
								if (_strnicmp(oColTypeName,TableCol[k].ColTypeOutput,strlen(oColTypeName)) != 0) 
									LogMsg(ERRMSG,"ColTypeName expect: %s and actual: %s are not matched\n",TableCol[k].ColTypeOutput,oColTypeName);
								if (TableCol[k].ColPrec != oColPrec)
									LogMsg(ERRMSG,"ColPrec expect: %d and actual: %d are not matched\n",TableCol[k].ColPrec,oColPrec);
								if (TableCol[k].ColLen != oColLen)
									LogMsg(ERRMSG,"ColLen expect: %d and actual: %d are not matched\n",TableCol[k].ColLen,oColLen);
								if (TableCol[k].ColScale != oColScale)
									LogMsg(ERRMSG,"ColScale expect: %d and actual: %d are not matched\n",TableCol[k].ColScale,oColScale);
								if (TableCol[k].ColRadix != oColRadix)
									LogMsg(ERRMSG,"ColRadix expect: %d and actual: %d are not matched\n",TableCol[k].ColRadix,oColRadix);
								if (TableCol[k].ColNullable != oColNullable)
									LogMsg(ERRMSG,"ColNullable expect: %d and actual: %d are not matched\n",TableCol[k].ColNullable,oColNullable);
								if (_stricmp(TableCol[k].Remark,oRemark) != 0)
									LogMsg(ERRMSG,"Remark expect: %s and actual: %s are not matched\n",TableCol[k].Remark,oRemark);
							}
						k++;
						}
					}
					SQLFreeStmt(hstmt,SQL_UNBIND);
					SQLFreeStmt(hstmt,SQL_CLOSE);
					if(k == 0)
					{
						TEST_FAILED;
						LogMsg(ERRMSG,"No Data Found => At least one row should be fetched(2)\n");
					} else {
                        LogMsg(NONE,"Number of rows fetched: %d\n", k);
                    }
				}
				TESTCASE_END;
			}
			returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
			i++;
		}

		returncode = SQLExecDirect(hstmt,(SQLCHAR*)TableOps[4].DrpTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)TableOps[3].DrpTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)TableOps[2].DrpTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)TableOps[0].DrpTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
	}

	free(TableColStr);
	free(TableStr); 

//=========================================================================================
// testing of wildcard ooptions
	
	// need to make sure it's set to FALSE so that it's treated as a pattern value!!!!
	sprintf(Heading,"Setting up Table & View to test SQLTables for wildcard options => \n");
	strcat(Heading,"\n");
	TESTCASE_BEGIN(Heading);
	SQLExecDirect(hstmt,(SQLCHAR*)TableOps[1].DrpTab,SQL_NTS);
	LogMsg(NONE,"%s\n", TableOps[1].CrtTab);
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)TableOps[1].CrtTab,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	else
	{
		LogMsg(NONE,"setting up tables executed successfully.\n");
		TESTCASE_END;
	}

	i = 0;
	while (_stricmp(ColumnWC[i].TabQua,"endloop") != 0)
	{
        returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_FALSE,0);
	    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	    {
		    TEST_FAILED;
		    LogAllErrors(henv,hdbc,hstmt);
	    }// end of setup

		memset (Heading, 0, MAX_HEADING_SIZE);  //RS: clean up buffer
		// sprintf(Heading,"");
		sprintf(Heading,"SQLColumns: wildcard options (%d)  => \nTable Qualifier: %s \nTable Owner: %s \nTable Name: %s \nColumn Name: %s\n",
			i,
			printSymbol(ColumnWC[i].TabQua,displayBuf.cat),
            printSymbol(ColumnWC[i].TabOwner,displayBuf.sch),
            printSymbol(ColumnWC[i].TabName,displayBuf.tab),
            printSymbol(ColumnWC[i].ColName,displayBuf.col));

		TESTCASE_BEGIN(Heading);
		NullValue = 0;		
		if (_stricmp(ColumnWC[i].TabQua,"NULL") == 0)
		{
			ColumnWC[i].TabQua = NULL;
			NullValue = 1;
		}
		if (_stricmp(ColumnWC[i].TabOwner,"NULL") == 0)
		{
			ColumnWC[i].TabOwner = NULL;
			NullValue = 1;
		}
		if (_stricmp(ColumnWC[i].TabName,"NULL") == 0)
		{
			ColumnWC[i].TabName = NULL;
			NullValue = 1;
		}
		if (_stricmp(ColumnWC[i].ColName,"NULL") == 0)
		{
			ColumnWC[i].ColName = NULL;
			NullValue = 1;
		}

		if (NullValue == 1)
		{
			returncode = SQLColumns(hstmt,(SQLCHAR*)ColumnWC[i].TabQua,SQL_NTS,(SQLCHAR*)ColumnWC[i].TabOwner,SQL_NTS,
										  (SQLCHAR*)ColumnWC[i].TabName,SQL_NTS,(SQLCHAR*)ColumnWC[i].ColName,SQL_NTS);
		}
		else
		{
			returncode = SQLColumns(hstmt,(SQLCHAR*)ColumnWC[i].TabQua,(SWORD)strlen(ColumnWC[i].TabQua),
										  (SQLCHAR*)ColumnWC[i].TabOwner,(SWORD)strlen(ColumnWC[i].TabOwner),
										  (SQLCHAR*)removeQuotes(ColumnWC[i].TabName,displayBuf.tab),(SWORD)strlen(displayBuf.tab),
										  (SQLCHAR*)removeQuotes(ColumnWC[i].ColName,displayBuf.col),(SWORD)strlen(displayBuf.col));
		}
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumns"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		else
		{
			LogMsg(NONE,"SQLColumns: Executed successfully.\n");
	 		strcpy(oTableQualifier,"");
			strcpy(oTableOwner,"");
			strcpy(oTableName,"");
			strcpy(oColName,"");
			oColDataType = 0;
			strcpy(oColTypeName,"");
			oColPrec = 0;
			oColLen = 0;
			oColScale = 0;
			oColRadix = 0;
			oColNullable = 0;
			strcpy(oRemark,"");
			returncode = SQLBindCol(hstmt,1,SQL_C_CHAR,oTableQualifier,NAME_LEN,&oTableQualifierlen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,2,SQL_C_CHAR,oTableOwner,NAME_LEN,&oTableOwnerlen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,3,SQL_C_CHAR,oTableName,NAME_LEN,&oTableNamelen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,4,SQL_C_CHAR,oColName,NAME_LEN,&oColNamelen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
			}
			returncode = SQLBindCol(hstmt,5,SQL_C_SSHORT,&oColDataType,0,&oColDataTypelen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,6,SQL_C_CHAR,oColTypeName,NAME_LEN,&oColTypeNamelen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,7,SQL_C_SLONG,&oColPrec,0,&oColPreclen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,8,SQL_C_SLONG,&oColLen,0,&oColLenlen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,9,SQL_C_SSHORT,&oColScale,0,&oColScalelen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,10,SQL_C_SSHORT,&oColRadix,0,&oColRadixlen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,11,SQL_C_SSHORT,&oColNullable,0,&oColNullablelen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,12,SQL_C_CHAR,oRemark,REM_LEN,&oRemarklen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
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
			if(k == 0)
			{
				TEST_FAILED;
				LogMsg(ERRMSG,"No Data Found => At least one row should be fetched(3)\n");
			} 
			else 
			{
                LogMsg(NONE,"Number of rows fetched: %d\n", k);
            }
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		TESTCASE_END;
		i++;
	}

//=========================================================================================

/* RS: To be disabled tempararily since MDAC 2.8 causes an access violation.

	TESTCASE_BEGIN("SQLColumns: Negative test with invalid handle\n");

	SQLAllocStmt((SQLHANDLE)hdbc, &hstmt1);
	SQLFreeStmt(hstmt1, SQL_DROP);
	returncode = SQLColumns(hstmt1,ColumnWC[0].TabQua,(SWORD)strlen(ColumnWC[0].TabQua),ColumnWC[0].TabOwner,(SWORD)strlen(ColumnWC[0].TabOwner),ColumnWC[0].TabName,(SWORD)strlen(ColumnWC[0].TabName),ColumnWC[0].ColName,(SWORD)strlen(ColumnWC[0].ColName));
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLColumns"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;
*/

//=========================================================================================

	TESTCASE_BEGIN("SQLColumns: Negative test with NULL handle\n");

	hstmt1 = (SQLHANDLE)NULL;
	returncode = SQLColumns(hstmt1,(SQLCHAR*)ColumnWC[0].TabQua,(SWORD)strlen(ColumnWC[0].TabQua),(SQLCHAR*)ColumnWC[0].TabOwner,(SWORD)strlen(ColumnWC[0].TabOwner),(SQLCHAR*)ColumnWC[0].TabName,(SWORD)strlen(ColumnWC[0].TabName),(SQLCHAR*)ColumnWC[0].ColName,(SWORD)strlen(ColumnWC[0].ColName));
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLColumns"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("SQLColumns: Negative test with Invalid lengths to valid SQLColumns args\n");

	t = 0;
	while (_stricmp(ColumnWC2[t].TabQua,"endloop") != 0)
	{
		returncode = SQLColumns(hstmt,(SQLCHAR*)ColumnWC2[t].TabQua,ColumnWC2[t].TabQuaLen,(SQLCHAR*)ColumnWC2[t].TabOwner,ColumnWC2[t].TabOwnerLen,(SQLCHAR*)ColumnWC2[t].TabName,ColumnWC2[t].TabNameLen,(SQLCHAR*)ColumnWC2[t].ColName,ColumnWC2[t].ColNameLen);
		if(!CHECKRC(SQL_ERROR,returncode,"SQLColumns"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG, "Test failed while inside negative test with invalid lengths");
			LogAllErrors(henv,hdbc,hstmt);
		}
		t++;
	}

	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("SQLColumns: Negative test with invalid SQLColumns arguments\n");

	t = 0;
	while (_stricmp(ColumnWC3[t].TabQua,"endloop") != 0)
	{
		returncode = SQLColumns(hstmt,(SQLCHAR*)ColumnWC3[t].TabQua,(SWORD)strlen(ColumnWC3[t].TabQua),(SQLCHAR*)ColumnWC3[t].TabOwner,(SWORD)strlen(ColumnWC3[t].TabOwner),(SQLCHAR*)ColumnWC3[t].TabName,(SWORD)strlen(ColumnWC3[t].TabName),(SQLCHAR*)ColumnWC3[t].ColName,(SWORD)strlen(ColumnWC3[t].ColName));
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumns"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG, "Test failed while inside negative test with invalid SQLColumns arguments SQLColumns Failed\n");
			LogAllErrors(henv,hdbc,hstmt);
		}
		returncode = SQLFetch(hstmt);
		if(returncode!=SQL_NO_DATA_FOUND)
		{
		  LogMsg(ERRMSG, "Test failed while inside negative test with invalid SQLColumns arguments SQLColumns returned some data\n");
		} 
		t++;
	}

	TESTCASE_END;

//=========================================================================================


	TESTCASE_BEGIN("Testing SQLColAttribute, SQLDescribeCol, SQLBindCol and SQLFetch functions for catalog names\n");

	for(k = 0; k < 5; k++)
	{
        returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_FALSE,0);
	    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	    {
		    TEST_FAILED;
		    LogAllErrors(henv,hdbc,hstmt);
	    }// end of setup

        sprintf(Heading,"SQLColumns: wildcard options (%d)=> \nTable Qualifier: %s \nTable Owner: %s \nTable Name: %s \nColumn Name: %s\n",
			i,
			printSymbol(ColumnWC[k].TabQua,displayBuf.cat),
            printSymbol(ColumnWC[k].TabOwner,displayBuf.sch),
            printSymbol(ColumnWC[k].TabName,displayBuf.tab),
            printSymbol(ColumnWC[k].ColName,displayBuf.col));
        LogMsg(NONE,Heading);

		returncode = SQLColumns(hstmt,(SQLCHAR*)ColumnWC[k].TabQua,(SWORD)strlen(ColumnWC[k].TabQua),(SQLCHAR*)ColumnWC[k].TabOwner,(SWORD)strlen(ColumnWC[k].TabOwner),(SQLCHAR*)ColumnWC[k].TabName,(SWORD)strlen(ColumnWC[k].TabName),(SQLCHAR*)ColumnWC[k].ColName,(SWORD)strlen(ColumnWC[k].ColName));
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumns"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		returncode = SQLNumResultCols(hstmt, &numOfCols);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultsCol"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG,"Test failed while executing call for SQLNUMRESULTSCOL\n");
			LogAllErrors(henv,hdbc,hstmt);
		}
		LogMsg(NONE,"Number of Columns fetched: %d\n", numOfCols);

		for(cols = 0; cols < numOfCols; cols++)
		{
			returncode = SQLDescribeCol(hstmt,(SWORD)(cols+1),(SQLCHAR*)cn,COLNAME_LEN,&cl,&st,&cp,&cs,&cnull);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDescribeCol"))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,"Test failed while executing call for SQLDESCRIBECOL of column\n");
				LogAllErrors(henv,hdbc,hstmt);
			}
			CharOutput[cols] = (char *)malloc(STR_LEN);
			for (iatt = 0; iatt <= totatt; iatt++)
			{
				strcpy(rgbDesc,"");
				pcbDesc = 0;
				pfDesc = 0;
				returncode = SQLColAttributes(hstmt,(SWORD)(cols+1),DescrType[iatt],rgbDesc,STR_LEN,&pcbDesc,&pfDesc);
				//LogMsg(NONE,"SQLColattributes(hstmt,%d,%d,%s,%d,%d,%d)\n",(SWORD)(cols+1),DescrType[iatt],rgbDesc,STR_LEN,&pcbDesc,&pfDesc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColAttribute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
			returncode = SQLBindCol(hstmt,(SWORD)1,SQL_C_CHAR,CharOutput[cols],STR_LEN,&stringlength);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,"Test failed while executing call for SQLBindCols of column : %d.\n",cols);
				LogAllErrors(henv,hdbc,hstmt);
			}
		}

		t = 0;
		while (returncode == SQL_SUCCESS)
		{
			returncode = SQLFetch(hstmt);
			if(returncode == SQL_ERROR)
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			} 
			else if (returncode == SQL_NO_DATA_FOUND) {
				break;
			} 
			else {
				if(returncode == SQL_SUCCESS_WITH_INFO)
					LogAllErrors(henv,hdbc,hstmt);
				t++;
			}
		}
		if(t == 0)
		{
			TEST_FAILED;
			LogMsg(ERRMSG,"No Data Found => At least one row should be fetched(4)\n");
        } 
		else 
		{
            LogMsg(NONE,"Number of rows fetched: %d\n", t);
        }
		
		for(cols = 0; cols < numOfCols; cols++)
		{
			free(CharOutput[cols]);
		}
		TESTCASE_END;
	}
	
	//clean up
	SQLExecDirect(hstmt,(SQLCHAR *)(TableOps[1].DrpTab),SQL_NTS);

//=========================================================================================

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => MX Specific SQLColumns.\n");
	free_list(var_list);
	TEST_RETURN;
}
