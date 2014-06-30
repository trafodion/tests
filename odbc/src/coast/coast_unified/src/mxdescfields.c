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

#define MAX_BUFFER_LEN			258
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




	SQLHDESC			hDesc [MAX_DESC_HANDLES];		//stores Desc handles

	
	SQLINTEGER			DescTypes[MAX_DESC_TYPES] = 
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
	SQLULEN 		ArraySize; // sushil
	SQLUSMALLINT*	ArrayStatusPtr;
	SQLLEN*			BindOffsetPtr; // sushil
	SQLINTEGER		BindType;
	//TCHAR            bef_guard[9] = "00000000";
	SQLSMALLINT		DescCount;
	//TCHAR            aft_guard[9] = "00000000";
	SQLULEN*    	RowsProcessedPtr; // sushil
	  //descriptor record fields
	SQLINTEGER		AutoUniqueValue;
	SQLTCHAR			BaseColumnName[MAX_BUFFER_LEN];
	SQLTCHAR			BaseTableName[MAX_BUFFER_LEN];
	SQLINTEGER		CaseSensitive;
	SQLTCHAR			CatalogName[MAX_BUFFER_LEN];
	SQLSMALLINT		ConciseType;
	SQLPOINTER		DataPtr;
	SQLSMALLINT		DatetimeIntervalCode;
	SQLINTEGER		DatetimeIntervalPrecision;
	SQLINTEGER		DisplaySize;
	SQLSMALLINT		FixedPrecScale;
	SQLINTEGER*		IndicatorPtr;
	SQLTCHAR			Label[MAX_BUFFER_LEN];
	SQLUINTEGER		Length;
	SQLTCHAR			LiteralPrefix[MAX_BUFFER_LEN];
	SQLTCHAR			LiteralSuffix[MAX_BUFFER_LEN];
	SQLTCHAR			LocalTypeName[MAX_BUFFER_LEN]; 
	SQLTCHAR			Name[MAX_BUFFER_LEN];
	SQLSMALLINT		Nullable;
	SQLINTEGER		NumPrecRadix;
	SQLINTEGER		OctetLength;
	SQLINTEGER*		OctetLengthPtr;
	SQLSMALLINT		ParameterType;
	SQLSMALLINT		Precision;
	SQLSMALLINT		Scale;
	SQLTCHAR			SchemaName[MAX_BUFFER_LEN];
	SQLSMALLINT		Searchable;
	SQLTCHAR			TableName[MAX_BUFFER_LEN];
	SQLSMALLINT		Type;
	SQLTCHAR			TypeName[MAX_BUFFER_LEN];
	SQLSMALLINT		Unnamed;
	SQLSMALLINT		Unsigned;
	SQLSMALLINT		Updatable;
	/* SEAQUEST */ TCHAR tmpbuf[MAX_BUFFER_LEN];

	//used in set
	SQLINTEGER		_tcslen;
	SQLINTEGER		Indicator;


	//loop variables
	int i, FieldIndex, j;	
	
	//variables for table
	TCHAR *DrpTabProject = _T("--");
	TCHAR *CrtTabProject = _T("--");
	TCHAR *InsTabProject = _T("--");
	TCHAR *SelTabProject = _T("--");

	//variables used for binding params and cols
	SQLSMALLINT	apdProjCode = 0,ardProjCode, 
				apdEmpNum = 0, ardEmpNum ;

	SQLTCHAR		apdProjDesc[MAX_BUFFER_LEN];
	SQLTCHAR		ardProjDesc[MAX_BUFFER_LEN];

	DATE_STRUCT	apdStartDate, ardStartDate;

	TIMESTAMP_STRUCT apdShipTimestamp, ardShipTimestamp;

#ifdef _LP64
	SQLLEN      ipdProjDesc64 = SQL_NTS; // sushil: ???
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
	  //TCHAR			irdBaseColumnName[MAX_BUFFER_LEN];
	  //TCHAR			irdBaseTableName[MAX_BUFFER_LEN];
	  	TCHAR			*irdBaseColumnName;
	  	TCHAR			*irdBaseTableName;
		SQLINTEGER		irdCaseSensitive;
		TCHAR*	    	irdCatalogName; //[MAX_BUFFER_LEN];
		SQLSMALLINT		irdConciseType;
		SQLSMALLINT		irdDatetimeIntervalCode;
		SQLINTEGER		irdDatetimeIntervalPrecision;
		SQLINTEGER		irdDisplaySize;
		SQLSMALLINT		irdFixedPrecScale;
		TCHAR			*irdLabel;
	  //TCHAR			irdLabel[MAX_BUFFER_LEN];
		SQLUINTEGER		irdLength;
		//TCHAR			irdLiteralPrefix[MAX_BUFFER_LEN];
		//TCHAR			irdLiteralSuffix[MAX_BUFFER_LEN];
		//TCHAR			irdLocalTypeName[MAX_BUFFER_LEN];
		//TCHAR			irdName[MAX_BUFFER_LEN];
		TCHAR			*irdLiteralPrefix;
		TCHAR			*irdLiteralSuffix;
		TCHAR			*irdLocalTypeName;
		TCHAR			*irdName;

		SQLSMALLINT		irdNullable;
		SQLINTEGER		irdNumPrecRadix;
		SQLINTEGER		irdOctetLength;
		SQLSMALLINT		irdPrecision;
		SQLSMALLINT		irdScale;
		TCHAR*   		irdSchemaName; //[MAX_BUFFER_LEN];
		SQLSMALLINT		irdSearchable;
	  //TCHAR     		irdTableName[MAX_BUFFER_LEN];
		TCHAR     		*irdTableName;
		SQLSMALLINT		irdType;
	  //TCHAR			irdTypeName[MAX_BUFFER_LEN];
		TCHAR			*irdTypeName;
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
		//TCHAR			ipdLocalTypeName[MAX_BUFFER_LEN];
		//TCHAR			ipdName[MAX_BUFFER_LEN];
		TCHAR			*ipdLocalTypeName;
		TCHAR			*ipdName;
		SQLSMALLINT		ipdNullable;
		SQLINTEGER		ipdNumPrecRadix;
		SQLINTEGER		ipdOctetLength;
		SQLSMALLINT		ipdParameterType;
		SQLSMALLINT		ipdPrecision;
		SQLSMALLINT		ipdScale;
		SQLSMALLINT		ipdType;
	  TCHAR			*ipdTypeName;//[MAX_BUFFER_LEN];
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

//IRD_REC IRD_ActualData[MAX_BOUND_PARAM];

//IRD_REC IRD_ActualData[MAX_BOUND_PARAM];
//	IRD_REC IRD_ExpData[MAX_BOUND_PARAM] =
//	{
//		//AutoUniqueValue	BaseColumnName			BaseTableName			CaseSensitive	CatalogName				ConciseType			DatetimeIntervalCode	DatetimeIntervalPrecision	DisplaySize		FixedPrecScale		Label						Length	Prefix		Suffix		LocalTypeName	Name					Nullable		NumPrecRadix	OctetLen	Precision	Scale	SchemaName			Searchable			TableName		Type			TypeName		Unamed		Unsigned	Updateable
//		{ SQL_FALSE,		_T("PROJCODE"),			_T("PROJECT"),			SQL_FALSE,		pTestInfo->Catalog,		SQL_INTEGER,		0,						0,							10,				SQL_FALSE,			_T("Project/Code"),			/* SEAQUEST 10 */4,		_T(""),		_T(""),		_T(""),			_T("PROJCODE"),			SQL_NO_NULLS,	/* SEAQUEST 0 */10,				4,			10,			0,		pTestInfo->Schema,	SQL_PRED_BASIC,		_T("PROJECT"),	SQL_INTEGER,	_T("INTEGER"),	SQL_NAMED,	SQL_TRUE,	SQL_ATTR_READWRITE_UNKNOWN},
//		{ SQL_FALSE,		_T("EMPNUM"),			_T("PROJECT"),			SQL_FALSE,		pTestInfo->Catalog,		SQL_INTEGER,		0,						0,							10,				SQL_FALSE,			_T("Employee/Number"),		/* SEAQUEST 10 */4,		_T(""),		_T(""),		_T(""),			_T("EMPNUM"),			SQL_NO_NULLS,	/* SEAQUEST 0 */10,				4,			10,			0,		pTestInfo->Schema,	SQL_PRED_BASIC,		_T("PROJECT"),	SQL_INTEGER,	_T("INTEGER"),	SQL_NAMED,	SQL_TRUE,	SQL_ATTR_READWRITE_UNKNOWN},
//		{ SQL_FALSE,		_T("PROJDESC"),			_T("PROJECT"),			SQL_TRUE,		pTestInfo->Catalog,		/* SEAQUEST SQL_WCHAR */SQL_VARCHAR,			0,						0,							18,				SQL_FALSE,			_T("Project/Description"),	/* SEAQUEST 13 */18,		/* SEAQUEST _T("N'") */_T("'"),	_T("'"),	/* SEAQUEST _T("") */ _T("VARCHAR CHARACTER SET ISO88591"),			_T("PROJDESC"),			SQL_NO_NULLS,	0,				/* SEAQUEST 24 */18,			/* SEAQUEST 0 */18,			0,		pTestInfo->Schema,	SQL_PRED_SEARCHABLE,_T("PROJECT"),	/* SEAQUEST SQL_WCHAR */SQL_VARCHAR,		_T("VARCHAR"),	SQL_NAMED,	SQL_TRUE,	SQL_ATTR_READWRITE_UNKNOWN},
//		{ SQL_FALSE,		_T("START_DATE"),		_T("PROJECT"),			SQL_FALSE,		pTestInfo->Catalog,		SQL_TYPE_DATE,		SQL_CODE_DATE,			0,							10,				SQL_FALSE,			_T("Start/Date"),			10,		_T("{d'"),	_T("'}"),	_T(""),			_T("START_DATE"),		SQL_NO_NULLS,	0,				6,			0,			0,		pTestInfo->Schema,	SQL_PRED_BASIC,		_T("PROJECT"),	SQL_DATETIME,	_T("DATE"),		SQL_NAMED,	SQL_TRUE,	SQL_ATTR_READWRITE_UNKNOWN},
//		{ SQL_FALSE,		_T("SHIP_TIMESTAMP"),	_T("PROJECT"),			SQL_FALSE,		pTestInfo->Catalog,		SQL_TYPE_TIMESTAMP, SQL_CODE_TIMESTAMP,		0,							26,				SQL_FALSE,			_T("Timestamp/Shipped"),	26,		_T("{ts'"),	_T("'}"),	_T(""),			_T("SHIP_TIMESTAMP"),	SQL_NO_NULLS,	0,				16,			6,			0,		pTestInfo->Schema,	SQL_PRED_BASIC,		_T("PROJECT"),	SQL_DATETIME,	_T("TIMESTAMP"),SQL_NAMED,	SQL_TRUE,	SQL_ATTR_READWRITE_UNKNOWN}
//	};


