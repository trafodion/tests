#include "include.h"
#include "defines.h"
#include "ODBCcommon.h"
#include "table.h"
#include "struct.h"
#include "sqlutil.h"
#include "commonglobals.h"

extern long gMaxRowSize;

/*>>>> this is just here temporarily */
struct VolumeList{
    char *VolumeName;
    };
typedef struct VolumeList VolumeList;

/***********************************************************************
** RandomDecimalString()
**
** This function will create a valid random DECIMAL or NUMERIC string
** based upon the precision and scale parameters.
* >>>for now this is a stub that returns a constant string.
************************************************************************/
char *RandomDecimalString(short Precision, short Scale)
{
   char *StringPtr;
   StringPtr=(char *)malloc(4);
	if(Scale==0){
	   strcpy(StringPtr,"1");
	}
	else {
	   strcpy(StringPtr,"1.1");
	}
   return(StringPtr);
}

/***********************************************************************
** RandomODBCDataType()
**
** This function returns a value for an ODBC data type.  The values returned
** by this function have nothing to do with the values used for the defines
** of the real ODBC data types as found in SQL.H
************************************************************************/
int RandomODBCDataType(void)
{
   return(RANDOM_NUM1(MAX_TYPES));
   }

/***********************************************************************
** RandomODBCDateTimeString()
**
** This function will create a valid random date & time string based upon
** the parameters passed in.
** >>>NOTE: for now we will just support the default format which is
**            yyyy-mm-dd:hh:mm:ss.msssss
************************************************************************/
char *RandomODBCDateTimeString(short DateTimeType)
{
   static char DateTimeString[100];
   short Year,Month,Day,Hour,Second,Minute,MsecPart1,MsecPart2;
   short offset,length;
	char *pReturnString;

   /* >>>check for some parameter conditions like valid DateTimeType */

   /* randomly generate a full length datetime string */
   Year=RANDOM_NUM1(9999);
   Month= RANDOM_NUM1(12);
   switch(Month){
      case 4:
      case 6:
      case 9:
      case 11:
         Day=RANDOM_NUM1(30);
         break;
      case 1:
      case 3:
      case 5:
      case 7:
      case 8:
      case 10:
      case 12:
         Day=RANDOM_NUM1(31);
         break;
      case 2:
         Day=RANDOM_NUM1(28);
         break;
      }
   Hour=RANDOM_NUM0(23);
   Minute=RANDOM_NUM0(59);
   Second=RANDOM_NUM0(59);
   MsecPart1=RANDOM_NUM0(999);
   MsecPart2=RANDOM_NUM0(999);
   sprintf(DateTimeString,"%04d-%02d-%02d %02d:%02d:%02d.%03d%03d",
           Year,Month,Day,Hour,Minute,Second,MsecPart1,MsecPart2);

   /* Determine which portion of the full string the caller wanted */
   switch(DateTimeType){

      case TYPE_DATE:      offset=0;  length=10; break;

      case TYPE_TIME:      offset=11; length=8;  break;

      case TYPE_TIMESTAMP: offset=0;  length=(short)strlen(DateTimeString); break;

      /* invalid DateTime Type, return a NULL pointer */
      default:
         return(NULL);
         break;
      } /* end switch */

   DateTimeString[offset+length]='\0';
	pReturnString=malloc(strlen(&DateTimeString[offset])+1);
	strcpy(pReturnString,&DateTimeString[offset]);

   return(pReturnString);

   } /* end: RandomODBCDateTimeString() */

/***********************************************************************
** RandomODBCDateTimeLiteral()
**
** This function will make a valid ODBC date time literal
**
**                  {  d 'yyyy-mm-dd' }
**                  {  t 'hh:mm:ss' }
**                  { ts 'yyyy-mm-dd:hh:mm:ss.msssss' }
************************************************************************/
char *RandomODBCDateTimeLiteral(short DateTimeType)
{
   static char buffer[100];
   char DateTimePrefix[100];
   char DateTimeSuffix[10];
   char DateTimeTypeString[5];

   /* randomly choose which style for the date time literal */
   strcpy(DateTimePrefix,"{");
   strcpy(DateTimeSuffix,"}");

/*   if(RANDOM_T_OR_F){
      strcpy(DateTimePrefix,"{");
      strcpy(DateTimeSuffix,"}");
      }
   else {
      strcpy(DateTimePrefix,"--(*vendor(microsoft),product(odbc)");
      strcpy(DateTimeSuffix,"*)--");
      }
*/

   /* translate the date time type into a string */
   switch(DateTimeType){
      case TYPE_DATE: strcpy(DateTimeTypeString,"d");  break;
      case TYPE_TIME: strcpy(DateTimeTypeString,"t");  break;
      case TYPE_TIMESTAMP: strcpy(DateTimeTypeString,"ts");  break;

      /* invalid DateTime Type, return a NULL pointer */
      default:
         return(NULL);
         break;
      }

   /* format the date time literal */
   sprintf(buffer,"%s %s '%s' %s",
           DateTimePrefix,
           DateTimeTypeString,
           RandomODBCDateTimeString(DateTimeType),
           DateTimeSuffix);

   return(buffer);

   } /* end: RandomODBCDateTimeLiteral() */

