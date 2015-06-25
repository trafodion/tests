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

/* *******************************************************************************************
	filenmame: MXDescField.c

		This file contains test for the ODBC 3.0 apis SQLGetDescField and SQLSetDescField

**********************************************************************************************/


#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"


/*
**********************************************************************************************************
--------------------------------------------------------------------------------------------------------
			Test Suite for ODBC 3.0 api SQLSetDescField and SQLGetDescField
--------------------------------------------------------------------------------------------------------
**********************************************************************************************************
*/

#define MAX_DESC_HANDLES		6
#define MAX_DESC_TYPES			4
#define MAX_DESC_FIELDS			40
#define MAX_HEADER_FIELDS		7

#define APD						0
#define	IPD						1
#define	ARD						2
#define	IRD						3
#define ExAPD					4
#define ExARD					5

#define MAX_BUFFER_LEN			129
#define MAX_BOUND_PARAM			5



PassFail TestMXSQLSetGetDescFields(TestInfo *pTestInfo)
{   
 //======================================================================================================
 //		 Declarations
 //======================================================================================================

	TEST_DECLARE;

	SQLRETURN			returncode;
	SQLHANDLE 			henv;
	SQLHANDLE 			hdbc;
	SQLHANDLE			hstmt, hstmt1;	

	SQLHDESC			hDesc [MAX_DESC_HANDLES];		//stores Desc handles, 6
	
	SQLINTEGER			DescTypes[MAX_DESC_TYPES] =     // MAX_DESC_TYPES = 4
							{	
									SQL_ATTR_APP_PARAM_DESC, 
									SQL_ATTR_IMP_PARAM_DESC, 
									SQL_ATTR_APP_ROW_DESC, 
									SQL_ATTR_IMP_ROW_DESC
							};

	SQLSMALLINT			DescFields[MAX_DESC_FIELDS] =		// all Descriptors Field names
							{
									//HEADER FIELDS
									SQL_DESC_ALLOC_TYPE,
									SQL_DESC_ARRAY_SIZE,
									SQL_DESC_ARRAY_STATUS_PTR,
									SQL_DESC_BIND_OFFSET_PTR,
									SQL_DESC_BIND_TYPE,
									SQL_DESC_COUNT,
									SQL_DESC_ROWS_PROCESSED_PTR,
									
									//RECORD FIELDS
									SQL_DESC_AUTO_UNIQUE_VALUE,
									SQL_DESC_BASE_COLUMN_NAME,
									SQL_DESC_BASE_TABLE_NAME,
									SQL_DESC_CASE_SENSITIVE,
									SQL_DESC_CATALOG_NAME,
									SQL_DESC_CONCISE_TYPE,
									SQL_DESC_DATA_PTR,
									SQL_DESC_DATETIME_INTERVAL_CODE,
									SQL_DESC_DATETIME_INTERVAL_PRECISION,
									SQL_DESC_DISPLAY_SIZE,
									SQL_DESC_FIXED_PREC_SCALE,
									SQL_DESC_INDICATOR_PTR,
									SQL_DESC_LABEL,
									SQL_DESC_LENGTH,
									SQL_DESC_LITERAL_PREFIX,
									SQL_DESC_LITERAL_SUFFIX,
									SQL_DESC_LOCAL_TYPE_NAME,
									SQL_DESC_NAME,
									SQL_DESC_NULLABLE,
									SQL_DESC_NUM_PREC_RADIX,
									SQL_DESC_OCTET_LENGTH,
									SQL_DESC_OCTET_LENGTH_PTR,
									SQL_DESC_PARAMETER_TYPE,
									SQL_DESC_PRECISION,
									SQL_DESC_SCALE,
									SQL_DESC_SCHEMA_NAME,
									SQL_DESC_SEARCHABLE,
									SQL_DESC_TABLE_NAME,
									SQL_DESC_TYPE,
									SQL_DESC_TYPE_NAME,
									SQL_DESC_UNNAMED,
									SQL_DESC_UNSIGNED,
									SQL_DESC_UPDATABLE
								};


	// valid values for status arrays
	
	// variables to hold descriptor values
	   //descriptor header fields
	SQLSMALLINT		AllocTypeValue;
	SQLULEN 		ArraySize; //  
	SQLUSMALLINT*	ArrayStatusPtr;
	SQLLEN*			BindOffsetPtr; //  
	SQLINTEGER		BindType;
	//char            bef_guard[9] = "00000000";
	SQLSMALLINT		DescCount;
	//char            aft_guard[9] = "00000000";
	SQLULEN*    	RowsProcessedPtr; //  
	  //descriptor record fields
	SQLINTEGER		AutoUniqueValue;
	SQLCHAR			BaseColumnName[MAX_BUFFER_LEN];
	SQLCHAR			BaseTableName[MAX_BUFFER_LEN];
	SQLINTEGER		CaseSensitive;
	SQLCHAR			CatalogName[MAX_BUFFER_LEN];
	SQLSMALLINT		ConciseType;
	SQLPOINTER		DataPtr;
	SQLSMALLINT		DatetimeIntervalCode;
	SQLINTEGER		DatetimeIntervalPrecision;
	SQLINTEGER		DisplaySize;
	SQLSMALLINT		FixedPrecScale;
	SQLINTEGER*		IndicatorPtr;
	SQLCHAR			Label[MAX_BUFFER_LEN];
	SQLUINTEGER		Length;
	SQLCHAR			LiteralPrefix[MAX_BUFFER_LEN];
	SQLCHAR			LiteralSuffix[MAX_BUFFER_LEN];
	SQLCHAR			LocalTypeName[MAX_BUFFER_LEN]; 
	SQLCHAR			Name[MAX_BUFFER_LEN];
	SQLSMALLINT		Nullable;
	SQLINTEGER		NumPrecRadix;
	SQLINTEGER		OctetLength;
	SQLINTEGER*		OctetLengthPtr;
	SQLSMALLINT		ParameterType;
	SQLSMALLINT		Precision;
	SQLSMALLINT		Scale;
	SQLCHAR			SchemaName[MAX_BUFFER_LEN];
	SQLSMALLINT		Searchable;
	SQLCHAR			TableName[MAX_BUFFER_LEN];
	SQLSMALLINT		Type;
	SQLCHAR			TypeName[MAX_BUFFER_LEN];
	SQLSMALLINT		Unnamed;
	SQLSMALLINT		Unsigned;
	SQLSMALLINT		Updatable;

	//used in set
	SQLINTEGER		StrLen;
	SQLINTEGER		Indicator;


	//loop variables
	int i, FieldIndex, j;	
	
	//variables for table
	char *DrpTabProject = "--";
	char *CrtTabProject = "--";
	char *InsTabProject = "--";
	char *SelTabProject = "--";

	//variables used for binding params and cols
	SQLSMALLINT	apdProjCode = 0,ardProjCode, 
				apdEmpNum = 0, ardEmpNum ;

	SQLCHAR		apdProjDesc[MAX_BUFFER_LEN];
	SQLCHAR		ardProjDesc[MAX_BUFFER_LEN];

	DATE_STRUCT	apdStartDate, ardStartDate;

	TIMESTAMP_STRUCT apdShipTimestamp, ardShipTimestamp;

#ifdef _LP64
	SQLLEN      ipdProjDesc64 = SQL_NTS; //  : ???
	SQLLEN  	ipdProjCode = SQL_NTS,		irdProjCode ,
				ipdEmpNum = SQL_NTS,		irdEmpNum ,
				ipdProjDesc = SQL_NTS,		irdProjDesc ,
				ipdStartDate = SQL_NTS,		irdStartDate,
				ipdShipTimestamp = SQL_NTS,	irdShipTimestamp;
#else
	SQLINTEGER	ipdProjCode = SQL_NTS,		irdProjCode ,
				ipdEmpNum = SQL_NTS,		irdEmpNum ,
				ipdProjDesc = SQL_NTS,		irdProjDesc ,
				ipdStartDate = SQL_NTS,		irdStartDate,
				ipdShipTimestamp = SQL_NTS,	irdShipTimestamp;
#endif

		
	typedef struct {
		SQLINTEGER		irdAutoUniqueValue;
		char			irdBaseColumnName[MAX_BUFFER_LEN];
		char			irdBaseTableName[MAX_BUFFER_LEN];
		SQLINTEGER		irdCaseSensitive;
		char*	    	irdCatalogName; //[MAX_BUFFER_LEN];
		SQLSMALLINT		irdConciseType;
		SQLSMALLINT		irdDatetimeIntervalCode;
		SQLINTEGER		irdDatetimeIntervalPrecision;
		SQLINTEGER		irdDisplaySize;
		SQLSMALLINT		irdFixedPrecScale;
		char			irdLabel[MAX_BUFFER_LEN];
		SQLUINTEGER		irdLength;
		char			irdLiteralPrefix[MAX_BUFFER_LEN];
		char			irdLiteralSuffix[MAX_BUFFER_LEN];
		char			irdLocalTypeName[MAX_BUFFER_LEN];
		char			irdName[MAX_BUFFER_LEN];
		SQLSMALLINT		irdNullable;
		SQLINTEGER		irdNumPrecRadix;
		SQLINTEGER		irdOctetLength;
		SQLSMALLINT		irdPrecision;
		SQLSMALLINT		irdScale;
		char*   		irdSchemaName; //[MAX_BUFFER_LEN];
		SQLSMALLINT		irdSearchable;
		char     		irdTableName[MAX_BUFFER_LEN];
		SQLSMALLINT		irdType;
		char			irdTypeName[MAX_BUFFER_LEN];
		SQLSMALLINT		irdUnnamed;
		SQLSMALLINT		irdUnsigned;
		SQLSMALLINT		irdUpdatable;
	}IRD_REC;

	typedef struct {
		SQLINTEGER		ipdCaseSensitive;
		SQLSMALLINT		ipdConciseType;
		SQLSMALLINT		ipdDatetimeIntervalCode;
		SQLINTEGER		ipdDatetimeIntervalPrecision;
		SQLSMALLINT		ipdFixedPrecScale;
		SQLUINTEGER		ipdLength;
		char			ipdLocalTypeName[MAX_BUFFER_LEN];
		char			ipdName[MAX_BUFFER_LEN];
		SQLSMALLINT		ipdNullable;
		SQLINTEGER		ipdNumPrecRadix;
		SQLINTEGER		ipdOctetLength;
		SQLSMALLINT		ipdParameterType;
		SQLSMALLINT		ipdPrecision;
		SQLSMALLINT		ipdScale;
		SQLSMALLINT		ipdType;
		char			ipdTypeName[MAX_BUFFER_LEN];
		SQLSMALLINT		ipdUnnamed;
		SQLSMALLINT		ipdUnsigned;
	}IPD_REC;

	typedef struct {
		SQLSMALLINT		appConciseType;
		SQLPOINTER		appDataPtr;
		SQLSMALLINT		appDatetimeIntervalCode;
		SQLINTEGER		appDatetimeIntervalPrecision;
		SQLINTEGER*		appIndicatorPtr;
		SQLUINTEGER		appLength;
		SQLINTEGER		appNumPrecRadix;
		SQLINTEGER		appOctetLength;
		SQLINTEGER*		appOctetLengthPtr;
		SQLSMALLINT		appPrecision;
		SQLSMALLINT		appScale;
		SQLSMALLINT		appType;
	}APP_REC;


  //data
  //IRD_REC IRD_ActualData[MAX_BOUND_PARAM];
	IRD_REC IRD_ExpData[MAX_BOUND_PARAM] =
	{
		//AutoUniqueValue	BaseColumnName	  BaseTableName	 CaseSensitive	CatalogName			ConciseType		    DatetimeIntervalCode	DatetimeIntervalPrecision	DisplaySize		FixedPrecScale		Label		           Length	Prefix	  Suffix   LocalTypeName		               Name					Nullable		NumPrecRadix	OctetLen	Precision	Scale		SchemaName				Searchable				TableName		Type			TypeName     	Unamed	   Unsigned  Updateable
		{ SQL_FALSE,        "PROJCODE",       "PROJECT",     SQL_FALSE,     pTestInfo->Catalog, SQL_INTEGER,	    0,                      0,                          10, 			SQL_FALSE, 			"Project/Code",        4,       "",       "",      "",                  			   "PROJCODE", 			SQL_NO_NULLS,	10, 			4, 			10, 		0, 			pTestInfo->Schema,		SQL_PRED_BASIC,			"PROJECT", 		SQL_INTEGER,	"INTEGER",  	SQL_NAMED, SQL_TRUE, SQL_ATTR_READWRITE_UNKNOWN},
		{ SQL_FALSE,        "EMPNUM",   	  "PROJECT", 	 SQL_FALSE,     pTestInfo->Catalog, SQL_INTEGER,        0,                      0, 							10,				SQL_FALSE,  		"Employee/Number",	   4,       "",	      "",      "",								   "EMPNUM", 			SQL_NO_NULLS,	10, 			4, 			10, 		0, 			pTestInfo->Schema,		SQL_PRED_BASIC,			"PROJECT", 		SQL_INTEGER,	"INTEGER",   	SQL_NAMED, SQL_TRUE, SQL_ATTR_READWRITE_UNKNOWN},
		{ SQL_FALSE,        "PROJDESC", 	  "PROJECT",     SQL_TRUE,      pTestInfo->Catalog, SQL_VARCHAR,        0,                      0, 							18, 			SQL_FALSE, 			"Project/Description", 18,      "'",      "'",     "VARCHAR CHARACTER SET ISO88591",   "PROJDESC", 			SQL_NO_NULLS, 	0, 				18, 		18, 		0, 			pTestInfo->Schema,		SQL_PRED_SEARCHABLE,	"PROJECT", 		SQL_VARCHAR,    "VARCHAR",   	SQL_NAMED, SQL_TRUE, SQL_ATTR_READWRITE_UNKNOWN},
		{ SQL_FALSE, 		"START_DATE", 	  "PROJECT",     SQL_FALSE,	    pTestInfo->Catalog, SQL_TYPE_DATE,      SQL_CODE_DATE,          0, 							10, 			SQL_FALSE, 			"Start/Date",          10,      "{d'",    "'}",    "", 								   "START_DATE",		SQL_NO_NULLS, 	0, 				6, 			0, 			0, 			pTestInfo->Schema, 		SQL_PRED_BASIC, 		"PROJECT",		SQL_DATETIME,   "DATE",      	SQL_NAMED, SQL_TRUE, SQL_ATTR_READWRITE_UNKNOWN},
		{ SQL_FALSE, 		"SHIP_TIMESTAMP", "PROJECT",     SQL_FALSE,     pTestInfo->Catalog,	SQL_TYPE_TIMESTAMP, SQL_CODE_TIMESTAMP,	    0, 							26, 			SQL_FALSE, 			"Timestamp/Shipped",   26,      "{ts'",   "'}",    "", 								   "SHIP_TIMESTAMP",	SQL_NO_NULLS, 	0,				16, 		6, 			0, 			pTestInfo->Schema, 		SQL_PRED_BASIC,     	"PROJECT",		SQL_DATETIME,   "TIMESTAMP", 	SQL_NAMED, SQL_TRUE, SQL_ATTR_READWRITE_UNKNOWN}
	};


	//COMMENTS:
	// The SQL_DESC_NAME for IPD is "" because the driver does not support Named Parameters : when Named Parameter are supported the column name should be returned.
	IPD_REC IPD_ExpData[MAX_BOUND_PARAM] =
	{
		//	CaseSensitive	ConciseType		        DatetimeIntervalCode	DatetimeIntervalPrecision	FixedPrecScale		Length	LocalTypeName		             	Name		   		Nullable			NumPrecRadix	OctetLen	ParameterType		Precision	Scale	Type			TypeName		Unamed			Unsigned
		{ 	SQL_FALSE,		SQL_INTEGER,			0,					    0,						    SQL_FALSE ,			4,		"",				                 	"PROJCODE",	   		SQL_NO_NULLS,		10,				4,			SQL_PARAM_INPUT,	10,			0,	 	SQL_INTEGER,	"INTEGER",		SQL_UNNAMED,	SQL_TRUE},
		{ 	SQL_FALSE,		SQL_INTEGER,			0,					    0,						    SQL_FALSE,			4,		"",								 	"EMPNUM",	   		SQL_NO_NULLS,		10,				4,			SQL_PARAM_INPUT,	10,			0,	 	SQL_INTEGER,	"INTEGER",		SQL_UNNAMED,	SQL_TRUE},
		{ 	SQL_TRUE,		SQL_CHAR,				0,					    0,						    SQL_FALSE,			129,	"VARCHAR CHARACTER SET ISO88591",	"PROJDESC",	   		SQL_NO_NULLS,		0,				129,		SQL_PARAM_INPUT,	0,			0,	 	SQL_CHAR,	    "CHAR",		    SQL_UNNAMED,	SQL_TRUE},
		{ 	SQL_FALSE,		SQL_TYPE_DATE,			SQL_CODE_DATE,		    0,						    SQL_FALSE,			10,		"",								 	"START_DATE",   	SQL_NO_NULLS,		0,				6,			SQL_PARAM_INPUT,	0,			0,	 	SQL_DATETIME,	"DATE",			SQL_UNNAMED,	SQL_TRUE},
		{ 	SQL_FALSE,		SQL_TYPE_TIMESTAMP,		SQL_CODE_TIMESTAMP,	    0,						    SQL_FALSE,			26,		"",				                 	"SHIP_TIMESTAMP",	SQL_NO_NULLS,		0,				16,			SQL_PARAM_INPUT,	6,			0,	 	SQL_DATETIME,	"TIMESTAMP",	SQL_UNNAMED,	SQL_TRUE}
	};


	APP_REC APP_ExpData[MAX_BOUND_PARAM] =
	{
		//ConciseType	      DataPtr	IntervalCode	    IntervalPrecision	IndicatorPtr	Length	PrecRadix	OctetLength		OctetLengthPtr		Precision	Scale	Type
	    {SQL_C_SSHORT,	      NULL,     0,                  0,                  NULL,           0,      0,          0,              NULL,               0,          0,	    SQL_C_SSHORT},		
		{SQL_C_SSHORT,	      NULL,     0,                  0,                  NULL,           0,      0,          0,              NULL,               0,          0,	    SQL_C_SSHORT},
		{SQL_C_CHAR,	      NULL,     0,                  0,                  NULL,           129,    0,          MAX_BUFFER_LEN, NULL,               0,          0,      SQL_C_CHAR},		
		{SQL_C_TYPE_DATE,     NULL,	    SQL_CODE_DATE,	    0,                  NULL,           10,     0,	        0,              NULL,               0,          0,	    SQL_DATETIME},		
		{SQL_C_TYPE_TIMESTAMP,NULL,     SQL_CODE_TIMESTAMP,	0,                  NULL,           0,      0,	        0,              NULL,               0,          0,	    SQL_DATETIME}		
	};

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLSetGetDescFields", charset_file);
	if (var_list == NULL) return FAILED;

	DrpTabProject = var_mapping("SQLSetGetDescFields_DrpTabProject", var_list);
	CrtTabProject = var_mapping("SQLSetGetDescFields_CrtTabProject", var_list);
	InsTabProject = var_mapping("SQLSetGetDescFields_InsTabProject", var_list);
	SelTabProject = var_mapping("SQLSetGetDescFields_SelTabProject", var_list);

	strcpy(IRD_ExpData[0].irdBaseColumnName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_0", var_list));
	strcpy(IRD_ExpData[0].irdBaseTableName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_0", var_list));
	strcpy(IRD_ExpData[0].irdLabel, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdLabel_0", var_list));
	strcpy(IRD_ExpData[0].irdName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdName_0", var_list));
	strcpy(IRD_ExpData[0].irdTableName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdTableName_0", var_list));

	strcpy(IRD_ExpData[1].irdBaseColumnName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_1", var_list));
	strcpy(IRD_ExpData[1].irdBaseTableName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_1", var_list));
	strcpy(IRD_ExpData[1].irdLabel, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdLabel_1", var_list));
	strcpy(IRD_ExpData[1].irdName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdName_1", var_list));
	strcpy(IRD_ExpData[1].irdTableName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdTableName_2", var_list));

	strcpy(IRD_ExpData[2].irdBaseColumnName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_2", var_list));
	strcpy(IRD_ExpData[2].irdBaseTableName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_2", var_list));
	strcpy(IRD_ExpData[2].irdLabel, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdLabel_2", var_list));
	strcpy(IRD_ExpData[2].irdName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdName_2", var_list));
	strcpy(IRD_ExpData[2].irdTableName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdTableName_2", var_list));

	strcpy(IRD_ExpData[3].irdBaseColumnName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_3", var_list));
	strcpy(IRD_ExpData[3].irdBaseTableName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_3", var_list));
	strcpy(IRD_ExpData[3].irdLabel, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdLabel_3", var_list));
	strcpy(IRD_ExpData[3].irdName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdName_3", var_list));
	strcpy(IRD_ExpData[3].irdTableName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdTableName_3", var_list));

	strcpy(IRD_ExpData[4].irdBaseColumnName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_4", var_list));
	strcpy(IRD_ExpData[4].irdBaseTableName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_4", var_list));
	strcpy(IRD_ExpData[4].irdLabel, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdLabel_4", var_list));
	strcpy(IRD_ExpData[4].irdName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdName_4", var_list));
	strcpy(IRD_ExpData[4].irdTableName, var_mapping("SQLSetGetDescFields_IRD_ExpData_irdTableName_4", var_list));

	strcpy(IPD_ExpData[0].ipdName, var_mapping("SQLSetGetDescFields_IPD_ExpData_ipdName_0", var_list));
	strcpy(IPD_ExpData[1].ipdName, var_mapping("SQLSetGetDescFields_IPD_ExpData_ipdName_1", var_list));
	strcpy(IPD_ExpData[2].ipdName, var_mapping("SQLSetGetDescFields_IPD_ExpData_ipdName_2", var_list));
	strcpy(IPD_ExpData[3].ipdName, var_mapping("SQLSetGetDescFields_IPD_ExpData_ipdName_3", var_list));
	strcpy(IPD_ExpData[4].ipdName, var_mapping("SQLSetGetDescFields_IPD_ExpData_ipdName_4", var_list));
 
 // ================================================================================================================
 //		begin common test setup 
 //==================================================================================================================
	
	// begin by marking the start of  test in the log file
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => SQLSetDescField and SQLGetDescField | SQLGetDescField | mxdescfields.c\n");
	TEST_INIT;


	TESTCASE_BEGIN("Begin setup.\n");
	//establish a connection to the DSN or test fails here
	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,"Unable to connect as ODBC3.0 application.\n");
		TEST_FAILED;
		TEST_RETURN;
	}
	
	//get env, db and stmt handles already allocated at connection time.
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;


	//alloc statement handle or fail here. (pTestInfo ->hstmt; //this is not allocated in FullConnectWithOptionsVer3)
	LogMsg(NONE,"Run API SQLAllocHandle to allocate STMT\n");
	returncode = SQLAllocHandle(SQL_HANDLE_STMT,(SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	

	//alloc another statement handle 
	LogMsg(NONE,"Run API SQLAllocHandle to allocate STMT1\n");
	returncode = SQLAllocHandle(SQL_HANDLE_STMT,(SQLHANDLE)hdbc, &hstmt1);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	// Fill up the first 4 elements of the array of hDesc with implicit Descriptor handles
	// #define MAX_DESC_TYPES			4
	// SQLGetStmtAttr returns the current setting of a statement attribute.
	LogMsg(NONE,"Run SQLGetStmtAttr to get the current setting of a statement attribute\n");
	for (i=0; i<MAX_DESC_TYPES; i++)
	{
		LogMsg(NONE,"Get STMT Attribute (DescTypes[%d]) to hDesc[%d]\n", i,i );
		returncode = SQLGetStmtAttr(hstmt, DescTypes[i], &(hDesc[i]), 0, NULL);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			LogMsg(ERRMSG,"Cannot allocate descriptor: IRD.\n");
			TEST_FAILED;
			TEST_RETURN;
		}
	}

	// fill up the next two elements with Explicit descriptor handles
	for (i= MAX_DESC_TYPES; i< MAX_DESC_HANDLES; i++)
	{
		LogMsg(NONE,"Run SQLAllocHandle to allocate descriptor handle to hDesc[%d]\n",i );
		returncode = SQLAllocHandle(SQL_HANDLE_DESC, (SQLHANDLE)hdbc, &hDesc[i]);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle to get explicit descriptors"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt1);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}

	}

	//associate explicit descriptors with statement2
	LogMsg(NONE,"Run SQLSetStmtAttr to set attributes (hDesc[4]) for STMT1\n");
	returncode = SQLSetStmtAttr(hstmt1, SQL_ATTR_APP_PARAM_DESC, (SQLPOINTER)hDesc[4], SQL_IS_POINTER);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr: explicit APD"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		LogMsg(ERRMSG, "Cannot set Explicit APD for statement.\n");
		TEST_FAILED;
		TEST_RETURN;
	}
	
	LogMsg(NONE,"Run SQLSetStmtAttr to set attributes (hDesc[5]) for STMT1\n");
	returncode = SQLSetStmtAttr(hstmt1, SQL_ATTR_APP_PARAM_DESC, (SQLPOINTER)hDesc[5], SQL_IS_POINTER);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr: explicit ARD"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		LogMsg(ERRMSG, "Cannot set Explicit ARD for statement.\n");
		TEST_FAILED;
		TEST_RETURN;
	}

	TESTCASE_END;

 //===========================================================================================================
 //	Section #1 	
 // Tests for Descriptor Fields Default Values: Header Fields
 //==============================================================================================================
	for(FieldIndex = 0; FieldIndex < MAX_HEADER_FIELDS  ; FieldIndex++)
	{
		switch (DescFields[FieldIndex])
		{
		//-------------------------------------------------------------------------------
		//		begin testing of Header field descriptors
		//--------------------------------------------------------------------------------
			case  SQL_DESC_ALLOC_TYPE:
				for (i= 0; i< MAX_DESC_HANDLES; i++)
				{
					AllocTypeValue = 0; 
					// SQLGetDescField returns the current setting or value of a single field of a descriptor record.
					LogMsg(NONE,"Run SQLGetDescField to get the current setting of hDesc[%d] under SQL_DESC_ALLOC_TYPE\n",i);	
					returncode = SQLGetDescField(hDesc[i], 0, SQL_DESC_ALLOC_TYPE, &AllocTypeValue, 0, NULL);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						TEST_FAILED;
						TEST_RETURN;
					}
					LogMsg(NONE,"Result -- %d \n",AllocTypeValue);	
					switch (i)
					{
						case APD:				// APD
							TESTCASE_BEGIN("SQL_DESC_ALLOC_TYPE: APD Default values.\n");
							if (AllocTypeValue != SQL_DESC_ALLOC_AUTO)
							{
								LogMsg(ERRMSG,"SQL_DESC_ALLOC_TYPE (case APD): expected SQL_DESC_ALLOC_AUTO and found %d, Line=%d\n",  AllocTypeValue, __LINE__);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;
						case IPD:				// IPD
							TESTCASE_BEGIN("SQL_DESC_ALLOC_TYPE: IPD Default values.\n");
							if (AllocTypeValue != SQL_DESC_ALLOC_AUTO)
							{
								LogMsg(ERRMSG,"SQL_DESC_ALLOC_TYPE (case IPD): expected SQL_DESC_ALLOC_AUTO and found %d, Line=%d\n", AllocTypeValue, __LINE__);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;		
						case ARD:				// ARD
							TESTCASE_BEGIN("SQL_DESC_ALLOC_TYPE: ARD Default values.\n");
							if (AllocTypeValue != SQL_DESC_ALLOC_AUTO)
							{
								LogMsg(ERRMSG,"SQL_DESC_ALLOC_TYPE (case ARD): expected SQL_DESC_ALLOC_AUTO and found %d, Line=%d\n", AllocTypeValue,__LINE__);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;
						case IRD:				// IRD
							TESTCASE_BEGIN("SQL_DESC_ALLOC_TYPE: IRD Default values.\n");
							if (AllocTypeValue != SQL_DESC_ALLOC_AUTO)
							{
								LogMsg(ERRMSG,"SQL_DESC_ALLOC_TYPE (case IRD): expected SQL_DESC_ALLOC_AUTO and found %d, Line=%d\n", AllocTypeValue,__LINE__);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;
						case ExAPD: 			// Explicit APD
							TESTCASE_BEGIN("SQL_DESC_ALLOC_TYPE: Explicit APD Default values.\n");
							if (AllocTypeValue != SQL_DESC_ALLOC_USER)
							{
								LogMsg(ERRMSG,"SQL_DESC_ALLOC_TYPE (case ExAPD): expected SQL_DESC_ALLOC_USER and found %d, Line=%d\n", AllocTypeValue,__LINE__);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;
						case ExARD: 			// Explicit ARD
							TESTCASE_BEGIN("SQL_DESC_ALLOC_TYPE: Explicit ARD Default values.\n");
							if (AllocTypeValue != SQL_DESC_ALLOC_USER)
							{
								LogMsg(ERRMSG,"SQL_DESC_ALLOC_TYPE (case ExARD): expected SQL_DESC_ALLOC_USER and found %d,\n", AllocTypeValue,__LINE__);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;
					} //end switch for different desc handles
				}//finish looping through all Desc handles
				break; 

			case SQL_DESC_ARRAY_SIZE:
				for (i= 0; i< (MAX_DESC_HANDLES - 2); i++)
				{

					switch (i)
					{
						case APD:
							TESTCASE_BEGIN("SQL_DESC_ARRAY_SIZE: APD Default values.\n");
							ArraySize = 0; 
							LogMsg(NONE,"Run SQLGetDescField to get the current setting of hDesc[%d] under SQL_DESC_ARRAY_SIZE\n",i);
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &ArraySize, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								break;	//get out: go to next test
							}

							if (ArraySize != 1)
							{
								LogMsg(ERRMSG,"SQL_DESC_ARRAY_SIZE (case APD): expected 1 and found %d.\n",  ArraySize);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;

						case ARD:
							TESTCASE_BEGIN("SQL_DESC_ARRAY_SIZE: ARD Default values.\n");
							ArraySize = 0; 
							LogMsg(NONE,"Run SQLGetDescField to get the current setting of hDesc[%d] under SQL_DESC_ARRAY_SIZE\n",i);
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &ArraySize, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								break;	//get out: go to next test
							}

							if (ArraySize != 1)
							{
								LogMsg(ERRMSG,"SQL_DESC_ARRAY_SIZE (case ARD): expected 1 and found %d.\n", ArraySize);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;

						default: ;
							//default: do nothing because this Field is not used by other kinds of descriptors.
							
					} //end switch for different desc handles
				}//finish looping through all Desc handles
				break;
				
		
			case SQL_DESC_ARRAY_STATUS_PTR:
				for (i= 0; i < (MAX_DESC_HANDLES - 2) ; i++)
				{
					TESTCASE_BEGIN("SQL_DESC_ARRAY_STATUS_PTR: Default values.\n");
					ArrayStatusPtr = NULL; 
					LogMsg(NONE,"Run SQLGetDescField to get the current setting of hDesc[%d] under SQL_DESC_ARRAY_STATUS_PTR\n",i);
					returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], ArrayStatusPtr, 0, NULL);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						TEST_FAILED;
						continue;
					}

					// all fields have default value NULL					
					if (ArrayStatusPtr != NULL)
					{
						LogMsg(ERRMSG,"SQL_DESC_ARRAY_STATUS_PTR : expected NULL and found %p.\n",  ArrayStatusPtr);
						TEST_FAILED;
							
					}
					TESTCASE_END;
				}// end for
				break;

			case SQL_DESC_BIND_OFFSET_PTR:
				for (i= 0; i <(MAX_DESC_HANDLES - 2); i++)
				{
					switch (i)
					{
						case ARD:
							TESTCASE_BEGIN("SQL_DESC_BIND_OFFSET_PTR: ARD Default values.\n");
							LogMsg(NONE,"Run SQLGetDescField to get the current setting of hDesc[%d] under SQL_DESC_BIND_OFFSET_PTR\n",i);
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &BindOffsetPtr, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								break;
							}

							if (BindOffsetPtr != NULL)
							{
								LogMsg(ERRMSG,"SQL_DESC_BIND_OFFSET_PTR (case ARD): expected NULL and found %p.\n",  BindOffsetPtr);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;

						case APD:
							TESTCASE_BEGIN("SQL_DESC_BIND_OFFSET_PTR: APD Default values.\n");
							LogMsg(NONE,"Run SQLGetDescField to get the current setting of hDesc[%d] under SQL_DESC_BIND_OFFSET_PTR\n",i);
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &BindOffsetPtr, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								break;
							}

							if (BindOffsetPtr != NULL)
							{
								LogMsg(ERRMSG,"SQL_DESC_BIND_OFFSET_PTR (case APD): expected NULL and found %p.\n",  BindOffsetPtr);
								TEST_FAILED;
							}
							TESTCASE_END;
							break;
						default: ; // do nothing because this SQL_DESC_BIND_OFFSET_PRT is not used
					}//end switch
				}// end for
				break;
							
			case SQL_DESC_BIND_TYPE:
				for (i= 0; i< (MAX_DESC_HANDLES - 2); i++)
				{
					switch (i)
					{
						case ARD:
							TESTCASE_BEGIN("SQL_DESC_BIND_TYPE: ARD Default values.\n");
							LogMsg(NONE,"Run SQLGetDescField to get the current setting of hDesc[%d] under SQL_DESC_BIND_TYPE\n",i);
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &BindType, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								break;
							}

							if (BindType != SQL_BIND_BY_COLUMN)
							{
								LogMsg(ERRMSG,"SQL_DESC_BIND_TYPE (case ARD): expected SQL_BIND_BY_COLUMN and found %d.\n",  BindType);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;

						case APD:
							TESTCASE_BEGIN("SQL_DESC_BIND_TYPE: APD Default values.\n");
							LogMsg(NONE,"Run SQLGetDescField to get the current setting of hDesc[%d] under SQL_DESC_BIND_TYPE\n",i);
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &BindType, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								break;
							}

							if (BindType != SQL_BIND_BY_COLUMN)
							{
								LogMsg(ERRMSG,"SQL_DESC_BIND_TYPE (case APD): expected SQL_BIND_BY_COLUMN and found %d.\n",  BindType);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;

						default: ;	//not valid for other types of descriptors

					}// end switch
				}//end for
				break;

			case SQL_DESC_COUNT:
				for (i= 0; i < (MAX_DESC_HANDLES - 2); i++)
				{
					TESTCASE_BEGIN("SQL_DESC_COUNT: Default values.\n");
					LogMsg(NONE,"Run SQLGetDescField to get the current setting of hDesc[%d] under SQL_DESC_COUNT\n",i);
					returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &DescCount, 0, NULL);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						TEST_FAILED;
						TESTCASE_END;	//tests ends here: marked as failed
						continue;		//go to next desc_handle
					}

					//check the deafult value
					if ( DescCount != 0)
					{
						LogMsg(ERRMSG,"SQL_DESC_COUNT (case %d): expected 0 and found %d.\n",  i, DescCount);
						TEST_FAILED;
							
					}						
					TESTCASE_END;
				}// end for
				break;

			case SQL_DESC_ROWS_PROCESSED_PTR:
				for (i = 0; i < (MAX_DESC_HANDLES - 2); i++)
				{
					switch (i)
					{
						case IRD: 		//same as next case
						case IPD:
							TESTCASE_BEGIN("SQL_DESC_ROWS_PROCESSED_PTR: Default values.\n");
							LogMsg(NONE,"Run SQLGetDescField to get the current setting of hDesc[%d] under SQL_DESC_ROWS_PROCESSED_PTR\n",i);
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &RowsProcessedPtr, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								TESTCASE_END;	//tests ends here: marked as failed
								break;			//go to next desc_handle
							}

							//check the deafult value
							if ( RowsProcessedPtr != NULL)
							{
								LogMsg(ERRMSG,"SQL_DESC_ROWS_PROCESSED_PTR (case %d): expected NULL and found %p.\n",  i, RowsProcessedPtr);
								TEST_FAILED;
								TESTCASE_END;
							}						
							TESTCASE_END;
							break;
						default: ; // not valid for other desc handles : do nothing
					}//end switch
				}// end for
				break;

			default: 
				LogMsg(NONE, "DescFields[%d]: no valid default values.\n", i); //do nothing 
		} //finish individual cases for all header descriptor fields
	}//end looping through all header descriptor fields

 //===========================================================================================================
 // Section #2
 //	populate Desc Fields: testing the record descriptor fields possible only after populating them.
 //==============================================================================================================
	
	TESTCASE_BEGIN("Setup for descriptor record fields.\n");
	returncode = SQLGetTypeInfo(hstmt, SQL_ALL_TYPES);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetTypeInfo"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	// increase the DESC_COUNT for all types of desc : effectively creating a new (bound) desc rec
	for (i = 0; i < MAX_DESC_TYPES; i++)
	{
		switch (i)
		{
			case IRD:	//do nothing : this is read only
				break; 

			default:
				DescCount = 1;
				returncode = SQLSetDescField(hDesc[i], 0, SQL_DESC_COUNT, (SQLPOINTER)DescCount, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_COUNT = 1"))	
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
		}//end switch
	} //end for

	TESTCASE_END;

 //===========================================================================================================
 // Section #3
 //	Tests for Descriptor Fields Default Values: Record Fields
 //==============================================================================================================
	for(FieldIndex = MAX_HEADER_FIELDS; FieldIndex < MAX_DESC_FIELDS ; FieldIndex++)
	{
		//LogMsg(SHORTTIMESTAMP,"SQLGetDescField : testing default values.\n");
		switch (DescFields[FieldIndex])
		{
		//-------------------------------------------------------------------------------
		//		begin testing of Record field descriptors
		//--------------------------------------------------------------------------------
			case SQL_DESC_AUTO_UNIQUE_VALUE:
				for (i = 0; i < (MAX_DESC_HANDLES - 2); i++)
				{
					switch (i)
					{
						case IRD:
							TESTCASE_BEGIN("SQL_DESC_AUTO_UNIQUE_VALUE: Default values.\n");
							//get default field value
							returncode = SQLGetDescField(hDesc[i], 1, DescFields[FieldIndex], &AutoUniqueValue, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								TESTCASE_END;	//tests ends here: marked as failed
								break;			//go to next desc_handle
							}

							//check the default value
							if (!(( AutoUniqueValue == SQL_TRUE) || (AutoUniqueValue == SQL_FALSE)))
							{
								LogMsg(ERRMSG,"SQL_DESC_AUTO_UNIQUE_VALUE (case %d): expected SQL_TRUE or SQL_FALSE and found %d.\n",  i, AutoUniqueValue);
								TEST_FAILED;
								TESTCASE_END;
								break;
							}						
							TESTCASE_END;
							break;

						default: ; //do nothing: not valid for descriptors otjer than IRDs
					}//end Switch
				}//end for
				break;
			
			case SQL_DESC_CONCISE_TYPE:
				for (i = 0; i < (MAX_DESC_HANDLES - 2); i++)
				{
					switch (i)
					{
						case ARD:	; //same as next

						case APD:
							TESTCASE_BEGIN("SQL_DESC_CONCISE_TYPE: Default values.\n");
							//get default field value
							returncode = SQLGetDescField(hDesc[i], 1, DescFields[FieldIndex], &ConciseType, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								TESTCASE_END;	//tests ends here: marked as failed
								break;			//go to next desc_handle
							}

							//check the default value
							if ( ConciseType != SQL_C_DEFAULT)
							{
								LogMsg(ERRMSG,"SQL_DESC_CONCISE_TYPE (case %d): expected SQL_C_DEFAULT and found %d.\n",  i, ConciseType);
								TEST_FAILED;
								TESTCASE_END;
								break;
							}						
							TESTCASE_END;
							break;

						default: ;
					}//end switch
				}//end for
				break;

			case SQL_DESC_TYPE:
				for (i = 0; i < (MAX_DESC_HANDLES - 2); i++)
				{
					switch (i)
					{
						case ARD:	; //same as next

						case APD:
							TESTCASE_BEGIN("SQL_DESC_TYPE: Default values.\n");
							//initialize buffer
							Type = 0; //initialized invalid value .
							//get default field value
							returncode = SQLGetDescField(hDesc[i], 1, DescFields[FieldIndex], &Type, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								TESTCASE_END;	//tests ends here: marked as failed
								break;			//go to next desc_handle
							}

							//check the default value
							if ( Type != SQL_C_DEFAULT)
							{
								LogMsg(ERRMSG,"SQL_DESC_TYPE (case %d): expected SQL_C_DEFAULT and found %d.\n",  i, Type);
								TEST_FAILED;
								TESTCASE_END;
								break;
							}						
							TESTCASE_END;
							break;

						default: ;
					}//end switch
				}//end for
				break;	


			case SQL_DESC_PARAMETER_TYPE:
				for (i = 0; i < (MAX_DESC_HANDLES - 2); i++)
				{
					switch (i)
					{
						case IPD:
							TESTCASE_BEGIN("SQL_DESC_PARAMETER_TYPE: Default values.\n");
							//get default field value
							returncode = SQLGetDescField(hDesc[i], 1, DescFields[FieldIndex], &ParameterType, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								TESTCASE_END;	//tests ends here: marked as failed
								break;			//go to next desc_handle
							}

							//check the default value
							// not used for IRD
							if ( ParameterType > 0) {
								LogMsg(ERRMSG,"SQL_DESC_PARAMETER_TYPE (case %d): expected NOTHING and found %d, line %d\n", i, ParameterType, __LINE__);
								TEST_FAILED;
								TESTCASE_END;
								break;
							}
							TESTCASE_END;
							break;

						default: ;
					}//end switch
				}//end for
				break;	
			default: ; //do nothing

		}//end of rec fields
	}//end for loop

	//cleanup
	// decrease the DESC_COUNT for all types of desc : effectively deleting a new (bound) desc rec
	for (i = 0; i < MAX_DESC_TYPES; i++)
	{
		switch (i)
		{
			case IRD:	//do nothing : this is read only
				break; 

			default:
				returncode = SQLSetDescField(hDesc[i], 0, SQL_DESC_COUNT, 0, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_COUNT = 0"))	
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
		}//end switch
	} //end for
 
    // Cleanup ------------------------------------------------
	// free explicit descriptors
	for (i = ExAPD; i < MAX_DESC_HANDLES; i++)
	{
		returncode = SQLFreeHandle(SQL_HANDLE_DESC, hDesc[i]);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle (for explicit descriptors)"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt1);

		}
	}

	// free statement associated with explicit descriptors
	returncode = SQLFreeHandle(SQL_HANDLE_STMT,hstmt1);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);

	}

	// free implicitly allocated descriptors by freeing statement
	returncode = SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);

	}	  

 //===========================================================================================================
 //	Section #4
 // Tests for Descriptor Fields: Set and Get
 //==============================================================================================================
	//do setup:
		// create table
		// prepare stmt
		// bind param
		// insert values
		// select from table
		// bind col


	// check all populated descriptors
	TESTCASE_BEGIN("Setup for Set & Get tests: populating Apd,Ipd,Ird,Ard descriptors\n");
	
	// drop table
	LogMsg(NONE,"SQLAllocHandle to allocate STMT\n");
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	LogMsg(NONE,"SQLExecDirect to drop table Project\n");
	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabProject,SQL_NTS);

	//create table
	LogMsg(NONE,"SQLFreeHandle to free STMT\n");
	SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
	
	LogMsg(NONE,"SQLAllocHandle to allocate STMT\n");
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	LogMsg(NONE,"SQLExecDirect to create table STMT\n");
	returncode = SQLExecDirect(hstmt,(SQLCHAR*) CrtTabProject,SQL_NTS);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		LogMsg(ERRMSG,"Cannot create table.\n");
		TEST_FAILED;
		TEST_RETURN;
	}

	//prepare stmt
	LogMsg(NONE,"SQLFreeHandle to free STMT\n");
	SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
	
	LogMsg(NONE,"SQLAllocHandle to allocate STMT\n");
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	LogMsg(NONE,"SQLPrepare to prepare the insert STMT\n");
	returncode = SQLPrepare(hstmt, (SQLCHAR*)InsTabProject, SQL_NTS);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		LogMsg(ERRMSG,"Cannot prepare stmt.\n");
		TEST_FAILED;
		TEST_RETURN;
	}


	//specify data
	apdProjCode					= 11;
	apdEmpNum					= 1234;
	strcpy((char*)apdProjDesc, "ODBC 3.0 TEST");
	apdStartDate.year			= 2000;
	apdStartDate.month			= 11;
	apdStartDate.day			= 9;
	apdShipTimestamp.year		= 1996;
	apdShipTimestamp.month		= 12;
	apdShipTimestamp.day		= 2;
	apdShipTimestamp.hour		= 1;
	apdShipTimestamp.minute		= 8;
	apdShipTimestamp.second		= 15;
	apdShipTimestamp.fraction	= 0;

	//*** USE SetDescField TO BIND DATA

	//get App handle
	LogMsg(NONE,"******For APP Handle******\n");
	LogMsg(NONE,"SQLGetStmtAttr to get STMT attribute SQL_ATTR_APP_PARAM_DESC for descriptor hDesc[0]\n");
	returncode = SQLGetStmtAttr(hstmt, SQL_ATTR_APP_PARAM_DESC, &hDesc[0], 0, NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
	{
		LogMsg(ERRMSG,"Cannot allocate descriptor: APD.\n");
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_RETURN;
	}

	//Set APD DescCount to number of bound param
	DescCount = MAX_BOUND_PARAM;  // 5
	
	LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_COUNT for descriptor hDesc[0]\n");
	returncode = SQLSetDescField(hDesc[0], 0, SQL_DESC_COUNT, (SQLPOINTER)DescCount, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_COUNT = MAX_BOUND_PARAM"))	
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	//assign field values
	LogMsg(NONE,"Run SQLSetDescField to assign field values for descriptor hDesc[0]\n");
	for (i=1; i <= MAX_BOUND_PARAM; i++)
	{
		//set SQL_DESC_TYPE
		LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_TYPE for descriptor hDesc[0] when I = %d \n", i);
		returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_TYPE, (SQLPOINTER)APP_ExpData[i-1].appType, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_TYPE "))	
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		
		//set SQL_DESC_CONCISE_TYPE
		LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_CONCISE_TYPE for descriptor hDesc[0] when I = %d\n", i);
		returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_CONCISE_TYPE, (SQLPOINTER)APP_ExpData[i-1].appConciseType, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_CONCISE_TYPE"))	
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		
		//set datetime_interval_code if required
		switch (APP_ExpData[i-1].appType)
		{
		    case SQL_DATETIME:
				//case SQL_C_TYPE_TIMESTAMP:
			    //set SQL_DESC_DATETIME_INTERVAL_CODE
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATETIME_INTERVAL_CODE for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_DATETIME_INTERVAL_CODE, (SQLPOINTER)APP_ExpData[i-1].appDatetimeIntervalCode, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATETIME_INTERVAL_CODE"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    break;

		    case SQL_C_CHAR:
				//set SQL_DESC_LENGTH : ignored for all except CHAR data
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_LENGTH for descriptor hDesc[0] when I = %d \n", i);
				returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_LENGTH, (SQLPOINTER)MAX_BUFFER_LEN, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_LENGTH"))	
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}			
			
			    //set SQL_DESC_OCTET_LENGTH : ignored for all except CHAR data
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH, (SQLPOINTER)MAX_BUFFER_LEN, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    break;

		}//end switch for data types
		
		switch (i - 1)		//to set data values
		{
		    case 0:
			    //set SQL_DESC_DATA_PTR
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &apdProjCode,0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogMsg(ERRMSG, "Setting DATA_PTR [%d]\n", (i-1));
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
				
			    //set SQL_DESC_OCTET_LENGTH_PTR
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH_PTR for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR,&ipdProjCode, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }

			    //set SQL_DESC_INDICATOR_PTR to same as SQL_DESC_OCTET_LENGTH_PTR (SQL_NTS)
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_INDICATOR_PTR for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_INDICATOR_PTR, &ipdProjCode, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    break;
		    case 1:
			    //set SQL_DESC_DATA_PTR
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_DATA_PTR,&apdEmpNum,0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogMsg(ERRMSG, "Setting DATA_PTR [%d]\n", (i-1));
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
				
			    //set SQL_DESC_OCTET_LENGTH_PTR
			    LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH_PTR for descriptor hDesc[0] when I = %d \n", i);
				returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR,&ipdEmpNum, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }

			    //set SQL_DESC_INDICATOR_PTR to same as SQL_DESC_OCTET_LENGTH_PTR (SQL_NTS)
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_INDICATOR_PTR for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_INDICATOR_PTR, &ipdEmpNum, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    break;
		    case 2:
			    //set SQL_DESC_DATA_PTR
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &apdProjDesc,sizeof(apdProjDesc));	//SQL_NTS, sizeof(apdProjDesc), MAX_BUFFER_LEN
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogMsg(ERRMSG, "Setting DATA_PTR [%d]\n", (i-1));
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    //set SQL_DESC_OCTET_LENGTH_PTR
			    #ifdef _LP64
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH_PTR for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR,&ipdProjDesc64, 0);
			    #else
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH_PTR for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR,&ipdProjDesc, 0);
			    #endif
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }

			    //set SQL_DESC_INDICATOR_PTR to same as SQL_DESC_OCTET_LENGTH_PTR (SQL_NTS)
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_INDICATOR_PTR for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_INDICATOR_PTR, &ipdProjDesc, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    break;
		    case 3:
			    //set SQL_DESC_DATA_PTR
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &apdStartDate,0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogMsg(ERRMSG, "Setting DATA_PTR [%d]\n", (i-1));
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
				
			    //set SQL_DESC_OCTET_LENGTH_PTR
			    LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH_PTR for descriptor hDesc[0] when I = %d \n", i);
				returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR,&ipdStartDate, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }

			    //set SQL_DESC_INDICATOR_PTR to same as SQL_DESC_OCTET_LENGTH_PTR (SQL_NTS)
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_INDICATOR_PTR for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_INDICATOR_PTR, &ipdStartDate, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    break;
		    case 4:
			    //set SQL_DESC_DATA_PTR
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[0] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &apdShipTimestamp,0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogMsg(ERRMSG, "Setting DATA_PTR [%d]\n", (i-1));
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
				
			    //set SQL_DESC_OCTET_LENGTH_PTR
			    LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH_PTR for descriptor hDesc[0] when I = %d \n", i);
				returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR,&ipdShipTimestamp, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }

			    //set SQL_DESC_INDICATOR_PTR to same as SQL_DESC_OCTET_LENGTH_PTR (SQL_NTS)
			    LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_INDICATOR_PTR for descriptor hDesc[0] when I = %d \n", i);
				returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_INDICATOR_PTR, &ipdShipTimestamp, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    break;
            default: break;
		}

	}//end i (assign values )

	//get Ipd handle
	LogMsg(NONE,"******For IPD Handle******\n");
	LogMsg(NONE,"SQLGetStmtAttr to get STMT attribute SQL_ATTR_IMP_PARAM_DESC for descriptor hDesc[1] \n");
	returncode = SQLGetStmtAttr(hstmt, SQL_ATTR_IMP_PARAM_DESC, &hDesc[1], 0, NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		LogMsg(ERRMSG,"Cannot allocate descriptor: IPD.\n");
		FullDisconnect(pTestInfo);
		TEST_RETURN;
	}

	//Set IPD DescCount to number of bound param
	DescCount = MAX_BOUND_PARAM; // 5
	
	LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_COUNT for descriptor hDesc[1] \n");
	returncode = SQLSetDescField(hDesc[1], 0, SQL_DESC_COUNT, (SQLPOINTER)DescCount, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_COUNT = MAX_BOUND_PARAM"))	
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	//assign field values
	LogMsg(NONE,"Run SQLSetDescField to assign field values for descriptor hDesc[1]\n");
	for (i=1; i <= MAX_BOUND_PARAM; i++)
	{
		//set SQL_DESC_TYPE
		LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_TYPE for descriptor hDesc[1] when I = %d \n", i);
		returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_TYPE, (SQLPOINTER)IPD_ExpData[i-1].ipdType, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_TYPE "))	
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		
		//set SQL_DESC_CONCISE_TYPE
		LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_CONCISE_TYPE for descriptor hDesc[1] when I = %d \n", i);
		returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_CONCISE_TYPE, (SQLPOINTER)IPD_ExpData[i-1].ipdConciseType, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_CONCISE_TYPE"))	
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		//set datetime_interval_code if required
		// switch (APP_ExpData[i].appType)
		switch (APP_ExpData[i-1].appType)
		{
		    case SQL_DATETIME:
			    //set SQL_DESC_DATETIME_INTERVAL_CODE
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATETIME_INTERVAL_CODE for descriptor hDesc[1] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_DATETIME_INTERVAL_CODE, (SQLPOINTER)IPD_ExpData[i-1].ipdDatetimeIntervalCode, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATETIME_INTERVAL_CODE"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    break;

		    case SQL_C_CHAR:
			    //set SQL_DESC_LENGTH : ignored for all except CHAR data				
			    //Length = MAX_BUFFER_LEN;  // 129
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_LENGTH for descriptor hDesc[1] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_LENGTH, (SQLPOINTER)MAX_BUFFER_LEN, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_LENGTH"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }		
			
			    //set SQL_DESC_OCTET_LENGTH : ignored for all except CHAR data
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH for descriptor hDesc[1] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH, (SQLPOINTER)MAX_BUFFER_LEN, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
				
				break;
/*				
		    case SQL_INTERVAL:
			    //set SQL_DESC_DATETIME_INTERVAL_PRECISION
				LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATETIME_INTERVAL_PRECISION for descriptor hDesc[1] when I = %d \n", i);
			    returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_DATETIME_INTERVAL_PRECISION, (SQLPOINTER)IPD_ExpData[i-1].ipdDatetimeIntervalPrecision, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATETIME_INTERVAL_PRECISION"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
*/
		    default: break;
		}//end switch
		
		//set SQL_DESC_DATETIME_INTERVAL_PRECISION
		LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATETIME_INTERVAL_PRECISION for descriptor hDesc[1] when I = %d \n", i);
		returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_DATETIME_INTERVAL_PRECISION, (SQLPOINTER)IPD_ExpData[i-1].ipdDatetimeIntervalPrecision, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATETIME_INTERVAL_PRECISION"))	
		{
		    LogAllErrorsVer3(henv,hdbc,hstmt);
		    FullDisconnect(pTestInfo);
		    TEST_FAILED;
		    TEST_RETURN;
		}
		
		//set SQL_DESC_PRECISION
		LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_PRECISION for descriptor hDesc[1] when I = %d \n", i);
		returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_PRECISION, (SQLPOINTER)IPD_ExpData[i-1].ipdPrecision, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_PRECISION"))	
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}

		//set SQL_DESC_SCALE to 0
		LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_SCALE for descriptor hDesc[1] when I = %d \n", i);
		returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_SCALE, (SQLPOINTER)0, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_SCALE"))	
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}

	}//end i (assign values )

	//execute
	LogMsg(NONE,"SQLExecute to run the insert STMT\n");
	returncode = SQLExecute(hstmt);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		LogMsg(ERRMSG,"Cannot insert row. Expected: SQL_SUCCESS, Actual: %d\n", returncode);
		TEST_FAILED;
		TEST_RETURN;
	}

	//allocate another stmt handle for select operation
	LogMsg(NONE,"SQLAllocHandle to allocate new STMT -- hstmt1\n");
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt1);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	//select from a table to populate the IRD
	LogMsg(NONE,"SQLExecDirect to select record from table Project with hstmt1\n");
	returncode = SQLExecDirect(hstmt1, (SQLCHAR*)SelTabProject,SQL_NTS);
	if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
	{

/*		//bind col
//-------------------------------------------------------------------------------------------------------------
		SQLBindCol(hstmt1, 1, SQL_C_SSHORT, &ardProjCode, 0, &irdProjCode);
		SQLBindCol(hstmt1, 2, SQL_C_SSHORT, &ardEmpNum, 0, &irdEmpNum);
		SQLBindCol(hstmt1, 3, SQL_C_CHAR, ardProjDesc, MAX_BUFFER_LEN, &irdProjDesc);
		SQLBindCol(hstmt1, 4, SQL_C_TYPE_DATE, &ardStartDate, 0, &irdStartDate);
		SQLBindCol(hstmt1, 5, SQL_C_TYPE_TIMESTAMP, &ardShipTimestamp, 0, &irdShipTimestamp);
//---------------------------------------------------------------------------------------------------------------
*/
		//***BIND by using SetDescField: populates the ARD
		
		//get Ard handle
		LogMsg(NONE,"SQLGetStmtAttr to get STMT1 attribute SQL_ATTR_APP_ROW_DESC for descriptor hDesc[2] \n");
		returncode = SQLGetStmtAttr(hstmt1, SQL_ATTR_APP_ROW_DESC, &hDesc[2], 0, NULL);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt1);
			LogMsg(ERRMSG,"Cannot allocate descriptor: ARD.\n");
			FullDisconnect(pTestInfo);
			TEST_RETURN;
		}

		//set Desc Count
		DescCount = MAX_BOUND_PARAM; // 5
		LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_COUNT for descriptor hDesc[2] \n");
		returncode = SQLSetDescField(hDesc[2], 0, SQL_DESC_COUNT, (SQLPOINTER)DescCount, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_COUNT = MAX_BOUND_PARAM"))	
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}

		//assign values
		for (i=1; i <= MAX_BOUND_PARAM; i++) // 5
		{
			//set SQL_DESC_TYPE
			LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_TYPE for descriptor hDesc[2] when I = %d \n", i);
			returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_TYPE, (SQLPOINTER)APP_ExpData[i-1].appType, 0);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_TYPE "))	
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
				FullDisconnect(pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			
			//set SQL_DESC_CONCISE_TYPE
			LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_CONCISE_TYPE for descriptor hDesc[2] when I = %d \n", i);
			returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_CONCISE_TYPE, (SQLPOINTER)APP_ExpData[i-1].appConciseType, 0);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_CONCISE_TYPE"))	
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
				FullDisconnect(pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			//set datetime_interval_code if required
			switch (APP_ExpData[i-1].appType)
			{
				// case SQL_C_TYPE_DATE:
				// case SQL_C_TYPE_TIMESTAMP:
				case SQL_DATETIME:
					//set SQL_DESC_DATETIME_INTERVAL_CODE
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATETIME_INTERVAL_CODE for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATETIME_INTERVAL_CODE, (SQLPOINTER)APP_ExpData[i-1].appDatetimeIntervalCode, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATETIME_INTERVAL_CODE"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					break;
				
				case SQL_C_CHAR:
					//set SQL_DESC_LENGTH : ignored for all except CHAR data
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_LENGTH for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_LENGTH, (SQLPOINTER)MAX_BUFFER_LEN, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_LENGTH"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					
					//set SQL_DESC_OCTET_LENGTH : ignored for all except CHAR data
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH, (SQLPOINTER)MAX_BUFFER_LEN, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					break;
				
				case SQL_C_SSHORT:
					//set SQL_DESC_INDICATOR_PTR to value 0 for all other types
					Indicator = 0;
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &Indicator, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					break;
				default: 
					break;
				
			}//end switch for data types

			//set SQL_DESC_OCTET_LENGTH to value MAX_BUFFER_LEN
/*
			LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH for descriptor hDesc[2] when I = %d \n", i);
			returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH, (SQLPOINTER)MAX_BUFFER_LEN, 0);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField:SQL_DESC_OCTET_LENGTH"))	
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
				FullDisconnect(pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
*/
			switch (i)		//to set data values
			{
				case 1:
					//set SQL_DESC_DATA_PTR
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &ardProjCode,0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
					{
						LogMsg(ERRMSG, "Setting DATA_PTR [%d]\n", (i-1));
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					
					//set SQL_DESC_INDICATOR_PTR 
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &irdProjCode, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}				
				
					//set SQL_DESC_OCTET_LENGTH_PTR 
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR, &irdProjCode, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					break;
				case 2:
					//set SQL_DESC_DATA_PTR
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &ardEmpNum,0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
					{
						LogMsg(ERRMSG, "Setting DATA_PTR [%d]\n", (i-1));
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					
					//set SQL_DESC_INDICATOR_PTR 
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &irdEmpNum, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					
					//set SQL_DESC_OCTET_LENGTH_PTR 
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR, &irdEmpNum, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					break;
				case 3:
					//set SQL_DESC_DATA_PTR
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, ardProjDesc,MAX_BUFFER_LEN);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
					{
						LogMsg(ERRMSG, "Setting DATA_PTR [%d]\n", (i-1));
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					
					//set SQL_DESC_INDICATOR_PTR 
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &irdProjDesc, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					
					//set SQL_DESC_OCTET_LENGTH_PTR 
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR, &irdProjDesc, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					break;
				case 4:
					//set SQL_DESC_DATA_PTR
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &ardStartDate,0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
					{
						LogMsg(ERRMSG, "Setting DATA_PTR [%d]\n", (i-1));
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					
					//set SQL_DESC_INDICATOR_PTR 
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &irdStartDate, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					
					//set SQL_DESC_OCTET_LENGTH_PTR 
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR, &irdStartDate, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					break;
				case 5:
					//set SQL_DESC_DATA_PTR
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &ardShipTimestamp,0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
					{
						LogMsg(ERRMSG, "Setting DATA_PTR [%d]\n", (i-1));
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					
					//set SQL_DESC_INDICATOR_PTR 
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_DATA_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &irdShipTimestamp, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					
					//set SQL_DESC_OCTET_LENGTH_PTR 
					LogMsg(NONE,"SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH_PTR for descriptor hDesc[2] when I = %d \n", i);
					returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR, &irdShipTimestamp, 0);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						FullDisconnect(pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					break;
			}
		}//end i (assign values )

		/* Fetch and print each row of data. On */
		/* an error, display a message and exit. */
		while (TRUE)
		{
			LogMsg(NONE,"SQLFetch to get result with hstmt1\n");
			returncode = SQLFetch(hstmt1);
			if (returncode != SQL_SUCCESS && returncode != SQL_NO_DATA_FOUND)
			{
				LogAllErrorsVer3(henv,hdbc,hstmt1);
				LogMsg(ERRMSG,"Cannot fetch data. returncode=%d \n", returncode);
				// This is where the 1st error is coming from
				break;
			} 
			else if (returncode == SQL_SUCCESS)
			{
				LogMsg(SHORTTIMESTAMP+LINEAFTER, "ProjCode = %d  EmpNum = %d  ProjDes = %s "
					"SDate = %d-%d-%d STStamp = %d-%d-%d %d:%d:%d:%d\n", 
					ardProjCode, ardEmpNum, ardProjDesc,
					ardStartDate.day, ardStartDate.month, ardStartDate.year,
					ardShipTimestamp.day, ardShipTimestamp.month, ardShipTimestamp.year,
					ardShipTimestamp.hour, ardShipTimestamp.minute, ardShipTimestamp.second,
					ardShipTimestamp.fraction);
			} 
			else 
			{
				break;
			}
		}
	
	}//end if

	TESTCASE_END;

	LogMsg(NONE,"SQLGetStmtAttr to get STMT1 attribute SQL_ATTR_IMP_ROW_DESC for descriptor hDesc[3] \n");
	returncode = SQLGetStmtAttr(hstmt1, SQL_ATTR_IMP_ROW_DESC, &hDesc[3], 0, NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		LogMsg(ERRMSG,"Cannot allocate descriptor: IRD.\n");
		TEST_RETURN;
	}

	// loop through all types of desc: APD, IPD, ARD, IRD
	for (i= 0; i < MAX_DESC_TYPES; i++)	// == 4
	{
			DescCount = 0; 
			LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_COUNT for descriptor hDesc[%d] \n",i);
			returncode = SQLGetDescField(hDesc[i], 0, SQL_DESC_COUNT, &DescCount, 0, NULL);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
			{
				LogMsg(ERRMSG, "Cannot get SQL_DESC_COUNT\n");
				LogAllErrorsVer3(henv,hdbc,hstmt1);
				LogAllErrorsVer3(henv,hdbc,hstmt);
				//FullDisconnect(pTestInfo);
				TEST_RETURN;			
			}
			LogMsg(NONE,"Result of SQLGetDescField is %d\n",DescCount);

			if (DescCount != MAX_BOUND_PARAM)	// == 5
			{
				LogMsg(ERRMSG, "Incorrect SQL_DESC_COUNT for hDesc[%d]: expected %d and got %d\n", i, MAX_BOUND_PARAM, DescCount);					
				TEST_RETURN;
			}
			else	
			{	
				switch (i)
				{
					case ARD:
						// this case is the same as next (APD): let fall to next case;
					case APD:
						LogMsg(LINEBEFORE+LINEAFTER,"***Here is I = APD = 0 or I = ARD = 2 \n");
						for (j = 1; j <= DescCount; j++) // == 5
						{
							for(FieldIndex = 0; FieldIndex < MAX_DESC_FIELDS  ; FieldIndex++)
							{
								LogMsg(NONE,"(1)When I = %d, J = %d, FieldIndex = %d\n", i,j,FieldIndex);
								switch (DescFields[FieldIndex])  // 11
								{
								case SQL_DESC_CONCISE_TYPE:
									TESTCASE_BEGIN("APD: SQL_DESC_CONCISE_TYPE\n");
									ConciseType = 0; 
									LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_CONCISE_TYPE for descriptor hDesc[%d] \n", i);
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &ConciseType, SQL_IS_SMALLINT, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, "Failed to get APP Field Value SQL_DESC_CONCISE_TYPE\n");
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									//check value
									if (ConciseType == APP_ExpData[j-1].appConciseType) 
									{
										LogMsg(NONE, "Result of SQLGetDescField -- ConciseType = %d\n", ConciseType);
									}
									else
									{
										LogMsg(ERRMSG, "Expected ConciseType %d and got %d, Line %d\n", APP_ExpData[j-1].appConciseType, ConciseType,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									break;

								case SQL_DESC_DATA_PTR:
									TESTCASE_BEGIN("APD: SQL_DESC_DATA_PTR\n");
									DataPtr = NULL; 									
									LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_DATA_PTR for descriptor hDesc[%d] \n", i);
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &DataPtr, SQL_IS_POINTER, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, "Failed to get APP Field Value SQL_DESC_DATA_PTR\n");
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									if (DataPtr != NULL) 
									{
										LogMsg(NONE, "Result of SQLGetDescField -- DataPtr = %p\n", DataPtr);
									}
									else
									{
										LogMsg(ERRMSG, "Expected DataPtr NOT NULL and got %p, line %d\n",  DataPtr,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									break;	
								
								case SQL_DESC_DATETIME_INTERVAL_CODE:
									TESTCASE_BEGIN("APD: SQL_DESC_DATETIME_INTERVAL_CODE\n");
									DatetimeIntervalCode = 999; 									
									LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_DATETIME_INTERVAL_CODE for descriptor hDesc[%d] \n", i);
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &DatetimeIntervalCode, SQL_IS_SMALLINT, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, "Failed to get APP Field Value SQL_DESC_DATETIME_INTERVAL_CODE\n");
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									if (DatetimeIntervalCode == APP_ExpData[j-1].appDatetimeIntervalCode) 
									{
										LogMsg(NONE, "Result of SQLGetDescField -- DatetimeIntervalCode = %d\n", DatetimeIntervalCode);
									}
									else
									{
										LogMsg(ERRMSG, "Expected DatetimeIntervalCode %d and got %d, line %d\n", APP_ExpData[j-1].appDatetimeIntervalCode, DatetimeIntervalCode,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									break;
				
								case SQL_DESC_INDICATOR_PTR:
									TESTCASE_BEGIN("APD: SQL_DESC_INDICATOR_PTR\n");
									IndicatorPtr = NULL; 
									LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_INDICATOR_PTR for descriptor hDesc[%d] \n", i);
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], IndicatorPtr, SQL_IS_POINTER, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, "Failed to get APP Field Value SQL_DESC_INDICATOR_PTR\n");
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									if (IndicatorPtr == APP_ExpData[j-1].appIndicatorPtr)
									{
										LogMsg(NONE, "Result of SQLGetDescField -- IndicatorPtr = %p \n", IndicatorPtr);
									}
									else
									{
										LogMsg(ERRMSG, "Expected IndicatorPtr %p and got %p, line %d\n", APP_ExpData[j-1].appIndicatorPtr, IndicatorPtr,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									break;
								
								case SQL_DESC_LENGTH:
									TESTCASE_BEGIN("APD: SQL_DESC_LENGTH\n");									
									Length = 99; 
									LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_LENGTH for descriptor hDesc[%d] \n", i);
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Length, SQL_IS_UINTEGER, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, "Failed to get APP Field Value SQL_DESC_LENGTH\n");
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									if (Length == APP_ExpData[j-1].appLength) 
									{
										LogMsg(NONE, "Result of SQLGetDescField -- Length is the same = %d\n", Length);
									}
									else
									{
										LogMsg(ERRMSG, "Expected Length %d and got %d, line %d\n", APP_ExpData[j-1].appLength, Length,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									break;
								
								case SQL_DESC_NUM_PREC_RADIX:
									TESTCASE_BEGIN("APD: SQL_DESC_NUM_PREC_RADIX\n");
									NumPrecRadix = 99; 
									LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_NUM_PREC_RADIX for descriptor hDesc[%d] \n", i);
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &NumPrecRadix, SQL_IS_INTEGER, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, "Failed to get APP Field Value SQL_DESC_NUM_PREC_RADIX\n");
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									if (NumPrecRadix == APP_ExpData[j-1].appNumPrecRadix) 
									{
										LogMsg(NONE, "Result of SQLGetDescField -- NumPrecRadix = %d\n", NumPrecRadix);
									}
									else
									{
										LogMsg(ERRMSG, "Expected NumPrecRadix %d and got %d, line %d\n", APP_ExpData[j-1].appNumPrecRadix, NumPrecRadix,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									break;
								
								case SQL_DESC_OCTET_LENGTH:
									TESTCASE_BEGIN("APD: SQL_DESC_OCTET_LENGTH\n");
									OctetLength = 99; 
									LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_OCTET_LENGTH for descriptor hDesc[%d] \n", i);
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &OctetLength, SQL_IS_INTEGER, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, "Failed to get APP Field Value SQL_DESC_OCTET_LENGTH\n");
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									if (OctetLength == APP_ExpData[j-1].appOctetLength) 
									{
										LogMsg(NONE, "Result of SQLGetDescField -- OctetLength = %d\n", OctetLength);
									}
									else
									{
										LogMsg(ERRMSG, "Expected OctetLength %d and got %d, line %d\n", APP_ExpData[j-1].appOctetLength, OctetLength,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									break;
								
								case SQL_DESC_OCTET_LENGTH_PTR:
									TESTCASE_BEGIN("APD: SQL_DESC_OCTET_LENGTH_PTR\n");
									OctetLengthPtr = NULL; 
									LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_OCTET_LENGTH_PTR for descriptor hDesc[%d] \n", i);
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], OctetLengthPtr, SQL_IS_POINTER, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, "Failed to get APP Field Value SQL_DESC_OCTET_LENGTH_PTR\n");
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									if (OctetLengthPtr == APP_ExpData[j-1].appOctetLengthPtr) 
									{
										LogMsg(NONE, "Result of SQLGetDescField -- OctetLengthPtr = %p\n", OctetLengthPtr);
									}
									else
									{
										LogMsg(ERRMSG, "Expected OctetLengthPtr %p and got %p, line %d\n", APP_ExpData[j-1].appOctetLengthPtr, OctetLengthPtr,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									break;
										
								case SQL_DESC_PRECISION:
									TESTCASE_BEGIN("APD: SQL_DESC_PRECISION\n");
									Precision = 99; 
									LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_PRECISION for descriptor hDesc[%d] \n", i);
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Precision, SQL_IS_SMALLINT, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, "Failed to get APP Field Value SQL_DESC_PRECISION\n");
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									if (Precision == APP_ExpData[j-1].appPrecision) 
									{
										LogMsg(NONE, "Result of SQLGetDescField -- Precision = %d\n", Precision);
									}
									else
									{
										LogMsg(ERRMSG, "Expected Precision %d and got %d,line %d\n", APP_ExpData[j-1].appPrecision, Precision,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									break;
								
								case SQL_DESC_SCALE:
									TESTCASE_BEGIN("APD: SQL_DESC_SCALE\n");
									Scale = 99; 
									LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_SCALE for descriptor hDesc[%d] \n", i);
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j,DescFields[FieldIndex], &Scale, SQL_IS_SMALLINT, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, "Failed to get APP Field Value SQL_DESC_SCALE\n");
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									if (Scale == APP_ExpData[j-1].appScale) 
									{
										LogMsg(NONE, "Result of SQLGetDescField -- Scale = %d\n", Scale);
									}
									else
									{
										LogMsg(ERRMSG, "Expected Scale %d and got %d, line %d\n", APP_ExpData[j-1].appScale, Scale,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									break;
								
								case SQL_DESC_TYPE:
									TESTCASE_BEGIN("APD: SQL_DESC_TYPE\n");
									Type = 0; 
									LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_TYPE for descriptor hDesc[%d] \n", i);
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Type, SQL_IS_SMALLINT, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, "Failed to get APP Field Value SQL_DESC_TYPE\n");
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									if (Type == APP_ExpData[j-1].appType) 
									{
										LogMsg(NONE, "Result of SQLGetDescField -- Type = %d\n", Type);
									}
									else
									{
										LogMsg(ERRMSG, "Expected DescType %d and got %d, line %d\n", APP_ExpData[j-1].appType, Type,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									break;
								default: ;
								} //end switch
							}//end FieldIndex
						}//end j
						break;

					case IPD:
						LogMsg(LINEBEFORE+LINEAFTER,"***Here is I = IPD = 1  \n");
						for (j = 1; j <= DescCount; j++) //iterate through all records
						{
							for(FieldIndex = 0; FieldIndex < MAX_DESC_FIELDS  ; FieldIndex++)
							{
								LogMsg(NONE,"(2)When I = %d, J = %d, FieldIndex = %d\n", i,j,FieldIndex);
								switch (DescFields[FieldIndex])  // 17
								{
									case SQL_DESC_CASE_SENSITIVE:
										TESTCASE_BEGIN("IPD: SQL_DESC_CASE_SENSITIVE\n");
										CaseSensitive = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_CASE_SENSITIVE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &CaseSensitive, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_CASE_SENSITIVE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (CaseSensitive == IPD_ExpData[j-1].ipdCaseSensitive) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- CaseSensitive = %d\n", CaseSensitive);
										}
										else
										{
											LogMsg(ERRMSG, "Expected CaseSensitive %d and got %d, line %d\n", IPD_ExpData[j-1].ipdCaseSensitive, CaseSensitive,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_DATETIME_INTERVAL_CODE:
										TESTCASE_BEGIN("IPD: SQL_DESC_DATETIME_INTERVAL_CODE\n");
										DatetimeIntervalCode = 0; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_DATETIME_INTERVAL_CODE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &DatetimeIntervalCode, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_DATETIME_INTERVAL_CODE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (DatetimeIntervalCode == IPD_ExpData[j-1].ipdDatetimeIntervalCode) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- DatetimeIntervalCode = %d\n", DatetimeIntervalCode);
										}
										else
										{
											LogMsg(ERRMSG, "Expected DatetimeIntervalCode %d and got %d, line %d\n", IPD_ExpData[j-1].ipdDatetimeIntervalCode, DatetimeIntervalCode,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
																				
									case SQL_DESC_DATETIME_INTERVAL_PRECISION:
										TESTCASE_BEGIN("IPD: SQL_DESC_DATETIME_INTERVAL_PRECISION\n");
										DatetimeIntervalPrecision =99;
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_DATETIME_INTERVAL_PRECISION for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &DatetimeIntervalPrecision, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_DATETIME_INTERVAL_PRECISION\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										IPD_ExpData[j-1].ipdDatetimeIntervalPrecision = 0; //default
										if (DatetimeIntervalPrecision == IPD_ExpData[j-1].ipdDatetimeIntervalPrecision) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- DatetimeIntervalPrecision = %d\n", DatetimeIntervalPrecision);
										}
										else
										{
											LogMsg(ERRMSG, "Expected DatetimeIntervalPrecision value %d and got %d, line %d\n", IPD_ExpData[j-1].ipdDatetimeIntervalPrecision, DatetimeIntervalPrecision,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										TESTCASE_END;
										break;

									case SQL_DESC_FIXED_PREC_SCALE:
										TESTCASE_BEGIN("IPD: SQL_DESC_FIXED_PREC_SCALE\n");
										FixedPrecScale = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_FIXED_PREC_SCALE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &FixedPrecScale, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_FIXED_PREC_SCALE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (FixedPrecScale == IPD_ExpData[j-1].ipdFixedPrecScale) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- FixedPrecScale = %d\n", FixedPrecScale);
										}
										else
										{
											LogMsg(ERRMSG, "Expected FixedPrecScale %d and got %d, line %d\n", IPD_ExpData[j-1].ipdFixedPrecScale, FixedPrecScale,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_LENGTH:
										TESTCASE_BEGIN("IPD: SQL_DESC_LENGTH\n");
										Length = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_LENGTH for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Length, SQL_IS_UINTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_LENGTH\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (Length == IPD_ExpData[j-1].ipdLength) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Length = %d\n", Length);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Length %d and got %d, line %d\n", IPD_ExpData[j-1].ipdLength, Length,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
									
									case SQL_DESC_LOCAL_TYPE_NAME:
										TESTCASE_BEGIN("IPD: SQL_DESC_LOCAL_TYPE_NAME\n");
										strcpy((char*)LocalTypeName, ""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_LOCAL_TYPE_NAME for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], LocalTypeName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_LOCAL_TYPE_NAME\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (!(_stricmp((char*)LocalTypeName, (char*)IPD_ExpData[j-1].ipdLocalTypeName)))
										{
											LogMsg(NONE, "Result of SQLGetDescField -- LocalTypeName = %s\n", LocalTypeName);
										}
										else
										{
											LogMsg(ERRMSG, "Expected LocalTypeName %s  and got %s, line %d\n", IPD_ExpData[j-1].ipdLocalTypeName, LocalTypeName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
									
									case SQL_DESC_NAME:
										// The SQL_DESC_NAME for IPD is "" because the driver does not support Named Parameters : when Named Parameter are supported the column name should be returned.
										TESTCASE_BEGIN("IPD: SQL_DESC_NAME\n");
										strcpy((char*)Name, ""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_NAME for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], Name, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_NAME\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										// Add Code here
										if (strlen((char*)Name) == 0)
										{
											LogMsg(NONE, "The SQL_DESC_NAME for IPD is NULL because the driver does not support Named Parameters\n");
										}
										else if (cstrcmp((char*)Name, (char*)IPD_ExpData[j-1].ipdName, TRUE,isCharSet) == 0)
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Name = %s\n", Name);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Desc Name %s  and got %s, line %d\n", IPD_ExpData[j-1].ipdName, Name,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
																			
									case SQL_DESC_NULLABLE:
										TESTCASE_BEGIN("IPD: SQL_DESC_NULLABLE\n");
										Nullable = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_NULLABLE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Nullable, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_NULLABLE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (Nullable == IPD_ExpData[j-1].ipdNullable) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Nullable = %d\n", Nullable);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Nullable value %d and got %d, line %d\n", IPD_ExpData[j-1].ipdNullable, Nullable,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_NUM_PREC_RADIX:
										//10 for exact numeric, 2 for approx numeric, 0 for char
										TESTCASE_BEGIN("IPD: SQL_DESC_NUM_PREC_RADIX\n");
										NumPrecRadix = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_NUM_PREC_RADIX for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &NumPrecRadix, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_NUM_PREC_RADIX\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										if (NumPrecRadix == IPD_ExpData[j-1].ipdNumPrecRadix) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- NumPrecRadix = %d\n", NumPrecRadix);
										}
										else
										{
											LogMsg(ERRMSG, "Expected NumPrecRadix value %d and got %d, line %d\n", IPD_ExpData[j-1].ipdNumPrecRadix, NumPrecRadix,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										TESTCASE_END;
										break;

									case SQL_DESC_OCTET_LENGTH:
										TESTCASE_BEGIN("IPD: SQL_DESC_OCTET_LENGTH\n");
										OctetLength = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_OCTET_LENGTH for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &OctetLength, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_OCTET_LENGTH\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (OctetLength == IPD_ExpData[j-1].ipdOctetLength) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- OctetLength = %d\n", OctetLength);
										}
										else
										{
											LogMsg(ERRMSG, "Expected OctetLength value %d and got %d, line %d\n", IPD_ExpData[j-1].ipdOctetLength, OctetLength,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_PARAMETER_TYPE:
										TESTCASE_BEGIN("IPD: SQL_DESC_PARAMETER_TYPE\n");
										ParameterType = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_PARAMETER_TYPE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &ParameterType, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_PARAMETER_TYPE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (ParameterType == IPD_ExpData[j-1].ipdParameterType) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- ParameterType = %d\n", ParameterType);
										}
										else
										{
											LogMsg(ERRMSG, "Expected ParameterType value %d and got %d, line %d\n", IPD_ExpData[j-1].ipdParameterType, ParameterType,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_PRECISION:
										TESTCASE_BEGIN("IPD: SQL_DESC_PRECISION\n");
										Precision = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_PRECISION for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Precision, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_PRECISION\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										if (Precision == IPD_ExpData[j-1].ipdPrecision) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Precision = %d\n", Precision);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Precision value %d and got %d, line %d\n", IPD_ExpData[j-1].ipdPrecision, Precision,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										TESTCASE_END;
										break;
											
									case SQL_DESC_SCALE:	//valid for decimal and numeric only
										TESTCASE_BEGIN("IPD: SQL_DESC_Scale\n");
										Scale = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_SCALE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Scale, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_SCALE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										if (Scale == IPD_ExpData[j-1].ipdScale) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Scale = %d\n", Scale);
										}
										else
										{
											LogMsg(ERRMSG, "ExpectedScale value %d and got %d, line %d\n", IPD_ExpData[j-1].ipdScale, Scale,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										TESTCASE_END;
										break;

									case SQL_DESC_TYPE:
										TESTCASE_BEGIN("IPD: SQL_DESC_TYPE\n");
										Type = 0; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_TYPE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Type, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_TYPE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (Type != IPD_ExpData[j-1].ipdType) 
										{
											LogMsg(ERRMSG, "Expected Type value %d and got %d, line %d\n", IPD_ExpData[j-1].ipdType, Type,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										LogMsg(NONE, "Result of SQLGetDescField -- Type = %d\n", Type);
										break;

									case SQL_DESC_TYPE_NAME:
										TESTCASE_BEGIN("IPD: SQL_DESC_TYPE_NAME\n");
										strcpy((char*)TypeName, ""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_TYPE_NAME for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], TypeName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_TYPE_NAME\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (!(_stricmp((char*)TypeName, (char*)IPD_ExpData[j-1].ipdTypeName)))
										{
											LogMsg(NONE, "Result of SQLGetDescField -- TypeName = %s\n",TypeName);
										}
										else
										{
											LogMsg(ERRMSG, "Expected TypeName %s  and got %s, line %d\n", IPD_ExpData[j-1].ipdTypeName, TypeName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_UNNAMED:
										TESTCASE_BEGIN("IPD: SQL_DESC_UNNAMED\n");
										Unnamed = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_UNNAMED for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Unnamed, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_UNNAMED\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (Unnamed == IPD_ExpData[j-1].ipdUnnamed) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Unnamed = %d\n", Unnamed);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Unnamed value %d and got %d, line %d\n", IPD_ExpData[j-1].ipdUnnamed, Unnamed,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
						
									case SQL_DESC_UNSIGNED:
										TESTCASE_BEGIN("IPD: SQL_DESC_UNSIGNED\n");
										Unsigned = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_UNSIGNED for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Unsigned, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IPD Field Value SQL_DESC_UNSIGNED\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (Unsigned == IPD_ExpData[j-1].ipdUnsigned) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Unsigned = %d\n", Unsigned);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Unsigned value %d and got %d, line %d\n", IPD_ExpData[j-1].ipdUnsigned, Unsigned,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									default: ;
								}//end switch for each field
							}//end for for each rec (Field Index)
						}//end for j (loop recs)
						break; //end case IPD

					case IRD:
						LogMsg(LINEBEFORE+LINEAFTER,"***Here is I = IRD = 3 \n");
						for (j = 1; j <= DescCount; j++) //iterate through all records
						{
							for(FieldIndex = 0; FieldIndex < MAX_DESC_FIELDS  ; FieldIndex++)
							{
								LogMsg(NONE,"(3)When I = %d, J = %d, FieldIndex = %d\n", i,j,FieldIndex);
								switch (DescFields[FieldIndex])  // 28
								{
									case SQL_DESC_AUTO_UNIQUE_VALUE:
										TESTCASE_BEGIN("IRD: SQL_DESC_AUTO_UNIQUE_VALUE\n");
										AutoUniqueValue = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_AUTO_UNIQUE_VALUE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &AutoUniqueValue, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_AUTO_UNIQUE_VALUE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (AutoUniqueValue == IRD_ExpData[j-1].irdAutoUniqueValue) //none of the columns are autoincrementing
										{
											LogMsg(NONE, "Result of SQLGetDescField -- AutoUniqueValue = %d\n", AutoUniqueValue);
										}
										else
										{
											LogMsg(ERRMSG, "Expected AutoUniqueValue %d (SQL_FALSE) and got %d, line %d\n", IRD_ExpData[j-1].irdAutoUniqueValue, AutoUniqueValue,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
									
									case SQL_DESC_BASE_COLUMN_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_BASE_COLUMN_NAME\n");
										strcpy((char*)BaseColumnName ,""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_BASE_COLUMN_NAME for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], BaseColumnName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_BASE_COLUMN_NAME\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (cstrcmp((char*)BaseColumnName, (char*)IRD_ExpData[j-1].irdBaseColumnName, TRUE,isCharSet) == 0)
										{
											LogMsg(NONE, "Result of SQLGetDescField -- BaseColumnName = %s\n", BaseColumnName);
										}
										else
										{
											LogMsg(ERRMSG, "Expected BaseColumnName %s  and got %s, line %d\n", IRD_ExpData[j-1].irdBaseColumnName, BaseColumnName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;	
										
									case SQL_DESC_BASE_TABLE_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_BASE_TABLE_NAME\n");
										strcpy((char*)BaseTableName ,""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_BASE_TABLE_NAME for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], BaseTableName,MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_BASE_TABLE_NAME\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (cstrcmp((char*)BaseTableName, (char*)IRD_ExpData[j-1].irdBaseTableName, TRUE,isCharSet) == 0)
										{
											LogMsg(NONE, "Result of SQLGetDescField -- BaseTableName = %s\n", BaseTableName);
										}
										else
										{
											LogMsg(ERRMSG, "Expected BaseTableName %s  and got %s, line %d\n", IRD_ExpData[j-1].irdBaseTableName, BaseTableName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
								
									case SQL_DESC_CASE_SENSITIVE:
										TESTCASE_BEGIN("IRD: SQL_DESC_CASE_SENSITIVE\n");
										CaseSensitive = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_CASE_SENSITIVE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &CaseSensitive, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_CASE_SENSITIVE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (CaseSensitive == IRD_ExpData[j-1].irdCaseSensitive) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- CaseSensitive = %d\n", CaseSensitive);
										}
										else
										{
											LogMsg(ERRMSG, "Expected CaseSensitive %d and got %d, line %d\n", IRD_ExpData[j-1].irdCaseSensitive, CaseSensitive,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
										
									case SQL_DESC_CATALOG_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_CATALOG_NAME\n");
										strcpy((char*)CatalogName ,""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_CATALOG_NAME for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], CatalogName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_CATALOG_NAME\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (!(_stricmp((char*)CatalogName, (char*)IRD_ExpData[j-1].irdCatalogName)))
										{
											LogMsg(NONE, "Result of SQLGetDescField -CatalogName = %s\n", CatalogName);
										}
										else
										{
											LogMsg(ERRMSG, "Expected CatalogName %s  and got %s, line %d\n", IRD_ExpData[j-1].irdCatalogName, CatalogName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
								
									case SQL_DESC_CONCISE_TYPE:
										TESTCASE_BEGIN("IRD: SQL_DESC_CONCISE_TYPE\n");
										ConciseType = 0; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_CONCISE_TYPE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &ConciseType, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_CONCISE_TYPE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (ConciseType == IRD_ExpData[j-1].irdConciseType) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- ConciseType = %d\n", ConciseType);
										}
										else
										{
											LogMsg(ERRMSG, "Expected ConciseType %d and got %d, line %d\n", IRD_ExpData[j-1].irdConciseType, ConciseType,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
								
									case SQL_DESC_DATETIME_INTERVAL_CODE:
										TESTCASE_BEGIN("IRD: SQL_DESC_DATETIME_INTERVAL_CODE\n");
										DatetimeIntervalCode = 0; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_DATETIME_INTERVAL_CODE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &DatetimeIntervalCode, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_DATETIME_INTERVAL_CODE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (DatetimeIntervalCode == IRD_ExpData[j-1].irdDatetimeIntervalCode) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- DatetimeIntervalCode = %d\n", DatetimeIntervalCode);
										}
										else
										{
											LogMsg(ERRMSG, "Expected DatetimeIntervalCode %d and got %d, line %d\n", IRD_ExpData[j-1].irdDatetimeIntervalCode, DatetimeIntervalCode,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;								
									
									case SQL_DESC_DISPLAY_SIZE:
										TESTCASE_BEGIN("IRD: SQL_DESC_DISPLAY_SIZE\n");
										DisplaySize = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_DISPLAY_SIZE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &DisplaySize, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_DISPLAY_SIZE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (DisplaySize == IRD_ExpData[j-1].irdDisplaySize) //none of the columns are autoincrementing
										{
											LogMsg(NONE, "Result of SQLGetDescField -- DisplaySize = %d\n", DisplaySize);
										}
										else
										{
											LogMsg(ERRMSG, "Expected DisplaySize %d and got %d, line %d\n", IRD_ExpData[j-1].irdDisplaySize, DisplaySize,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
									
									case SQL_DESC_FIXED_PREC_SCALE:
										TESTCASE_BEGIN("IRD: SQL_DESC_FIXED_PREC_SCALE\n");
										FixedPrecScale = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_FIXED_PREC_SCALE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &FixedPrecScale, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_FIXED_PREC_SCALE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (FixedPrecScale == IRD_ExpData[j-1].irdFixedPrecScale) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- FixedPrecScale = %d\n", FixedPrecScale);
										}
										else
										{
											LogMsg(ERRMSG, "Expected FixedPrecScale %d and got %d, line %d\n", IRD_ExpData[j-1].irdFixedPrecScale, FixedPrecScale,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
									
									case SQL_DESC_LABEL:
										TESTCASE_BEGIN("IRD: SQL_DESC_LABEL\n");
										strcpy((char*)Label , ""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_LABEL for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], Label, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_LABEL\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//if (!(_stricmp((char*)Label, (char*)IRD_ExpData[j-1].irdLabel)))
										if (!(_stricmp((char*)Label, (char*)IRD_ExpData[j-1].irdName)))
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Label = %s\n", Label);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Label %s  and got %s, line %d\n", IRD_ExpData[j-1].irdLabel, Label,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_LENGTH:
										TESTCASE_BEGIN("IRD: SQL_DESC_LENGTH\n");
										Length = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_LENGTH for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Length, SQL_IS_UINTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_LENGTH\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (Length == IRD_ExpData[j-1].irdLength) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Length = %d\n", Length);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Length %d and got %d, line %d\n", IRD_ExpData[j-1].irdLength, Length,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
									
									case SQL_DESC_LITERAL_PREFIX:
										TESTCASE_BEGIN("IRD: SQL_DESC_LITERAL_PREFIX\n");
										strcpy((char*)LiteralPrefix , ""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_LITERAL_PREFIX for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], LiteralPrefix, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_LITERAL_PREFIX\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (!(_stricmp((char*)LiteralPrefix, (char*)IRD_ExpData[j-1].irdLiteralPrefix)))
										{
											LogMsg(NONE, "Result of SQLGetDescField -- LiteralPrefix = %s\n",LiteralPrefix);
										}
										else
										{
											LogMsg(ERRMSG, "Expected LiteralPrefix %s  and got %s, line %d\n", IRD_ExpData[j-1].irdLiteralPrefix, LiteralPrefix,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
									
									case SQL_DESC_LITERAL_SUFFIX:
										TESTCASE_BEGIN("IRD: SQL_DESC_LITERAL_SUFFIX\n");
										strcpy((char*)LiteralSuffix, ""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_LITERAL_SUFFIX for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], LiteralSuffix,MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_LITERAL_SUFFIX\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (!(_stricmp((char*)LiteralSuffix, (char*)IRD_ExpData[j-1].irdLiteralSuffix)))
										{
											LogMsg(NONE, "Result of SQLGetDescField -- LiteralSuffix = %s\n", LiteralSuffix);
										}
										else
										{
											LogMsg(ERRMSG, "Expected LiteralSuffix %s  and got %s, line %d\n", IRD_ExpData[j-1].irdLiteralSuffix, LiteralSuffix,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
									
									case SQL_DESC_LOCAL_TYPE_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_LOCAL_TYPE_NAME\n");
										strcpy((char*)LocalTypeName, ""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_LOCAL_TYPE_NAME for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], LocalTypeName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_LOCAL_TYPE_NAME\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (!(_stricmp((char*)LocalTypeName, (char*)IRD_ExpData[j-1].irdLocalTypeName)))
										{
											LogMsg(NONE, "Result of SQLGetDescField -- LocalTypeName = %s\n", LocalTypeName);
										}
										else
										{
											LogMsg(ERRMSG, "Expected LocalTypeName %s  and got %s, line %d\n", IRD_ExpData[j-1].irdLocalTypeName, LocalTypeName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
									
									case SQL_DESC_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_NAME\n");
										strcpy((char*)Name, ""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_NAME for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], Name, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_NAME\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (cstrcmp((char*)Name, (char*)IRD_ExpData[j-1].irdName, TRUE,isCharSet) == 0)
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Name = %s\n", Name);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Desc Name %s  and got %s, line %d\n", IRD_ExpData[j-1].irdName, Name,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_NULLABLE:
										TESTCASE_BEGIN("IRD: SQL_DESC_NULLABLE\n");
										Nullable = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_NULLABLE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Nullable, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_NULLABLE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (Nullable == IRD_ExpData[j-1].irdNullable) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Nullable = %d\n", Nullable);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Nullable value %d and got %d, line %d\n", IRD_ExpData[j-1].irdNullable, Nullable,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_NUM_PREC_RADIX:
										//10 for exact numeric, 2 for approx numeric, 0 for char
										TESTCASE_BEGIN("IRD: SQL_DESC_NUM_PREC_RADIX\n");
										NumPrecRadix = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_NUM_PREC_RADIX for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &NumPrecRadix, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_NUM_PREC_RADIX\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										//IRD_ExpData[j-1].irdNumPrecRadix = 2;
										if (NumPrecRadix == IRD_ExpData[j-1].irdNumPrecRadix) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- NumPrecRadix = %d\n", NumPrecRadix);
										}
										else
										{
											LogMsg(ERRMSG, "Expected NumPrecRadix value %d and got %d, line %d\n", IRD_ExpData[j-1].irdNumPrecRadix, NumPrecRadix,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										TESTCASE_END;
										break;

									case SQL_DESC_OCTET_LENGTH:
										TESTCASE_BEGIN("IRD: SQL_DESC_OCTET_LENGTH\n");
										OctetLength = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_OCTET_LENGTH for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &OctetLength, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_OCTET_LENGTH\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (OctetLength == IRD_ExpData[j-1].irdOctetLength) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- OctetLength = %d\n", OctetLength);
										}
										else
										{
											LogMsg(ERRMSG, "Expected OctetLength value %d and got %d, line %d\n", IRD_ExpData[j-1].irdOctetLength, OctetLength,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_PRECISION:
										//is valid for numeric, timestamp, time and interval only
										TESTCASE_BEGIN("IRD: SQL_DESC_PRECISION\n");
										Precision = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_PRECISION for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Precision, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_PRECISION\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										if (Precision == IRD_ExpData[j-1].irdPrecision) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Precision = %d\n", Precision);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Precision value %d and got %d, line %d\n", IRD_ExpData[j-1].irdPrecision, Precision,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										TESTCASE_END;
										break;
										
									case SQL_DESC_SCALE:
										TESTCASE_BEGIN("IRD: SQL_DESC_Scale\n");
										Scale = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_SCALE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Scale, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_SCALE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										if (Scale == IRD_ExpData[j-1].irdScale) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Scale = %d\n", Scale);
										}
										else
										{
											LogMsg(ERRMSG, "ExpectedScale value %d and got %d, line %d\n", IRD_ExpData[j-1].irdScale, Scale,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										TESTCASE_END;
										break;
									
									case SQL_DESC_SCHEMA_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_SCHEMA_NAME\n");
										strcpy((char*)SchemaName,""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_SCHEMA_NAME for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], SchemaName,MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_SCHEMA_NAME\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (!(_stricmp((char*)SchemaName, (char*)IRD_ExpData[j-1].irdSchemaName)))
										{
											LogMsg(NONE, "Result of SQLGetDescField -- SchemaName = %s\n", SchemaName);
										}
										else
										{
											LogMsg(ERRMSG, "Expected SchemaName %s  and got %s, line %d\n", IRD_ExpData[j-1].irdSchemaName, SchemaName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
									
									case SQL_DESC_SEARCHABLE:
										TESTCASE_BEGIN("IRD: SQL_DESC_SEARCHABLE\n");
										Searchable = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_SEARCHABLE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Searchable, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_SEARCHABLE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (Searchable == IRD_ExpData[j-1].irdSearchable) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Searchable = %d\n", Searchable);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Searchable value %d and got %d, line %d\n", IRD_ExpData[j-1].irdSearchable, Searchable,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
							
									case SQL_DESC_TABLE_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_TABLE_NAME\n");
										strcpy((char*)TableName, ""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_TABLE_NAME for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], TableName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_TABLE_NAME\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (cstrcmp((char*)TableName, (char*)IRD_ExpData[j-1].irdTableName, TRUE,isCharSet) == 0)
										{
											LogMsg(NONE, "Result of SQLGetDescField -- TableName = %s\n", TableName);
										}
										else
										{
											LogMsg(ERRMSG, "Expected TableName %s  and got %s, line %d\n", IRD_ExpData[j-1].irdTableName, TableName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_TYPE:
										TESTCASE_BEGIN("IRD: SQL_DESC_TYPE\n");
										Type = 0; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_TYPE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Type, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_TYPE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (Type != IRD_ExpData[j-1].irdType) 
										{
											LogMsg(ERRMSG, "Expected Type value %d and got %d, line %d\n", IRD_ExpData[j-1].irdType, Type,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										LogMsg(NONE, "Result of SQLGetDescField -- Type = %d\n", Type);
										break;
							
									case SQL_DESC_TYPE_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_TYPE_NAME\n");
										strcpy((char*)TypeName, ""); 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_TYPE_NAME for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], TypeName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_TYPE_NAME\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (!(_stricmp((char*)TypeName, (char*)IRD_ExpData[j-1].irdTypeName)))
										{
											LogMsg(NONE, "Result of SQLGetDescField -- TypeName = %s\n",TypeName);
										}
										else
										{
											LogMsg(ERRMSG, "Expected TypeName %s  and got %s, line %d\n", IRD_ExpData[j-1].irdTypeName, TypeName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_UNNAMED:
										TESTCASE_BEGIN("IRD: SQL_DESC_UNNAMED\n");
										Unnamed = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_UNNAMED for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Unnamed, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_UNNAMED\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (Unnamed == IRD_ExpData[j-1].irdUnnamed) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Unnamed = %d\n", Unnamed);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Unnamed value %d and got %d, line %d\n", IRD_ExpData[j-1].irdUnnamed, Unnamed,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_UNSIGNED:
										TESTCASE_BEGIN("IRD: SQL_DESC_UNSIGNED\n");
										Unsigned = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_UNSIGNED for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Unsigned, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_UNSIGNED\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (Unsigned == IRD_ExpData[j-1].irdUnsigned) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Unsigned = %d\n", Unsigned);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Unsigned value %d and got %d, line %d\n", IRD_ExpData[j-1].irdUnsigned, Unsigned,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;

									case SQL_DESC_UPDATABLE:
										TESTCASE_BEGIN("IRD: SQL_DESC_UPDATABLE\n");
										Updatable = 99; 
										LogMsg(NONE,"SQLGetDescField to get attribute SQL_DESC_UPDATABLE for descriptor hDesc[%d] \n", i);
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Updatable, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, "Failed to get IRD Field Value SQL_DESC_UPDATABLE\n");
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										if (Updatable == IRD_ExpData[j-1].irdUpdatable) 
										{
											LogMsg(NONE, "Result of SQLGetDescField -- Updatable = %d\n", Updatable);
										}
										else
										{
											LogMsg(ERRMSG, "Expected Updatable value %d and got %d, line %d\n", IRD_ExpData[j-1].irdUpdatable, Updatable,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										break;
									
									default: ;
										//do nothing : field not valid for this type of descriptor
								}//end switch
							}//end of looping through all desc fields (FieldIndex)
						}//end of looping through all records (j)
						break;
				}//end switch 
			}
	}//end of tests for all DESC TYPES

 //===========================================================================================================
 //		Cleanup 
 //==============================================================================================================
	//mark end of test in log file. 
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLSetDescField and SQLGetDescField.\n");
	//cleanup--------------------
/*	freeing hstmt results in error
	returncode = SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"Free Handle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLFreeHandle(SQL_HANDLE_STMT,hstmt1);
	if(!CHECKRC(SQL_SUCCESS,returncode,"FreeHandle: hstmt1"))
	{
			LogAllErrorsVer3(henv,hdbc,hstmt1);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
	}
*/

	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);
	returncode = SQLExecDirect(hstmt,(SQLCHAR*) DrpTabProject,SQL_NTS);
	returncode = SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
	// diconnect : free everything	
	FullDisconnect3(pTestInfo);
	free_list(var_list);
	TEST_RETURN;
}//end of test suite