//IRD_REC IRD_ActualData[MAX_BOUND_PARAM];
	IRD_REC IRD_ExpData[MAX_BOUND_PARAM] =
	{
		//AutoUniqueValue	BaseColumnName		BaseTableName		CaseSensitive	CatalogName				ConciseType							DatetimeIntervalCode	DatetimeIntervalPrecision	DisplaySize		FixedPrecScale		Label		Length					Prefix							Suffix			LocalTypeName												Name		Nullable		NumPrecRadix		OctetLen			Precision			Scale		SchemaName			Searchable			TableName	Type							TypeName		Unamed		Unsigned	Updateable
		{ SQL_FALSE,		_T("--"),			_T("--"),			SQL_FALSE,		pTestInfo->Catalog,		SQL_INTEGER,						0,						0,							10,				SQL_FALSE,			_T("--"),	/* SEAQUEST 10 */4,		_T(""),							_T(""),			_T(""),														_T("--"),	SQL_NO_NULLS,	/* SEAQUEST 0 */10,	4,					10,					0,			pTestInfo->Schema,	SQL_PRED_BASIC,		_T("--"),	SQL_INTEGER,						_T("INTEGER"),	SQL_NAMED,	SQL_TRUE,	SQL_ATTR_READWRITE_UNKNOWN},
		{ SQL_FALSE,		_T("--"),			_T("--"),			SQL_FALSE,		pTestInfo->Catalog,		SQL_INTEGER,						0,						0,							10,				SQL_FALSE,			_T("--"),	/* SEAQUEST 10 */4,		_T(""),							_T(""),			_T(""),														_T("--"),	SQL_NO_NULLS,	/* SEAQUEST 0 */10,	4,					10,					0,			pTestInfo->Schema,	SQL_PRED_BASIC,		_T("--"),	SQL_INTEGER,						_T("INTEGER"),	SQL_NAMED,	SQL_TRUE,	SQL_ATTR_READWRITE_UNKNOWN},
		{ SQL_FALSE,		_T("--"),			_T("--"),			SQL_TRUE,		pTestInfo->Catalog,		/* SEAQUEST SQL_WCHAR */SQL_VARCHAR,0,						0,							18,				SQL_FALSE,			_T("--"),	/* SEAQUEST 13 */18,	/* SEAQUEST _T("N'") */_T("'"),	_T("'"),		/* SEAQUEST _T("") */ _T("VARCHAR CHARACTER SET ISO88591"),	_T("--"),	SQL_NO_NULLS,	0,					/* SEAQUEST 24 */18,/* SEAQUEST 0 */18,	0,			pTestInfo->Schema,	SQL_PRED_SEARCHABLE,_T("--"),	/* SEAQUEST SQL_WCHAR */SQL_VARCHAR,_T("VARCHAR"),	SQL_NAMED,	SQL_TRUE,	SQL_ATTR_READWRITE_UNKNOWN},
		{ SQL_FALSE,		_T("--"),			_T("--"),			SQL_FALSE,		pTestInfo->Catalog,		SQL_TYPE_DATE,						SQL_CODE_DATE,			0,							10,				SQL_FALSE,			_T("--"),	10,						_T("{d'"),						_T("'}"),		_T(""),														_T("--"),	SQL_NO_NULLS,	0,					6,					0,					0,			pTestInfo->Schema,	SQL_PRED_BASIC,		_T("--"),	SQL_DATETIME,						_T("DATE"),		SQL_NAMED,	SQL_TRUE,	SQL_ATTR_READWRITE_UNKNOWN},
		{ SQL_FALSE,		_T("--"),			_T("--"),			SQL_FALSE,		pTestInfo->Catalog,		SQL_TYPE_TIMESTAMP,					SQL_CODE_TIMESTAMP,		0,							26,				SQL_FALSE,			_T("--"),	26,						_T("{ts'"),						_T("'}"),		_T(""),														_T("--"),	SQL_NO_NULLS,	0,					16,					6,					0,			pTestInfo->Schema,	SQL_PRED_BASIC,		_T("--"),	SQL_DATETIME,						_T("TIMESTAMP"),SQL_NAMED,	SQL_TRUE,	SQL_ATTR_READWRITE_UNKNOWN}
	};

	//COMMENTS:
	// The SQL_DESC_NAME for IPD is "" because the driver does not support Named Parameters : when Named Parameter are supported the column name should be returned.
	IPD_REC IPD_ExpData[MAX_BOUND_PARAM] =
	{
		//	CaseSensitive	ConciseType		DatetimeIntervalCode	DatetimeIntervalPrecision	FixedPrecScale	Length							LocalTypeName												Name						Nullable		NumPrecRadix	OctetLen						ParameterType		Precision	Scale	Type			TypeName									Unamed									Unsigned
		{ 	SQL_FALSE,		SQL_INTEGER,			0,					/* SEAQUEST 0 */ 10,	SQL_FALSE ,		/* SEAQUEST 0 */ 4,				_T(""),														/*PROJCODE*/_T("--"),		SQL_NO_NULLS,	10,				4,								SQL_PARAM_INPUT,	10,			0,		SQL_INTEGER,	_T("INTEGER"),								/* SEAQUEST SQL_NAMED */ SQL_UNNAMED,	SQL_TRUE},
		{ 	SQL_FALSE,		SQL_INTEGER,			0,					/* SEAQUEST 0 */ 10,	SQL_FALSE,		/* SEAQUEST 0 */MAX_BUFFER_LEN,	_T(""),														/*EMPNUM*/_T("--"),			SQL_NO_NULLS,	10,				/* SEAQUEST 4 */ MAX_BUFFER_LEN,SQL_PARAM_INPUT,	10,			0,		SQL_INTEGER,	_T("INTEGER"),								/* SEAQUEST SQL_NAMED */ SQL_UNNAMED,	SQL_TRUE},
		{ 	SQL_TRUE,		SQL_WCHAR,				0,					/* SEAQUEST 0 */ 18,	SQL_FALSE,		/* SEAQUEST 13 */18,			/* SEAQUEST _T("") */ _T("VARCHAR CHARACTER SET ISO88591"),	/*PROJDESC*/_T("--"),		SQL_NO_NULLS,	0,				/* SEAQUEST 18 */36,			SQL_PARAM_INPUT,	0,			0,		SQL_WCHAR,		/* SEAQUEST _T("VARCHAR") */ _T("NCHAR"),	/* SEAQUEST SQL_NAMED */ SQL_UNNAMED,	SQL_TRUE},
		{ 	SQL_FALSE,		SQL_TYPE_DATE,			SQL_CODE_DATE,		0,						SQL_FALSE,		10,								_T(""),														/*START_DATE*/_T("--"),		SQL_NO_NULLS,	0,				6,								SQL_PARAM_INPUT,	0,			0,		SQL_DATETIME,	_T("DATE"),									/* SEAQUEST SQL_NAMED */ SQL_UNNAMED,	SQL_TRUE},
		{ 	SQL_FALSE,		SQL_TYPE_TIMESTAMP,		SQL_CODE_TIMESTAMP,	/* SEAQUEST 0 */ 6,		SQL_FALSE,		/* SEAQUEST 19 */ 26,			_T(""),														/*SHIP_TIMESTAMP*/_T("--"),	SQL_NO_NULLS,	0,				16,								SQL_PARAM_INPUT,	6,			0,		SQL_DATETIME,	_T("TIMESTAMP"),							/* SEAQUEST SQL_NAMED */ SQL_UNNAMED,	SQL_TRUE}
	};

	APP_REC APP_ExpData[MAX_BOUND_PARAM] =
	{
		//ConciseType	    DataPtr		IntervalCode	IntervalPrecision	IndicatorPtr			Length				PrecRadix											OctetLength		OctetLengthPtr		Precision	Scale	Type
	    {SQL_C_SSHORT,	    NULL,       0,              0,                  NULL,					0,					0,													0,              NULL,               0,          0,	    SQL_C_SSHORT},		
		{SQL_C_SSHORT,	    NULL,       0,              0,                  NULL,					0,					0,													0,              NULL,               0,          0,	    SQL_C_SSHORT},
#ifdef UNICODE
		{SQL_C_TCHAR,	    NULL,       0,              0,                  NULL,   /* SEAQUEST 13 */MAX_BUFFER_LEN,    0,					/* SEAQUEST MAX_BUFFER_LEN */MAX_BUFFER_LEN*2,	NULL,				0,			0,		SQL_C_TCHAR},	
#else	
		{SQL_C_TCHAR,	    NULL,       0,              0,                  NULL,   /* SEAQUEST 13 */MAX_BUFFER_LEN,    0,					/* SEAQUEST MAX_BUFFER_LEN */MAX_BUFFER_LEN,	NULL,				0,			0,		SQL_C_TCHAR},		
#endif
		{SQL_C_TYPE_DATE,   NULL,	    SQL_CODE_DATE,	0,                  NULL,					10,					0,													0,              NULL,               0,          0,	    SQL_DATETIME},		
		{SQL_C_TYPE_TIMESTAMP,NULL,     SQL_CODE_TIMESTAMP,	0,              NULL,   /* SEAQUEST 19 */0,					0,													0,              NULL,               0,          0,	    SQL_DATETIME}		
	};

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLSetGetDescFields"), charset_file);
	if (var_list == NULL) return FAILED;

	DrpTabProject = var_mapping(_T("SQLSetGetDescFields_DrpTabProject"), var_list);
	CrtTabProject = var_mapping(_T("SQLSetGetDescFields_CrtTabProject"), var_list);
	InsTabProject = var_mapping(_T("SQLSetGetDescFields_InsTabProject"), var_list);
	SelTabProject = var_mapping(_T("SQLSetGetDescFields_SelTabProject"), var_list);

