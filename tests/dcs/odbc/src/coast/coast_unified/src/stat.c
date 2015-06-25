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
#define NUM_OUTPUTS	13
#define NUM_UNIQUE	2
#define NUM_ACCU		2
#define NUM_IDX			2
#define COLNAME_LEN	30
#define	RGB_MAX_LEN	50
#define STR_LEN     (128+1)*sizeof(TCHAR)    //added to test SQLBindCols and SQLFetch
#define TABTYPE_LEN	30
#define TOTALATTRIBS 18

/*
---------------------------------------------------------
   TestSQLStatistics
---------------------------------------------------------
*/
PassFail TestSQLStatistics(TestInfo *pTestInfo, int MX_MP_SPECIFIC)
{                  
	TEST_DECLARE;
 	TCHAR			Heading[MAX_HEADING_SIZE];
 	SQLRETURN		returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt, hstmt1;
 	TCHAR			TQualifier[NAME_LEN],TOwner[NAME_LEN],TName[NAME_LEN],End_Loop[10];
	UWORD			Unique[NUM_UNIQUE] = {SQL_INDEX_UNIQUE,SQL_INDEX_ALL};
	UWORD			Accuracy[NUM_ACCU] = {SQL_ENSURE,SQL_QUICK};
	TCHAR			otqua[NAME_LEN],otowner[NAME_LEN],otname[NAME_LEN];
	TCHAR			oiqua[NAME_LEN],riqua[NAME_LEN];
	TCHAR			oiname[NAME_LEN],riname[NAME_LEN],ocname[NAME_LEN],rcname[MAX_NOS_SIZE];
	TCHAR			ocsort[2],rcsort[3];
	TCHAR			oifil[NAME_LEN],rifil[NAME_LEN];
	SWORD			ounique,runique = 0;
	SWORD			otype,rtype = SQL_INDEX_OTHER;
	SWORD			oiseq = 0;
	SDWORD			ocar,rcar = 0;
	SDWORD			opages,rpages = 0;
	SQLLEN			otqualen,otownerlen,otnamelen,ouniquelen,oiqualen,oinamelen,otypelen,oiseqlen;
	SQLLEN			ocnamelen,ocsortlen,ocarlen,opageslen,oifillen;

	int				cols;
	int				iatt;
	SWORD			numOfCols = 0;
	SWORD			pcbDesc;
	SQLLEN			pfDesc;
	TCHAR			cn[COLNAME_LEN];
	SWORD			cl;
	SWORD			st;
	SQLULEN			cp;
	SWORD			cs, cnull;
	TCHAR			rgbDesc[RGB_MAX_LEN];
	TCHAR			*CharOutput[40];
	SQLLEN			stringlength;


	struct
	{
		TCHAR		*ColName;
		TCHAR		*ColType;
		TCHAR		*sort;
	} Columns[] = {
							{_T("")		,_T("")				,_T("")},
							{_T("--")	,_T("char(10) CHARACTER SET ISO88591")		,_T("ASC")},
							{_T("--")	,_T("varchar(10) CHARACTER SET ISO88591")	,_T("DESC")},
							{_T("--")	,_T("char(10) CHARACTER SET UCS2")		,_T("ASC")},
							{_T("--")	,_T("varchar(10) CHARACTER SET UCS2")	,_T("DESC")},
							{_T("--")	,_T("char(10) CHARACTER SET utf8")		,_T("ASC")},
							{_T("--")	,_T("varchar(10) CHARACTER SET utf8")	,_T("DESC")},
							{_T("--")	,_T("decimal(10,5)"),_T("ASC")},
							{_T("--")	,_T("numeric(10,5)"),_T("DESC")},
							{_T("--")	,_T("numeric(19,6)"),_T("DESC")},			//for bignum
							{_T("--")	,_T("numeric(10,5) unsigned"),_T("ASC")},	//for bignum
							{_T("--")	,_T("smallint")		,_T("ASC")},
							{_T("--")	,_T("integer")		,_T("DESC")},
							{_T("--")	,_T("bigint")		,_T("ASC")},
							{_T("--")	,_T("date")			,_T("ASC")},
							{_T("--")	,_T("time")			,_T("DESC")},
							{_T("--")	,_T("timestamp")	,_T("ASC")},
							{_T("--")	,_T("bit")			,_T("ASC")},
							#ifdef UNICODE
							{_T("--")	,_T("tinyint")		,_T("DESC")},
							{_T("--")	,_T("binary(10)")	,_T("ASC")},
							#endif
							//{_T("--")	,_T("varbinary(10)"),_T("DESC")},
							{_T("")	,_T("endloop")		,_T("")}
							//{_T("C8")	,_T("real")	,_T("DESC")},
							//{_T("C9")	,_T("float")	,_T("ASC")},
							//{_T("C10"),_T("double precision"),_T("DESC")},
						};

	struct
	{
		TCHAR		*TabQua;
		TCHAR		*TabOwner;
		TCHAR		*TabName;
	} StatisticsWC[] = {								/* wild cards from here */
							//{"TRAFODIN",pTestInfo->Schema,""},
							//{"endloop",},
							//{"",pTestInfo->Schema,""}, 
							//{"",pTestInfo->Schema,"OBJECTS"}, 
							//{"",pTestInfo->Schema,""}, 
							//{"TRAFODIN",pTestInfo->Schema,""},
							// Changing schema name to ODBC_SCHEMA for R2.0	
							//{"TRAFODIN","DEFINITION_SCHEMA_VERSION_1000","TSTTBLST"},
							//{"TRAFODIN","DEFINITION_SCHEMA_VERSION_1000","TSTTBLEI"},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--")},
							{_T("endloop"),}
	};
	//same table but with inaccurate lengths added for negative testing
	struct
	{
		TCHAR		*TabQua;
		SWORD		TabQuaLen;
		TCHAR		*TabOwner;
		SWORD		TabOwnerLen;
		TCHAR		*TabName;
		SWORD		TabNameLen;
	} StatisticsWC2[] = {								/* wild cards from here */
							{pTestInfo->Catalog, (SWORD)-1, pTestInfo->Schema,(SWORD)-1, _T("--"),(SWORD)-1},
						  //{"TRAFODIN", (SWORD)4, pTestInfo->Schema,(SWORD)2, "OBJECTS",(SWORD)2},
						  //{"TRAFODIN", (SWORD)0, pTestInfo->Schema,(SWORD)0, "OBJECTS",(SWORD)0},
							{_T("endloop"),}
						};
	
	//same table but with mixed case letters for testing METADATA_ID = TRUE
	struct
	{
		TCHAR		*TabQua;
		TCHAR		*TabOwner;
		TCHAR		*TabName;
	} StatisticsWC3[] = {				/* wild cards from here */
							//{"TRAFODIN",pTestInfo->Schema,""},
							//{"endloop",},
							//{"",pTestInfo->Schema,""}, 
							//{"",pTestInfo->Schema,"OBJECTS"}, 
							//{"",pTestInfo->Schema,""}, 
							//{"TRAFODIN",pTestInfo->Schema,""},
							// Changing schema name to ODBC_SCHEMA for R2.0					
							//{"TRAFODIN","DEFINITION_SCHEMA_VERSION_1000","TsTtBlSt"},
							//{"TRAFODIN","DEFINITION_SCHEMA_VERSION_1000","tStTbLeI"},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--")},
							{pTestInfo->Catalog,pTestInfo->Schema,_T("--")},
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

	
	TCHAR	*TableStr[3];
	TCHAR	*IndexStr[3];
	TCHAR	*DrpTab[5];
	TCHAR	*CrtTab[2];
	TCHAR	*TabName[3];
	TCHAR	ColStr[MAX_NOS_SIZE],KeyStr[MAX_NOS_SIZE], IdxStr[MAX_NOS_SIZE],*CreateTbl[2],CreateIdx[MAX_NOS_SIZE];
	int		i = 0,k = 0, a = 0,t = 0,idx = 0,l = 0,m = 0;


//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLStatistics"), charset_file);
	if (var_list == NULL) return FAILED;

	Columns[1].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_1"), var_list);
	Columns[2].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_2"), var_list);
	Columns[3].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_3"), var_list);
	Columns[4].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_4"), var_list);
	Columns[5].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_5"), var_list);
	Columns[6].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_6"), var_list);
	Columns[7].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_7"), var_list);
	Columns[8].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_8"), var_list);
	Columns[9].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_9"), var_list);
	Columns[10].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_10"), var_list);
	Columns[11].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_11"), var_list);
	Columns[12].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_12"), var_list);
	Columns[13].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_13"), var_list);
	Columns[14].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_14"), var_list);
	Columns[15].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_15"), var_list);
	Columns[16].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_16"), var_list);
	Columns[17].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_17"), var_list);
	Columns[18].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_18"), var_list);

#ifdef UNICODE
	Columns[19].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_19"), var_list);
	Columns[20].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_20"), var_list);
#endif

	//Columns[21].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_21"), var_list);
	//Columns[22].ColName = var_mapping(_T("SQLStatistics_Columns_ColName_22"), var_list);

	StatisticsWC[0].TabName = var_mapping(_T("SQLStatistics_StatisticsWC_TabName_0"), var_list);
	StatisticsWC[1].TabName = var_mapping(_T("SQLStatistics_StatisticsWC_TabName_1"), var_list);

	StatisticsWC2[0].TabName = var_mapping(_T("SQLStatistics_StatisticsWC2_TabName_0"), var_list);

	StatisticsWC3[0].TabName = var_mapping(_T("SQLStatistics_StatisticsWC3_TabName_0"), var_list);
	StatisticsWC3[1].TabName = var_mapping(_T("SQLStatistics_StatisticsWC3_TabName_1"), var_list);

	TableStr[0] = var_mapping(_T("SQLStatistics_TableStr_0"), var_list);
	TableStr[1] = var_mapping(_T("SQLStatistics_TableStr_1"), var_list);
	TableStr[2] = var_mapping(_T("SQLStatistics_TableStr_2"), var_list);

	IndexStr[0] = var_mapping(_T("SQLStatistics_IndexStr_0"), var_list);
	IndexStr[1] = var_mapping(_T("SQLStatistics_IndexStr_1"), var_list);
	IndexStr[2] = var_mapping(_T("SQLStatistics_IndexStr_2"), var_list);
	
	DrpTab[0] = var_mapping(_T("SQLStatistics_DrpTab_0"), var_list);
	DrpTab[1] = var_mapping(_T("SQLStatistics_DrpTab_1"), var_list);
	DrpTab[2] = var_mapping(_T("SQLStatistics_DrpTab_2"), var_list);
	DrpTab[3] = var_mapping(_T("SQLStatistics_DrpTab_3"), var_list);
	DrpTab[4] = var_mapping(_T("SQLStatistics_DrpTab_4"), var_list);

	CrtTab[0] = var_mapping(_T("SQLStatistics_CrtTab_0"), var_list);
	CrtTab[1] = var_mapping(_T("SQLStatistics_CrtTab_1"), var_list);

	TabName[0] = var_mapping(_T("SQLStatistics_TabName_0"), var_list);
	TabName[1] = var_mapping(_T("SQLStatistics_TabName_1"), var_list);
	TabName[2] = var_mapping(_T("SQLStatistics_TabName_2"), var_list);

//=========================================================================================

	_tcscpy(riqua, _T(""));
	_tcscpy(rcsort, _T("AD"));
	_tcscpy(rifil, _T(""));


	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => MX Specific SQLStatistics.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLStatistics tests\n");

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

	TESTCASE_END;  // end of setup

	ColStr[0] = '\0';											
	KeyStr[0] = '\0';
	IdxStr[0] = '\0';
	_tcscpy(End_Loop,_T(""));
	_tcscpy(TQualifier,pTestInfo->Catalog);
	_tcscpy(TOwner,pTestInfo->Schema);
	_tcscpy(End_Loop,_T("endloop"));
	_tcscpy(TName,TabName[0]);

	i = 1;
	while (_tcsicmp(Columns[i].ColType,End_Loop) != 0)
	{
		_stprintf(Heading,_T("Positive Test #%d for SQLStatistics\n"),i);
		TESTCASE_BEGINW(Heading);
		
		// clean up
		SQLExecDirect(hstmt,(SQLTCHAR*)DrpTab[0],SQL_NTS);
		SQLExecDirect(hstmt,(SQLTCHAR*)DrpTab[1],SQL_NTS);
		SQLExecDirect(hstmt,(SQLTCHAR*)DrpTab[2],SQL_NTS);

		CreateTbl[t] = (TCHAR *)malloc(MAX_NOS_SIZE);
		if (i > 1)
		{
			_tcscat(ColStr,_T(","));
			_tcscat(KeyStr,_T(","));
			_tcscat(IdxStr,_T(","));
		}
		_tcscat(ColStr, Columns[i].ColName);
		_tcscat(ColStr, _T(" "));
		_tcscat(ColStr, Columns[i].ColType);
		_tcscat(ColStr, _T(" NOT NULL"));   // 	not null is a manadatory constraint for primary keys.
		_tcscat(KeyStr, Columns[i].ColName);
		_tcscat(IdxStr,Columns[i].ColName);
		_tcscat(IdxStr, _T(" "));
		_tcscat(IdxStr, Columns[i].sort);
		_stprintf(CreateTbl[t],_T("%s%s%s%s%s"), TableStr[0], ColStr, TableStr[1], KeyStr, TableStr[2]);

		LogMsg(NONE,_T("Creating table:\n %s\n"), CreateTbl[t]);

		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CreateTbl[t],SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		for (idx = 0; idx < NUM_IDX; idx++)
		{
			_stprintf(CreateIdx, _T("%s%s%s"), IndexStr[idx], IdxStr, IndexStr[2]);
            LogMsg(NONE,_T("Creating index:\n %s\n"),CreateIdx);
			
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CreateIdx,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLStatistics(hstmt,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TName,(SWORD)_tcslen(TName),Unique[idx],Accuracy[a]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLStatistics"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				otqua[0]	= '\0';
				otowner[0]	= '\0';
				otname[0]	= '\0';
				ounique		= 0;
				otype		= 0;
				oiseq		= 0;
				ocar		= 0;
				opages		= 0;
				oiqua[0]	= '\0';
				oiname[0]	= '\0';
				ocname[0]	= '\0';
				ocsort[0]	= '\0';
				oifil[0]	= '\0';
				returncode=SQLBindCol(hstmt,1,SQL_C_TCHAR,otqua,NAME_LEN,&otqualen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,2,SQL_C_TCHAR,otowner,NAME_LEN,&otownerlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,3,SQL_C_TCHAR,otname,NAME_LEN,&otnamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,4,SQL_C_SHORT,&ounique,MAX_COLUMN_NAME,&ouniquelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,5,SQL_C_TCHAR,oiqua,NAME_LEN,&oiqualen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,6,SQL_C_TCHAR,oiname,NAME_LEN,&oinamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,7,SQL_C_SHORT,&otype,0,&otypelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,8,SQL_C_SHORT,&oiseq,0,&oiseqlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,9,SQL_C_TCHAR,ocname,NAME_LEN,&ocnamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,10,SQL_C_TCHAR,ocsort,NAME_LEN,&ocsortlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,11,SQL_C_LONG,&ocar,0,&ocarlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,12,SQL_C_LONG,&opages,0,&opageslen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,13,SQL_C_TCHAR,&oifil,NAME_LEN,&oifillen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				k = 0;
				while (returncode == SQL_SUCCESS)
				{
					otqua[0]	= '\0';
					otowner[0]	= '\0';
					otname[0]	= '\0';
					ounique		= 0;
					otype		= 0;
					oiseq		= 0;
					ocar		= 0;
					opages		= 0;
					oiqua[0]	= '\0';
					oiname[0]	= '\0';
					ocname[0]	= '\0';
					ocsort[0]	= '\0';
					oifil[0]	= '\0';
					returncode = SQLFetch(hstmt);
					if((returncode!=SQL_NO_DATA_FOUND) &&(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						if (returncode == SQL_NO_DATA_FOUND)
							break;
						if (oiname[0] == '\0') // Ignore extra row
						{
							SQLFreeStmt(hstmt,SQL_UNBIND);
							SQLFreeStmt(hstmt,SQL_CLOSE);
							break;
						}
						_stprintf(riname,_T("%s %s %s"),TName, TabName[1], TabName[2]);
						if (cwcscmp(oiname, TabName[2],TRUE) == 0)
							runique = 1;
						else
							runique = 0;
						_tcscpy(rcname,KeyStr);	
						LogMsg(NONE,_T("Comparing results\n"));
						if ((cwcscmp(otqua,TQualifier,TRUE) == 0)
							&& (cwcscmp(otowner,TOwner,TRUE) == 0)
							&& (cwcscmp(otname,TName,TRUE) == 0)
							&& (ounique == runique)
							&& (cwcscmp(riqua,oiqua,TRUE) == 0)
							&& (_tcsstr(riname,oiname) != NULL)
							&& (otype == rtype)
							&& (oiseq >= 1)
							&& (_tcsstr(rcname,ocname) != NULL)
							&& (_tcsstr(rcsort,ocsort) != NULL)
							&& (ocar == rcar)
							&& (opages == rpages)
							&& (cwcscmp(rifil,oifil,TRUE) == 0))
						{
							//LogMsg(NONE,_T("Table Qualifier actual: %s and expected: %s are matched\n"),otqua,TQualifier);
							//LogMsg(NONE,_T("Table Owner actual: %s and expected: %s are matched\n"),otowner,TOwner);
							//LogMsg(NONE,_T("Table Name actual: %s and expected: %s are matched\n"),otname,TName);
							//LogMsg(NONE,_T("Unique actual: %d and expected: %d are matched\n"),ounique,runique);
							//LogMsg(NONE,_T("Index Qualifier actual: %s and expected: %s are matched\n"),oiqua,riqua);
							//LogMsg(NONE,_T("Index Name actual: %s and expected: %s are matched\n"),oiname,riname);
							//LogMsg(NONE,_T("Type actual: %d and expected: %d are matched\n"),otype,rtype);
							//LogMsg(NONE,_T("Sequence in Index actual: %d and expected: %d are matched\n"),oiseq, oiseq);
							//LogMsg(NONE,_T("Column Name actual: %s and expected: %s are matched\n"),ocname,rcname);
							//LogMsg(NONE,_T("Collation actual: %s and expected: %s are matched\n"),ocsort,rcsort);
							//LogMsg(NONE,_T("Cardinality actual: %d and expected: %d are matched\n"),ocar,rcar);
							//LogMsg(NONE,_T("Pages actual: %d and expected: %d are matched\n"),opages,rpages);
							//LogMsg(NONE,_T("Filter Condition actual: %s and expected: %s are matched\n"),oifil,rifil);
						}	
						else
						{
							TEST_FAILED;	
							if (_tcsicmp(otqua,TQualifier) != 0)
								LogMsg(ERRMSG,_T("Table Qualifier: actual: %s and expected: %s are not matched\n"),otqua,TQualifier);
						   if (_tcsicmp(otowner,TOwner) != 0)
								LogMsg(ERRMSG,_T("Table Owner: actual: %s and expected: %s are not matched\n"),otowner,TOwner);
							if (cwcscmp(otname,TName,TRUE) != 0)
								LogMsg(ERRMSG,_T("Table Name: actual: %s and expected: %s are not matched\n"),otname,TName);
							if (ounique != runique)
								LogMsg(ERRMSG,_T("Unique: actual: %d and expected: %d are not matched\n"),ounique,runique);
							if (_tcsicmp(riqua,oiqua) != 0)
								LogMsg(ERRMSG,_T("Index Qualifier: actual: %s and expected: %s are not matched\n"),oiqua,riqua);
							if (_tcsstr( riname, oiname) == NULL)
								LogMsg(ERRMSG,_T("Index Name: actual: %s and expected: %s are not matched\n"),oiname,riname);
							if (otype != rtype)
								LogMsg(ERRMSG,_T("Type: actual: %d and expected: %d are not matched\n"),otype,rtype);
							if (oiseq < 1)
								LogMsg(ERRMSG,_T("Sequence in Index: actual: %d and expected: %d are not matched\n"),oiseq,oiseq);
							if (_tcsstr( rcname, ocname) == NULL)
								LogMsg(ERRMSG,_T("Column Names : actual: %s and expected: %s are not matched\n"),ocname,rcname);
							if (_tcsstr( rcsort, ocsort) == NULL)
								LogMsg(ERRMSG,_T("Collation: actual: '%s' and expected: '%s' are not matched\n"),ocsort,rcsort);
							if (ocar != rcar)
								LogMsg(ERRMSG,_T("Cardinality: actual: %d and expected: %d are not matched\n"),ocar,rcar);
							if (opages != rpages)
								LogMsg(ERRMSG,_T("Pages: actual: %d and expected: %d are not matched\n"),opages,rpages);
							if (_tcsicmp(rifil,oifil) != 0)
								LogMsg(ERRMSG,_T("Filter Condition: actual: '%s' and expected: '%s' are not matched\n"),oifil,rifil);
						}
					}	
					k++;
				}
			}
		}  // end for index loop

		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLExecDirect(hstmt,(SQLTCHAR*)DrpTab[0],SQL_NTS);
		SQLExecDirect(hstmt,(SQLTCHAR*)DrpTab[1],SQL_NTS);
		SQLExecDirect(hstmt,(SQLTCHAR*)DrpTab[2],SQL_NTS);
		free(CreateTbl[t]);
		i++;
		TESTCASE_END;
	}
//=========================================================================================
/*RS: Test temporarily disabled since MDAC 2.8 driver manager causes an access violation

	TESTCASE_BEGIN("SQLStat: Negative test with invalid handle\n");
	
	SQLAllocStmt((SQLHANDLE)hdbc, &hstmt1);
	SQLFreeStmt(hstmt1, SQL_DROP);
	
	returncode = SQLStatistics(hstmt1,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TName,(SWORD)_tcslen(TName),Unique[0],Accuracy[0]);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLStat"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;
*/
//=========================================================================================
	_stprintf(Heading,_T("Setting up Table & view to test SQLTables for wildcard options => \n"));
	_tcscat(Heading,_T("\n"));
	TESTCASE_BEGINW(Heading);

	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DrpTab[3],SQL_NTS);
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DrpTab[4],SQL_NTS);

	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTab[0],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
	}
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTab[1],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
	}
	TESTCASE_END;

	TESTCASE_BEGIN("SQLStatistics: Negative test with NULL handle\n");
	
	hstmt1 = (SQLHANDLE)NULL;
	returncode = SQLStatistics(hstmt1,(SQLTCHAR*)TQualifier,(SWORD)_tcslen(TQualifier),(SQLTCHAR*)TOwner,(SWORD)_tcslen(TOwner),(SQLTCHAR*)TName,(SWORD)_tcslen(TName),Unique[0],Accuracy[0]);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLStat"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("SQLStatistics: Negative test with invalid arg lengths.\n");
	
	i = 0;
	while (_tcsicmp(StatisticsWC2[i].TabQua,_T("endloop")) != 0)
	{
		returncode = SQLStatistics(hstmt,(SQLTCHAR*)StatisticsWC2[i].TabQua,(SWORD)StatisticsWC2[i].TabQuaLen,(SQLTCHAR*)StatisticsWC2[i].TabOwner,(SWORD)StatisticsWC2[i].TabOwnerLen,(SQLTCHAR*)StatisticsWC2[i].TabName,(SWORD)StatisticsWC2[i].TabNameLen,Unique[0],Accuracy[0]);
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
	
    i = 0; 
	while (_tcsicmp(StatisticsWC[i].TabQua,_T("endloop")) != 0)
	{
      for(l=0;l<2;l++)
	  {
	    for(m=0;m<2;m++)
		{	
			returncode = SQLStatistics(hstmt,(SQLTCHAR*)StatisticsWC[i].TabQua,(SWORD)_tcslen(StatisticsWC[i].TabQua),(SQLTCHAR*)StatisticsWC[i].TabOwner,(SWORD)_tcslen(StatisticsWC[i].TabOwner),(SQLTCHAR*)StatisticsWC[i].TabName,(SWORD)_tcslen(StatisticsWC[i].TabName),Unique[l],Accuracy[m]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLStatistics"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLNumResultCols(hstmt, &numOfCols);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultsCol"))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,_T("Test failed while executing call for SQLNUMRESULTSCOL"));
				LogAllErrors(henv,hdbc,hstmt);
			}
			for(cols = 0; cols < numOfCols; cols++)
			{
				returncode = SQLDescribeCol(hstmt,(SWORD)(cols+1),(SQLTCHAR*)cn,TABTYPE_LEN,&cl,&st,&cp,&cs,&cnull);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDescribeCol"))
				{
					TEST_FAILED;
					LogMsg(ERRMSG,_T("Test failed while executing call for SQLDESCRIBECOL of column"));
					LogAllErrors(henv,hdbc,hstmt);
				}
				CharOutput[cols] = (TCHAR *)malloc(STR_LEN);
				for (iatt = 0; iatt <= TOTALATTRIBS; iatt++)
				{
					_tcscpy(rgbDesc,_T(""));
					pcbDesc = 0;
					pfDesc = 0;
					returncode = SQLColAttributes(hstmt,(SWORD)(cols+1),DescrType[iatt],rgbDesc,STR_LEN,&pcbDesc,&pfDesc);
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
				LogMsg(ERRMSG,_T("No Data Found => Atleast one row should be fetched\n"));
				LogMsg(ERRMSG,_T("Values of l: %d m: %d\n"),l,m);
			}
			if (k != 0)
				LogMsg(NONE,_T("SUCCESS of l: %d m: %d\n"),l,m);

			for(cols = 0; cols < numOfCols; cols++)
			{
				free(CharOutput[cols]);
			}
		}
	  }
	i++;
	}
	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("Testing SQLStatistics for METADATA_ID = TRUE.\n");
	
	returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_TRUE,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
    i = 0; 
	while (_tcsicmp(StatisticsWC3[i].TabQua,_T("endloop")) != 0)
	{
      for(l=0;l<2;l++)
	  {
	    for(m=0;m<2;m++)
		{	
			returncode = SQLStatistics(hstmt,(SQLTCHAR*)StatisticsWC3[i].TabQua,(SWORD)_tcslen(StatisticsWC3[i].TabQua),(SQLTCHAR*)StatisticsWC3[i].TabOwner,(SWORD)_tcslen(StatisticsWC3[i].TabOwner),(SQLTCHAR*)StatisticsWC3[i].TabName,(SWORD)_tcslen(StatisticsWC3[i].TabName),Unique[l],Accuracy[m]);
			//LogMsg(NONE,_T("SQLStatistics(hstm,%s,%d,%s,%d,%s,%d,%d,%d)\n"), (SQLTCHAR*)StatisticsWC3[i].TabQua,(SWORD)_tcslen(StatisticsWC3[i].TabQua),(SQLTCHAR*)StatisticsWC3[i].TabOwner,(SWORD)_tcslen(StatisticsWC3[i].TabOwner),(SQLTCHAR*)StatisticsWC3[i].TabName,(SWORD)_tcslen(StatisticsWC3[i].TabName),Unique[l],Accuracy[m]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLStatistics"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLNumResultCols(hstmt, &numOfCols);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultsCol"))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,_T("Test failed while executing call for SQLNUMRESULTSCOL"));
				LogAllErrors(henv,hdbc,hstmt);
			}
			for(cols = 0; cols < numOfCols; cols++)
			{
				returncode = SQLDescribeCol(hstmt,(SWORD)(cols+1),(SQLTCHAR*)cn,TABTYPE_LEN,&cl,&st,&cp,&cs,&cnull);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDescribeCol"))
				{
					TEST_FAILED;
					LogMsg(ERRMSG,_T("Test failed while executing call for SQLDESCRIBECOL of column"));
					LogAllErrors(henv,hdbc,hstmt);
				}
				CharOutput[cols] = (TCHAR *)malloc(STR_LEN);
				for (iatt = 0; iatt <= TOTALATTRIBS; iatt++)
				{
					_tcscpy(rgbDesc,_T(""));
					pcbDesc = 0;
					pfDesc = 0;
					returncode = SQLColAttributes(hstmt,(SWORD)(cols+1),DescrType[iatt],rgbDesc,STR_LEN,&pcbDesc,&pfDesc);
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
				LogMsg(ERRMSG,_T("No Data Found => Atleast one row should be fetched\n"));
			}
		
			for(cols = 0; cols < numOfCols; cols++)
			{
				free(CharOutput[cols]);
			}
		}
	  }
	i++;
	}
	TESTCASE_END;

//=========================================================================================


	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLStatistics.\n"));
	free_list(var_list);
	TEST_RETURN;
}