/***********************************************************************
** Get all information about ODBC SQL data types and store it in a
** linked list.
***********************************************************************/
SQLTypeInfo *GetSQLTypeInfo(char *DataSource,char *UserID, char *Password)
{
	char	TempStr[10];
	SQLLEN	StrLen;
	long	ODBCVersion;
	SQLRETURN	rc;
	HENV	henv;
	HDBC	hdbc;
	HSTMT	hstmt;
	SQLTypeInfo	*pSQLTypeInfo;
	SQLTypeInfo	*pSQLTypeInfoTemp;
	SQLTypeInfo	*pSQLTypeInfoList;

	// Connect to the data source so we can get the needed info
	rc=SQLAllocEnv(&henv);
	if(rc!=SQL_SUCCESS) return NULL;
	rc=SQLAllocConnect(henv,&hdbc);
	if(rc!=SQL_SUCCESS){LogAllErrors(henv,NULL,NULL);return NULL;}
	rc=SQLConnect(hdbc,DataSource,SQL_NTS,UserID,SQL_NTS,Password,SQL_NTS);
	if(!SQL_SUCCEEDED(rc)){
		LogPrintf("DataSource='%s'  UserID='%s'  Password='%s'\n",DataSource,UserID,Password);
        LogAllErrors(henv,hdbc,NULL);return NULL;
	}
	rc=SQLAllocStmt(hdbc,&hstmt);
	if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,NULL);return NULL;}

	// get the version of ODBC the driver supports
	rc=SQLGetInfo(hdbc,SQL_DRIVER_ODBC_VER,TempStr,sizeof(TempStr),(short *)&StrLen);
	if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt);return NULL;}
	ODBCVersion=atol(TempStr);

	// Ask for info for all data types
	rc=SQLGetTypeInfo(hstmt,SQL_ALL_TYPES);
	if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt);return NULL;}

	pSQLTypeInfoList=NULL;
	pSQLTypeInfoTemp=NULL;
	while(SQLFetch(hstmt)==SQL_SUCCESS){

		// Allocate next element in the list
		pSQLTypeInfo=malloc(sizeof(SQLTypeInfo));
		pSQLTypeInfo->pNext=NULL;

		// Read in results and fill out info into structures
		rc=SQLGetData(hstmt,1,SQL_C_DEFAULT,pSQLTypeInfo->TypeName,SQL_MAX_COL_NAME+1,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,2,SQL_C_SHORT,&pSQLTypeInfo->SQLDataType,0,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,3,SQL_C_SHORT,&pSQLTypeInfo->ColumnSize,0,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,4,SQL_C_DEFAULT,pSQLTypeInfo->LiteralPrefix,SQL_MAX_COL_NAME+1,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,5,SQL_C_DEFAULT,pSQLTypeInfo->LiteralSuffix,SQL_MAX_COL_NAME+1,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,6,SQL_C_DEFAULT,pSQLTypeInfo->CreateParams,SQL_MAX_COL_NAME+1,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,7,SQL_C_SHORT,&pSQLTypeInfo->Nullable,0,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,8,SQL_C_SHORT,&pSQLTypeInfo->CaseSensitive,0,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,9,SQL_C_SHORT,&pSQLTypeInfo->Searchable,0,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,10,SQL_C_SHORT,&pSQLTypeInfo->UnsignedAttr,0,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,11,SQL_C_SHORT,&pSQLTypeInfo->FixedPrecScale,0,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,12,SQL_C_SHORT,&pSQLTypeInfo->AutoIncrement,0,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,13,SQL_C_DEFAULT,pSQLTypeInfo->LocalTypeName,SQL_MAX_COL_NAME+1,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,14,SQL_C_SHORT,&pSQLTypeInfo->MinScale,0,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
		rc=SQLGetData(hstmt,15,SQL_C_SHORT,&pSQLTypeInfo->MaxScale,0,&StrLen);
		if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}


		if(ODBCVersion>=SQL_OV_ODBC3){
			rc=SQLGetData(hstmt,16,SQL_C_SHORT,&pSQLTypeInfo->SQLDataType2,0,&StrLen);
			if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
			rc=SQLGetData(hstmt,17,SQL_C_SHORT,&pSQLTypeInfo->SQLDatetimeSub,0,&StrLen);
			if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
			rc=SQLGetData(hstmt,18,SQL_C_LONG,&pSQLTypeInfo->NumPrecRadix,0,&StrLen);
			if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
			rc=SQLGetData(hstmt,19,SQL_C_SHORT,&pSQLTypeInfo->IntervalPrecision,0,&StrLen);
			if(rc!=SQL_SUCCESS){LogAllErrors(henv,hdbc,hstmt); free(pSQLTypeInfo);return NULL;}
			}

		// add new element onto end of list
		if(pSQLTypeInfoTemp!=NULL){
			pSQLTypeInfoTemp->pNext=pSQLTypeInfo;
			}
		pSQLTypeInfoTemp=pSQLTypeInfo;


		// if this is the first element in the list the we better remember it
		// as the beginning of the list.
		if(pSQLTypeInfoList==NULL) pSQLTypeInfoList=pSQLTypeInfo;
		}

	// disconnect and free things up.  We really don't care about the return codes
	rc=SQLFreeStmt(hstmt,SQL_CLOSE);
	rc=SQLDisconnect(hdbc);
	rc=SQLFreeConnect(hdbc);
	rc=SQLFreeEnv(henv);

	return(pSQLTypeInfoList);
	}	// end of GetSQLTypeInfo