/*
	_tcscpy(IRD_ExpData[0].irdBaseColumnName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_0"), var_list));
	_tcscpy(IRD_ExpData[0].irdBaseTableName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_0"), var_list));
	_tcscpy(IRD_ExpData[0].irdLabel, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdLabel_0"), var_list));
	_tcscpy(IRD_ExpData[0].irdName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdName_0"), var_list));
	_tcscpy(IRD_ExpData[0].irdTableName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdTableName_0"), var_list));

	_tcscpy(IRD_ExpData[1].irdBaseColumnName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_1"), var_list));
	_tcscpy(IRD_ExpData[1].irdBaseTableName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_1"), var_list));
	_tcscpy(IRD_ExpData[1].irdLabel, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdLabel_1"), var_list));
	_tcscpy(IRD_ExpData[1].irdName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdName_1"), var_list));
	_tcscpy(IRD_ExpData[1].irdTableName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdTableName_2"), var_list));

	_tcscpy(IRD_ExpData[2].irdBaseColumnName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_2"), var_list));
	_tcscpy(IRD_ExpData[2].irdBaseTableName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_2"), var_list));
	_tcscpy(IRD_ExpData[2].irdLabel, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdLabel_2"), var_list));
	_tcscpy(IRD_ExpData[2].irdName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdName_2"), var_list));
	_tcscpy(IRD_ExpData[2].irdTableName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdTableName_2"), var_list));

	_tcscpy(IRD_ExpData[3].irdBaseColumnName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_3"), var_list));
	_tcscpy(IRD_ExpData[3].irdBaseTableName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_3"), var_list));
	_tcscpy(IRD_ExpData[3].irdLabel, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdLabel_3"), var_list));
	_tcscpy(IRD_ExpData[3].irdName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdName_3"), var_list));
	_tcscpy(IRD_ExpData[3].irdTableName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdTableName_3"), var_list));

	_tcscpy(IRD_ExpData[4].irdBaseColumnName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_4"), var_list));
	_tcscpy(IRD_ExpData[4].irdBaseTableName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_4"), var_list));
	_tcscpy(IRD_ExpData[4].irdLabel, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdLabel_4"), var_list));
	_tcscpy(IRD_ExpData[4].irdName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdName_4"), var_list));
	_tcscpy(IRD_ExpData[4].irdTableName, var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdTableName_4"), var_list));
	
	_tcscpy(IPD_ExpData[0].ipdName, var_mapping(_T("SQLSetGetDescFields_IPD_ExpData_ipdName_0"), var_list));
	_tcscpy(IPD_ExpData[1].ipdName, var_mapping(_T("SQLSetGetDescFields_IPD_ExpData_ipdName_1"), var_list));
	_tcscpy(IPD_ExpData[2].ipdName, var_mapping(_T("SQLSetGetDescFields_IPD_ExpData_ipdName_2"), var_list));
	_tcscpy(IPD_ExpData[3].ipdName, var_mapping(_T("SQLSetGetDescFields_IPD_ExpData_ipdName_3"), var_list));
	_tcscpy(IPD_ExpData[4].ipdName, var_mapping(_T("SQLSetGetDescFields_IPD_ExpData_ipdName_4"), var_list));	
*/
	IRD_ExpData[0].irdBaseColumnName = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_0"), var_list);
	IRD_ExpData[0].irdBaseTableName  = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_0"), var_list);
	IRD_ExpData[0].irdLabel          = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdLabel_0"), var_list);
	IRD_ExpData[0].irdName           = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdName_0"), var_list);
	IRD_ExpData[0].irdTableName      = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdTableName_0"), var_list);

	IRD_ExpData[1].irdBaseColumnName = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_1"), var_list);
	IRD_ExpData[1].irdBaseTableName	 = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_1"), var_list);
	IRD_ExpData[1].irdLabel			 = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdLabel_1"), var_list);
	IRD_ExpData[1].irdName			 = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdName_1"), var_list);
	IRD_ExpData[1].irdTableName		 = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdTableName_2"), var_list);
	
	IRD_ExpData[2].irdBaseColumnName = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_2"), var_list);
	IRD_ExpData[2].irdBaseTableName	 = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_2"), var_list);
	IRD_ExpData[2].irdLabel			 = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdLabel_2"), var_list);
	IRD_ExpData[2].irdName			 = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdName_2"), var_list);
	IRD_ExpData[2].irdTableName		 = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdTableName_2"), var_list);
	
	IRD_ExpData[3].irdBaseColumnName = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_3"), var_list);
	IRD_ExpData[3].irdBaseTableName  = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_3"), var_list);
	IRD_ExpData[3].irdLabel          = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdLabel_3"), var_list);
	IRD_ExpData[3].irdName           = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdName_3"), var_list);
	IRD_ExpData[3].irdTableName      = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdTableName_3"), var_list);
	
	IRD_ExpData[4].irdBaseColumnName = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseColumnName_4"), var_list);
	IRD_ExpData[4].irdBaseTableName  = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdBaseTableName_4"), var_list);
	IRD_ExpData[4].irdLabel          = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdLabel_4"), var_list);
	IRD_ExpData[4].irdName           = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdName_4"), var_list);
	IRD_ExpData[4].irdTableName      = var_mapping(_T("SQLSetGetDescFields_IRD_ExpData_irdTableName_4"), var_list);
	
	IPD_ExpData[0].ipdName			 = var_mapping(_T("SQLSetGetDescFields_IPD_ExpData_ipdName_0"), var_list);
	IPD_ExpData[1].ipdName			 = var_mapping(_T("SQLSetGetDescFields_IPD_ExpData_ipdName_1"), var_list);
	IPD_ExpData[2].ipdName			 = var_mapping(_T("SQLSetGetDescFields_IPD_ExpData_ipdName_2"), var_list);
	IPD_ExpData[3].ipdName			 = var_mapping(_T("SQLSetGetDescFields_IPD_ExpData_ipdName_3"), var_list);
	IPD_ExpData[4].ipdName			 = var_mapping(_T("SQLSetGetDescFields_IPD_ExpData_ipdName_4"), var_list);
 
 // ================================================================================================================
 //		begin common test setup 
 //==================================================================================================================
	
	// begin by marking the start of  test in the log file
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => SQLSetDescField and SQLGetDescField.\n"));
	TEST_INIT;


	TESTCASE_BEGIN("Begin setup.\n");
	//establish a connection to the DSN or test fails here
	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect as ODBC3.0 application.\n"));
		TEST_FAILED;
		TEST_RETURN;
	}
	
	//get env, db and stmt handles already allocated at connection time.
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;


	//alloc statement handle or fail here. (pTestInfo ->hstmt; //this is not allocated in FullConnectWithOptionsVer3)
	returncode = SQLAllocHandle(SQL_HANDLE_STMT,(SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	

	//alloc another statement handle 
	returncode = SQLAllocHandle(SQL_HANDLE_STMT,(SQLHANDLE)hdbc, &hstmt1);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	//fill up the first 4 elements of the array of hDesc with implicit Descriptor handles
	for (i=0; i<MAX_DESC_TYPES; i++)
	{

		returncode = SQLGetStmtAttr(hstmt, DescTypes[i], &(hDesc[i]), 0, NULL);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			LogMsg(ERRMSG,_T("Cannot allocate descriptor: IRD.\n"));
			TEST_FAILED;
			TEST_RETURN;
		}
	}

	// fill up the next two elements with Explicit descriptor handles
	for (i= MAX_DESC_TYPES; i< MAX_DESC_HANDLES; i++)
	{
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
	returncode = SQLSetStmtAttr(hstmt1, SQL_ATTR_APP_PARAM_DESC, (SQLPOINTER)hDesc[4], SQL_IS_POINTER);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr: explicit APD"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		LogMsg(ERRMSG, _T("Cannot set Explicit APD for statement.\n"));
		TEST_FAILED;
		TEST_RETURN;
	}
	
	returncode = SQLSetStmtAttr(hstmt1, SQL_ATTR_APP_PARAM_DESC, (SQLPOINTER)hDesc[5], SQL_IS_POINTER);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr: explicit ARD"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		LogMsg(ERRMSG, _T("Cannot set Explicit ARD for statement.\n"));
		TEST_FAILED;
		TEST_RETURN;
	}

	TESTCASE_END;


	

 //===========================================================================================================
 //		Tests for Descriptor Fields Default Values: Header Fields
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
					//initialize buffer
					AllocTypeValue = 0; //valid values are 1 and 2
					//get default field value
					returncode = SQLGetDescField(hDesc[i], 0, SQL_DESC_ALLOC_TYPE, &AllocTypeValue, 0, NULL);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						TEST_FAILED;
						TEST_RETURN;
					}
					switch (i)
					{
						case APD:				// APD
							TESTCASE_BEGIN("SQL_DESC_ALLOC_TYPE: APD Default values.\n");
							if (AllocTypeValue != SQL_DESC_ALLOC_AUTO)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_ALLOC_TYPE (case APD): expected SQL_DESC_ALLOC_AUTO and found %d, Line=%d\n"),  AllocTypeValue, __LINE__);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;
						case IPD:				// IPD
							TESTCASE_BEGIN("SQL_DESC_ALLOC_TYPE: IPD Default values.\n");
							if (AllocTypeValue != SQL_DESC_ALLOC_AUTO)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_ALLOC_TYPE (case IPD): expected SQL_DESC_ALLOC_AUTO and found %d, Line=%d\n"), AllocTypeValue, __LINE__);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;		
						case ARD:				// ARD
							TESTCASE_BEGIN("SQL_DESC_ALLOC_TYPE: ARD Default values.\n");
							if (AllocTypeValue != SQL_DESC_ALLOC_AUTO)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_ALLOC_TYPE (case ARD): expected SQL_DESC_ALLOC_AUTO and found %d, Line=%d\n"), AllocTypeValue,__LINE__);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;
						case IRD:				// IRD
							TESTCASE_BEGIN("SQL_DESC_ALLOC_TYPE: IRD Default values.\n");
							if (AllocTypeValue != SQL_DESC_ALLOC_AUTO)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_ALLOC_TYPE (case IRD): expected SQL_DESC_ALLOC_AUTO and found %d, Line=%d\n"), AllocTypeValue,__LINE__);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;
						case ExAPD: 			// Explicit APD
							TESTCASE_BEGIN("SQL_DESC_ALLOC_TYPE: Explicit APD Default values.\n");
							if (AllocTypeValue != SQL_DESC_ALLOC_USER)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_ALLOC_TYPE (case ExAPD): expected SQL_DESC_ALLOC_USER and found %d, Line=%d\n"), AllocTypeValue,__LINE__);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;
						case ExARD: 			// Explicit ARD
							TESTCASE_BEGIN("SQL_DESC_ALLOC_TYPE: Explicit ARD Default values.\n");
							if (AllocTypeValue != SQL_DESC_ALLOC_USER)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_ALLOC_TYPE (case ExARD): expected SQL_DESC_ALLOC_USER and found %d,\n"), AllocTypeValue,__LINE__);
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
							//initialize buffer
							ArraySize = 0; //valid values are 1 and greater
							//get default field value
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &ArraySize, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								break;	//get out: go to next test
							}

							if (ArraySize != 1)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_ARRAY_SIZE (case APD): expected 1 and found %d.\n"),  ArraySize);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;

						case ARD:
							TESTCASE_BEGIN("SQL_DESC_ARRAY_SIZE: ARD Default values.\n");
							//initialize buffer
							ArraySize = 0; //valid values are 1 and greater
							//get default field value
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &ArraySize, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								break;	//get out: go to next test
							}

							if (ArraySize != 1)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_ARRAY_SIZE (case ARD): expected 1 and found %d.\n"), ArraySize);
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
					TESTCASE_BEGIN("SQL_DESC_ARRAY_SIZE: Default values.\n");
					//initialize buffer
					ArrayStatusPtr = NULL; //valid values not null
					//get default field value
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
						LogMsg(ERRMSG,_T("SQL_DESC_ARRAY_STATUS_PTR : expected NULL and found %p.\n"),  ArrayStatusPtr);
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
							//get default field value
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &BindOffsetPtr, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								break;
							}

							if (BindOffsetPtr != NULL)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_BIND_OFFSET_PTR (case ARD): expected NULL and found %p.\n"),  BindOffsetPtr);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;

						case APD:
							TESTCASE_BEGIN("SQL_DESC_BIND_OFFSET_PTR: APD Default values.\n");
							//get default field value
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &BindOffsetPtr, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								break;
							}

							if (BindOffsetPtr != NULL)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_BIND_OFFSET_PTR (case APD): expected NULL and found %p.\n"),  BindOffsetPtr);
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
							//get default field value
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &BindType, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								break;
							}

							if (BindType != SQL_BIND_BY_COLUMN)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_BIND_TYPE (case ARD): expected SQL_BIND_BY_COLUMN and found %d.\n"),  BindType);
								TEST_FAILED;
							
							}
							TESTCASE_END;
							break;

						case APD:
							TESTCASE_BEGIN("SQL_DESC_BIND_TYPE: APD Default values.\n");
							//get default field value
							returncode = SQLGetDescField(hDesc[i], 0, DescFields[FieldIndex], &BindType, 0, NULL);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
								break;
							}

							if (BindType != SQL_BIND_BY_COLUMN)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_BIND_TYPE (case APD): expected SQL_BIND_BY_COLUMN and found %d.\n"),  BindType);
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
					//getting of the field is common, so begin testcase here
					TESTCASE_BEGIN("SQL_DESC_COUNT: Default values.\n");
					//get default field value
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
						LogMsg(ERRMSG,_T("SQL_DESC_COUNT (case %d): expected 0 and found %d.\n"),  i, DescCount);
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
						case IRD: ;		//same as next case

						case IPD:
							//getting of the field is common, so begin testcase here
							TESTCASE_BEGIN("SQL_DESC_ROWS_PROCESSED_PTR: Default values.\n");
							//get default field value
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
								LogMsg(ERRMSG,_T("SQL_DESC_ROWS_PROCESSED_PTR (case %d): expected NULL and found %p.\n"),  i, RowsProcessedPtr);
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
				LogMsg(NONE, _T("DescFields[%d]: no valid default values.\n"), i); //do nothing 


		} //finish individual cases for all header descriptor fields
	}//end looping through all header descriptor fields

