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
#define STR_LEN     128+1    //added to test SQLBindCols and SQLFetch
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
 	char			Heading[MAX_HEADING_SIZE];
 	SQLRETURN		returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt, hstmt1;
 	CHAR			TQualifier[NAME_LEN],TOwner[NAME_LEN],TName[NAME_LEN],End_Loop[10];
	UWORD			Unique[NUM_UNIQUE] = {SQL_INDEX_UNIQUE,SQL_INDEX_ALL};
	UWORD			Accuracy[NUM_ACCU] = {SQL_ENSURE,SQL_QUICK};
	char			otqua[NAME_LEN],otowner[NAME_LEN],otname[NAME_LEN];
	char			oiqua[NAME_LEN],riqua[NAME_LEN]="";
	char			oiname[NAME_LEN],riname[NAME_LEN],ocname[NAME_LEN],rcname[NAME_LEN];
	char			ocsort[2],rcsort[3]= "AD";
	char			oifil[NAME_LEN],rifil[NAME_LEN]="";
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
	CHAR			cn[COLNAME_LEN];
	SWORD			cl;
	SWORD			st;
	SQLULEN			cp;
	SWORD			cs, cnull;
	CHAR			rgbDesc[RGB_MAX_LEN];
	CHAR			*CharOutput[40];
	SQLLEN			stringlength;


	struct
	{
		CHAR		*ColName;
		CHAR		*ColType;
		CHAR		*sort;
	} Columns[] = {
							{""		,""				,""},
							{"--"	,"char(10)"		,"ASC"},
							{"--"	,"varchar(10)"	,"DESC"},
							{"--"	,"decimal(10,5)","ASC"},
							{"--"	,"numeric(10,5)","DESC"},
							{"--"	,"smallint"		,"ASC"},
							{"--"	,"integer"		,"DESC"},
							{"--"	,"bigint"		,"ASC"},
							{"--"	,"date"			,"ASC"},
							{"--"	,"time"			,"DESC"},
							{"--"	,"timestamp"	,"ASC"},
							{"--"	,"bit"			,"ASC"},
							{"--"	,"tinyint"		,"DESC"},
							{"--"	,"binary(10)"	,"ASC"},
							{"--"	,"varbinary(10)","DESC"},
							//{"C8"	,"real"			,"DESC"},
							//{"C9"	,"float"		,"ASC"},
							//{"C10","double precision","DESC"},
							//{"--"	,"numeric(19,0)","ASC"},			//for bignum
							{"--"	,"numeric(19,6)","DESC"},			//for bignum
							//{"--"	,"numeric(20,0)","ASC"},			//for bignum
							//{"--"	,"numeric(64,64)","DESC"},			//for bignum
							//{"--"	,"numeric(25,10)","ASC"},			//for bignum
							//{"--"	,"numeric(10,5) unsigned","DESC"},	//for bignum
							{"--"	,"numeric(10,5) unsigned","ASC"},	//for bignum
							//{"--"	,"numeric(30,10) unsigned","DESC"},	//for bignum
							{""		,"endloop"		,""}
						};

	struct
	{
		CHAR		*TabQua;
		CHAR		*TabOwner;
		CHAR		*TabName;
	} StatisticsWC[] = {								/* wild cards from here */
							//{" ",pTestInfo->Schema,""},
							//{"endloop",},
							//{"",pTestInfo->Schema,""}, 
							//{"",pTestInfo->Schema,"OBJECTS"}, 
							//{"",pTestInfo->Schema,""}, 
							//{" ",pTestInfo->Schema,""},
							// Changing schema name to ODBC_SCHEMA for R2.0	
							//{" ","DEFINITION_SCHEMA_VERSION_1000","TSTTBLST"},
							//{" ","DEFINITION_SCHEMA_VERSION_1000","TSTTBLEI"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--"},
							{"endloop",}
	};
	//same table but with inaccurate lengths added for negative testing
	struct
	{
		CHAR		*TabQua;
		SWORD		TabQuaLen;
		CHAR		*TabOwner;
		SWORD		TabOwnerLen;
		CHAR		*TabName;
		SWORD		TabNameLen;
	} StatisticsWC2[] = {								/* wild cards from here */
							{pTestInfo->Catalog, (SWORD)-1, pTestInfo->Schema,(SWORD)-1, "--",(SWORD)-1},
						  //{" ", (SWORD)4, pTestInfo->Schema,(SWORD)2, "OBJECTS",(SWORD)2},
						  //{" ", (SWORD)0, pTestInfo->Schema,(SWORD)0, "OBJECTS",(SWORD)0},
							{"endloop",}
						};
	
	//same table but with mixed case letters for testing METADATA_ID = TRUE
	struct
	{
		CHAR		*TabQua;
		CHAR		*TabOwner;
		CHAR		*TabName;
	} StatisticsWC3[] = {				/* wild cards from here */
							//{" ",pTestInfo->Schema,""},
							//{"endloop",},
							//{"",pTestInfo->Schema,""}, 
							//{"",pTestInfo->Schema,"OBJECTS"}, 
							//{"",pTestInfo->Schema,""}, 
							//{" ",pTestInfo->Schema,""},
							// Changing schema name to ODBC_SCHEMA for R2.0					
							//{" ","DEFINITION_SCHEMA_VERSION_1000","TsTtBlSt"},
							//{" ","DEFINITION_SCHEMA_VERSION_1000","tStTbLeI"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--"},
							{pTestInfo->Catalog,pTestInfo->Schema,"--"},
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

	
	char	*TableStr[3];
	CHAR	*IndexStr[3];
	CHAR	*DrpTab[5];
	CHAR	*CrtTab[2];
	CHAR	*TabName[3];
	char	ColStr[MAX_NOS_SIZE],KeyStr[MAX_NOS_SIZE], IdxStr[MAX_NOS_SIZE],*CreateTbl[2],CreateIdx[MAX_NOS_SIZE];
	int		i = 0,k = 0, a = 0,t = 0,idx = 0,l = 0,m = 0;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLStatistics", charset_file);
	if (var_list == NULL) return FAILED;

	Columns[1].ColName = var_mapping("SQLStatistics_Columns_ColName_1", var_list);
	Columns[2].ColName = var_mapping("SQLStatistics_Columns_ColName_2", var_list);
	Columns[3].ColName = var_mapping("SQLStatistics_Columns_ColName_3", var_list);
	Columns[4].ColName = var_mapping("SQLStatistics_Columns_ColName_4", var_list);
	Columns[5].ColName = var_mapping("SQLStatistics_Columns_ColName_5", var_list);
	Columns[6].ColName = var_mapping("SQLStatistics_Columns_ColName_6", var_list);
	Columns[7].ColName = var_mapping("SQLStatistics_Columns_ColName_7", var_list);
	Columns[8].ColName = var_mapping("SQLStatistics_Columns_ColName_8", var_list);
	Columns[9].ColName = var_mapping("SQLStatistics_Columns_ColName_9", var_list);
	Columns[10].ColName = var_mapping("SQLStatistics_Columns_ColName_10", var_list);
	Columns[11].ColName = var_mapping("SQLStatistics_Columns_ColName_11", var_list);
	Columns[12].ColName = var_mapping("SQLStatistics_Columns_ColName_12", var_list);
	Columns[13].ColName = var_mapping("SQLStatistics_Columns_ColName_13", var_list);
	Columns[14].ColName = var_mapping("SQLStatistics_Columns_ColName_14", var_list);
	Columns[15].ColName = var_mapping("SQLStatistics_Columns_ColName_15", var_list);
	Columns[16].ColName = var_mapping("SQLStatistics_Columns_ColName_16", var_list);
	//Columns[17].ColName = var_mapping("SQLStatistics_Columns_ColName_17", var_list);
	//Columns[18].ColName = var_mapping("SQLStatistics_Columns_ColName_18", var_list);
	//Columns[19].ColName = var_mapping("SQLStatistics_Columns_ColName_19", var_list);
	//Columns[20].ColName = var_mapping("SQLStatistics_Columns_ColName_20", var_list);
	//Columns[21].ColName = var_mapping("SQLStatistics_Columns_ColName_21", var_list);
	//Columns[22].ColName = var_mapping("SQLStatistics_Columns_ColName_22", var_list);

	StatisticsWC[0].TabName = var_mapping("SQLStatistics_StatisticsWC_TabName_0", var_list);
	StatisticsWC[1].TabName = var_mapping("SQLStatistics_StatisticsWC_TabName_1", var_list);

	StatisticsWC2[0].TabName = var_mapping("SQLStatistics_StatisticsWC2_TabName_0", var_list);

	StatisticsWC3[0].TabName = var_mapping("SQLStatistics_StatisticsWC3_TabName_0", var_list);
	StatisticsWC3[1].TabName = var_mapping("SQLStatistics_StatisticsWC3_TabName_1", var_list);

	TableStr[0] = var_mapping("SQLStatistics_TableStr_0", var_list);
	TableStr[1] = var_mapping("SQLStatistics_TableStr_1", var_list);
	TableStr[2] = var_mapping("SQLStatistics_TableStr_2", var_list);

	IndexStr[0] = var_mapping("SQLStatistics_IndexStr_0", var_list);
	IndexStr[1] = var_mapping("SQLStatistics_IndexStr_1", var_list);
	IndexStr[2] = var_mapping("SQLStatistics_IndexStr_2", var_list);
	
	DrpTab[0] = var_mapping("SQLStatistics_DrpTab_0", var_list);
	DrpTab[1] = var_mapping("SQLStatistics_DrpTab_1", var_list);
	DrpTab[2] = var_mapping("SQLStatistics_DrpTab_2", var_list);
	DrpTab[3] = var_mapping("SQLStatistics_DrpTab_3", var_list);
	DrpTab[4] = var_mapping("SQLStatistics_DrpTab_4", var_list);

	CrtTab[0] = var_mapping("SQLStatistics_CrtTab_0", var_list);
	CrtTab[1] = var_mapping("SQLStatistics_CrtTab_1", var_list);

	TabName[0] = var_mapping("SQLStatistics_TabName_0", var_list);
	TabName[1] = var_mapping("SQLStatistics_TabName_1", var_list);
	TabName[2] = var_mapping("SQLStatistics_TabName_2", var_list);

//=========================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => MX Specific SQLStatistics | SQLStatistics | stat.c\n");

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLStatistics tests\n");

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

	TESTCASE_END;  // end of setup

	ColStr[0] = '\0';											
	KeyStr[0] = '\0';
	IdxStr[0] = '\0';
	strcpy(End_Loop,"");
	strcpy(TQualifier,pTestInfo->Catalog);
	strcpy(TOwner,pTestInfo->Schema);
	strcpy(End_Loop,"endloop");
	strcpy(TName,TabName[0]);

	i = 1;
	while (_stricmp(Columns[i].ColType,End_Loop) != 0)
	{
		sprintf(Heading,"Positive Test #%d for SQLStatistics\n",i);
		TESTCASE_BEGIN(Heading);
		
		// clean up
		SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[0],SQL_NTS);
		SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[1],SQL_NTS);
		SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[2],SQL_NTS);

		CreateTbl[t] = (char *)malloc(MAX_NOS_SIZE);
		if (i > 1)
		{
			strcat(ColStr,",");
			strcat(KeyStr,",");
			strcat(IdxStr,",");
		}
		strcat(ColStr, Columns[i].ColName);
		strcat(ColStr, " ");
		strcat(ColStr, Columns[i].ColType);
		strcat(ColStr, " NOT NULL");   // 	not null is a manadatory constraint for primary keys.
		strcat(KeyStr, Columns[i].ColName);
		strcat(IdxStr,Columns[i].ColName);
		strcat(IdxStr, " ");
		strcat(IdxStr, Columns[i].sort);
		sprintf(CreateTbl[t],"%s%s%s%s%s", TableStr[0], ColStr, TableStr[1], KeyStr, TableStr[2]);

		//LogMsg(NONE,"Creating table:\n %s\n", CreateTbl[t]);

		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CreateTbl[t],SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		for (idx = 0; idx < NUM_IDX; idx++)
		{
			sprintf(CreateIdx, "%s%s%s", IndexStr[idx], IdxStr, IndexStr[2]);
            //LogMsg(NONE,"Creating index:\n %s\n",CreateIdx);
			
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)CreateIdx,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLStatistics(hstmt,(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TName,(SWORD)strlen(TName),Unique[idx],Accuracy[a]);
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
				returncode=SQLBindCol(hstmt,1,SQL_C_CHAR,otqua,NAME_LEN,&otqualen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,2,SQL_C_CHAR,otowner,NAME_LEN,&otownerlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,3,SQL_C_CHAR,otname,NAME_LEN,&otnamelen);
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
				returncode=SQLBindCol(hstmt,5,SQL_C_CHAR,oiqua,NAME_LEN,&oiqualen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,6,SQL_C_CHAR,oiname,NAME_LEN,&oinamelen);
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
				returncode=SQLBindCol(hstmt,9,SQL_C_CHAR,ocname,NAME_LEN,&ocnamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				returncode=SQLBindCol(hstmt,10,SQL_C_CHAR,ocsort,NAME_LEN,&ocsortlen);
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
				returncode=SQLBindCol(hstmt,13,SQL_C_CHAR,&oifil,NAME_LEN,&oifillen);
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
						sprintf(riname,"%s %s %s",TName, TabName[1], TabName[2]);
						if (cstrcmp(oiname, TabName[2],TRUE,isCharSet) == 0)
							runique = 1;
						else
							runique = 0;
						strcpy(rcname,KeyStr);	
						LogMsg(NONE,"Comparing results\n");
						if ((cstrcmp(otqua,TQualifier,TRUE,isCharSet) == 0)
							&& (cstrcmp(otowner,TOwner,TRUE,isCharSet) == 0)
							&& (cstrcmp(otname,TName,TRUE,isCharSet) == 0)
							&& (ounique == runique)
							&& (cstrcmp(riqua,oiqua,TRUE,isCharSet) == 0)
							&& (strstr(riname,oiname) != NULL)
							&& (otype == rtype)
							&& (oiseq >= 1)
							&& (strstr(rcname,ocname) != NULL)
							&& (strstr(rcsort,ocsort) != NULL)
							&& (ocar == rcar)
							&& (opages == rpages)
							&& (cstrcmp(rifil,oifil,TRUE,isCharSet) == 0))
						{
							LogMsg(NONE,"Table Qualifier actual: %s and expected: %s are matched\n",otqua,TQualifier);
							LogMsg(NONE,"Table Owner actual: %s and expected: %s are matched\n",otowner,TOwner);
							LogMsg(NONE,"Table Name actual: %s and expected: %s are matched\n",otname,TName);
							LogMsg(NONE,"Unique actual: %d and expected: %d are matched\n",ounique,runique);
							LogMsg(NONE,"Index Qualifier actual: %s and expected: %s are matched\n",oiqua,riqua);
							LogMsg(NONE,"Index Name actual: %s and expected: %s are matched\n",oiname,riname);
							LogMsg(NONE,"Type actual: %d and expected: %d are matched\n",otype,rtype);
							LogMsg(NONE,"Sequence in Index actual: %d and expected: %d are matched\n",oiseq, oiseq);
							LogMsg(NONE,"Column Name actual: %s and expected: %s are matched\n",ocname,rcname);
							LogMsg(NONE,"Collation actual: %s and expected: %s are matched\n",ocsort,rcsort);
							LogMsg(NONE,"Cardinality actual: %d and expected: %d are matched\n",ocar,rcar);
							LogMsg(NONE,"Pages actual: %d and expected: %d are matched\n",opages,rpages);
							LogMsg(NONE,"Filter Condition actual: %s and expected: %s are matched\n",oifil,rifil);
						}	
						else
						{
							TEST_FAILED;	
							if (_stricmp(otqua,TQualifier) != 0)
								LogMsg(ERRMSG,"Table Qualifier: actual: %s and expected: %s are not matched\n",otqua,TQualifier);
						    if (_stricmp(otowner,TOwner) != 0)
								LogMsg(ERRMSG,"Table Owner: actual: %s and expected: %s are not matched\n",otowner,TOwner);
							if (cstrcmp(otname,TName,TRUE,isCharSet) != 0)
								LogMsg(ERRMSG,"Table Name: actual: %s and expected: %s are not matched\n",otname,TName);
							if (ounique != runique)
								LogMsg(ERRMSG,"Unique: actual: %d and expected: %d are not matched\n",ounique,runique);
							if (_stricmp(riqua,oiqua) != 0)
								LogMsg(ERRMSG,"Index Qualifier: actual: %s and expected: %s are not matched\n",oiqua,riqua);
							if (strstr( riname, oiname) == NULL)
								LogMsg(ERRMSG,"Index Name: actual: %s and expected: %s are not matched\n",oiname,riname);
							if (otype != rtype)
								LogMsg(ERRMSG,"Type: actual: %d and expected: %d are not matched\n",otype,rtype);
							if (oiseq < 1)
								LogMsg(ERRMSG,"Sequence in Index: actual: %d and expected: %d are not matched\n",oiseq,oiseq);
							if (strstr( rcname, ocname) == NULL)
								LogMsg(ERRMSG,"Column Names : actual: %s and expected: %s are not matched\n",ocname,rcname);
							if (strstr( rcsort, ocsort) == NULL)
								LogMsg(ERRMSG,"Collation: actual: '%s' and expected: '%s' are not matched\n",ocsort,rcsort);
							if (ocar != rcar)
								LogMsg(ERRMSG,"Cardinality: actual: %d and expected: %d are not matched\n",ocar,rcar);
							if (opages != rpages)
								LogMsg(ERRMSG,"Pages: actual: %d and expected: %d are not matched\n",opages,rpages);
							if (_stricmp(rifil,oifil) != 0)
								LogMsg(ERRMSG,"Filter Condition: actual: '%s' and expected: '%s' are not matched\n",oifil,rifil);
						}
					}	
					k++;
				}
			}
		}  // end for index loop

		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[0],SQL_NTS);
		SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[1],SQL_NTS);
		SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[2],SQL_NTS);
		free(CreateTbl[t]);
		i++;
		TESTCASE_END;
	}