/***********************************************************************
** Returns a pointer to the SQLTypeInfo structure which corresponds to
** the DataType passed in.
***********************************************************************/
SQLTypeInfo *FindSQLTypeInfo(short DataType)
{
	short MatchingSQLType;
	Boolean	found;
	SQLTypeInfo	*pSQLTypeInfo;

	// find the matching SQL data type
	switch(DataType){
		case TYPE_CHAR:		MatchingSQLType=SQL_CHAR; break;
      case TYPE_NUMERIC:	MatchingSQLType=SQL_NUMERIC; break;
      case TYPE_DECIMAL:	MatchingSQLType=SQL_DECIMAL; break;
      case TYPE_INT:			MatchingSQLType=SQL_INTEGER; break;
      case TYPE_SMALLINT:	MatchingSQLType=SQL_SMALLINT; break;
      case TYPE_FLOAT:		MatchingSQLType=SQL_FLOAT; break;
		case TYPE_REAL:		MatchingSQLType=SQL_REAL; break;
      case TYPE_DOUBLE:		MatchingSQLType=SQL_DOUBLE; break;
      case TYPE_VARCHAR:	MatchingSQLType=SQL_VARCHAR; break;
      case TYPE_LONGVARCHAR:	MatchingSQLType=SQL_VARCHAR; break;
      case TYPE_DATE:		MatchingSQLType=SQL_TYPE_DATE; break;
      case TYPE_TIME:		MatchingSQLType=SQL_TYPE_TIME; break;
      case TYPE_TIMESTAMP: MatchingSQLType=SQL_TYPE_TIMESTAMP; break;
      case TYPE_BINARY:		MatchingSQLType=SQL_BINARY; break;
      case TYPE_VARBINARY: MatchingSQLType=SQL_VARBINARY; break;
      case TYPE_LONGVARBINARY: MatchingSQLType=SQL_LONGVARBINARY; break;
      case TYPE_BIGINT:		MatchingSQLType=SQL_BIGINT; break;
      case TYPE_TINYINT:	MatchingSQLType=SQL_TINYINT; break;
      case TYPE_BIT:			MatchingSQLType=SQL_BIT; break;
		default:
	   	LogPrintf("Internal error: DataType not found, datatype=%d\n",DataType);
			exit(-1);
		}

	// Look through the linked list for the entry that matches
	found=FALSE;
	pSQLTypeInfo=gpSQLTypeInfoList;
	while((pSQLTypeInfo!=NULL)&&(!found)){
		if(pSQLTypeInfo->SQLDataType==MatchingSQLType) found=TRUE;
		else pSQLTypeInfo=pSQLTypeInfo->pNext;
		}

	if(!found){
   	LogPrintf("Internal error: no matching SQL datatype for datatype=%d, matchingtype=%d\n",DataType,MatchingSQLType);
   	exit(-1);
	}

	return(pSQLTypeInfo);

	} // end of FindSQLTypeInfo

/***********************************************************************
** Returns a SQLType that corresponds to the ODBC DataType passed in.
***********************************************************************/
short FindODBCType(short DataType)
{
	short MatchingODBCType;

	// find the matching SQL data type
	switch(DataType){
		case SQL_CHAR:			MatchingODBCType=TYPE_CHAR; break;
      case SQL_NUMERIC:		MatchingODBCType=TYPE_NUMERIC; break;
      case SQL_DECIMAL:		MatchingODBCType=TYPE_DECIMAL; break;
      case SQL_INTEGER:		MatchingODBCType=TYPE_INT; break;
      case SQL_SMALLINT:	MatchingODBCType=TYPE_SMALLINT; break;
      case SQL_FLOAT:		MatchingODBCType=TYPE_FLOAT; break;
		case SQL_REAL:			MatchingODBCType=TYPE_REAL; break;
      case SQL_DOUBLE:		MatchingODBCType=TYPE_DOUBLE; break;
      case SQL_VARCHAR:		MatchingODBCType=TYPE_VARCHAR; break;
      case SQL_TYPE_DATE:	MatchingODBCType=TYPE_DATE; break;
      case SQL_TYPE_TIME:	MatchingODBCType=TYPE_TIME; break;
      case SQL_TYPE_TIMESTAMP: MatchingODBCType=TYPE_TIMESTAMP; break;
      case SQL_LONGVARCHAR:MatchingODBCType=TYPE_VARCHAR; break;
      case SQL_BINARY:		MatchingODBCType=TYPE_BINARY; break;
      case SQL_VARBINARY:	MatchingODBCType=TYPE_VARBINARY; break;
      case SQL_LONGVARBINARY: MatchingODBCType=TYPE_LONGVARBINARY; break;
      case SQL_BIGINT:		MatchingODBCType=TYPE_BIGINT; break;
      case SQL_TINYINT:		MatchingODBCType=TYPE_TINYINT; break;
      case SQL_BIT:			MatchingODBCType=TYPE_BIT; break;
		default:
	   	LogPrintf("Internal error: ODBC DataType not found, datatype=%d\n",DataType);
			exit(-1);
		}

	return(MatchingODBCType);

	} // end of FindODBCType


/***********************************************************************
** Allocate a column structure in memory and initialize all the column
** fields, then return a pointer which points to the structure.
***********************************************************************/
ColumnInfo *AllocateCol(void)
{
  ColumnInfo *CPtr;

  CPtr = (ColumnInfo *)malloc(sizeof(ColumnInfo));
  memset(CPtr,-1,sizeof(ColumnInfo));
  CPtr->CName[0]          = '\0';
  CPtr->Literal           = NULL;
  CPtr->CHeading[0]       = '\0';
  CPtr->DataTypeLen       = RANDOM;
  return (CPtr);
}