//===========================================================================================================
 //		populate Desc Fields: testing the record descriptor fields possible only after populating them.
 //==============================================================================================================
	
	TESTCASE_BEGIN("Setup for descriptor record fields.\n");
	//populate the IRDs
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
 //		Tests for Descriptor Fields Default Values: Record Fields
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
								LogMsg(ERRMSG,_T("SQL_DESC_AUTO_UNIQUE_VALUE (case %d): expected SQL_TRUE or SQL_FALSE and found %d.\n"),  i, AutoUniqueValue);
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
								LogMsg(ERRMSG,_T("SQL_DESC_CONCISE_TYPE (case %d): expected SQL_C_DEFAULT and found %d.\n"),  i, ConciseType);
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
								LogMsg(ERRMSG,_T("SQL_DESC_TYPE (case %d): expected SQL_C_DEFAULT and found %d.\n"),  i, Type);
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
							/* SEAQUEST 
							if ( ParameterType != SQL_PARAM_INPUT)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_PARAMETER_TYPE (case %d): expected SQL_PARAM_INPUT and found %d, (FieldIndex: %d) line %d\n"),  i, ParameterType, FieldIndex, __LINE__);
								TEST_FAILED;
								TESTCASE_END;
								break;
							}	
							*/
							/* SEAQUEST new */
							if ( ParameterType > 0)
							{
								LogMsg(ERRMSG,_T("SQL_DESC_PARAMETER_TYPE (case %d): expected NOTHING and found %d, (FieldIndex: %d) line %d\n"),  i, ParameterType, FieldIndex, __LINE__);
								TEST_FAILED;
								TESTCASE_END;
								break;			
							}
							/* end of SEAQUEST new */
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
 
 //		Cleanup ------------------------------------------------
 
	//free explicit descriptors
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
 //		Tests for Descriptor Fields: Set and Get
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
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabProject,SQL_NTS);


	//create table
	SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLExecDirect(hstmt,(SQLTCHAR*) CrtTabProject,SQL_NTS);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		LogMsg(ERRMSG,_T("Cannot create table.\n"));
		TEST_FAILED;
		TEST_RETURN;
	}



	//prepare stmt
	SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLPrepare(hstmt, (SQLTCHAR*)InsTabProject, SQL_NTS);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		LogMsg(ERRMSG,_T("Cannot prepare stmt.\n"));
		TEST_FAILED;
		TEST_RETURN;
	}


	//specify data
	apdProjCode					= 11;
	apdEmpNum					= 1234;
	_tcscpy((TCHAR*)apdProjDesc, _T("ODBC 3.0 TEST"));
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

	//get Apd handle
	returncode = SQLGetStmtAttr(hstmt, SQL_ATTR_APP_PARAM_DESC, &hDesc[0], 0, NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
	{
		LogMsg(ERRMSG,_T("Cannot allocate descriptor: APD.\n"));
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_RETURN;
	}

	//Set APD DescCount to number of bound param
	DescCount = MAX_BOUND_PARAM;
	returncode = SQLSetDescField(hDesc[0], 0, SQL_DESC_COUNT, (SQLPOINTER)DescCount, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_COUNT = MAX_BOUND_PARAM"))	
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	//assign field values
	for (i=1; i <= MAX_BOUND_PARAM; i++)
	{
		//set SQL_DESC_TYPE
		returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_TYPE, (SQLPOINTER)APP_ExpData[i-1].appType, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_TYPE "))	
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		//set SQL_DESC_CONCISE_TYPE
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
		    case SQL_C_TYPE_TIMESTAMP:
			    //set SQL_DESC_DATETIME_INTERVAL_CODE
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_DATETIME_INTERVAL_CODE, (SQLPOINTER)APP_ExpData[i-1].appDatetimeIntervalCode, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATETIME_INTERVAL_CODE"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    break;

		    case SQL_C_TCHAR:
/* SEAQUEST1 new */
				//set SQL_DESC_LENGTH : ignored for all except TCHAR data
//				LogMsg(NONE,_T("SQLSetDescField to set attribute SQL_DESC_LENGTH for descriptor hDesc[0] when I = %d \n"), i);
				LogMsg(NONE,_T("SQLSetDescField to set attribute SQL_DESC_LENGTH for descriptor hDesc[0] when I = %d and SQL_DESC_LENGTH = %d \n"), i, MAX_BUFFER_LEN);
				returncode = SQLSetDescFieldW(hDesc[0], (SQLSMALLINT)i, SQL_DESC_LENGTH, (SQLPOINTER)MAX_BUFFER_LEN, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_LENGTH"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
/* End of SEAQUEST1 new */
			    	//set SQL_DESC_OCTET_LENGTH : ignored for all except TCHAR data
				LogMsg(NONE,_T("SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH for descriptor hDesc[0] when I = %d and SQL_DESC_OCTET_LENGTH = %d\n"), i, MAX_BUFFER_LEN);
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
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &apdProjCode,0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogMsg(ERRMSG, _T("Setting DATA_PTR [%d]\n"), (i-1));
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    //set SQL_DESC_OCTET_LENGTH_PTR
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR,&ipdProjCode, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }

			    //set SQL_DESC_INDICATOR_PTR to same as SQL_DESC_OCTET_LENGTH_PTR (SQL_NTS)
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
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_DATA_PTR,&apdEmpNum,0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogMsg(ERRMSG, _T("Setting DATA_PTR [%d]\n"), (i-1));
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    //set SQL_DESC_OCTET_LENGTH_PTR
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR,&ipdEmpNum, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }

			    //set SQL_DESC_INDICATOR_PTR to same as SQL_DESC_OCTET_LENGTH_PTR (SQL_NTS)
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
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &apdProjDesc,sizeof(apdProjDesc));	//SQL_NTS, sizeof(apdProjDesc), MAX_BUFFER_LEN
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogMsg(ERRMSG, _T("Setting DATA_PTR [%d]\n"), (i-1));
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    //set SQL_DESC_OCTET_LENGTH_PTR
			    #ifdef _LP64
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR,&ipdProjDesc64, 0);
			    #else
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
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &apdStartDate,0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogMsg(ERRMSG, _T("Setting DATA_PTR [%d]\n"), (i-1));
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    //set SQL_DESC_OCTET_LENGTH_PTR
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR,&ipdStartDate, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }

			    //set SQL_DESC_INDICATOR_PTR to same as SQL_DESC_OCTET_LENGTH_PTR (SQL_NTS)
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
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &apdShipTimestamp,0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
			    {
				    LogMsg(ERRMSG, _T("Setting DATA_PTR [%d]\n"), (i-1));
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    //set SQL_DESC_OCTET_LENGTH_PTR
			    returncode = SQLSetDescField(hDesc[0], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR,&ipdShipTimestamp, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }

			    //set SQL_DESC_INDICATOR_PTR to same as SQL_DESC_OCTET_LENGTH_PTR (SQL_NTS)
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
	returncode = SQLGetStmtAttr(hstmt, SQL_ATTR_IMP_PARAM_DESC, &hDesc[1], 0, NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		LogMsg(ERRMSG,_T("Cannot allocate descriptor: IPD.\n"));
		FullDisconnect(pTestInfo);
		TEST_RETURN;
	}

	//Set IPD DescCount to number of bound param
	DescCount = MAX_BOUND_PARAM;
	returncode = SQLSetDescField(hDesc[1], 0, SQL_DESC_COUNT, (SQLPOINTER)DescCount, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_COUNT = MAX_BOUND_PARAM"))	
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	//assign field values
	}
	for (i=1; i <= MAX_BOUND_PARAM; i++)
	{
		//set SQL_DESC_TYPE
		returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_TYPE, (SQLPOINTER)IPD_ExpData[i-1].ipdType, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_TYPE "))	
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		//set SQL_DESC_CONCISE_TYPE
		returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_CONCISE_TYPE, (SQLPOINTER)IPD_ExpData[i-1].ipdConciseType, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_CONCISE_TYPE"))	
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		//set datetime_interval_code if required
		switch (APP_ExpData[i].appType)
		{
		    case SQL_DATETIME:
			    //set SQL_DESC_DATETIME_INTERVAL_CODE
			    returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_DATETIME_INTERVAL_CODE, (SQLPOINTER)IPD_ExpData[i-1].ipdDatetimeIntervalCode, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATETIME_INTERVAL_CODE"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
			    break;
		    case SQL_TYPE_TIMESTAMP:
			    //set SQL_DESC_DATETIME_INTERVAL_CODE
			    returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_DATETIME_INTERVAL_CODE, (SQLPOINTER)IPD_ExpData[i-1].ipdDatetimeIntervalCode, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATETIME_INTERVAL_CODE"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }

			    break;
			    /* SEAQUEST1 case SQL_WCHAR: */
//		     case SQL_C_WCHAR:
		     case SQL_C_TCHAR:
			    //set SQL_DESC_LENGTH : ignored for all except TCHAR data
			    Length = MAX_BUFFER_LEN;
			    LogMsg(NONE,_T("SQLSetDescField to set attribute SQL_DESC_LENGTH for descriptor hDesc[1] when I = %d and SQL_DESC_LENGTH = %d\n"), i, Length);
			    returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_LENGTH, (SQLPOINTER)Length, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_LENGTH"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
/* SEAQUEST1 new */
			    //set SQL_DESC_OCTET_LENGTH : ignored for all except TCHAR data
//			    LogMsg(NONE,_T("SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH for descriptor hDesc[1] when I = %d \n"), i);
			    LogMsg(NONE,_T("SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH for descriptor hDesc[1] when I = %d and SQL_DESC_OCTET_LENGTH = %d\n"), i, MAX_BUFFER_LEN);
			    returncode = SQLSetDescFieldW(hDesc[1], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH, (SQLPOINTER)MAX_BUFFER_LEN, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField:SQL_DESC_OCTET_LENGTH"))
			    {
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
			    }
/* end of SEAQUEST1 new */
			    break;
		    case SQL_INTERVAL:
			    //set SQL_DESC_DATETIME_INTERVAL_PRECISION
			    returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_DATETIME_INTERVAL_PRECISION, (SQLPOINTER)IPD_ExpData[i-1].ipdDatetimeIntervalPrecision, 0);
			    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATETIME_INTERVAL_PRECISION"))	
			    {
				    LogAllErrorsVer3(henv,hdbc,hstmt);
				    FullDisconnect(pTestInfo);
				    TEST_FAILED;
				    TEST_RETURN;
			    }
		    default: break;
		}//end switch

		
		//set SQL_DESC_PRECISION
		returncode = SQLSetDescField(hDesc[1], (SQLSMALLINT)i, SQL_DESC_PRECISION, (SQLPOINTER)IPD_ExpData[i-1].ipdPrecision, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_PRECISION"))	
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}

		//set SQL_DESC_SCALE to 0
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
	returncode = SQLExecute(hstmt);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		LogMsg(ERRMSG,_T("Cannot insert row. Expected: SQL_SUCCESS, Actual: %d\n"), returncode);
		TEST_FAILED;
		TEST_RETURN;
	}

	//allocate another stmt handle for select operation
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt1);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	//select from a table to populate the IRD
	returncode = SQLExecDirect(hstmt1, (SQLTCHAR*)SelTabProject,SQL_NTS);
	if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
	{

/*		//bind col
//-------------------------------------------------------------------------------------------------------------
		SQLBindCol(hstmt1, 1, SQL_C_SSHORT, &ardProjCode, 0, &irdProjCode);
		SQLBindCol(hstmt1, 2, SQL_C_SSHORT, &ardEmpNum, 0, &irdEmpNum);
		SQLBindCol(hstmt1, 3, SQL_C_TCHAR, ardProjDesc, MAX_BUFFER_LEN, &irdProjDesc);
		SQLBindCol(hstmt1, 4, SQL_C_TYPE_DATE, &ardStartDate, 0, &irdStartDate);
		SQLBindCol(hstmt1, 5, SQL_C_TYPE_TIMESTAMP, &ardShipTimestamp, 0, &irdShipTimestamp);
//---------------------------------------------------------------------------------------------------------------
*/
		//***BIND by using SetDescField: populates the ARD
		
		//get Ard handle
		returncode = SQLGetStmtAttr(hstmt1, SQL_ATTR_APP_ROW_DESC, &hDesc[2], 0, NULL);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt1);
			LogMsg(ERRMSG,_T("Cannot allocate descriptor: ARD.\n"));
			FullDisconnect(pTestInfo);
			TEST_RETURN;
		}

		//set Desc Count
		DescCount = MAX_BOUND_PARAM;
		returncode = SQLSetDescField(hDesc[2], 0, SQL_DESC_COUNT, (SQLPOINTER)DescCount, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_COUNT = MAX_BOUND_PARAM"))	
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}

		//assign values
		for (i=1; i <= MAX_BOUND_PARAM; i++)
		{
			//set SQL_DESC_TYPE
			returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_TYPE, (SQLPOINTER)APP_ExpData[i-1].appType, 0);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_TYPE "))	
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
				FullDisconnect(pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			//set SQL_DESC_CONCISE_TYPE
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
			// SEAQUEST1 case SQL_C_TYPE_DATE:
			// SEAQUEST1 case SQL_C_TYPE_TIMESTAMP:
				/* SEAQUEST1 new */
			case SQL_DATETIME:
				//set SQL_DESC_DATETIME_INTERVAL_CODE
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATETIME_INTERVAL_CODE, (SQLPOINTER)APP_ExpData[i-1].appDatetimeIntervalCode, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATETIME_INTERVAL_CODE"))	
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				break;

			case SQL_C_TCHAR:
				//set SQL_DESC_LENGTH : ignored for all except TCHAR data
				LogMsg(NONE,_T("SQLSetDescField to set attribute SQL_DESC_LENGTH for descriptor hDesc[2] when I = %d and SQL_DESC_LENGTH = %d\n"), i, MAX_BUFFER_LEN);
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_LENGTH, (SQLPOINTER)MAX_BUFFER_LEN, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_LENGTH"))	
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}

#if 0 /* SEAQUEST1 */
				//set SQL_DESC_OCTET_LENGTH_PTR
				_tcslen = SQL_NTS;
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH_PTR, &_tcslen, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH_PTR"))	
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				//set SQL_DESC_INDICATOR_PTR to the same ptr as above
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &_tcslen, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
#endif /* SEAQUEST1 */
/* SEAQUEST1 new */
				//set SQL_DESC_OCTET_LENGTH : ignored for all except CHAR data
