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


#define NAME_LEN	300
#define NUM_OUTPUTS	8
#define REM_LEN		254
#define NUM_PATTERN	5
#define ACCESS_MODE 2
#define COLNAME_LEN	128+1
#define	RGB_MAX_LEN		50
#define STR_LEN     300    //added to test SQLBindCols and SQLFetch

/*
---------------------------------------------------------
   TestSQLColumns for MX Specific (file is columns.c)
---------------------------------------------------------
*/
PassFail TestMXSQLColumns( TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	TCHAR		Heading[MAX_HEADING_SIZE];
 	RETCODE		returncode;
 	SQLHANDLE 	henv;
 	SQLHANDLE 	hdbc;
 	SQLHANDLE	hstmt, hstmt1;
	TCHAR		TableQualifier[NAME_LEN],TableOwner[NAME_LEN],TableName[NAME_LEN],*TableColStr,*TableStr;
	//TCHAR		ColInput[NAME_LEN] = _T("%");
	TCHAR		*ColInput = _T("%");
	TCHAR		*ColNull[] = {_T(" not null"), _T(""),_T(" not null")};
	TCHAR		oTableQualifier[NAME_LEN];
	TCHAR		oTableOwner[NAME_LEN];
	TCHAR		oTableName[NAME_LEN];
	TCHAR		oColName[NAME_LEN];
	SWORD		oColDataType;
	TCHAR		oColTypeName[NAME_LEN];
	SDWORD		oColPrec;
	SDWORD		oColLen;
	SWORD		oColScale;
	SWORD		oColRadix;
	SWORD		oColNullable;
	TCHAR		oRemark[REM_LEN];
	SQLLEN		oTableQualifierlen; 
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
	SQLLEN pfDesc; 
	TCHAR cn[COLNAME_LEN];
	SWORD cl;
	SWORD st;
	SQLULEN cp; 
	SWORD cs, cnull;
	TCHAR rgbDesc[RGB_MAX_LEN];
	TCHAR *CharOutput[40];
	SQLLEN stringlength; 
	TCHAR *TabName;
	TCHAR *MVSName[3];

	struct
	{
		TCHAR *CrtTab;
		TCHAR *DrpTab;
	} TableOps[] = {
		{_T("--"), _T("--")},	//for normal table
		{_T("--"), _T("--")},	//for wildcard
		{_T("--"), _T("--")},	//for view
		{_T("--"), _T("--")},	//for materialized view
		{_T("--"), _T("--")}	//for synonym
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
		TCHAR		*ColName;
		SWORD		ColDataType;
		TCHAR		*ColTypeName;
		TCHAR		*ColTypePrec;
		TCHAR		*ColTypeOutput;
		SDWORD		ColPrec;												
		SDWORD		ColLen;
		SWORD		ColScale;
		SWORD		ColRadix;
		SWORD		ColNullable;
		TCHAR		*Remark;
	} TableCol[] = {
							{_T("--"),SQL_CHAR,_T("char"),_T("(10) CHARACTER SET ISO88591"),_T("CHAR"),10,10,0,0,SQL_NULLABLE,_T("CHARACTER CHARACTER SET ISO88591")},
							{_T("--"),SQL_VARCHAR,_T("varchar"),_T("(10) CHARACTER SET ISO88591"),_T("VARCHAR"),10,10,0,0,SQL_NULLABLE,_T("VARCHAR CHARACTER SET ISO88591")},
							{_T("--"),SQL_VARCHAR,_T("long varchar"),_T(" CHARACTER SET ISO88591"),_T("VARCHAR"),2000,2000,0,0,SQL_NULLABLE,_T("VARCHAR CHARACTER SET ISO88591")},
							{_T("--"),SQL_DECIMAL,_T("decimal"),_T("(10,5)"),_T("DECIMAL SIGNED"),10,12,5,10,SQL_NULLABLE,_T("SIGNED DECIMAL ")},
							{_T("--"),SQL_DECIMAL,_T("decimal"),_T("(5,2) unsigned"),_T("DECIMAL UNSIGNED"),5,7,2,10,SQL_NULLABLE,_T("UNSIGNED DECIMAL ")},
							{_T("--"),SQL_NUMERIC,_T("numeric"),_T("(10,5)"),_T("NUMERIC SIGNED"),10,12,5,10,SQL_NULLABLE,_T("SIGNED NUMERIC ")},
							{_T("--"),SQL_NUMERIC,_T("numeric"),_T("(5,2) unsigned"),_T("NUMERIC UNSIGNED"),5,7,2,10,SQL_NULLABLE,_T("UNSIGNED NUMERIC ")},
							{_T("--"),SQL_SMALLINT,_T("smallint"),_T(""),_T("SMALLINT SIGNED"),5,2,0,10,SQL_NULLABLE,_T("SIGNED SMALLINT ")},
							{_T("--"),SQL_SMALLINT,_T("smallint"),_T(" unsigned"),_T("SMALLINT UNSIGNED"),5,2,0,10,SQL_NULLABLE,_T("UNSIGNED SMALLINT ")},
							{_T("--"),SQL_INTEGER,_T("integer"),_T(""),_T("INTEGER SIGNED"),10,4,0,10,SQL_NULLABLE,_T("SIGNED INTEGER ")},
							{_T("--"),SQL_INTEGER,_T("integer"),_T(" unsigned"),_T("INTEGER UNSIGNED"),10,4,0,10,SQL_NULLABLE,_T("UNSIGNED INTEGER ")},
							{_T("--"),SQL_BIGINT,_T("bigint"),_T(""),_T("BIGINT SIGNED"),19,20,0,10,SQL_NULLABLE,_T("SIGNED LARGEINT ")},
							{_T("--"),SQL_REAL,_T("real"),_T(""),_T("REAL"),22,4,0,2,SQL_NULLABLE,_T("REAL ")},
							{_T("--"),SQL_FLOAT,_T("float"),_T(""),_T("FLOAT"),54,8,0,2,SQL_NULLABLE,_T("FLOAT ")},
							{_T("--"),SQL_DOUBLE,_T("double precision"),_T(""),_T("DOUBLE PRECISION"),54,8,0,2,SQL_NULLABLE,_T("DOUBLE ")},
							{_T("--"),SQL_DATE,_T("date"),_T(""),_T("DATE"),10,6,0,0,SQL_NULLABLE,_T("DATE ")},
							{_T("--"),SQL_TIME,_T("time"),_T(""),_T("TIME"),8,6,0,0,SQL_NULLABLE,_T("TIME (0)")},
							{_T("--"),SQL_TIMESTAMP,_T("timestamp"),_T(""),_T("TIMESTAMP"),26,16,6,0,SQL_NULLABLE,_T("TIMESTAMP (6)")},
							{_T("--"),SQL_NUMERIC,_T("numeric"),_T("(19,0)"),_T("NUMERIC SIGNED"),19,21,0,10,SQL_NULLABLE,_T("SIGNED NUMERIC ")},
							{_T("--"),SQL_NUMERIC,_T("numeric"),_T("(19,6)"),_T("NUMERIC SIGNED"),19,21,6,10,SQL_NULLABLE,_T("SIGNED NUMERIC ")},
							{_T("--"),SQL_NUMERIC,_T("numeric"),_T("(60,30)"),_T("NUMERIC SIGNED"),60,62,30,10,SQL_NULLABLE,_T("SIGNED NUMERIC ")},
							{_T("--"),SQL_NUMERIC,_T("numeric"),_T("(128,0)"),_T("NUMERIC SIGNED"),128,130,0,10,SQL_NULLABLE,_T("SIGNED NUMERIC ")},
							{_T("--"),SQL_NUMERIC,_T("numeric"),_T("(128,128)"),_T("NUMERIC SIGNED"),128,130,128,10,SQL_NULLABLE,_T("SIGNED NUMERIC ")},
							{_T("--"),SQL_NUMERIC,_T("numeric"),_T("(10,5) unsigned"),_T("NUMERIC UNSIGNED"),10,12,5,10,SQL_NULLABLE,_T("UNSIGNED NUMERIC ")},
							{_T("--"),SQL_NUMERIC,_T("numeric"),_T("(18,5) unsigned"),_T("NUMERIC UNSIGNED"),18,20,5,10,SQL_NULLABLE,_T("UNSIGNED NUMERIC ")},
							{_T("--"),SQL_NUMERIC,_T("numeric"),_T("(30,10) unsigned"),_T("NUMERIC UNSIGNED"),30,32,10,10,SQL_NULLABLE,_T("UNSIGNED NUMERIC ")},
							{_T("--"),SQL_WCHAR,_T("char"),_T("(10)  CHARACTER SET UCS2"),_T("NCHAR"),10,20,0,0,SQL_NULLABLE,_T("CHARACTER CHARACTER SET UCS2")},
							{_T("--"),SQL_WVARCHAR,_T("varchar"),_T("(10) CHARACTER SET UCS2"),_T("NCHAR VARYING"),10,20,0,0,SQL_NULLABLE,_T("VARCHAR CHARACTER SET UCS2")},
							{_T("--"),SQL_WVARCHAR,_T("long varchar"),_T(" CHARACTER SET UCS2"),_T("NCHAR VARYING"),2000,4000,0,0,SQL_NULLABLE,_T("VARCHAR CHARACTER SET UCS2")},
							{_T("endloop"),}
						};

	struct
	{
		TCHAR		*TabQua;
		TCHAR		*TabOwner;
		TCHAR		*TabName;
		TCHAR		*ColName;
	} ColumnWC[] = {								// wild cards from here
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--"),_T("--")},
							{_T("endloop"),}
						};

	// same table but with inaccurate lengths added for negative testing
	struct
	{
		TCHAR		*TabQua;
		SWORD		TabQuaLen;
		TCHAR		*TabOwner;
		SWORD		TabOwnerLen;
		TCHAR		*TabName;
		SWORD		TabNameLen;
		TCHAR		*ColName;
		SWORD		ColNameLen;
	} ColumnWC2[] = {								/* wild cards from here */
							{pTestInfo->Catalog, (SWORD)-1, pTestInfo->Schema,(SWORD)-1, _T(""),(SWORD)-1, _T(""), (SWORD)-1},
							{_T("endloop"),}
						};

	struct
	{
		TCHAR		*TabQua;
		TCHAR		*TabOwner;
		TCHAR		*TabName;
		TCHAR		*ColName;
	} ColumnWC3[] = {								// wild cards from here
							{_T("--"),_T("--"),_T("--"),_T("--")},
							{_T("--"),_T("--"),_T("--"),_T("--")},
							{_T("endloop"),}
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
	//TCHAR charUCS2[] = _T("CHARACTER  CHARACTER SET UCS2");
	//TCHAR varcharUCS2[] = _T("VARCHAR  CHARACTER SET UCS2");
	//TCHAR *charNameUCS2 = _T("NCHAR");
	//TCHAR *varcharNameUCS2 = _T("NCHAR VARYING");
	//TCHAR *longvarcharNameUCS2 = _T("NCHAR VARYING");

    struct {
        TCHAR cat[STR_LEN];
        TCHAR sch[STR_LEN];
        TCHAR tab[STR_LEN];
        TCHAR col[STR_LEN];
    } displayBuf;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLColumns"), charset_file);
	if (var_list == NULL) return FAILED;

	TableCol[0].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_0"), var_list);
	TableCol[1].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_1"), var_list);
	TableCol[2].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_2"), var_list);
	TableCol[3].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_3"), var_list);
	TableCol[4].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_4"), var_list);
	TableCol[5].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_5"), var_list);
	TableCol[6].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_6"), var_list);
	TableCol[7].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_7"), var_list);
	TableCol[8].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_8"), var_list);
	TableCol[9].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_9"), var_list);
	TableCol[10].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_10"), var_list);
	TableCol[11].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_11"), var_list);
	TableCol[12].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_12"), var_list);
	TableCol[13].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_13"), var_list);
	TableCol[14].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_14"), var_list);
	TableCol[15].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_15"), var_list);
	TableCol[16].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_16"), var_list);
	TableCol[17].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_17"), var_list);
	TableCol[18].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_18"), var_list);
	TableCol[19].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_19"), var_list);
	TableCol[20].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_20"), var_list);
	TableCol[21].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_21"), var_list);
	TableCol[22].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_22"), var_list);
	TableCol[23].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_23"), var_list);
	TableCol[24].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_24"), var_list);
	TableCol[25].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_25"), var_list);
	TableCol[26].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_26"), var_list);
	TableCol[27].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_27"), var_list);
	TableCol[28].ColName = var_mapping(_T("SQLColumns_TableCol_ColName_28"), var_list);

	ColumnWC[0].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_0"), var_list);
	ColumnWC[0].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_0"), var_list);
	ColumnWC[1].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_1"), var_list);
	ColumnWC[1].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_1"), var_list);
	ColumnWC[2].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_2"), var_list);
	ColumnWC[2].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_2"), var_list);
	ColumnWC[3].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_3"), var_list);
	ColumnWC[3].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_3"), var_list);
	ColumnWC[4].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_4"), var_list);
	ColumnWC[4].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_4"), var_list);
	ColumnWC[5].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_5"), var_list);
	ColumnWC[5].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_5"), var_list);
	ColumnWC[6].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_6"), var_list);
	ColumnWC[6].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_6"), var_list);
	ColumnWC[7].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_7"), var_list);
	ColumnWC[7].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_7"), var_list);
	ColumnWC[8].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_8"), var_list);
	ColumnWC[8].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_8"), var_list);
	ColumnWC[9].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_9"), var_list);
	ColumnWC[9].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_9"), var_list);
	ColumnWC[10].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_10"), var_list);
	ColumnWC[10].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_10"), var_list);
	ColumnWC[11].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_11"), var_list);
	ColumnWC[11].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_11"), var_list);
	ColumnWC[12].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_12"), var_list);
	ColumnWC[12].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_12"), var_list);
	ColumnWC[13].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_13"), var_list);
	ColumnWC[13].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_13"), var_list);
	ColumnWC[14].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_14"), var_list);
	ColumnWC[14].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_14"), var_list);

	ColumnWC[15].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_15"), var_list);
	ColumnWC[15].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_15"), var_list);
	ColumnWC[16].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_16"), var_list);
	ColumnWC[16].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_16"), var_list);
	ColumnWC[17].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_17"), var_list);
	ColumnWC[17].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_17"), var_list);
	ColumnWC[18].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_18"), var_list);
	ColumnWC[18].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_18"), var_list);
	ColumnWC[19].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_19"), var_list);
	ColumnWC[19].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_19"), var_list);
	ColumnWC[20].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_20"), var_list);
	ColumnWC[20].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_20"), var_list);
	ColumnWC[21].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_21"), var_list);
	ColumnWC[21].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_21"), var_list);
	ColumnWC[22].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_22"), var_list);
	ColumnWC[22].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_22"), var_list);
	ColumnWC[23].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_23"), var_list);
	ColumnWC[23].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_23"), var_list);
	ColumnWC[24].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_24"), var_list);
	ColumnWC[24].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_24"), var_list);
	ColumnWC[25].TabName = var_mapping(_T("SQLColumns_ColumnWC_TabName_25"), var_list);
	ColumnWC[25].ColName = var_mapping(_T("SQLColumns_ColumnWC_ColName_25"), var_list);

	ColumnWC2[0].TabName = var_mapping(_T("SQLColumns_ColumnWC2_TabName_0"), var_list);
	ColumnWC2[0].ColName = var_mapping(_T("SQLColumns_ColumnWC2_ColName_0"), var_list);

	ColumnWC3[0].TabName = var_mapping(_T("SQLColumns_ColumnWC3_TabName_0"), var_list);
	ColumnWC3[0].ColName = var_mapping(_T("SQLColumns_ColumnWC3_ColName_0"), var_list);
	ColumnWC3[1].TabName = var_mapping(_T("SQLColumns_ColumnWC3_TabName_1"), var_list);
	ColumnWC3[1].ColName = var_mapping(_T("SQLColumns_ColumnWC3_ColName_1"), var_list);

	TabName    = var_mapping(_T("SQLColumns_TableName"), var_list);
	MVSName[0] = var_mapping(_T("SQLColumns_ViewName"), var_list);
	MVSName[1] = var_mapping(_T("SQLColumns_MVName"), var_list);
	MVSName[2] = var_mapping(_T("SQLColumns_SynonymName"), var_list);

	TableOps[0].CrtTab = var_mapping(_T("SQLColumns_TableOps_CrtTab_0"), var_list);
	TableOps[0].DrpTab = var_mapping(_T("SQLColumns_TableOps_DrpTab_0"), var_list);
	TableOps[1].CrtTab = var_mapping(_T("SQLColumns_TableOps_CrtTab_1"), var_list);
	TableOps[1].DrpTab = var_mapping(_T("SQLColumns_TableOps_DrpTab_1"), var_list);
	TableOps[2].CrtTab = var_mapping(_T("SQLColumns_TableOps_CrtTab_2"), var_list);
	TableOps[2].DrpTab = var_mapping(_T("SQLColumns_TableOps_DrpTab_2"), var_list);
	TableOps[3].CrtTab = var_mapping(_T("SQLColumns_TableOps_CrtTab_3"), var_list);
	TableOps[3].DrpTab = var_mapping(_T("SQLColumns_TableOps_DrpTab_3"), var_list);
	TableOps[4].CrtTab = var_mapping(_T("SQLColumns_TableOps_CrtTab_4"), var_list);
	TableOps[4].DrpTab = var_mapping(_T("SQLColumns_TableOps_DrpTab_4"), var_list);

//=========================================================================================

	//if(isUCS2) {
	//	LogMsg(NONE,_T("Setup for UCS2 mode testing: ColPrec has to be doubled\n"));

	//	i = 0;
	//	while(_tcsicmp(TableCol[i].ColName,_T("endloop")) != 0) {
	//		if((TableCol[i].ColDataType == SQL_WCHAR) ||
	//			(TableCol[i].ColDataType == SQL_WVARCHAR) ||
	//			(TableCol[i].ColDataType == SQL_WLONGVARCHAR))
	//		{
	//			//TableCol[i].ColPrec *= 2;    --> This is in character, so no need to double
	//			TableCol[i].ColLen *= 2;
	//			if(TableCol[i].ColDataType == SQL_WCHAR) {
	//				TableCol[i].ColDataType = SQL_WCHAR;
	//				TableCol[i].ColTypeOutput = charNameUCS2;
	//				TableCol[i].Remark = charUCS2;
	//			}
	//			else if (TableCol[i].ColDataType == SQL_WVARCHAR) {
	//				TableCol[i].ColDataType = SQL_WVARCHAR;
	//				TableCol[i].ColTypeOutput = varcharNameUCS2;
	//				TableCol[i].Remark = varcharUCS2;
	//			}
	//			else {
	//				TableCol[i].ColDataType = SQL_WLONGVARCHAR;
	//				TableCol[i].ColTypeOutput = longvarcharNameUCS2;
	//				TableCol[i].Remark = varcharUCS2;
	//			}
	//		}
	//		i++;
	//	}
	//	i = 0;
	//}

//=========================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => MX Specific SQLColumns.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLColumns tests\n");

        if(!FullConnectWithOptions(pTestInfo,CONNECT_ODBC_VERSION_3))
//	if(!FullConnect(pTestInfo))
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

	TESTCASE_END;  // end of setup

//=========================================================================================

	_tcscpy(TableQualifier,pTestInfo->Catalog);
	_tcscpy(TableOwner,pTestInfo->Schema);
	TableColStr = (TCHAR *)malloc(MAX_NOS_SIZE);
	TableStr = (TCHAR *)malloc(MAX_NOS_SIZE);
	for (j = 0; j < ACCESS_MODE; j++)
	{
		i = 0;
		_tcscpy(TableName,TabName);
		_tcscpy(TableColStr,_T(""));
		while (_tcsicmp(TableCol[i].ColName,_T("endloop")) != 0)
		{
			if ( i > 0) _tcscat(TableColStr,_T(","));
			_tcscat(TableColStr, TableCol[i].ColName);
			_tcscat(TableColStr,_T(" "));
			_tcscat(TableColStr, TableCol[i].ColTypeName);
			_tcscat(TableColStr, TableCol[i].ColTypePrec);
			_tcscat(TableColStr, ColNull[TableCol[i].ColNullable]);
			_tcscpy(TableStr, TableOps[0].CrtTab);
			_tcscat(TableStr, TableColStr);

			_tcscat(TableStr,_T(") no partition"));
			
			_stprintf(Heading,_T("Test create table =>"));
			_tcscat(Heading,TableStr);
			_tcscat(Heading,_T("\n"));
			TESTCASE_BEGINW(Heading);
			returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
			SQLExecDirect(hstmt,(SQLTCHAR*)TableOps[0].DrpTab,SQL_NTS);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableStr,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			else
			{
				TESTCASE_END;
				_stprintf(Heading,_T("SQLColumns: Test #%d \n"),i);
				//_tcscat(Heading,TableStr);
				//_tcscat(Heading,"\n");
				TESTCASE_BEGINW(Heading);
				//LogMsg(NONE, "SQLSetConnectOption(SQL_ACCESS_MODE,%d)\n", ConnectOption.vParamInt[j]);
				returncode = SQLSetConnectOption((SQLHANDLE)hdbc,ConnectOption.fOption,ConnectOption.vParamInt[j]);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				if (_tcslen(TableQualifier) > 0) {
					returncode = SQLColumns(hstmt,(SQLTCHAR*)TableQualifier,(SWORD)_tcslen(TableQualifier),(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName),(SQLTCHAR*)ColInput,(SWORD)_tcslen(ColInput));
					//LogMsg(NONE,_T("SQLColumns(hstmt,%s,%d,%s,%d,%s,%d,%s,%d)\n"),(SQLTCHAR*)TableQualifier,(SWORD)_tcslen(TableQualifier),(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName),(SQLTCHAR*)ColInput,(SWORD)_tcslen(ColInput));
				}
				else {
					returncode = SQLColumns(hstmt,NULL,0,(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName),(SQLTCHAR*)ColInput,(SWORD)_tcslen(ColInput));
					//LogMsg(NONE,_T("SQLColumns(hstmt,%s,%d,%s,%d,%s,%d,%s,%d)\n"),(SQLTCHAR*)"NULL",(SWORD)0,(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName),(SQLTCHAR*)ColInput,(SWORD)_tcslen(ColInput));
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumns"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				else
				{
					LogMsg(NONE,_T("SQLColumns: SQLColumns function call executed correctly.\n"));
					_tcscpy(oTableQualifier,_T(""));
					_tcscpy(oTableOwner,_T(""));
					_tcscpy(oTableName,_T(""));
					_tcscpy(oColName,_T(""));
					oColDataType = 0;
					_tcscpy(oColTypeName,_T(""));
					oColPrec = 0;
					oColLen = 0;
					oColScale = 0;
					oColRadix = 0;
					oColNullable = 0;
					_tcscpy(oRemark,_T(""));
					returncode = SQLBindCol(hstmt,1,SQL_C_TCHAR,oTableQualifier,NAME_LEN,&oTableQualifierlen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,2,SQL_C_TCHAR,oTableOwner,NAME_LEN,&oTableOwnerlen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,3,SQL_C_TCHAR,oTableName,NAME_LEN,&oTableNamelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,4,SQL_C_TCHAR,oColName,NAME_LEN,&oColNamelen);
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
					returncode = SQLBindCol(hstmt,6,SQL_C_TCHAR,oColTypeName,NAME_LEN,&oColTypeNamelen);
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
					returncode = SQLBindCol(hstmt,12,SQL_C_TCHAR,oRemark,REM_LEN,&oRemarklen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					k = 0;
					while (returncode == SQL_SUCCESS)
					{
						_tcscpy(oTableQualifier,_T(""));
						_tcscpy(oTableOwner,_T(""));
						_tcscpy(oTableName,_T(""));
						_tcscpy(oColName,_T(""));
						oColDataType = 0;
						_tcscpy(oColTypeName,_T(""));
						oColPrec = 0;
						oColLen = 0;
						oColScale = 0;
						oColRadix = 0;
						oColNullable = 0;
						_tcscpy(oRemark,_T(""));
						returncode = SQLFetch(hstmt);
						if((returncode!=SQL_NO_DATA_FOUND) && (!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
						{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
						}
						else if (returncode == SQL_SUCCESS)
						{
							_stprintf(Heading,_T("\nSQLColumns: compare results of columns fetched for following column \n"));
							_tcscat(Heading,_T("The Column Name is ")); 
							_tcscat(Heading,TableCol[k].ColName);
							_tcscat(Heading,_T(" and column type is "));
							_tcscat(Heading,TableCol[k].ColTypeName);
							_tcscat(Heading,_T("\n"));
							LogMsg(NONE,Heading);
							if (_tcslen(TableQualifier) == 0)
							{
								//_tcscpy(TableQualifier, _T("TRAFODION"));
								_tcscpy(TableQualifier, _T("TRAFODION"));
							}
							if ((cwcscmp(TableQualifier,oTableQualifier,TRUE) == 0) 
								&& (cwcscmp(TableOwner,oTableOwner,TRUE) == 0) 
								&& (cwcscmp(TableName,oTableName,TRUE) == 0) 
								&& (cwcscmp(TableCol[k].ColName,oColName,TRUE) == 0) 
								&& (TableCol[k].ColDataType == oColDataType) 
								&& (_tcsnicmp(oColTypeName,TableCol[k].ColTypeOutput,_tcslen(oColTypeName)) == 0) 
								&& (TableCol[k].ColPrec == oColPrec)
								&& (TableCol[k].ColLen == oColLen)
								&& (TableCol[k].ColScale == oColScale)
								&& (TableCol[k].ColRadix == oColRadix)
								&& (TableCol[k].ColNullable == oColNullable)
								&& (_tcsicmp(TableCol[k].Remark,oRemark) == 0))
							{
								LogMsg(NONE,_T("TableQualifier expect: %s and actual: %s are matched\n"),TableQualifier,oTableQualifier);
								LogMsg(NONE,_T("TableOwner expect: %s and actual: %s are matched\n"),TableOwner,oTableOwner);
								LogMsg(NONE,_T("TableName expect: %s and actual: %s are matched\n"),TableName,oTableName);
								LogMsg(NONE,_T("ColName expect: %s and actual: %s are matched\n"),TableCol[k].ColName,oColName);
								LogMsg(NONE,_T("ColDataType expect: %d and actual: %d are matched\n"),TableCol[k].ColDataType,oColDataType);
								LogMsg(NONE,_T("ColTypeName expect: %s and actual: %s are matched\n"),TableCol[k].ColTypeOutput,oColTypeName);
								LogMsg(NONE,_T("ColPrec expect: %d and actual: %d are matched\n"),TableCol[k].ColPrec,oColPrec);
								LogMsg(NONE,_T("ColLen expect: %d and actual: %d are matched\n"),TableCol[k].ColLen,oColLen);
								LogMsg(NONE,_T("ColScale expect: %d and actual: %d are matched\n"),TableCol[k].ColScale,oColScale);
								LogMsg(NONE,_T("ColRadix expect: %d and actual: %d are matched\n"),TableCol[k].ColRadix,oColRadix);
								LogMsg(NONE,_T("ColNullable expect: %d and actual: %d are matched\n"),TableCol[k].ColNullable,oColNullable);
								LogMsg(NONE,_T("Remark expect: %s and actual: %s are matched\n"),TableCol[k].Remark,oRemark);
							}	
							else
							{
								TEST_FAILED;	
								if (cwcscmp(TableQualifier,oTableQualifier,TRUE) != 0)
									LogMsg(ERRMSG,_T("TableQualifier expect: %s and actual: %s are not matched\n"),TableQualifier,oTableQualifier);
								if (cwcscmp(TableOwner,oTableOwner,TRUE) != 0) 
									LogMsg(ERRMSG,_T("TableOwner expect: %s and actual: %s are not matched\n"),TableOwner,oTableOwner);
								if (cwcscmp(TableName,oTableName,TRUE) != 0) 
									LogMsg(ERRMSG,_T("TableName expect: %s and actual: %s are not matched\n"),TableName,oTableName);
								if (cwcscmp(TableCol[k].ColName,oColName,TRUE) != 0) 
									LogMsg(ERRMSG,_T("ColName expect: %s and actual: %s are not matched\n"),TableCol[k].ColName,oColName);
								if (TableCol[k].ColDataType != oColDataType) 
									LogMsg(ERRMSG,_T("ColDataType expect: %d and actual: %d are not matched\n"),TableCol[k].ColDataType,oColDataType);
								if (_tcsnicmp(oColTypeName,TableCol[k].ColTypeOutput,_tcslen(oColTypeName)) != 0) 
									LogMsg(ERRMSG,_T("ColTypeName expect: %s and actual: %s are not matched\n"),TableCol[k].ColTypeOutput,oColTypeName);
								if (TableCol[k].ColPrec != oColPrec)
									LogMsg(ERRMSG,_T("ColPrec expect: %d and actual: %d are not matched\n"),TableCol[k].ColPrec,oColPrec);
								if (TableCol[k].ColLen != oColLen)
									LogMsg(ERRMSG,_T("ColLen expect: %d and actual: %d are not matched\n"),TableCol[k].ColLen,oColLen);
								if (TableCol[k].ColScale != oColScale)
									LogMsg(ERRMSG,_T("ColScale expect: %d and actual: %d are not matched\n"),TableCol[k].ColScale,oColScale);
								if (TableCol[k].ColRadix != oColRadix)
									LogMsg(ERRMSG,_T("ColRadix expect: %d and actual: %d are not matched\n"),TableCol[k].ColRadix,oColRadix);
								if (TableCol[k].ColNullable != oColNullable)
									LogMsg(ERRMSG,_T("ColNullable expect: %d and actual: %d are not matched\n"),TableCol[k].ColNullable,oColNullable);
								if (_tcsicmp(TableCol[k].Remark,oRemark) != 0)
									LogMsg(ERRMSG,_T("Remark expect: %s and actual: %s are not matched\n"),TableCol[k].Remark,oRemark);
							}
						k++;
						}
					}
					SQLFreeStmt(hstmt,SQL_UNBIND);
					SQLFreeStmt(hstmt,SQL_CLOSE);
					if(k == 0)
					{
						TEST_FAILED;
						LogMsg(ERRMSG,_T("No Data Found => Atleast one row should be fetched\n"));
					} else {
                        LogMsg(NONE,_T("Number of rows fetched: %d\n"), k);
                    }
				}
				TESTCASE_END;
			}
			returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
			SQLExecDirect(hstmt,(SQLTCHAR*)TableOps[0].DrpTab,SQL_NTS);
			i++;
		}

		//Testing view, materialized view and synonym
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		i = 2;
		while (i<5)
		{
			_tcscpy(TableName,MVSName[i-2]);
			_stprintf(Heading,_T("Test create table =>"));
			_tcscat(Heading,TableOps[i].CrtTab);
			_tcscat(Heading,_T("\n"));
			TESTCASE_BEGINW(Heading);
			returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
			SQLExecDirect(hstmt,(SQLTCHAR*)TableOps[i].DrpTab,SQL_NTS);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableOps[i].CrtTab,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			else
			{
				TESTCASE_END;
				_stprintf(Heading,_T("SQLColumns: Test #%d \n"),i);
				TESTCASE_BEGINW(Heading);
				returncode = SQLSetConnectOption((SQLHANDLE)hdbc,ConnectOption.fOption,ConnectOption.vParamInt[j]);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectOption"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				if (_tcslen(TableQualifier) > 0) {
					returncode = SQLColumns(hstmt,(SQLTCHAR*)TableQualifier,(SWORD)_tcslen(TableQualifier),(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName),(SQLTCHAR*)ColInput,(SWORD)_tcslen(ColInput));
					//LogMsg(NONE,_T("SQLColumns(hstmt,%s,%d,%s,%d,%s,%d,%s,%d)\n"),(SQLTCHAR*)TableQualifier,(SWORD)_tcslen(TableQualifier),(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName),(SQLTCHAR*)ColInput,(SWORD)_tcslen(ColInput));
				}
				else {
					returncode = SQLColumns(hstmt,NULL,0,(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName),(SQLTCHAR*)ColInput,(SWORD)_tcslen(ColInput));
					//LogMsg(NONE,_T("SQLColumns(hstmt,%s,%d,%s,%d,%s,%d,%s,%d)\n"),(SQLTCHAR*)"NULL",(SWORD)0,(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName),(SQLTCHAR*)ColInput,(SWORD)_tcslen(ColInput));
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumns"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				else
				{
					LogMsg(NONE,_T("SQLColumns: SQLColumns function call executed correctly.\n"));
					_tcscpy(oTableQualifier,_T(""));
					_tcscpy(oTableOwner,_T(""));
					_tcscpy(oTableName,_T(""));
					_tcscpy(oColName,_T(""));
					oColDataType = 0;
					_tcscpy(oColTypeName,_T(""));
					oColPrec = 0;
					oColLen = 0;
					oColScale = 0;
					oColRadix = 0;
					oColNullable = 0;
					_tcscpy(oRemark,_T(""));
					returncode = SQLBindCol(hstmt,1,SQL_C_TCHAR,oTableQualifier,NAME_LEN,&oTableQualifierlen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,2,SQL_C_TCHAR,oTableOwner,NAME_LEN,&oTableOwnerlen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,3,SQL_C_TCHAR,oTableName,NAME_LEN,&oTableNamelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,4,SQL_C_TCHAR,oColName,NAME_LEN,&oColNamelen);
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
					returncode = SQLBindCol(hstmt,6,SQL_C_TCHAR,oColTypeName,NAME_LEN,&oColTypeNamelen);
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
					returncode = SQLBindCol(hstmt,12,SQL_C_TCHAR,oRemark,REM_LEN,&oRemarklen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
					}
					k = 0;
					while (returncode == SQL_SUCCESS)
					{
						_tcscpy(oTableQualifier,_T(""));
						_tcscpy(oTableOwner,_T(""));
						_tcscpy(oTableName,_T(""));
						_tcscpy(oColName,_T(""));
						oColDataType = 0;
						_tcscpy(oColTypeName,_T(""));
						oColPrec = 0;
						oColLen = 0;
						oColScale = 0;
						oColRadix = 0;
						oColNullable = 0;
						_tcscpy(oRemark,_T(""));
						returncode = SQLFetch(hstmt);
						if((returncode!=SQL_NO_DATA_FOUND) && (!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
						{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
						}
						else if (returncode == SQL_SUCCESS)
						{
							_stprintf(Heading,_T("\nSQLColumns: compare results of columns fetched for following column \n"));
							_tcscat(Heading,_T("The Column Name is ")); 
							_tcscat(Heading,TableCol[k].ColName);
							_tcscat(Heading,_T(" and column type is "));
							_tcscat(Heading,TableCol[k].ColTypeName);
							_tcscat(Heading,_T("\n"));
							LogMsg(NONE,Heading);
							if (_tcslen(TableQualifier) == 0)
							{
								//_tcscpy(TableQualifier, _T("TRAFODION"));
								_tcscpy(TableQualifier, _T("TRAFODION"));
							}
							if ((cwcscmp(TableQualifier,oTableQualifier,TRUE) == 0) 
								&& (cwcscmp(TableOwner,oTableOwner,TRUE) == 0) 
								&& (cwcscmp(TableName,oTableName,TRUE) == 0) 
								&& (cwcscmp(TableCol[k].ColName,oColName,TRUE) == 0) 
								&& (TableCol[k].ColDataType == oColDataType) 
								&& (_tcsnicmp(oColTypeName,TableCol[k].ColTypeOutput,_tcslen(oColTypeName)) == 0) 
								&& (TableCol[k].ColPrec == oColPrec)
								&& (TableCol[k].ColLen == oColLen)
								&& (TableCol[k].ColScale == oColScale)
								&& (TableCol[k].ColRadix == oColRadix)
								&& (TableCol[k].ColNullable == oColNullable)
								&& (_tcsicmp(TableCol[k].Remark,oRemark) == 0))
							{
								LogMsg(NONE,_T("TableQualifier expect: %s and actual: %s are matched\n"),TableQualifier,oTableQualifier);
								LogMsg(NONE,_T("TableOwner expect: %s and actual: %s are matched\n"),TableOwner,oTableOwner);
								LogMsg(NONE,_T("TableName expect: %s and actual: %s are matched\n"),TableName,oTableName);
								LogMsg(NONE,_T("ColName expect: %s and actual: %s are matched\n"),TableCol[k].ColName,oColName);
								LogMsg(NONE,_T("ColDataType expect: %d and actual: %d are matched\n"),TableCol[k].ColDataType,oColDataType);
								LogMsg(NONE,_T("ColTypeName expect: %s and actual: %s are matched\n"),TableCol[k].ColTypeOutput,oColTypeName);
								LogMsg(NONE,_T("ColPrec expect: %d and actual: %d are matched\n"),TableCol[k].ColPrec,oColPrec);
								LogMsg(NONE,_T("ColLen expect: %d and actual: %d are matched\n"),TableCol[k].ColLen,oColLen);
								LogMsg(NONE,_T("ColScale expect: %d and actual: %d are matched\n"),TableCol[k].ColScale,oColScale);
								LogMsg(NONE,_T("ColRadix expect: %d and actual: %d are matched\n"),TableCol[k].ColRadix,oColRadix);
								LogMsg(NONE,_T("ColNullable expect: %d and actual: %d are matched\n"),TableCol[k].ColNullable,oColNullable);
								LogMsg(NONE,_T("Remark expect: %s and actual: %s are matched\n"),TableCol[k].Remark,oRemark);
							}	
							else
							{
								TEST_FAILED;	
								if (cwcscmp(TableQualifier,oTableQualifier,TRUE) != 0)
									LogMsg(ERRMSG,_T("TableQualifier expect: %s and actual: %s are not matched\n"),TableQualifier,oTableQualifier);
								if (cwcscmp(TableOwner,oTableOwner,TRUE) != 0) 
									LogMsg(ERRMSG,_T("TableOwner expect: %s and actual: %s are not matched\n"),TableOwner,oTableOwner);
								if (cwcscmp(TableName,oTableName,TRUE) != 0) 
									LogMsg(ERRMSG,_T("TableName expect: %s and actual: %s are not matched\n"),TableName,oTableName);
								if (cwcscmp(TableCol[k].ColName,oColName,TRUE) != 0) 
									LogMsg(ERRMSG,_T("ColName expect: %s and actual: %s are not matched\n"),TableCol[k].ColName,oColName);
								if (TableCol[k].ColDataType != oColDataType) 
									LogMsg(ERRMSG,_T("ColDataType expect: %d and actual: %d are not matched\n"),TableCol[k].ColDataType,oColDataType);
								if (_tcsnicmp(oColTypeName,TableCol[k].ColTypeOutput,_tcslen(oColTypeName)) != 0) 
									LogMsg(ERRMSG,_T("ColTypeName expect: %s and actual: %s are not matched\n"),TableCol[k].ColTypeOutput,oColTypeName);
								if (TableCol[k].ColPrec != oColPrec)
									LogMsg(ERRMSG,_T("ColPrec expect: %d and actual: %d are not matched\n"),TableCol[k].ColPrec,oColPrec);
								if (TableCol[k].ColLen != oColLen)
									LogMsg(ERRMSG,_T("ColLen expect: %d and actual: %d are not matched\n"),TableCol[k].ColLen,oColLen);
								if (TableCol[k].ColScale != oColScale)
									LogMsg(ERRMSG,_T("ColScale expect: %d and actual: %d are not matched\n"),TableCol[k].ColScale,oColScale);
								if (TableCol[k].ColRadix != oColRadix)
									LogMsg(ERRMSG,_T("ColRadix expect: %d and actual: %d are not matched\n"),TableCol[k].ColRadix,oColRadix);
								if (TableCol[k].ColNullable != oColNullable)
									LogMsg(ERRMSG,_T("ColNullable expect: %d and actual: %d are not matched\n"),TableCol[k].ColNullable,oColNullable);
								if (_tcsicmp(TableCol[k].Remark,oRemark) != 0)
									LogMsg(ERRMSG,_T("Remark expect: %s and actual: %s are not matched\n"),TableCol[k].Remark,oRemark);
							}
						k++;
						}
					}
					SQLFreeStmt(hstmt,SQL_UNBIND);
					SQLFreeStmt(hstmt,SQL_CLOSE);
					if(k == 0)
					{
						TEST_FAILED;
						LogMsg(ERRMSG,_T("No Data Found => Atleast one row should be fetched\n"));
					} else {
                        LogMsg(NONE,_T("Number of rows fetched: %d\n"), k);
                    }
				}
				TESTCASE_END;
			}
			returncode = SQLSetConnectOption((SQLHANDLE)hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
			i++;
		}

		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableOps[4].DrpTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableOps[3].DrpTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableOps[2].DrpTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableOps[0].DrpTab,SQL_NTS);
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
	_stprintf(Heading,_T("Setting up Table & view to test SQLTables for wildcard options => \n"));
	_tcscat(Heading,_T("\n"));
	TESTCASE_BEGINW(Heading);
	SQLExecDirect(hstmt,(SQLTCHAR*)TableOps[1].DrpTab,SQL_NTS);
	LogMsg(NONE,_T("%s\n"), TableOps[1].CrtTab);
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableOps[1].CrtTab,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	else
	{
		LogMsg(NONE,_T("setting up tables executed successfully.\n"));
		TESTCASE_END;
	}

	i = 0;
	while (_tcsicmp(ColumnWC[i].TabQua,_T("endloop")) != 0)
	{
        returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_FALSE,0);
	    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	    {
		    TEST_FAILED;
		    LogAllErrors(henv,hdbc,hstmt);
	    }// end of setup

		memset (Heading, 0, MAX_HEADING_SIZE);  //RS: clean up buffer
		// _stprintf(Heading,_T(""));
		_stprintf(Heading,_T("SQLColumns: wildcard options => \nTable Qualifier: %s \nTable Owner: %s \nTable Name: %s \nColumn Name: %s\n"),
			printSymbol(ColumnWC[i].TabQua,displayBuf.cat),
            printSymbol(ColumnWC[i].TabOwner,displayBuf.sch),
            printSymbol(ColumnWC[i].TabName,displayBuf.tab),
            printSymbol(ColumnWC[i].ColName,displayBuf.col));

		TESTCASE_BEGINW(Heading);
		NullValue = 0;		
		if (_tcsicmp(ColumnWC[i].TabQua,_T("NULL")) == 0)
		{
			ColumnWC[i].TabQua = NULL;
			NullValue = 1;
		}
		if (_tcsicmp(ColumnWC[i].TabOwner,_T("NULL")) == 0)
		{
			ColumnWC[i].TabOwner = NULL;
			NullValue = 1;
		}
		if (_tcsicmp(ColumnWC[i].TabName,_T("NULL")) == 0)
		{
			ColumnWC[i].TabName = NULL;
			NullValue = 1;
		}
		if (_tcsicmp(ColumnWC[i].ColName,_T("NULL")) == 0)
		{
			ColumnWC[i].ColName = NULL;
			NullValue = 1;
		}

		if (NullValue == 1)
		{
			returncode = SQLColumns(hstmt,(SQLTCHAR*)ColumnWC[i].TabQua,SQL_NTS,(SQLTCHAR*)ColumnWC[i].TabOwner,SQL_NTS,
										  (SQLTCHAR*)ColumnWC[i].TabName,SQL_NTS,(SQLTCHAR*)ColumnWC[i].ColName,SQL_NTS);
		}
		else
		{
			returncode = SQLColumns(hstmt,(SQLTCHAR*)ColumnWC[i].TabQua,(SWORD)_tcslen(ColumnWC[i].TabQua),
										  (SQLTCHAR*)ColumnWC[i].TabOwner,(SWORD)_tcslen(ColumnWC[i].TabOwner),
										  (SQLTCHAR*)removeQuotes(ColumnWC[i].TabName,displayBuf.tab),(SWORD)_tcslen(displayBuf.tab),
										  (SQLTCHAR*)removeQuotes(ColumnWC[i].ColName,displayBuf.col),(SWORD)_tcslen(displayBuf.col));
		}
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumns"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		else
		{
			LogMsg(NONE,_T("SQLColumns: Executed successfully.\n"));
	 		_tcscpy(oTableQualifier,_T(""));
			_tcscpy(oTableOwner,_T(""));
			_tcscpy(oTableName,_T(""));
			_tcscpy(oColName,_T(""));
			oColDataType = 0;
			_tcscpy(oColTypeName,_T(""));
			oColPrec = 0;
			oColLen = 0;
			oColScale = 0;
			oColRadix = 0;
			oColNullable = 0;
			_tcscpy(oRemark,_T(""));
			returncode = SQLBindCol(hstmt,1,SQL_C_TCHAR,oTableQualifier,NAME_LEN,&oTableQualifierlen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,2,SQL_C_TCHAR,oTableOwner,NAME_LEN,&oTableOwnerlen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,3,SQL_C_TCHAR,oTableName,NAME_LEN,&oTableNamelen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,4,SQL_C_TCHAR,oColName,NAME_LEN,&oColNamelen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
			}
			returncode = SQLBindCol(hstmt,5,SQL_C_SHORT,&oColDataType,0,&oColDataTypelen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,6,SQL_C_TCHAR,oColTypeName,NAME_LEN,&oColTypeNamelen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,7,SQL_C_LONG,&oColPrec,0,&oColPreclen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,8,SQL_C_LONG,&oColLen,0,&oColLenlen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,9,SQL_C_SHORT,&oColScale,0,&oColScalelen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,10,SQL_C_SHORT,&oColRadix,0,&oColRadixlen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,11,SQL_C_SHORT,&oColNullable,0,&oColNullablelen);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLBindCol(hstmt,12,SQL_C_TCHAR,oRemark,REM_LEN,&oRemarklen);
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
				LogMsg(ERRMSG,_T("No Data Found => Atleast one row should be fetched\n"));
			} else {
                LogMsg(NONE,_T("Number of rows fetched: %d\n"), k);
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
	returncode = SQLColumns(hstmt1,ColumnWC[0].TabQua,(SWORD)_tcslen(ColumnWC[0].TabQua),ColumnWC[0].TabOwner,(SWORD)_tcslen(ColumnWC[0].TabOwner),ColumnWC[0].TabName,(SWORD)_tcslen(ColumnWC[0].TabName),ColumnWC[0].ColName,(SWORD)_tcslen(ColumnWC[0].ColName));
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
	returncode = SQLColumns(hstmt1,(SQLTCHAR*)ColumnWC[0].TabQua,(SWORD)_tcslen(ColumnWC[0].TabQua),(SQLTCHAR*)ColumnWC[0].TabOwner,(SWORD)_tcslen(ColumnWC[0].TabOwner),(SQLTCHAR*)ColumnWC[0].TabName,(SWORD)_tcslen(ColumnWC[0].TabName),(SQLTCHAR*)ColumnWC[0].ColName,(SWORD)_tcslen(ColumnWC[0].ColName));
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLColumns"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("SQLColumns: Negative test with Invalid lengths to valid SQLColumns args\n");

	t = 0;
	while (_tcsicmp(ColumnWC2[t].TabQua,_T("endloop")) != 0)
	{
		returncode = SQLColumns(hstmt,(SQLTCHAR*)ColumnWC2[t].TabQua,ColumnWC2[t].TabQuaLen,(SQLTCHAR*)ColumnWC2[t].TabOwner,ColumnWC2[t].TabOwnerLen,(SQLTCHAR*)ColumnWC2[t].TabName,ColumnWC2[t].TabNameLen,(SQLTCHAR*)ColumnWC2[t].ColName,ColumnWC2[t].ColNameLen);
		if(!CHECKRC(SQL_ERROR,returncode,"SQLColumns"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG, _T("Test failed while inside negative test with invalid lengths"));
			LogAllErrors(henv,hdbc,hstmt);
		}
		t++;
	}

	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("SQLColumns: Negative test with invalid SQLColumns arguments\n");

	t = 0;
	while (_tcsicmp(ColumnWC3[t].TabQua,_T("endloop")) != 0)
	{
		returncode = SQLColumns(hstmt,(SQLTCHAR*)ColumnWC3[t].TabQua,(SWORD)_tcslen(ColumnWC3[t].TabQua),(SQLTCHAR*)ColumnWC3[t].TabOwner,(SWORD)_tcslen(ColumnWC3[t].TabOwner),(SQLTCHAR*)ColumnWC3[t].TabName,(SWORD)_tcslen(ColumnWC3[t].TabName),(SQLTCHAR*)ColumnWC3[t].ColName,(SWORD)_tcslen(ColumnWC3[t].ColName));
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumns"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG, _T("Test failed while inside negative test with invalid SQLColumns arguments SQLColumns Failed\n"));
			LogAllErrors(henv,hdbc,hstmt);
		}
		returncode = SQLFetch(hstmt);
		if(returncode!=SQL_NO_DATA_FOUND)
		{
		  LogMsg(ERRMSG, _T("Test failed while inside negative test with invalid SQLColumns arguments SQLColumns returned some data\n"));
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

        _stprintf(Heading,_T("SQLColumns: wildcard options => \nTable Qualifier: %s \nTable Owner: %s \nTable Name: %s \nColumn Name: %s\n"),
			printSymbol(ColumnWC[k].TabQua,displayBuf.cat),
            printSymbol(ColumnWC[k].TabOwner,displayBuf.sch),
            printSymbol(ColumnWC[k].TabName,displayBuf.tab),
            printSymbol(ColumnWC[k].ColName,displayBuf.col));
        LogMsg(NONE,Heading);

		returncode = SQLColumns(hstmt,(SQLTCHAR*)ColumnWC[k].TabQua,(SWORD)_tcslen(ColumnWC[k].TabQua),
									  (SQLTCHAR*)ColumnWC[k].TabOwner,(SWORD)_tcslen(ColumnWC[k].TabOwner),
									  (SQLTCHAR*)removeQuotes(ColumnWC[k].TabName,displayBuf.tab),(SWORD)_tcslen(displayBuf.tab),
									  (SQLTCHAR*)removeQuotes(ColumnWC[k].ColName,displayBuf.col),(SWORD)_tcslen(displayBuf.col));

		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumns"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		returncode = SQLNumResultCols(hstmt, &numOfCols);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultsCol"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG,_T("Test failed while executing call for SQLNUMRESULTSCOL\n"));
			LogAllErrors(henv,hdbc,hstmt);
		}


		for(cols = 0; cols < numOfCols; cols++)
		{
			returncode = SQLDescribeCol(hstmt,(SWORD)(cols+1),(SQLTCHAR*)cn,COLNAME_LEN,&cl,&st,&cp,&cs,&cnull);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDescribeCol"))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,_T("Test failed while executing call for SQLDESCRIBECOL of column\n"));
				LogAllErrors(henv,hdbc,hstmt);
			}
			CharOutput[cols] = (TCHAR *)malloc(STR_LEN);
			for (iatt = 0; iatt <= totatt; iatt++)
			{
				_tcscpy(rgbDesc,_T(""));
				pcbDesc = 0;
				pfDesc = 0;
				returncode = SQLColAttributes(hstmt,(SWORD)(cols+1),DescrType[iatt],rgbDesc,STR_LEN,&pcbDesc,&pfDesc);
				//LogMsg(NONE,_T("SQLColattributes(hstmt,%d,%d,%s,%d,%d,%d)\n"),(SWORD)(cols+1),DescrType[iatt],rgbDesc,STR_LEN,&pcbDesc,&pfDesc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColAttribute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
			returncode = SQLBindCol(hstmt,(SWORD)(cols+1),SQL_C_TCHAR,CharOutput[cols],STR_LEN,&stringlength);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,_T("Test failed while executing call for SQLBindCols of column : %d.\n"),cols);
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
			} else if (returncode == SQL_NO_DATA_FOUND) {
				break;
			} else {
				if(returncode == SQL_SUCCESS_WITH_INFO)
					LogAllErrors(henv,hdbc,hstmt);
				t++;
			}
		}
		if(t == 0)
		{
			TEST_FAILED;
			LogMsg(ERRMSG,_T("No Data Found => Atleast one row should be fetched\n"));
        } else {
            LogMsg(NONE,_T("Number of rows fetched: %d\n"), t);
        }
		
		for(cols = 0; cols < numOfCols; cols++)
		{
			free(CharOutput[cols]);
		}
		TESTCASE_END;
	}
	
	//clean up
	SQLExecDirect(hstmt,(SQLTCHAR *)(TableOps[1].DrpTab),SQL_NTS);

//=========================================================================================

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => MX Specific SQLColumns.\n"));
	free_list(var_list);
	TEST_RETURN;
}