/*******************************************************************
** Allocate 'n' column structures in one block of memory
*******************************************************************/
void InitializeColumns(TableInfo *TP)
{
  ColumnInfo *CP;
  ColumnInfo *DefaultColPtr;
  short j;

  /* allocate a block of contiguouse space for all column definitions */
  TP->ColPtr=(ColumnInfo *)malloc(TP->NumOfCol*sizeof(ColumnInfo));

  /* loop through, initializing each column definition */
  DefaultColPtr=AllocateCol();
  CP = TP->ColPtr;
  for (j = 0;j < TP->NumOfCol;j++) {
    memcpy(CP,DefaultColPtr,sizeof(ColumnInfo));
    CP++;
    }
  free(DefaultColPtr);
  }

/*******************************************************************
** Allocate 'n' key column structures in one block of memory
*******************************************************************/
void InitializeKeyColumns(TableInfo *TP)
{
  KeyDef *KP;
  short j;

  /* allocate a block of contiguouse space for all key column definitions */
  TP->KeyPtr=(KeyDef *)malloc(TP->KeyColCount*sizeof(KeyDef));

  /* loop through, initializing each key column definition */
  KP = TP->KeyPtr;
  for (j = 0;j < TP->KeyColCount;j++) {
    memset(KP,-1,sizeof(KeyDef));
    KP++;
    }
  }

/*********************************************************************
** Allocate one table structure and initialize all table fields, then
** return a pointer which points to the table structure.
*********************************************************************/
TableInfo *InitializeTableInfo(short NCol,short NKeyCol)
{
  TableInfo *Tptr;

  /* check input parameters for valid values */
  if ((NCol == 0) || (NKeyCol>NCol)) return(NULL);

  /* if caller specified this function should choose a random value for any...*/
  /*...of the input paramters then choose that random value now */
  if (NCol == RANDOM) NCol = RANDOM_NUM1(SQL_MAX_COLUMNS);
  if (NKeyCol == RANDOM) NKeyCol = RANDOM_NUM0(NCol);


  /* allocate and initialize the TableInfo structure (or 'object' for those...*/
  /*...who prefer a more C++ flavor) */
  Tptr                     = malloc(sizeof(TableInfo));
  Tptr->TableName[0]           = '\0';
  Tptr->TCatalog[0]        = '\0';
  Tptr->Organization       = KEY_SEQ;   /* SQL/MX & ODBC table type is always Key Seq. */

  /* initialize space for column information */
  Tptr->NumOfCol           = NCol;
  InitializeColumns(Tptr);

  /* initialize space for key column infomation */
  Tptr->KeyType            = RANDOM;
  Tptr->KeyColCount        = SQL_MAX_KEY_COLUMNS;
  if (Tptr->KeyColCount >=1) InitializeKeyColumns(Tptr);
  else Tptr->KeyPtr=NULL;
  Tptr->KeyColCount        = NKeyCol;

  /* >>>>Indexes are not supported for now */
  Tptr->IndexCount         = 0;
  Tptr->IndexPtr           = NULL;

  return(Tptr);
  } /* end: InitializeTableInfo() */

/***********************************************************************
** FreeTableInfo()
** This function returns all storage associated with the TableInfo
** structure.
************************************************************************/
void FreeTableInfo(TableInfo *TPtr)
{
   short i;
   ColumnInfo *CPtr;

   /* free all column infomation */
   CPtr=TPtr->ColPtr;
   for(i=0;i<TPtr->NumOfCol;i++){
      if(CPtr->Literal!=NULL) free(CPtr->Literal);
      CPtr++;
      }
   free(TPtr->ColPtr);

   /* free any key info */
   if(TPtr->KeyPtr!=NULL) free(TPtr->KeyPtr);

   /* free up any index info */
   if(TPtr->IndexPtr!=NULL) free(TPtr->IndexPtr);

   /* finally, free the TableInfo structure */
   free(TPtr);

   } /* end: FreeTableInfo() */

/***********************************************************************
** CopyTableInfo()
**
** This function will copy the contents of a table info structure.
************************************************************************/
void CopyTableInfo(TableInfo *ToPtr,TableInfo *FromPtr)
{
   ColumnInfo *ToColPtr;
   ColumnInfo *FromColPtr;
   short i;

   /* First copy the basic information */
   strcpy(ToPtr->TableName,FromPtr->TableName);
   strcpy(ToPtr->TCatalog,FromPtr->TCatalog);
   ToPtr->Organization=FromPtr->Organization;
   ToPtr->KeyType=FromPtr->KeyType;
   ToPtr->RowLength=FromPtr->RowLength;

   /* copy the Column information */
   memcpy(ToPtr->ColPtr,FromPtr->ColPtr,
          (sizeof(ColumnInfo)*FromPtr->NumOfCol));

   FromColPtr=FromPtr->ColPtr;
   ToColPtr=ToPtr->ColPtr;
   for(i=0;i<FromPtr->NumOfCol;i++){

      if(FromColPtr->Literal!=NULL){
         ToColPtr->Literal=(char *)malloc(strlen(FromColPtr->Literal)+1);
         strcpy(ToColPtr->Literal,FromColPtr->Literal);
         }

      FromColPtr++;
      ToColPtr++;
      }

   /* Copy any Key definitions */
   if(FromPtr->KeyColCount!=0){
      memcpy(ToPtr->KeyPtr,FromPtr->KeyPtr,
             (sizeof(KeyDef)*FromPtr->KeyColCount));
      }

   /* copy index definitions >>>>indexes NOT supported, yet */

   } /* end: CopyTableInfo() */