//				LogMsg(NONE,_T("SQLSetDescField to set attrbute SQL_DESC_OCTET_LENGTH for descriptor hDesc[2] when I = %d \n"), i);
				LogMsg(NONE,_T("SQLSetDescField to set attribute SQL_DESC_OCTET_LENGTH for descriptor hDesc[2] when I = %d and SQL_DESC_OCTET_LENGTH = %d\n"), i, MAX_BUFFER_LEN);
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH, (SQLPOINTER)MAX_BUFFER_LEN, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_OCTET_LENGTH"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
/* end of SEAQUSET1 new */
				break;

			case SQL_C_SSHORT:
				//set SQL_DESC_INDICATOR_PTR to value 0 for all other types
				Indicator = 0;
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_INDICATOR_PTR, &Indicator, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_INDICATOR_PTR"))	
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
#if 0 /* SEAQUEST1 */
			returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_OCTET_LENGTH, (SQLPOINTER)MAX_BUFFER_LEN, 0);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField:SQL_DESC_OCTET_LENGTH"))	
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
				FullDisconnect(pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
#endif /* SEAQUEST1 */

			switch (i)		//to set data values
			{
			case 1:
				//set SQL_DESC_DATA_PTR
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &ardProjCode,0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
				{
					LogMsg(ERRMSG, _T("Setting DATA_PTR [%d]\n"), (i-1));
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				//set SQL_DESC_INDICATOR_PTR 
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i,SQL_DESC_INDICATOR_PTR, &irdProjCode, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_INDICATOR_PTR"))	
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				//set SQL_DESC_OCTET_LENGTH_PTR 
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
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &ardEmpNum,0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
				{
					LogMsg(ERRMSG, _T("Setting DATA_PTR [%d]\n"), (i-1));
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				//set SQL_DESC_INDICATOR_PTR 
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i,SQL_DESC_INDICATOR_PTR, &irdEmpNum, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_INDICATOR_PTR"))	
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				//set SQL_DESC_OCTET_LENGTH_PTR 
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
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, ardProjDesc,MAX_BUFFER_LEN);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
				{
					LogMsg(ERRMSG, _T("Setting DATA_PTR [%d]\n"), (i-1));
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				//set SQL_DESC_INDICATOR_PTR 
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_INDICATOR_PTR, &irdProjDesc, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_INDICATOR_PTR"))	
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				//set SQL_DESC_OCTET_LENGTH_PTR 
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
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &ardStartDate,0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
				{
					LogMsg(ERRMSG, _T("Setting DATA_PTR [%d]\n"), (i-1));
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				//set SQL_DESC_INDICATOR_PTR 
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_INDICATOR_PTR, &irdStartDate, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_INDICATOR_PTR"))	
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				//set SQL_DESC_OCTET_LENGTH_PTR 
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
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_DATA_PTR, &ardShipTimestamp,0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_DATA_PTR"))	
				{
					LogMsg(ERRMSG, _T("Setting DATA_PTR [%d]\n"), (i-1));
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				//set SQL_DESC_INDICATOR_PTR 
				returncode = SQLSetDescField(hDesc[2], (SQLSMALLINT)i, SQL_DESC_INDICATOR_PTR, &irdShipTimestamp, 0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetDescField: SQL_DESC_INDICATOR_PTR"))	
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					FullDisconnect(pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				//set SQL_DESC_OCTET_LENGTH_PTR 
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
			returncode = SQLFetch(hstmt1);
			if (returncode != SQL_SUCCESS /* SEAQUEST */ && returncode != SQL_NO_DATA_FOUND)
			{
				LogAllErrorsVer3(henv,hdbc,hstmt1);
				LogMsg(ERRMSG,_T("Cannot fetch data. returncode=%d line %d\n"), returncode, __LINE__);
				// This is where the 1st error is coming from
				break;
			}
			/* SEAQUEST2 new */ 
			// SEAQUEST2 if (returncode == SQL_SUCCESS)
			else if (returncode == SQL_SUCCESS)
			{
//				LogMsg(SHORTTIMESTAMP+LINEAFTER, _T(" ProjCode = %d\t EmpNum = %d\n"), ardProjCode, ardEmpNum);
                                LogMsg(SHORTTIMESTAMP+LINEAFTER, _T(" ProjCode = %d\t EmpNum = %d\t ProjDesc = %s\t StartDate = %d-%02d-%02d\t ShipTimestamp = %d-%02d-%02d %02d:%02d:%02d\n"), 
				ardProjCode, ardEmpNum,ardProjDesc,
				ardStartDate.year,ardStartDate.month,ardStartDate.day,
				ardShipTimestamp.year, ardShipTimestamp.month, ardShipTimestamp.day, ardShipTimestamp.hour, ardShipTimestamp.minute, ardShipTimestamp.second);
			}
			/* SEAQUEST2 * new */
			else
			{
				break;
			}
			/* end of SEAQUEST2 new */
		}
	
	}//end if

	TESTCASE_END;


	//-----------------------------------------------------------------------------------------------------
	// begin tests for APD,IPD, ARD, IRD
	// the above setup populates the the descriptors
	//------------------------------------------------------------------------------------------------------
	
	//LogMsg(NONE,_T("Verifying (Get_tests) all populated descriptors\n"));

	//get Ird handle : others are already allocated
	returncode = SQLGetStmtAttr(hstmt1, SQL_ATTR_IMP_ROW_DESC, &hDesc[3], 0, NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		LogMsg(ERRMSG,_T("Cannot allocate descriptor: IRD.\n"));
		//FullDisconnect(pTestInfo);
		TEST_RETURN;
	}

	// loop through all types of desc: APD, IPD, ARD, IRD
	for (i= 0; i < MAX_DESC_TYPES; i++)	//test each type of Desc
	{
			//check Desc Count
			//initialize Buffer
			DescCount = 0; //valid default
			returncode = SQLGetDescField(hDesc[i], 0, SQL_DESC_COUNT, &DescCount, 0, NULL);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
			{
				LogMsg(ERRMSG, _T("Cannot get SQL_DESC_COUNT\n"));
				LogAllErrorsVer3(henv,hdbc,hstmt1);
				LogAllErrorsVer3(henv,hdbc,hstmt);
				//FullDisconnect(pTestInfo);
				TEST_RETURN;			
			}

			if (DescCount != MAX_BOUND_PARAM)	//descriptor did not get populated
			{
				LogMsg(ERRMSG, _T("Incorrect SQL_DESC_COUNT for hDesc[%d]: expected %d and got %d\n"), i, MAX_BOUND_PARAM, DescCount);				
				//FullDisconnect(pTestInfo);				
				TEST_RETURN;
			}
			else	//(success) test
			{	//begin tests
				switch (i)
				{
					case ARD:
						// this case is the same as next (APD): let fall to next case;

					case APD:
						
						for (j = 1; j <= DescCount; j++) //iterate through all records
						{
							//LogMsg(NONE, _T("*************************************************\n"));
							//LogMsg(NONE, _T("Testing values of APP hDesc[%d]: param %d\n"), i,j);
							//LogMsg(NONE, _T("*************************************************\n"));
							for(FieldIndex = 0; FieldIndex < MAX_DESC_FIELDS  ; FieldIndex++)
							{
								//LogMsg(NONE,_T("SQLGetDescField : verifying populated IPD values.\n"));
								switch (DescFields[FieldIndex])
								{
								case SQL_DESC_CONCISE_TYPE:
									TESTCASE_BEGIN("APP: SQL_DESC_CONCISE_TYPE\n");
									//initialize buffer
									ConciseType = 0; //initialized invalid value											
									//get value
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, SQL_DESC_CONCISE_TYPE, &ConciseType, SQL_IS_SMALLINT, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, _T("Failed to get APP Field Value SQL_DESC_CONCISE_TYPE\n"));
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									//check value
									if (ConciseType == APP_ExpData[j-1].appConciseType) 
									{
										//LogMsg(NONE, _T("ConciseType = %d\n"), ConciseType);
									}
									else
									{
										LogMsg(ERRMSG, _T("Expected ConciseType %d and got %d, Line %d\n"), APP_ExpData[j-1].appConciseType, ConciseType,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									//LogMsg(NONE, _T("ConciseType = %d\n"), ConciseType);
									break;

								case SQL_DESC_DATA_PTR:
									TESTCASE_BEGIN("APP: SQL_DESC_DATA_PTR\n");
									//initialize buffer
									DataPtr = NULL; //initialized invalid value											
									//get value
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, SQL_DESC_DATA_PTR, &DataPtr, SQL_IS_POINTER, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, _T("Failed to get APP Field Value SQL_DESC_DATA_PTR\n"));
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									//check value
									if (DataPtr != NULL) 
									{
										//LogMsg(NONE, _T("DataPtr = %p\n"), DataPtr);
									}
									else
									{
										LogMsg(ERRMSG, _T("Expected DataPtr NOT NULL and got %p, line %d\n"),  DataPtr,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									//LogMsg(NONE, _T("DataPtr = %p\n"), DataPtr);
									break;
								

								
								case SQL_DESC_DATETIME_INTERVAL_CODE:
									TESTCASE_BEGIN("APP: SQL_DESC_DATETIME_INTERVAL_CODE\n");
									//initialize buffer
									DatetimeIntervalCode = 999; //initialized invalid value											
									//get value
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &DatetimeIntervalCode, SQL_IS_SMALLINT, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, _T("Failed to get APP Field Value SQL_DESC_DATETIME_INTERVAL_CODE\n"));
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									//check value
									if (DatetimeIntervalCode == APP_ExpData[j-1].appDatetimeIntervalCode) 
									{
										//LogMsg(NONE, _T("DatetimeIntervalCode = %d\n"), DatetimeIntervalCode);
									}
									else
									{
										LogMsg(ERRMSG, _T("Expected DatetimeIntervalCode %d and got %d, line %d\n"), APP_ExpData[j-1].appDatetimeIntervalCode, DatetimeIntervalCode,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									//LogMsg(NONE, _T("DatetimeIntervalCode = %d\n"), DatetimeIntervalCode);
									break;

				
								case SQL_DESC_INDICATOR_PTR:
									TESTCASE_BEGIN("APP: SQL_DESC_INDICATOR_PTR\n");
									//initialize buffer
									IndicatorPtr = NULL; //initialized invalid value
									//get value
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, SQL_DESC_INDICATOR_PTR, IndicatorPtr, SQL_IS_POINTER, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, _T("Failed to get APP Field Value SQL_DESC_INDICATOR_PTR\n"));
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									//check value
									if (IndicatorPtr == APP_ExpData[j-1].appIndicatorPtr)
									{
										//LogMsg(NONE, _T("IndicatorPtr = %p \n"), IndicatorPtr);
									}
									else
									{
										LogMsg(ERRMSG, _T("Expected IndicatorPtr %p and got %p, line %d\n"), APP_ExpData[j-1].appIndicatorPtr, IndicatorPtr,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									//LogMsg(NONE, _T("IndicatorPtr = %p\n"), IndicatorPtr);
									break;
								
								case SQL_DESC_LENGTH:
									TESTCASE_BEGIN("APP: SQL_DESC_LENGTH\n");
									//initialize buffer
									Length = 99; //initialized invalid value											
									//get value
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, SQL_DESC_LENGTH, &Length, SQL_IS_UINTEGER, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, _T("Failed to get APP Field Value SQL_DESC_LENGTH\n"));
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									//check value
									if (Length == APP_ExpData[j-1].appLength) 
									{
										//LogMsg(NONE, _T("Length = %d\n"), Length);
									}
									else
									{
										LogMsg(ERRMSG, _T("Expected Length %d and got %d, (j:%d) line %d\n"), APP_ExpData[j-1].appLength, Length,j, __LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									//LogMsg(NONE, _T("Length = %d\n"), Length);
									break;
								
								case SQL_DESC_NUM_PREC_RADIX:
									TESTCASE_BEGIN("APP: SQL_DESC_NUM_PREC_RADIX\n");
									//initialize buffer
									NumPrecRadix = 99; //initialized invalid value											
									//get value
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, SQL_DESC_NUM_PREC_RADIX, &NumPrecRadix, SQL_IS_INTEGER, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, _T("Failed to get APP Field Value SQL_DESC_NUM_PREC_RADIX\n"));
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									//check value
									if (NumPrecRadix == APP_ExpData[j-1].appNumPrecRadix) 
									{
										//LogMsg(NONE, _T("NumPrecRadix = %d\n"), NumPrecRadix);
									}
									else
									{
										LogMsg(ERRMSG, _T("Expected NumPrecRadix %d and got %d, line %d\n"), APP_ExpData[j-1].appNumPrecRadix, NumPrecRadix,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									//LogMsg(NONE, _T("NumPrecRadix = %d\n"), NumPrecRadix);
									break;
								
								case SQL_DESC_OCTET_LENGTH:
									TESTCASE_BEGIN("APP: SQL_DESC_OCTET_LENGTH\n");
									//initialize buffer
									OctetLength = 99; //initialized invalid value											
									//get value
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, SQL_DESC_OCTET_LENGTH, &OctetLength, SQL_IS_INTEGER, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, _T("Failed to get APP Field Value SQL_DESC_OCTET_LENGTH\n"));
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									//check value
									if (OctetLength == APP_ExpData[j-1].appOctetLength) 
									{
										//LogMsg(NONE, _T("OctetLength = %d\n"), OctetLength);
									}
									else
									{
										LogMsg(ERRMSG, _T("Expected OctetLength %d and got %d, (j:%d) line %d\n"), APP_ExpData[j-1].appOctetLength, OctetLength, j, __LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									//LogMsg(NONE, _T("OctetLength = %d\n"), OctetLength);
									break;
								
								case SQL_DESC_OCTET_LENGTH_PTR:
									TESTCASE_BEGIN("APP: SQL_DESC_OCTET_LENGTH_PTR\n");
									//initialize buffer
									OctetLengthPtr = NULL; //initialized  value											
									//get value
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, SQL_DESC_OCTET_LENGTH_PTR, OctetLengthPtr, SQL_IS_POINTER, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, _T("Failed to get APP Field Value SQL_DESC_OCTET_LENGTH_PTR\n"));
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									//check value
									if (OctetLengthPtr == APP_ExpData[j-1].appOctetLengthPtr) 
									{
										//LogMsg(NONE, _T("OctetLengthPtr = %p\n"), OctetLengthPtr);
									}
									else
									{
										LogMsg(ERRMSG, _T("Expected OctetLengthPtr %p and got %p, line %d\n"), APP_ExpData[j-1].appOctetLengthPtr, OctetLengthPtr,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									//LogMsg(NONE, _T("OctetLengthPtr = %p\n"), OctetLengthPtr);
									break;
										
								case SQL_DESC_PRECISION:
									TESTCASE_BEGIN("APP: SQL_DESC_PRECISION\n");
									//initialize buffer
									Precision = 99; //initialized invalid value											
									//get value
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, SQL_DESC_PRECISION, &Precision, SQL_IS_SMALLINT, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, _T("Failed to get APP Field Value SQL_DESC_PRECISION\n"));
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									//check value
									if (Precision == APP_ExpData[j-1].appPrecision) 
									{
										//LogMsg(NONE, _T("Precision = %d\n"), Precision);
									}
									else
									{
										LogMsg(ERRMSG, _T("Expected Precision %d and got %d,line %d\n"), APP_ExpData[j-1].appPrecision, Precision,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									//LogMsg(NONE, _T("Precision = %d\n"), Precision);
									break;
								
								case SQL_DESC_SCALE:
									TESTCASE_BEGIN("APP: SQL_DESC_SCALE\n");
									//initialize buffer
									Scale = 99; //initialized invalid value											
									//get value
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j,SQL_DESC_SCALE, &Scale, SQL_IS_SMALLINT, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, _T("Failed to get APP Field Value SQL_DESC_SCALE\n"));
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									//check value
									if (Scale == APP_ExpData[j-1].appScale) 
									{
										//LogMsg(NONE, _T("Scale = %d\n"), Scale);
									}
									else
									{
										LogMsg(ERRMSG, _T("Expected Scale %d and got %d, line %d\n"), APP_ExpData[j-1].appScale, Scale,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									//LogMsg(NONE, _T("Scale = %d\n"), Scale);
									break;
								
								case SQL_DESC_TYPE:
									TESTCASE_BEGIN("APP: SQL_DESC_TYPE\n");
									//initialize buffer
									Type = 0; //initialized invalid value											
									//get value
									returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, SQL_DESC_TYPE, &Type, SQL_IS_SMALLINT, NULL);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
									{
										LogMsg(ERRMSG, _T("Failed to get APP Field Value SQL_DESC_TYPE\n"));
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;			//go to next desc_field
									}
									//check value
									if (Type == APP_ExpData[j-1].appType) 
									{
										//LogMsg(NONE, _T("Type = %d\n"), Type);
									}
									else
									{
										LogMsg(ERRMSG, _T("Expected DescType %d and got %d, line %d\n"), APP_ExpData[j-1].appType, Type,__LINE__);
										TEST_FAILED;
										TESTCASE_END;	//tests ends here: marked as failed
										break;
									}
									TESTCASE_END;
									//LogMsg(NONE, _T("Type = %d\n"), Type);
									break;
								

								default: ;
								} //end switch
							}//end FieldIndex
						}//end j
						break;


					case IPD:

						for (j = 1; j <= DescCount; j++) //iterate through all records
						{
							//LogMsg(NONE, _T("*************************************************\n"));
							//LogMsg(NONE, _T("Testing values of  IPD hDesc[%d]: param %d\n"), i,j);
							//LogMsg(NONE, _T("*************************************************\n"));
							
							for(FieldIndex = 0; FieldIndex < MAX_DESC_FIELDS  ; FieldIndex++)
							{
								//LogMsg(NONE,_T("SQLGetDescField : verifying populated IPD values.\n"));
								switch (DescFields[FieldIndex])
								{
									case SQL_DESC_CASE_SENSITIVE:
										TESTCASE_BEGIN("IPD: SQL_DESC_CASE_SENSITIVE\n");
										//initialize buffer
										CaseSensitive = 99; //valid values are 0 and 1;
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &CaseSensitive, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_CASE_SENSITIVE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (CaseSensitive == IPD_ExpData[j-1].ipdCaseSensitive) 
										{
											//LogMsg(NONE, _T("CaseSensitive = %d\n"), CaseSensitive);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected CaseSensitive %d and got %d, line %d\n"), IPD_ExpData[j-1].ipdCaseSensitive, CaseSensitive,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("CaseSensitive = %d\n"), CaseSensitive);
										break;


									case SQL_DESC_DATETIME_INTERVAL_CODE:
										TESTCASE_BEGIN("IPD: SQL_DESC_DATETIME_INTERVAL_CODE\n");
										//initialize buffer
										DatetimeIntervalCode = 0; //valid values are greater than 0 ;
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &DatetimeIntervalCode, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_DATETIME_INTERVAL_CODE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (DatetimeIntervalCode == IPD_ExpData[j-1].ipdDatetimeIntervalCode) 
										{
											//LogMsg(NONE, _T("DatetimeIntervalCode = %d\n"), DatetimeIntervalCode);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected DatetimeIntervalCode %d and got %d, line %d\n"), IPD_ExpData[j-1].ipdDatetimeIntervalCode, DatetimeIntervalCode,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
										//LogMsg(NONE, _T("DatetimeIntervalCode = %d\n"), DatetimeIntervalCode);
										break;
										
										
									case SQL_DESC_DATETIME_INTERVAL_PRECISION:
										TESTCASE_BEGIN("IPD: SQL_DESC_DATETIME_INTERVAL_PRECISION\n");
										//initialize buffer
										DatetimeIntervalPrecision =99; //invalid precision value ;										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &DatetimeIntervalPrecision, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_DATETIME_INTERVAL_PRECISION\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
													//go to next desc_field
										}
										//check value
										/* SEAQUEST IPD_ExpData[j-1].ipdDatetimeIntervalPrecision = 0; */ //default
										if (DatetimeIntervalPrecision == IPD_ExpData[j-1].ipdDatetimeIntervalPrecision) 
										{
											//LogMsg(NONE, _T("DatetimeIntervalPrecision = %d\n"), DatetimeIntervalPrecision);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected DatetimeIntervalPrecision value %d and got %d (j:%d), line %d\n"), IPD_ExpData[j-1].ipdDatetimeIntervalPrecision, DatetimeIntervalPrecision,j, __LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											
										}

										TESTCASE_END;
										//LogMsg(NONE, _T("DatetimeIntervalPrecision = %d\n"), DatetimeIntervalPrecision);
										break;


									case SQL_DESC_FIXED_PREC_SCALE:
										TESTCASE_BEGIN("IPD: SQL_DESC_FIXED_PREC_SCALE\n");
										//initialize buffer
										FixedPrecScale = 99; //invalid precision value : 0 and 1 are valid.										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &FixedPrecScale, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_FIXED_PREC_SCALE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (FixedPrecScale == IPD_ExpData[j-1].ipdFixedPrecScale) 
										{
											//LogMsg(NONE, _T("FixedPrecScale = %d\n"), FixedPrecScale);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected FixedPrecScale %d and got %d, line %d\n"), IPD_ExpData[j-1].ipdFixedPrecScale, FixedPrecScale,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("FixedPrecScale = %d\n"), FixedPrecScale);
										break;


									case SQL_DESC_LENGTH:
										TESTCASE_BEGIN("IPD: SQL_DESC_LENGTH\n");
										//initialize buffer
										Length = 99; //initialized value .	
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Length, SQL_IS_UINTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_LENGTH\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (Length == IPD_ExpData[j-1].ipdLength) 
										{
											//LogMsg(NONE, _T("Length = %d\n"), Length);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Length %d and got %d, (j:%d) line %d\n"), IPD_ExpData[j-1].ipdLength, Length,j, __LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("Length = %d\n"), Length);
										break;

									
									case SQL_DESC_LOCAL_TYPE_NAME:
										TESTCASE_BEGIN("IPD: SQL_DESC_LOCAL_TYPE_NAME\n");
										//initialize buffer
										_tcscpy((TCHAR*)LocalTypeName, _T("")); //initialized value .	
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], LocalTypeName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_LOCAL_TYPE_NAME\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (!(_tcsicmp((TCHAR*)LocalTypeName, (TCHAR*)IPD_ExpData[j-1].ipdLocalTypeName)))
										{
											
											//LogMsg(NONE, _T("LocalTypeName = %s\n"), LocalTypeName);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected LocalTypeName %s  and got %s, (j:%d) line %d\n"), IPD_ExpData[j-1].ipdLocalTypeName, LocalTypeName,j, __LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("LocalTypeName = %s\n"), LocalTypeName);
										break;

									
									case SQL_DESC_NAME:
										TESTCASE_BEGIN("IPD: SQL_DESC_NAME\n");

										//initialize buffer
										_tcscpy((TCHAR*)Name, _T("")); //initialized value .	
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], Name, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_NAME\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										/* SEAQUEST NEW*/
										if (cwcscmp((TCHAR*)Name, _T(""), TRUE) == 0)
										{
										LogMsg(NONE, _T("The SQL_DESC_NAME for IPD is NULL because the driver does not support Named Parameters\n"));
										}
										else if (cwcscmp((TCHAR*)Name, (TCHAR*)IPD_ExpData[j-1].ipdName, TRUE) == 0)
										/* end of SEAQUEST NEW*/
										// SEAQUEST if (cwcscmp((TCHAR*)Name, (TCHAR*)IPD_ExpData[j-1].ipdName, TRUE) == 0)
										{
											
											//LogMsg(NONE, _T("Name = %s\n"), Name);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Desc Name %s  and got %s, line %d\n"), IPD_ExpData[j-1].ipdName, Name,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("Name = %s\n"), Name);
										break;

																			
									case SQL_DESC_NULLABLE:
										TESTCASE_BEGIN("IPD: SQL_DESC_NULLABLE\n");

										//initialize buffer
										Nullable = 99; //initialized invalid value .
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Nullable, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_NULLABLE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (Nullable == IPD_ExpData[j-1].ipdNullable) 
										{
											//LogMsg(NONE, _T("Nullable = %d\n"), Nullable);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Nullable value %d and got %d, line %d\n"), IPD_ExpData[j-1].ipdNullable, Nullable,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("Nullable = %d\n"), Nullable);
										break;


									case SQL_DESC_NUM_PREC_RADIX:
										//10 for exact numeric, 2 for approx numeric, 0 for TCHAR
										TESTCASE_BEGIN("IPD: SQL_DESC_NUM_PREC_RADIX\n");

										//initialize buffer
										NumPrecRadix = 99; //initialized invalid value .
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &NumPrecRadix, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_NUM_PREC_RADIX\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										
										}
										//check value
										if (NumPrecRadix == IPD_ExpData[j-1].ipdNumPrecRadix) 
										{
											//LogMsg(NONE, _T("NumPrecRadix = %d\n"), NumPrecRadix);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected NumPrecRadix value %d and got %d, line %d\n"), IPD_ExpData[j-1].ipdNumPrecRadix, NumPrecRadix,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("NumPrecRadix = %d\n"), NumPrecRadix);
										break;

									case SQL_DESC_OCTET_LENGTH:
										TESTCASE_BEGIN("IPD: SQL_DESC_OCTET_LENGTH\n");

										//initialize buffer
										OctetLength = 99; //initialized invalid value .
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &OctetLength, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_OCTET_LENGTH\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (OctetLength == IPD_ExpData[j-1].ipdOctetLength) 
										{
											//LogMsg(NONE, _T("OctetLength = %d\n"), OctetLength);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected OctetLength value %d and got %d, (j:%d) line %d\n"), IPD_ExpData[j-1].ipdOctetLength, OctetLength,j, __LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("OctetLength = %d\n"), OctetLength);
										break;

									case SQL_DESC_PARAMETER_TYPE:
										TESTCASE_BEGIN("IPD: SQL_DESC_PARAMETER_TYPE\n");

										//initialize buffer
										ParameterType = 99; //initialized invalid value .
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &ParameterType, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_PARAMETER_TYPE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (ParameterType == IPD_ExpData[j-1].ipdParameterType) 
										{
											//LogMsg(NONE, _T("ParameterType = %d\n"), ParameterType);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected ParameterType value %d and got %d, line %d\n"), IPD_ExpData[j-1].ipdParameterType, ParameterType,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("ParameterType = %d\n"), ParameterType);
										break;


									case SQL_DESC_PRECISION:
										//is valid for numeric, timestamp, time and interval only
										TESTCASE_BEGIN("IPD: SQL_DESC_PRECISION\n");

										//initialize buffer
										Precision = 99; //initialized invalid value .
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Precision, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_PRECISION\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										//check value
										if (Precision == IPD_ExpData[j-1].ipdPrecision) 
										{
											//LogMsg(NONE, _T("Precision = %d\n"), Precision);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Precision value %d and got %d, line %d\n"), IPD_ExpData[j-1].ipdPrecision, Precision,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("Precision = %d\n"), Precision);
										break;

											
									case SQL_DESC_SCALE:	//valid for decimal and numeric only
										TESTCASE_BEGIN("IPD: SQL_DESC_Scale\n");

										//initialize buffer
										Scale = 99; //initialized invalid value .
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Scale, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_SCALE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										
										}
										//check value
										if (Scale == IPD_ExpData[j-1].ipdScale) 
										{
											//LogMsg(NONE, _T("Scale = %d\n"), Scale);
										}
										else
										{
											LogMsg(ERRMSG, _T("ExpectedScale value %d and got %d, line %d\n"), IPD_ExpData[j-1].ipdScale, Scale,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
									
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("Scale = %d\n"), Scale);
										break;

									case SQL_DESC_TYPE:
										TESTCASE_BEGIN("IPD: SQL_DESC_TYPE\n");

										//initialize buffer
										Type = 0; //initialized invalid value .
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Type, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_TYPE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (Type != IPD_ExpData[j-1].ipdType) 
										{
											LogMsg(ERRMSG, _T("Expected Type value %d and got %d, line %d\n"), IPD_ExpData[j-1].ipdType, Type,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("Type = %d\n"), Type);
										break;


									case SQL_DESC_TYPE_NAME:
										TESTCASE_BEGIN("IPD: SQL_DESC_TYPE_NAME\n");

										//initialize buffer
										_tcscpy((TCHAR*)TypeName, _T("")); //initialized invalid value .										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], TypeName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_TYPE_NAME\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (!(_tcsicmp((TCHAR*)TypeName, (TCHAR*)IPD_ExpData[j-1].ipdTypeName)))
										{
											
											//LogMsg(NONE, _T("TypeName = %s\n"),TypeName);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected TypeName %s  and got %s, (j:%d) line %d\n"), IPD_ExpData[j-1].ipdTypeName, TypeName,j, __LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
										//LogMsg(NONE, _T("TypeName = %s\n"),TypeName);
										break;


									case SQL_DESC_UNNAMED:
										TESTCASE_BEGIN("IPD: SQL_DESC_UNNAMED\n");
										//initialize buffer
										Unnamed = 99; //initialized invalid value										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Unnamed, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_UNNAMED\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (Unnamed == IPD_ExpData[j-1].ipdUnnamed) 
										{
											//LogMsg(NONE, _T("Unnamed = %d\n"), Unnamed);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Unnamed value %d and got %d, line %d\n"), IPD_ExpData[j-1].ipdUnnamed, Unnamed,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
										//LogMsg(NONE, _T("Unnamed = %d\n"), Unnamed);
										break;


							
									case SQL_DESC_UNSIGNED:
										TESTCASE_BEGIN("IPD: SQL_DESC_UNSIGNED\n");
										//initialize buffer
										Unsigned = 99; //initialized invalid value
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Unsigned, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IPD Field Value SQL_DESC_UNSIGNED\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (Unsigned == IPD_ExpData[j-1].ipdUnsigned) 
										{
											//LogMsg(NONE, _T("Unsigned = %d\n"), Unsigned);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Unsigned value %d and got %d, line %d\n"), IPD_ExpData[j-1].ipdUnsigned, Unsigned,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										TESTCASE_END;
										//LogMsg(NONE, _T("Unsigned = %d\n"), Unsigned);
										break;

									default: ;
								}//end switch for each field
							}//end for for each rec (Field Index)
						}//end for j (loop recs)
						break; //end case IPD


					case IRD:
						
						//populated IRD has DescCount=MAX_BOUND_PARAM number of records
						for (j = 1; j <= DescCount; j++) //iterate through all records
						{
							//LogMsg(NONE, _T("*************************************************\n"));
							//LogMsg(NONE, _T("Testing values of IRD hDesc[%d]: param %d\n"), i,j);
							//LogMsg(NONE, _T("*************************************************\n"));
							for(FieldIndex = 0; FieldIndex < MAX_DESC_FIELDS  ; FieldIndex++)
							{
								//Descriptor = DescFields[FieldIndex];
								//LogMsg(NONE,_T("SQLGetDescField : verifying populated IRD values.\n"));
								switch (DescFields[FieldIndex])
								{
									case SQL_DESC_AUTO_UNIQUE_VALUE:
										TESTCASE_BEGIN("IRD: SQL_DESC_AUTO_UNIQUE_VALUE\n");
										//initialize buffer
										AutoUniqueValue = 99; //initialized invalid value											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &AutoUniqueValue, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_AUTO_UNIQUE_VALUE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (AutoUniqueValue == IRD_ExpData[j-1].irdAutoUniqueValue) //none of the columns are autoincrementing
										{
											//LogMsg(NONE, _T("AutoUniqueValue = %d\n"), AutoUniqueValue);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected AutoUniqueValue %d (SQL_FALSE) and got %d, line %d\n"), IRD_ExpData[j-1].irdAutoUniqueValue, AutoUniqueValue,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
										//LogMsg(SHORTTIMESTAMP, _T("AutoUniqueValue = %d\n"), AutoUniqueValue);
										break;

									
									case SQL_DESC_BASE_COLUMN_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_BASE_COLUMN_NAME\n");
										//initialize buffer
										_tcscpy((TCHAR*)BaseColumnName ,_T("")); //initialized invalid value										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], BaseColumnName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_BASE_COLUMN_NAME\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (cwcscmp((TCHAR*)BaseColumnName, (TCHAR*)IRD_ExpData[j-1].irdBaseColumnName, TRUE) == 0)
										{
											
											//LogMsg(NONE, _T("BaseColumnName = %s\n"), BaseColumnName);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected BaseColumnName %s  and got %s, line %d\n"), IRD_ExpData[j-1].irdBaseColumnName, BaseColumnName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
										//LogMsg(NONE, _T("BaseColumnName = %s\n"), BaseColumnName);
										break;	
										
									
									case SQL_DESC_BASE_TABLE_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_BASE_TABLE_NAME\n");
										//initialize buffer
										_tcscpy((TCHAR*)BaseTableName ,_T("")); //initialized invalid value											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], BaseTableName,MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_BASE_TABLE_NAME\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (cwcscmp((TCHAR*)BaseTableName, (TCHAR*)IRD_ExpData[j-1].irdBaseTableName, TRUE) == 0)
										{
											
//											LogMsg(NONE, _T("BaseTableName = %s\n"), BaseTableName);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected BaseTableName %s  and got %s, line %d\n"), IRD_ExpData[j-1].irdBaseTableName, BaseTableName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("BaseTableName = %s\n"), BaseTableName);
										break;
										
								
									case SQL_DESC_CASE_SENSITIVE:
										TESTCASE_BEGIN("IRD: SQL_DESC_CASE_SENSITIVE\n");
										//initialize buffer
										CaseSensitive = 99; //valid values are 0 and 1;										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &CaseSensitive, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_CASE_SENSITIVE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (CaseSensitive == IRD_ExpData[j-1].irdCaseSensitive) 
										{
//											LogMsg(NONE, _T("CaseSensitive = %d\n"), CaseSensitive);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected CaseSensitive %d and got %d, line %d\n"), IRD_ExpData[j-1].irdCaseSensitive, CaseSensitive,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("CaseSensitive = %d\n"), CaseSensitive);
										break;
										
									
									case SQL_DESC_CATALOG_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_BASE_TABLE_NAME\n");
										//initialize buffer
										_tcscpy((TCHAR*)CatalogName ,_T("")); //initialized invalid value											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], CatalogName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_CATALOG_NAME\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (!(_tcsicmp((TCHAR*)CatalogName, (TCHAR*)IRD_ExpData[j-1].irdCatalogName)))
										{
											
//											LogMsg(NONE, _T("CatalogName = %s\n"), CatalogName);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected CatalogName %s  and got %s, line %d\n"), IRD_ExpData[j-1].irdCatalogName, CatalogName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("CatalogName = %s\n"), CatalogName);
										break;

								
									case SQL_DESC_CONCISE_TYPE:
										TESTCASE_BEGIN("IRD: SQL_DESC_CONCISE_TYPE\n");
										//initialize buffer
										ConciseType = 0; //initialized invalid value											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &ConciseType, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_CONCISE_TYPE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (ConciseType == IRD_ExpData[j-1].irdConciseType) 
										{
//											LogMsg(NONE, _T("ConciseType = %d\n"), ConciseType);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected ConciseType %d and got %d, (j:%d) line %d\n"), IRD_ExpData[j-1].irdConciseType, ConciseType,j, __LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("ConciseType = %d\n"), ConciseType);
										break;
								
								
									case SQL_DESC_DATETIME_INTERVAL_CODE:
										TESTCASE_BEGIN("IRD: SQL_DESC_DATETIME_INTERVAL_CODE\n");
										//initialize buffer
										DatetimeIntervalCode = 0; //valid values are greater than 0 ;										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &DatetimeIntervalCode, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_DATETIME_INTERVAL_CODE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (DatetimeIntervalCode == IRD_ExpData[j-1].irdDatetimeIntervalCode) 
										{
//											LogMsg(NONE, _T("DatetimeIntervalCode = %d\n"), DatetimeIntervalCode);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected DatetimeIntervalCode %d and got %d, line %d\n"), IRD_ExpData[j-1].irdDatetimeIntervalCode, DatetimeIntervalCode,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("DatetimeIntervalCode = %d\n"), DatetimeIntervalCode);
										break;
								
									
									case SQL_DESC_DISPLAY_SIZE:
										TESTCASE_BEGIN("IRD: SQL_DESC_DISPLAY_SIZE\n");
										//initialize buffer
										DisplaySize = 99; //initialized invalid value											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &DisplaySize, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_DISPLAY_SIZE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (DisplaySize == IRD_ExpData[j-1].irdDisplaySize) //none of the columns are autoincrementing
										{
//											LogMsg(NONE, _T("DisplaySize = %d\n"), DisplaySize);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected DisplaySize %d and got %d, line %d\n"), IRD_ExpData[j-1].irdDisplaySize, DisplaySize,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("DisplaySize = %d\n"), DisplaySize);
										break;
										
									
									case SQL_DESC_FIXED_PREC_SCALE:
										TESTCASE_BEGIN("IRD: SQL_DESC_FIXED_PREC_SCALE\n");
										//initialize buffer
										FixedPrecScale = 99; //invalid precision value : 0 and 1 are valid.											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &FixedPrecScale, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_FIXED_PREC_SCALE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (FixedPrecScale == IRD_ExpData[j-1].irdFixedPrecScale) 
										{
//											LogMsg(NONE, _T("FixedPrecScale = %d\n"), FixedPrecScale);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected FixedPrecScale %d and got %d, line %d\n"), IRD_ExpData[j-1].irdFixedPrecScale, FixedPrecScale,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("FixedPrecScale = %d\n"), FixedPrecScale);
										break;

									
									case SQL_DESC_LABEL:
										TESTCASE_BEGIN("IRD: SQL_DESC_LABEL\n");
										//initialize buffer
										_tcscpy((TCHAR*)Label , _T("")); //initialized invalid value											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], Label, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_LABEL\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (!(_tcsicmp((TCHAR*)Label, (TCHAR*)/* SEAQUEST IRD_ExpData[j-1].irdLabel */ removeQuotes(IRD_ExpData[j-1].irdLabel,tmpbuf))))
										{
											
//											LogMsg(NONE, _T("Label = %s\n"), Label);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Label %s  and got %s, line %d\n"), IRD_ExpData[j-1].irdLabel, Label,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("Label = %s\n"), Label);
										break;

					
									case SQL_DESC_LENGTH:
										TESTCASE_BEGIN("IRD: SQL_DESC_LENGTH\n");
										//initialize buffer
										Length = 99; //initialized value .											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Length, SQL_IS_UINTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_LENGTH\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (Length == IRD_ExpData[j-1].irdLength) 
										{
//											LogMsg(NONE, _T("Length = %d\n"), Length);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Length %d and got %d, (j:%d) line %d\n"), IRD_ExpData[j-1].irdLength, Length,j, __LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("Length = %d\n"), Length);
										break;
									
									case SQL_DESC_LITERAL_PREFIX:
										TESTCASE_BEGIN("IRD: SQL_DESC_LITERAL_PREFIX\n");
										//initialize buffer
										_tcscpy((TCHAR*)LiteralPrefix , _T("")); //initialized invalid value										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], LiteralPrefix, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_LITERAL_PREFIX\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (!(_tcsicmp((TCHAR*)LiteralPrefix, (TCHAR*)IRD_ExpData[j-1].irdLiteralPrefix)))
										{
											
//											LogMsg(NONE, _T("LiteralPrefix = %s\n"),LiteralPrefix);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected LiteralPrefix %s  and got %s, line %d\n"), IRD_ExpData[j-1].irdLiteralPrefix, LiteralPrefix,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("LiteralPrefix = %s\n"),LiteralPrefix);
										break;
									
									case SQL_DESC_LITERAL_SUFFIX:
										TESTCASE_BEGIN("IRD: SQL_DESC_LITERAL_SUFFIX\n");
										//initialize buffer
										_tcscpy((TCHAR*)LiteralSuffix, _T("")); //initialized invalid value											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], LiteralSuffix,MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_LITERAL_SUFFIX\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (!(_tcsicmp((TCHAR*)LiteralSuffix, (TCHAR*)IRD_ExpData[j-1].irdLiteralSuffix)))
										{
											
//											LogMsg(NONE, _T("LiteralSuffix = %s\n"), LiteralSuffix);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected LiteralSuffix %s  and got %s, line %d\n"), IRD_ExpData[j-1].irdLiteralSuffix, LiteralSuffix,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("LiteralSuffix = %s\n"), LiteralSuffix);
										break;
									
									case SQL_DESC_LOCAL_TYPE_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_LOCAL_TYPE_NAME\n");
										//initialize buffer
										_tcscpy((TCHAR*)LocalTypeName, _T("")); //initialized value .											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], LocalTypeName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_LOCAL_TYPE_NAME\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (!(_tcsicmp((TCHAR*)LocalTypeName, (TCHAR*)IRD_ExpData[j-1].irdLocalTypeName)))
										{
											//LogMsg(NONE, _T("LocalTypeName = %s\n"), LocalTypeName);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected LocalTypeName %s  and got %s, (j:%d) line %d\n"), IRD_ExpData[j-1].irdLocalTypeName, LocalTypeName,j,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
										//LogMsg(NONE, _T("LocalTypeName = %s\n"), LocalTypeName);
										break;
									
									case SQL_DESC_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_NAME\n");
										//initialize buffer
										_tcscpy((TCHAR*)Name, _T("")); //initialized value .										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], Name, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_NAME\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (cwcscmp((TCHAR*)Name, (TCHAR*)IRD_ExpData[j-1].irdName, TRUE) == 0)
										{
											
//											LogMsg(NONE, _T("Name = %s\n"), Name);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Desc Name %s  and got %s, line %d\n"), IRD_ExpData[j-1].irdName, Name,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("Name = %s\n"), Name);
										break;
																			
									case SQL_DESC_NULLABLE:
										TESTCASE_BEGIN("IRD: SQL_DESC_NULLABLE\n");
										//initialize buffer
										Nullable = 99; //initialized invalid value .										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Nullable, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_NULLABLE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (Nullable == IRD_ExpData[j-1].irdNullable) 
										{
//											LogMsg(NONE, _T("Nullable = %d\n"), Nullable);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Nullable value %d and got %d, line %d\n"), IRD_ExpData[j-1].irdNullable, Nullable,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("Nullable = %d\n"), Nullable);
										break;

									case SQL_DESC_NUM_PREC_RADIX:
										//10 for exact numeric, 2 for approx numeric, 0 for TCHAR
										TESTCASE_BEGIN("IRD: SQL_DESC_NUM_PREC_RADIX\n");
										//initialize buffer
										NumPrecRadix = 99; //initialized invalid value .														
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &NumPrecRadix, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_NUM_PREC_RADIX\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										
										}
										//check value
										/* SEAQUEST IRD_ExpData[j-1].irdNumPrecRadix = 2; */
										if (NumPrecRadix == IRD_ExpData[j-1].irdNumPrecRadix) 
										{
//											LogMsg(NONE, _T("NumPrecRadix = %d\n"), NumPrecRadix);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected NumPrecRadix value %d and got %d, (j:%d) line %d\n"), IRD_ExpData[j-1].irdNumPrecRadix, NumPrecRadix,j,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										
										}
//										LogMsg(NONE, _T("NumPrecRadix = %d\n"), NumPrecRadix);
										TESTCASE_END;
										break;

									case SQL_DESC_OCTET_LENGTH:
										TESTCASE_BEGIN("IRD: SQL_DESC_OCTET_LENGTH\n");
										//initialize buffer
										OctetLength = 99; //initialized invalid value .										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &OctetLength, SQL_IS_INTEGER, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_OCTET_LENGTH\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (OctetLength == IRD_ExpData[j-1].irdOctetLength) 
										{
//											LogMsg(NONE, _T("OctetLength = %d\n"), OctetLength);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected OctetLength value %d and got %d, line %d\n"), IRD_ExpData[j-1].irdOctetLength, OctetLength,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("OctetLength = %d\n"), OctetLength);
										break;

									case SQL_DESC_PRECISION:
										//is valid for numeric, timestamp, time and interval only
										TESTCASE_BEGIN("IRD: SQL_DESC_PRECISION\n");
										//initialize buffer
										Precision = 99; //initialized invalid value .														
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Precision, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_PRECISION\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}
										//check value
										if (Precision == IRD_ExpData[j-1].irdPrecision) 
										{
//											LogMsg(NONE, _T("Precision = %d\n"), Precision);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Precision value %d and got %d, line %d\n"), IRD_ExpData[j-1].irdPrecision, Precision,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("Precision = %d\n"), Precision);
										break;

										
									case SQL_DESC_SCALE:
										TESTCASE_BEGIN("IRD: SQL_DESC_Scale\n");
										//initialize buffer
										Scale = 99; //initialized invalid value .														
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Scale, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_SCALE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
										
										}
										//check value
										if (Scale == IRD_ExpData[j-1].irdScale) 
										{
//											LogMsg(NONE, _T("Scale = %d\n"), Scale);
										}
										else
										{
											LogMsg(ERRMSG, _T("ExpectedScale value %d and got %d, line %d\n"), IRD_ExpData[j-1].irdScale, Scale,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
									
										}
										TESTCASE_END;
//										LogMsg(NONE, _T("Scale = %d\n"), Scale);
										break;

									
									case SQL_DESC_SCHEMA_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_SCHEMA_NAME\n");
										//initialize buffer
										_tcscpy((TCHAR*)SchemaName,_T("")); //initialized invalid value											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], SchemaName,MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_SCHEMA_NAME\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (!(_tcsicmp((TCHAR*)SchemaName, (TCHAR*)IRD_ExpData[j-1].irdSchemaName)))
										{
											
//											LogMsg(NONE, _T("SchemaName = %s\n"), SchemaName);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected SchemaName %s  and got %s, line %d\n"), IRD_ExpData[j-1].irdSchemaName, SchemaName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("SchemaName = %s\n"), SchemaName);
										break;

									
									case SQL_DESC_SEARCHABLE:
										TESTCASE_BEGIN("IRD: SQL_DESC_SEARCHABLE\n");
										//initialize buffer
										Searchable = 99; //initialized invalid value											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Searchable, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_SEARCHABLE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (Searchable == IRD_ExpData[j-1].irdSearchable) 
										{
//											LogMsg(NONE, _T("Searchable = %d\n"), Searchable);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Searchable value %d and got %d, line %d\n"), IRD_ExpData[j-1].irdSearchable, Searchable,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("Searchable = %d\n"), Searchable);
										break;

							
									case SQL_DESC_TABLE_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_TABLE_NAME\n");
										//initialize buffer
										_tcscpy((TCHAR*)TableName, _T("")); //initialized invalid value											
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], TableName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_TABLE_NAME\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (cwcscmp((TCHAR*)TableName, (TCHAR*)IRD_ExpData[j-1].irdTableName, TRUE) == 0)
										{
//											LogMsg(NONE, _T("TableName = %s\n"), TableName);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected TableName %s  and got %s, line %d\n"), IRD_ExpData[j-1].irdTableName, TableName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("TableName = %s\n"), TableName);
										break;

									case SQL_DESC_TYPE:
										TESTCASE_BEGIN("IRD: SQL_DESC_TYPE\n");
										//initialize buffer
										Type = 0; //initialized invalid value .										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Type, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_TYPE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (Type != IRD_ExpData[j-1].irdType) 
										{
											LogMsg(ERRMSG, _T("Expected Type value %d and got %d, (j:%d) line %d\n"), IRD_ExpData[j-1].irdType, Type,j,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}
										
										TESTCASE_END;
//										LogMsg(NONE, _T("Type = %d\n"), Type);
										break;


							
									case SQL_DESC_TYPE_NAME:
										TESTCASE_BEGIN("IRD: SQL_DESC_TYPE_NAME\n");
										//initialize buffer
										_tcscpy((TCHAR*)TypeName, _T("")); //initialized invalid value .										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], TypeName, MAX_BUFFER_LEN, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_TYPE_NAME\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (!(_tcsicmp((TCHAR*)TypeName, (TCHAR*)IRD_ExpData[j-1].irdTypeName)))
										{
											
//											LogMsg(NONE, _T("TypeName = %s\n"),TypeName);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected TypeName %s  and got %s, line %d\n"), IRD_ExpData[j-1].irdTypeName, TypeName,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("TypeName = %s\n"),TypeName);
										break;

							
									case SQL_DESC_UNNAMED:
										TESTCASE_BEGIN("IRD: SQL_DESC_UNNAMED\n");
										//initialize buffer
										Unnamed = 99; //initialized invalid value .										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Unnamed, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_UNNAMED\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (Unnamed == IRD_ExpData[j-1].irdUnnamed) 
										{
//											LogMsg(NONE, _T("Unnamed = %d\n"), Unnamed);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Unnamed value %d and got %d, line %d\n"), IRD_ExpData[j-1].irdUnnamed, Unnamed,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("Unnamed = %d\n"), Unnamed);
										break;


							
									case SQL_DESC_UNSIGNED:
										TESTCASE_BEGIN("IRD: SQL_DESC_UNSIGNED\n");
										//initialize buffer
										Unsigned = 99; //initialized invalid value										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Unsigned, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_UNSIGNED\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (Unsigned == IRD_ExpData[j-1].irdUnsigned) 
										{
//											LogMsg(NONE, _T("Unsigned = %d\n"), Unsigned);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Unsigned value %d and got %d, line %d\n"), IRD_ExpData[j-1].irdUnsigned, Unsigned,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("Unsigned = %d\n"), Unsigned);
										break;

									

							
									case SQL_DESC_UPDATABLE:
										TESTCASE_BEGIN("IRD: SQL_DESC_UPDATABLE\n");
										//initialize buffer
										Updatable = 99; //initialized invalid value										
										//get value
										returncode = SQLGetDescField(hDesc[i], (SQLSMALLINT)j, DescFields[FieldIndex], &Updatable, SQL_IS_SMALLINT, NULL);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetDescField"))
										{
											LogMsg(ERRMSG, _T("Failed to get IRD Field Value SQL_DESC_UPDATABLE\n"));
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;			//go to next desc_field
										}
										//check value
										if (Updatable == IRD_ExpData[j-1].irdUpdatable) 
										{
//											LogMsg(NONE, _T("Updatable = %d\n"), Updatable);
										}
										else
										{
											LogMsg(ERRMSG, _T("Expected Updatable value %d and got %d, line %d\n"), IRD_ExpData[j-1].irdUpdatable, Updatable,__LINE__);
											TEST_FAILED;
											TESTCASE_END;	//tests ends here: marked as failed
											break;
										}

										TESTCASE_END;
//										LogMsg(NONE, _T("Updatable = %d\n"), Updatable);
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
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLSetDescField and SQLGetDescField.\n"));


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

	returncode = SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabProject,SQL_NTS);

	returncode = SQLFreeHandle(SQL_HANDLE_STMT,hstmt);

	// diconnect : free everything	
	FullDisconnect3(pTestInfo);
	free_list(var_list);
	TEST_RETURN;

}//end of test suite