//=========================================================================================
/*RS: Test temporarily disabled since MDAC 2.8 driver manager causes an access violation

	TESTCASE_BEGIN("SQLStat: Negative test with invalid handle\n");
	
	SQLAllocStmt((SQLHANDLE)hdbc, &hstmt1);
	SQLFreeStmt(hstmt1, SQL_DROP);
	
	returncode = SQLStatistics(hstmt1,(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TName,(SWORD)strlen(TName),Unique[0],Accuracy[0]);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLStat"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;
*/
//=========================================================================================
	sprintf(Heading,"Setting up Table & view to test SQLTables for wildcard options => \n");
	strcat(Heading,"\n");
	TESTCASE_BEGIN(Heading);

	returncode = SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[3],SQL_NTS);
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)DrpTab[4],SQL_NTS);

	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[0],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
	}
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab[1],SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
	}
	TESTCASE_END;

	TESTCASE_BEGIN("SQLStatistics: Negative test with NULL handle\n");
	
	hstmt1 = (SQLHANDLE)NULL;
	returncode = SQLStatistics(hstmt1,(SQLCHAR*)TQualifier,(SWORD)strlen(TQualifier),(SQLCHAR*)TOwner,(SWORD)strlen(TOwner),(SQLCHAR*)TName,(SWORD)strlen(TName),Unique[0],Accuracy[0]);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLStat"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("SQLStatistics: Negative test with invalid arg lengths.\n");
	
	i = 0;
	while (_stricmp(StatisticsWC2[i].TabQua,"endloop") != 0)
	{
		returncode = SQLStatistics(hstmt,(SQLCHAR*)StatisticsWC2[i].TabQua,(SWORD)StatisticsWC2[i].TabQuaLen,(SQLCHAR*)StatisticsWC2[i].TabOwner,(SWORD)StatisticsWC2[i].TabOwnerLen,(SQLCHAR*)StatisticsWC2[i].TabName,(SWORD)StatisticsWC2[i].TabNameLen,Unique[0],Accuracy[0]);
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
	while (_stricmp(StatisticsWC[i].TabQua,"endloop") != 0)
	{
      for(l=0;l<2;l++)
	  {
	    for(m=0;m<2;m++)
		{	
			returncode = SQLStatistics(hstmt,(SQLCHAR*)StatisticsWC[i].TabQua,(SWORD)strlen(StatisticsWC[i].TabQua),(SQLCHAR*)StatisticsWC[i].TabOwner,(SWORD)strlen(StatisticsWC[i].TabOwner),(SQLCHAR*)StatisticsWC[i].TabName,(SWORD)strlen(StatisticsWC[i].TabName),Unique[l],Accuracy[m]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLStatistics"))
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
				returncode = SQLDescribeCol(hstmt,(SWORD)(cols+1),(SQLCHAR*)cn,TABTYPE_LEN,&cl,&st,&cp,&cs,&cnull);
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
					returncode = SQLColAttributes(hstmt,(SWORD)(cols+1),DescrType[iatt],rgbDesc,STR_LEN,&pcbDesc,&pfDesc);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColAttribute"))
					{
					    TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
				}
				returncode = SQLBindCol(hstmt,(SWORD)(cols+1),SQL_C_CHAR,CharOutput[cols],STR_LEN,&stringlength);
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
				TEST_FAILED;
				LogMsg(ERRMSG,"No Data Found => Atleast one row should be fetched\n");
				LogMsg(ERRMSG,"Values of l: %d m: %d\n",l,m);
			}
			if (k != 0)
				LogMsg(NONE,"SUCCESS of l: %d m: %d\n",l,m);

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
	while (_stricmp(StatisticsWC3[i].TabQua,"endloop") != 0)
	{
      for(l=0;l<2;l++)
	  {
	    for(m=0;m<2;m++)
		{	
			returncode = SQLStatistics(hstmt,(SQLCHAR*)StatisticsWC3[i].TabQua,(SWORD)strlen(StatisticsWC3[i].TabQua),(SQLCHAR*)StatisticsWC3[i].TabOwner,(SWORD)strlen(StatisticsWC3[i].TabOwner),(SQLCHAR*)StatisticsWC3[i].TabName,(SWORD)strlen(StatisticsWC3[i].TabName),Unique[l],Accuracy[m]);
			//LogMsg(NONE,"SQLStatistics(hstm,%s,%d,%s,%d,%s,%d,%d,%d)\n", (SQLCHAR*)StatisticsWC3[i].TabQua,(SWORD)strlen(StatisticsWC3[i].TabQua),(SQLCHAR*)StatisticsWC3[i].TabOwner,(SWORD)strlen(StatisticsWC3[i].TabOwner),(SQLCHAR*)StatisticsWC3[i].TabName,(SWORD)strlen(StatisticsWC3[i].TabName),Unique[l],Accuracy[m]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLStatistics"))
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
				returncode = SQLDescribeCol(hstmt,(SWORD)(cols+1),(SQLCHAR*)cn,TABTYPE_LEN,&cl,&st,&cp,&cs,&cnull);
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
					returncode = SQLColAttributes(hstmt,(SWORD)(cols+1),DescrType[iatt],rgbDesc,STR_LEN,&pcbDesc,&pfDesc);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColAttribute"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
				}
				returncode = SQLBindCol(hstmt,(SWORD)(cols+1),SQL_C_CHAR,CharOutput[cols],STR_LEN,&stringlength);
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
				TEST_FAILED;
				LogMsg(ERRMSG,"No Data Found => Atleast one row should be fetched\n");
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
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLStatistics.\n");
	free_list(var_list);
	TEST_RETURN;
}