/****************************************************************************
** FillColumnInfo()
**
** This function will randomly fill in any unspecified column attributes in
** the ColumnInfo structure.  Any attributes previously set by the caller will
** not be altered in any way.
*****************************************************************************/
void FillColumnInfo(ColumnInfo *ColumnPtr)
{
   char Literal[SQL_MAX_CHAR_COLUMN_LENGTH];
   long LiteralLength;
	char *TempStr;

   /* if no column name then randomly create one */
   if (ColumnPtr->CName[0] == '\0') {
		TempStr=RandomString((short)RANDOM_NUM1(SQL_MAX_COL_NAME));
		strcpy(ColumnPtr->CName,TempStr);
		free(TempStr);
		}

   /* Randomly fill in ODBC data type attributes where none were specified */
   if (ColumnPtr->DataType == RANDOM) {
      ColumnPtr->DataType = RandomODBCDataType();
      }
	ColumnPtr->pTypeInfo=FindSQLTypeInfo(ColumnPtr->DataType);

	switch (ColumnPtr->DataType) {

     case TYPE_CHAR:
     case TYPE_VARCHAR:
     case TYPE_LONGVARCHAR:
     case TYPE_BINARY:
     case TYPE_VARBINARY:
     case TYPE_LONGVARBINARY:
			if (ColumnPtr->DataTypeLen == RANDOM){
            ColumnPtr->DataTypeLen = RANDOM_NUM1(ColumnPtr->pTypeInfo->ColumnSize);
				}

          /* Tandem SQL/MP Restriction */
          /* a character literal cannot be longer than 8 characters */
          if(ColumnPtr->DataTypeLen<8) LiteralLength=ColumnPtr->DataTypeLen;
          else LiteralLength=8;
          strcpy(Literal,RandomString((short)RANDOM_NUM1(LiteralLength)));
          break;

     case TYPE_NUMERIC:
     case TYPE_DECIMAL:
          if (ColumnPtr->DataTypeLen == RANDOM)
            ColumnPtr->DataTypeLen = RANDOM_NUM1(ColumnPtr->pTypeInfo->ColumnSize);
          if (ColumnPtr->DataTypeScale == RANDOM){
				 if(ColumnPtr->pTypeInfo->MaxScale<=ColumnPtr->DataTypeLen){
					ColumnPtr->DataTypeScale = RANDOM_RANGE(ColumnPtr->pTypeInfo->MinScale,ColumnPtr->pTypeInfo->MaxScale);
					}
				else{
	            ColumnPtr->DataTypeScale = (short)RANDOM_RANGE(ColumnPtr->pTypeInfo->MinScale,ColumnPtr->DataTypeLen);
					}
				 }
          ColumnPtr->UnsignedColumn = ColumnPtr->pTypeInfo->UnsignedAttr;
          /* (10) to (18) must always be SIGNED >>>is this just for SQL/MP only?*/
          //if(ColumnPtr->DataTypeLen>=10) ColumnPtr->UnsignedColumn=TRUE;
          strcpy(Literal,"1");
          break;

     case TYPE_TINYINT:
     case TYPE_SMALLINT:
     case TYPE_INT:
     case TYPE_BIGINT:
     case TYPE_REAL:
     case TYPE_DOUBLE:
     case TYPE_FLOAT:
          ColumnPtr->UnsignedColumn = ColumnPtr->pTypeInfo->UnsignedAttr;
          ColumnPtr->DataTypeLen = ColumnPtr->pTypeInfo->ColumnSize;
          strcpy(Literal,"1");
          break;


     // NOTE: ColumnSize for DATE,TIME, and TIMESTAMP is not returned
     //       by SQLGetTypeInfo so we hard code the values here
	  case TYPE_DATE:
          ColumnPtr->pTypeInfo->ColumnSize=10;
          ColumnPtr->DataTypeLen=ColumnPtr->pTypeInfo->ColumnSize;
          strcpy(Literal,RandomODBCDateTimeLiteral(TYPE_DATE));
          break;

     case TYPE_TIME:
          ColumnPtr->pTypeInfo->ColumnSize=8;
          ColumnPtr->DataTypeLen=ColumnPtr->pTypeInfo->ColumnSize;
          strcpy(Literal,RandomODBCDateTimeLiteral(TYPE_TIME));
          break;

     case TYPE_TIMESTAMP:
          ColumnPtr->pTypeInfo->ColumnSize=26;
          ColumnPtr->DataTypeLen=ColumnPtr->pTypeInfo->ColumnSize;
          strcpy(Literal,RandomODBCDateTimeLiteral(TYPE_TIMESTAMP));
          break;

     } /* switch datatype statement */

   if (ColumnPtr->DefaultType == RANDOM) {
     switch(RANDOM_NUM1(3)){
        case 1: ColumnPtr->DefaultType=COL_DEFAULT_NULL; break;
        case 2: ColumnPtr->DefaultType=COL_DEFAULT_NONE; break;
        case 3: ColumnPtr->DefaultType=COL_DEFAULT_LITERAL; break;
//        case 4: ColumnPtr->DefaultType=COL_DEFAULT_USER; break;
        } /* end switch */
     }

/*>>>> something should be done here, to generate better literals */
   if(ColumnPtr->DefaultType==COL_DEFAULT_LITERAL){
      ColumnPtr->Literal=(char *)malloc(strlen(Literal)+1);
      strcpy(ColumnPtr->Literal,Literal);
      } /* end if */

   if (ColumnPtr->Nullable == RANDOM)
      ColumnPtr->Nullable = RANDOM_T_OR_F;

   } /* end FillColumnInfo() */

/***********************************************************************
** GetColumnNumber()
**
** This function will search through the list of column structures for a
** table and return the column number (one based) for the one with the
** matching column name.  If no match is found, FAILURE is returned.
** The search is case insensitive.
************************************************************************/
extern short GetColumnNumber(TableInfo *pTable,char *CPtr)
{
   char UpperCaseName1[SQL_MAX_COL_NAME];
   char UpperCaseName2[SQL_MAX_COL_NAME];
   short i;
	ColumnInfo *ColumnListPtr;

	ColumnListPtr=pTable->ColPtr;
	strcpy(UpperCaseName1,CPtr);
   toupper_s(UpperCaseName1);
   for(i=0;i<pTable->NumOfCol;i++){
      strcpy(UpperCaseName2,ColumnListPtr->CName);
      toupper_s(UpperCaseName2);
      if(strcmp(UpperCaseName1,UpperCaseName2)==0) return(i+1);
      ColumnListPtr++;
      }

   /* matching column name not found */
   return(FAILURE);
	} // end GetColumnNumber()

/***********************************************************************
** GetColumnInfoByName()
**
** This function will search through an array of column info structures
** and return a pointer to the one with the matching column name.  If
** not match is found, NULL is returned.
************************************************************************/
ColumnInfo *GetColumnInfoByName(ColumnInfo *ColumnListPtr,short ColumnCount,
                                char *CPtr)
{
   char UpperCaseName1[SQL_MAX_COL_NAME];
   char UpperCaseName2[SQL_MAX_COL_NAME];
   short i;

   strcpy(UpperCaseName1,CPtr);
   toupper_s(UpperCaseName1);
   for(i=0;i<ColumnCount;i++){
      strcpy(UpperCaseName2,ColumnListPtr->CName);
      toupper_s(UpperCaseName2);
      if(strcmp(UpperCaseName1,UpperCaseName2)==0) return(ColumnListPtr);
      ColumnListPtr++;
      }

   /* matching column name not found */
   return(NULL);
   } /* end: GetColumnInfoByName() */

/***********************************************************************
** ChooseKeyColumns()
**
** This function will randomly choose which columns will be used for the
** key.  It will attempt to use the number of key columns requested
** unless it cannot build a key that is less than the maximum key length.
** In which case it will use as many columns as possible to build the
** key without exceeding the maximum key length.  It will also set
** whether the column is ascending or descending.
************************************************************************/
void ChooseKeyColumns(TableInfo *TPtr)
{
   KeyDef *KPtr;
   long KeyLength;
   short KeyLengthMax;
   short i,j;
   short temp;
   short ColumnCount;
   short ActualKeyColCount;
   short Columns[SQL_MAX_COLUMNS];

   /* set the maximum key length allowed */
   /* Primary key = 255 */
   /*>>>> unique index = 253 */
   /*>>>> nonunique index = 253-primary key */
   if(TPtr->KeyType==PRIMARY_KEY) KeyLengthMax=255;
   else KeyLengthMax=247;

   /* build a list of columns to choose a key from.  */
   /*>>> NOTE: Could optimize this by not includiing any */
   /*>>> columns that exceed the maximum key length because they could not */
   /*>>> be part of the key anyway */
   for(i=0;i<TPtr->NumOfCol;i++) Columns[i]=i;
   ColumnCount=TPtr->NumOfCol;

   /* see if the user has chosen some key columns already and if so, */
   /* compute the key length */
   ActualKeyColCount=0;
   KPtr=TPtr->KeyPtr;
   KeyLength=0;
   for(i=0;i<TPtr->KeyColCount;i++){
      if(KPtr->ColNum!=RANDOM){
         KeyLength+=(TPtr->ColPtr+(KPtr->ColNum))->DataTypeLen;
         ActualKeyColCount++;

         /* remove it from the list of column choices for keys */
         temp=0;
         while((KPtr->ColNum!=Columns[temp])&&(temp<ColumnCount)) temp++;

         /*>>> if temp==ColumnCount then caller specified an invalid key */
         /*>>> column number.  We really should figure out what to do in */
         /*>>> that case. */

         for(j=temp;j+1<ColumnCount;j++) Columns[j]=Columns[j+1];
         ColumnCount--;
         }
      KPtr++;
      }

   /* loop until we have the number of key columns we wanted or until */
   /* we run out of columns to choose from */
   i=ActualKeyColCount;
   KPtr=TPtr->KeyPtr;
   while((i<TPtr->KeyColCount)&&(ColumnCount!=0)){

      /* choose a key column, if not selected by the user already */
      if(KPtr->ColNum==RANDOM){
         temp=RANDOM_NUM0(ColumnCount);
         KPtr->ColNum=Columns[temp];


         /* remove it from the list of column choices */
         for(j=temp;j+1<ColumnCount;j++) Columns[j]=Columns[j+1];
         ColumnCount--;


         /* see if this key column will make the total key length exceed */
         /* the maximum key length.  If it doesn't then we can use this one */
         /* for part of the key */
         if((KeyLength+(TPtr->ColPtr+(KPtr->ColNum))->DataTypeLen) <=
             KeyLengthMax){
            ActualKeyColCount++;
            KeyLength+=(TPtr->ColPtr+(KPtr->ColNum))->DataTypeLen;
            KPtr->ColNum=temp;
            KPtr++;
            i++;
            }
         }
      else {
         KPtr++;
         i++;
         }
      } /* end: while */

   /* it might have been the case that we could not select the requested */
   /* number of key columns because the maximum key length would have */
   /* been exceed no matter which combination of columns were chosen */
   /* So, we'll adjust the key column count here to be the actual count */
   TPtr->KeyColCount=ActualKeyColCount;

   /* setup the ordering (ascending/decending) for each key column */
   KPtr=TPtr->KeyPtr;
   for (i = 0;i < TPtr->KeyColCount;i++){
      if (KPtr->AscDesc == RANDOM) KPtr->AscDesc=RANDOM_NUM1(2);
		// each key column cannot be NULL
		(TPtr->ColPtr+(KPtr->ColNum))->Nullable=FALSE;
      KPtr++;
      }

   } /* end: ChooseKeyColumns() */


/**************************************************************************
** FillTableInfo()
**
** This function fills in all empty information in the table structure
***************************************************************************/
void FillTableInfo (TableInfo *TP)
{
  short i;
  short SpaceRemaining;
  short MaxColumnSize;
  Boolean UserSuppliedLength;
  Boolean UserSuppliedName;
  ColumnInfo *CurrentCptr;
  char TableNum[8] = {"0000000"};
  short ActualColCount;
  Boolean done;

  /***** Table Name (default format: T00nnnnn) *****/
  if (TP->TableName[0] == '\0') {
    strcpy(TP->TableName,"T");
    sprintf(TableNum,"%06d",rand());
    strcat(TP->TableName,TableNum);
    }

  /***** Table Organization *****/
  /* cannot be set on create */

  /***** Columns *****/
  CurrentCptr = TP->ColPtr;
  ActualColCount = 1;
  TP->RowLength = 0;
  for(i=0;i<TP->NumOfCol;i++){

    if(CurrentCptr->DataTypeLen!=RANDOM) UserSuppliedLength=TRUE;
    else UserSuppliedLength=FALSE;

    if(CurrentCptr->CName[0]!='\0') UserSuppliedName=TRUE;
    else UserSuppliedName=FALSE;

    /* fill in column info making sure we don't have a duplicate name */
    /* allow duplicates in the case of user supplied names */
    done=FALSE;
    do{
       FillColumnInfo(CurrentCptr);
       if(UserSuppliedName) done=TRUE;
       else {
          if(GetColumnInfoByName(TP->ColPtr,i,CurrentCptr->CName)==NULL){
             done=TRUE;
             }
          /* have to zero the column name otherwise FillColumnInfo() will */
          /* not provide another name when it is called again because it */
          /* think the name was supplied by the user */
          else CurrentCptr->CName[0]='\0';
          }
       }while(!done);

    /* We need to adjust some datatype columns' length to */
    /* insure we have enough remaining space in the record to accomodate */
    /* the columns yet to be determined, however, only adjust those columns */
    /* which the caller did NOT supply the length */
    if(!UserSuppliedLength){

       SpaceRemaining = (short)(gMaxRowSize - TP->RowLength);
       MaxColumnSize=SpaceRemaining/(TP->NumOfCol-i);
       if(MaxColumnSize<1) MaxColumnSize=1;

       if(CurrentCptr->DataTypeLen>MaxColumnSize){

          switch(CurrentCptr->DataType){
             case TYPE_CHAR:
             case TYPE_VARCHAR:
             case TYPE_BINARY:
             case TYPE_VARBINARY:
             case TYPE_LONGVARBINARY:
                CurrentCptr->DataTypeLen=MaxColumnSize;
                break;

/*             case TYPE_NUMERIC:
             case TYPE_DECIMAL:
                CurrentCptr->DataTypeLen=MaxColumnSize;
                CurrentCptr->DataTypeScale = (short)RANDOM_NUM0(CurrentCptr->DataTypeLen);
                break;
*/
             /* don't adjust the size if not any of the above SQL types */

             } /* end: switch on datatype */

          } /* end: if length > maxcolumnsize */

       } /* end: if not UserSuppliedLength */

    TP->RowLength+=CurrentCptr->DataTypeLen;
	 AllocateValueBuffer(CurrentCptr);
	 // >>>>check for errors??


    /* move to next column */
    CurrentCptr++;
    ActualColCount++;

    } /* end: for each column */

  /***** Key Field *****/
  if (TP->KeyType == RANDOM){
/*>>> does this really matter for ODBC ? */
     }

  /* choose which columns will be key columns, if needed */
  ChooseKeyColumns(TP);

  } /* end: FillTableInfo() */


/***********************************************************************
** BuildColumnString()
**
** This function returns a string pointer which contains an ASCII
** representation of the column definition passed in as input to this
** function.
************************************************************************/
char *BuildColumnString(ColumnInfo *ColumnPtr)
{
  char buffer[2048];  /* should be large enough to hold a column's info */
  short clen;
  char *TempPtr;

  strcpy(buffer,ColumnPtr->CName);

  switch (ColumnPtr->DataType) {

    case TYPE_CHAR:
    case TYPE_VARCHAR:
    case TYPE_LONGVARCHAR:
    case TYPE_BINARY:
    case TYPE_VARBINARY:
    case TYPE_LONGVARBINARY:
         clen = (short)strlen(buffer);
         sprintf(&buffer[clen]," %s(%ld)",ColumnPtr->pTypeInfo->TypeName,
				ColumnPtr->DataTypeLen);
         break;

    case TYPE_NUMERIC:
    case TYPE_DECIMAL:
         clen = (short)strlen(buffer);
         sprintf(&buffer[clen]," %s(%ld,%d)",ColumnPtr->pTypeInfo->TypeName,
				ColumnPtr->DataTypeLen,ColumnPtr->DataTypeScale);
         clen = (short)strlen(buffer);

         break;

    case TYPE_BIT:
    case TYPE_TINYINT:
    case TYPE_SMALLINT:
    case TYPE_INT:
    case TYPE_BIGINT:
    case TYPE_FLOAT:
    case TYPE_REAL:
    case TYPE_DOUBLE:
    case TYPE_DATE:
    case TYPE_TIME:
    case TYPE_TIMESTAMP:
         clen = (short)strlen(buffer);
         sprintf(&buffer[clen]," %s",ColumnPtr->pTypeInfo->TypeName);
         break;

    } /*switch on data type*/

  switch (ColumnPtr->DefaultType) {
    case COL_DEFAULT_NULL:
      clen = (short)strlen(buffer);
      printf(&buffer[clen]," default null");
      break;
    case COL_DEFAULT_USER:
      clen = (short)strlen(buffer);
      sprintf(&buffer[clen]," default user");
      break;
    case COL_DEFAULT_LITERAL:
      clen = (short)strlen(buffer);
      switch (ColumnPtr->DataType) {
         case TYPE_CHAR:
         case TYPE_VARCHAR:
           sprintf(&buffer[clen]," default '%s'",ColumnPtr->Literal);
           break;
         case TYPE_NUMERIC:
         case TYPE_BIT:
         case TYPE_TINYINT:
         case TYPE_BIGINT:
         case TYPE_SMALLINT:
         case TYPE_INT:
         case TYPE_FLOAT:
         case TYPE_REAL:
         case TYPE_DOUBLE:
         case TYPE_DECIMAL:
         case TYPE_DATE:
         case TYPE_TIME:
         case TYPE_TIMESTAMP:
            sprintf(&buffer[clen]," default %s",ColumnPtr->Literal);
            break;
         } /*switch*/
      break;

    case COL_DEFAULT_NONE:
       break;

    }  /*switch defaulttype*/

  if (!(ColumnPtr->Nullable)) {
    clen = (short)strlen(buffer);
    sprintf(&buffer[clen]," not null");
    }

  buffer[strlen(buffer)]='\0';

  /* <buffer> is a local array and shouldn't be returned so, allocate a...*/
  /*...buffer that can be returned */
  TempPtr=(char *)malloc(strlen(buffer)+1);
  strcpy(TempPtr,buffer);
  return(TempPtr);

  } /* end BuildColumnString() */


/************************************************************************
** Build the CREATE TABLE command according to the information in
** the table structure.
************************************************************************/
char *BuildCreateTableString (TableInfo *TP)
{

  short i;
  ColumnInfo *CurrentCptr;
  char *ColStrPtr;
  KeyDef *KPtr;
  char *command_line;
  char *StrPtr;

  /* Yes, it could be this big (maybe even bigger) */
  command_line=(char *)malloc(32767);

  sprintf(command_line,"Create Table %s ( ",TP->TableName);

  /* loop through each column definition building its string */
  CurrentCptr = TP->ColPtr;
  for(i=0;i<TP->NumOfCol;i++) {
    ColStrPtr=BuildColumnString(CurrentCptr);
    strcat(command_line,ColStrPtr);
    free(ColStrPtr);
    CurrentCptr++;
    if(i!=TP->NumOfCol-1){
       strcat(command_line," ,");
       }
    }

  /* build key string, if any */
  switch (TP->KeyType) {

     /* system defined key */
     case SYSTEM_KEY:
        strcat(command_line," )");
        break;

     /* primary key columns */
     case PRIMARY_KEY:
        if(TP->KeyColCount>0){
           strcat(command_line," ,primary key (");
           KPtr=TP->KeyPtr;
           for (i = 0;i < TP->KeyColCount;i++) {
              strcat(command_line,(TP->ColPtr+KPtr->ColNum)->CName);
              switch (KPtr->AscDesc) {
                 case KEY_ASC: strcat(command_line," asc"); break;
                 case KEY_DESC: strcat(command_line," desc"); break;
                 }  /*switch*/
              if (i < (TP->KeyColCount - 1)){
                 strcat(command_line," ,");
                 }
              else strcat(command_line," ) )");
              KPtr++;
              }
           }
        break;

     default:
        strcat(command_line," )");
        break;

     }  /* end: switch TP->KeyType */

  StrPtr=(char *)malloc(strlen(command_line)+1);
  strcpy(StrPtr,command_line);
  free(command_line);
  return(StrPtr);

  } /* end: BuildCreateTableString() */

