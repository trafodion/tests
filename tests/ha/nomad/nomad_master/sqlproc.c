/************************************************************************
** sqlproc.c
**
** This source module contains a collection of routines which work with
** SQL file information.
**
************************************************************************/

/******************
** Include files **
******************/
#include "defines.h"
#include "include.h"
#include "bitlib.h"
#include "table.h"
#include "mstruct.h"
#include "sqlutil.h"
#include "globals.h"
#include "ODBCcommon.h"

/***********************************************************************
** FormatForSQLCI()
**
** This function formats a long string into smaller strings that can
** then be used for input into a SQL Command Interpreter.
** It is used for debugging only.
************************************************************************/
void FormatForSQLCI(char *StrPtr)
{
   char LineOut[500];
   char *LinePtr;
   FILE *fp;

   LinePtr=LineOut;

   fp=fopen("DebugTrace.txt","a");
   if(fp==NULL){
      printf("Unable to open 'DEBUG' file\n");
      return;
      }

   fprintf(fp,"\n-- The following SQL statement generated an error.\n"
              "-- This file was created to aid in debugging as it can\n"
              "-- be used as input to a SQL Command Interpreter to help\n"
              "-- figure out why this statement caused an error.\n");

   while(*StrPtr!='\0'){
      *LinePtr=*StrPtr;
      if(*StrPtr==','){
         *++LinePtr='\0';
         fprintf(fp,"%s\n",LineOut);
         LinePtr=LineOut;
         }
      else{
         LinePtr++;
         }
      StrPtr++;
      }

   *LinePtr='\0';
   fprintf(fp,"%s\n;",LineOut);

   fclose(fp);

   } /* end: FormatForSQLCI() */


/***********************************************************************
** is_key_column()
**
** This function searches through the list of key columns and returns
** TRUE if the <column_number> specified is in the list, otherwise it
** returns FALSE.
************************************************************************/
Boolean is_key_column(TableDescription *table_ptr,short column_number)
{
   short i;
   key_info *temp_ptr;

   temp_ptr=table_ptr->NomadInfoPtr->key_ptr;

   /* search key column list */
   for(i=0;i<table_ptr->NomadInfoPtr->key_column_count;i++){
      if(column_number==temp_ptr->ColNum) return(TRUE);
      temp_ptr++;
      }

   return(FALSE);
   } /* end: is_key_column() */


/***********************************************************************
** SetKeyColumnValue2()
**
** This function sets the specified key value into the set of key columns.
** This function is needed in the case of multi-column keys.  One key column
** is set to the key value and all other key columns are set to a random
** default value.
************************************************************************/
ReturnStatus *SetKeyColumnValue2(TableDescription *tab_ptr,long KeyValue)
{
	key_info *pKey;
	ColumnInfo *pCol;
	char *pMessage;
	ReturnStatus *pReturnStatus;
	TableInfo *pTable;
	NomadInfo *pNomad;
	short i;
	RETCODE rc;

	pTable=tab_ptr->TableInfoPtr;
	pNomad=tab_ptr->NomadInfoPtr;
	pReturnStatus=NULL;

	// copy default values from key descriptions into column values
	pKey=pNomad->key_ptr;
	for(i=0;i<pTable->KeyColCount;i++){
		pCol=&(pTable->ColPtr[pKey->ColNum]);
		memcpy(pCol->Value.pChar,pKey->DefaultValue,pCol->DataTypeLen);
		pKey++;
		}

	// overlay the key column used with our key value
	pCol=&(pTable->ColPtr[pNomad->key_column_used]);
	memcpy(pCol->Value.pChar,&KeyValue,sizeof(KeyValue));
	rc=SQLBindParameter(tab_ptr->hstmt,(SQLUSMALLINT)((pNomad->key_column_used)+1),SQL_PARAM_INPUT,SQL_C_LONG,
		pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
		pCol->Value.pChar,0,NULL);
	pMessage=CHECKRC_STR(SQL_SUCCESS,rc,"SQLBindParameter");
	if(pMessage!=NULL){
		pReturnStatus=BuildReturnStatus(RT_ODBC,rc,pMessage,NULL);
		free(pMessage);
		if(gDebug) assert(FALSE);
		return(pReturnStatus);
		}

	return(pReturnStatus);
	}


/********************************************************************
** FindRequiredColumns()
**
** This function finds the required column numbers for the three
** required columns in an SQL table (in addition to any key columns).
** The three columns can be of any SQL data type EXCEPT date-time and
** can NOT be a key column.  The three columns are ZEROSUM, ABORT, and
** LAST PROCESS ID and are used for consistency checking and problem
** analysis.  While the key may be composed of several columns, there is
** the requirement that at least one column of the key MUST not be a
** date-time SQL data type and have a scale of 5 or greater.
**
** Input:
**    - TableDescription
********************************************************************/
ReturnStatus *FindRequiredColumns(TableDescription *table_ptr)
{
   short key_column[SQL_MAX_KEY_COLUMNS];
   TableInfo *TPtr;
   NomadInfo *NPtr;
   ReturnStatus *RSPtr;
   short column_number;
   short temp_size;
   Boolean done;
   key_info *tptr_key;
   short temp_data_type;
   short i;
   short memory_required;
   short unknown; /* counter for key column data types */


   /* initialize some pointers to save typing in long pointer names */
   TPtr=table_ptr->TableInfoPtr;
   NPtr=table_ptr->NomadInfoPtr;
   RSPtr=NULL;

   switch(TPtr->Organization){
      case RELATIVE_TABLE:
         NPtr->key_column_used=0;
         NPtr->key_column_count=1;
         NPtr->key_ptr=(key_info *)malloc(sizeof(key_info));
         if(NPtr->key_ptr==NULL) return(BuildReturnStatusMALLOC);
         NPtr->key_ptr->ColNum=0;
			memory_required=(short)TPtr->ColPtr[0].DataTypeLen;
         NPtr->key_ptr->DefaultValue=(char *)malloc(memory_required);
         if(NPtr->key_ptr->DefaultValue==NULL) return(BuildReturnStatusMALLOC);
         break;
      case ENTRY_SEQ:
         NPtr->key_column_used=
            ScanTableColumnsForNondatetime(TPtr,0);
         NPtr->key_column_count=1;
         NPtr->key_ptr=(key_info *)malloc(sizeof(key_info));
         if(NPtr->key_ptr==NULL) return(BuildReturnStatusMALLOC);
         NPtr->key_ptr->ColNum=NPtr->key_column_used;
			memory_required=(short)TPtr->ColPtr[NPtr->key_column_used].DataTypeLen;
         NPtr->key_ptr->DefaultValue=(char *)malloc(memory_required);
         if(NPtr->key_ptr->DefaultValue==NULL) return(BuildReturnStatusMALLOC);
         break;
      case KEY_SEQ:

			NPtr->key_column_count=TPtr->KeyColCount;
         for(i=0;i<NPtr->key_column_count;i++){
				key_column[i]=TPtr->KeyPtr[i].ColNum;
				}

         /* remove SYSKEY column from our key column list if it is there */
         /* because we ignore it when dealing with key sequenced tables */
         /* the SYSKEY column is always the first column of a table */
         /* SYSKEY is also the least significant key column of a clustering key */
         if((TPtr->KeyType==CLUSTERING_KEY) ||
            (TPtr->KeyType==SYSTEM_KEY)){
            for(i=0;i+1<NPtr->key_column_count;i++){
               key_column[i]=key_column[i+1];
               }
            NPtr->key_column_count--;
            }
			// check that we have at least one non-SYSKEY key to proceed
			if(NPtr->key_column_count<=0){
		      RSPtr=BuildReturnStatus(RT_PROGRAMERR,0,NULL,
		         "%s need at least one primary key column (other than SYSKEY) in '%s'.\n",
		         g_errstr,TPtr->TableName);
		      return(RSPtr);
			}

         /* allocate space for key column numbers */
         temp_size=NPtr->key_column_count*sizeof(key_info);
         NPtr->key_ptr=(key_info *)malloc(temp_size);
         if(NPtr->key_ptr==NULL) return(BuildReturnStatusMALLOC);

         /* set column numbers of key columns into TableDescription structure */
         unknown=0;
         NPtr->key_column_used=-1;
         tptr_key=NPtr->key_ptr;
         FillTableInfo(TPtr);

         for(i=0;i<NPtr->key_column_count;i++){
            tptr_key->ColNum=key_column[i];
				temp_data_type=TPtr->ColPtr[key_column[i]].pTypeInfo->SQLDataType;
				memory_required=(short)TPtr->ColPtr[key_column[i]].DataTypeLen;

            /* pick a key column to use as our record number key */
            /* NOTE: can NOT be a datetime data type and must be able to hold...*/
            /* ... a five digit value if any other SQL data type */
            /* The FIRST key column which meets our requirements will be chosen */
				switch(temp_data_type){

					case SQL_INTEGER:
					case SQL_SMALLINT:
					case SQL_FLOAT:
					case SQL_REAL:
					case SQL_DOUBLE:
					case SQL_BIGINT:
						if(NPtr->key_column_used==-1){
							NPtr->key_column_used=key_column[i];
							}
						break;

					case SQL_NUMERIC:
					case SQL_DECIMAL:
						if(TPtr->ColPtr[key_column[i]].DataTypePrecision>=5){
							if(NPtr->key_column_used==-1){
								NPtr->key_column_used=key_column[i];
								}
							}
						break;

					case SQL_CHAR:
					case SQL_VARCHAR:
					case SQL_LONGVARCHAR:
						if(TPtr->ColPtr[key_column[i]].DataTypeLen>=5){
							if(NPtr->key_column_used==-1){
								NPtr->key_column_used=key_column[i];
								}
							}
						memory_required++;	// add byte for NULL terminator
						break;

					case SQL_BINARY:
					case SQL_VARBINARY:
					case SQL_LONGVARBINARY:
						if(TPtr->ColPtr[key_column[i]].DataTypeLen>=5){
							if(NPtr->key_column_used==-1){
								NPtr->key_column_used=key_column[i];
								}
							}
						break;

					// These types can't be used for the record number key column
					case SQL_DATE:
					case SQL_TIME:
					case SQL_TIMESTAMP:
					case SQL_TINYINT:
					case SQL_BIT:

					/* an unknown data type */
					default:
						unknown++;

					} /* end switch */

				/* allocate space for the constant value used for key columns */
            /* in the case of more than one column in the key.  We will select */
            /* one column to use and the others will have a fixed value */
            tptr_key->DefaultValue=(char *)malloc(memory_required);
            if(tptr_key->DefaultValue==NULL) return(BuildReturnStatusMALLOC);

            /* save a random fixed value to use for this key column */
            memcpy(tptr_key->DefaultValue,
                   TPtr->ColPtr[key_column[i]].Value.pChar,
                   memory_required);
            tptr_key++;
            }
            break;
      } /* end: switch on file type */

   /* check that we found a key column to use that met our requirements */
   if(NPtr->key_column_used<=-1){
      RSPtr=BuildReturnStatus(RT_PROGRAMERR,0,NULL,
         "%s ONE column of the key MUST meet these requirements:\n"
         "        o  NOT be an SQL date-time or interval data type\n"
         "        o  if NUMERIC or DECIMAL it MUST have precision >= 5\n"
         "        o  if any CHAR or BINARY types it MUST have length >= 5\n"
         "   Hey, who knows why...ask my boss...at any rate I wasn't able to find\n"
         "   a column within the key of table '%s'\n"
         "   that met all those lofty requirements.\n"
         "   I know you already know what this means but, I'm going to tell you\n"
         "   anyway, just to make it official: 'I can't use this table'\n"
         "   Change the key for this table or give me another table\n\n",
         g_errstr,TPtr->TableName);
      return(RSPtr);
      }

   /* scan fields looking for 16 bit (or larger) short field to be zerosum */
   column_number=0;
   done=FALSE;
	column_number=ScanTableColumnsForNumber(TPtr,column_number);
   while((!done) && (column_number>=0)) {

      /* make sure the column is large enough to hold the zerosum values */
      if(TPtr->ColPtr[column_number].DataTypePrecision>=5){

         /* make sure its not one of the columns of the key */
         if(is_key_column(table_ptr,column_number)) {
         	column_number++;
				column_number=ScanTableColumnsForNumber(TPtr,column_number);
      	   }
         else done=TRUE;
         }
      else {
      	column_number++;
      	column_number=ScanTableColumnsForNumber(TPtr,column_number);
	      }
      }

   if(column_number<0){
      RSPtr=BuildReturnStatus(RT_PROGRAMERR,0,NULL,
         "%s unable to find two numeric columns and one non-datetime\n"
         "   column that are not part of the key\n",
         g_errstr);
      return(RSPtr);
      }

   NPtr->zerosum_column=column_number;


   /* scan fields looking for 16 bit (or larger) short field to be abort */
   column_number=0;
   done=FALSE;
	column_number=ScanTableColumnsForNumber(TPtr,column_number);
   while(!done) {

		/* make sure its not one of the columns of the key or zerosum */
      if((is_key_column(table_ptr,column_number))||
         (column_number==NPtr->zerosum_column)){
				column_number++;
				column_number=ScanTableColumnsForNumber(TPtr,column_number);
            }
      else done=TRUE;
      }

   if(column_number<0){
      RSPtr=BuildReturnStatus(RT_PROGRAMERR,0,NULL,
         "%s unable to find two numeric columns and one non-datetime\n"
         "   column that are not part of the key\n",
         g_errstr);
      return(RSPtr);
      }

   NPtr->abort_column=column_number;


   /* scan fields looking for any non-date-time column to be process-id */
   column_number=0;
   done=FALSE;
	column_number=ScanTableColumnsForNumber(TPtr,column_number);
   while(!done) {

      /* make sure its not one of the columns of the key, zerosum, or ...*/
      /*...abort columns */
      if((is_key_column(table_ptr,column_number))||
         (column_number==NPtr->zerosum_column)||
         (column_number==NPtr->abort_column)){
            column_number++;
				column_number=ScanTableColumnsForNumber(TPtr,column_number);
            }
      else done=TRUE;
      }

   if(column_number<0){
      RSPtr=BuildReturnStatus(RT_PROGRAMERR,0,NULL,
         "%s unable to find three numeric columns that are not part of the key\n",
         g_errstr);
      return(RSPtr);
      }
   NPtr->last_process_id_column=column_number;

   return(NULL);
   } /* end: FindRequiredColumns() */

/***********************************************************************
** FreeNomadInfo()
**
** This function will return the space of a NomadInfo structure.
************************************************************************/
void FreeNomadInfo(NomadInfo *NPtr)
{
   if(NPtr->key_ptr!=NULL) free(NPtr->key_ptr);
   if(NPtr->BitmapPtr!=NULL) FreeBitmap(NPtr->BitmapPtr);
   free(NPtr);
   } /* end: FreeNomadInfo() */

/***********************************************************************
** FreeTableDesc()
**
** This function will return the space of a Table Description structure.
************************************************************************/
void FreeTableDesc(TableDescription *TPtr)
{
   if(TPtr->NomadInfoPtr!=NULL) FreeNomadInfo(TPtr->NomadInfoPtr);
   if(TPtr->TableInfoPtr!=NULL) FreeTableInfo(TPtr->TableInfoPtr);
   free(TPtr);
   } /* end: FreeTableDesc() */


/***********************************************************************
** GetExistingTableDesc()
**
** This function will attempt to get various pieces of information about
** a given table name.  The table name needs to be fully qualified.
** A pointer to the table's description is returned.
************************************************************************/
TableDescription *GetExistingTableDesc(HDBC hdbc,char *table_name,ReturnStatus **RSPtr)
{
   TableDescription *table_ptr;
   TableInfo *TPtr;
//  char FullTableName[SQL_MAX_TABLE_NAME_LEN+1];

   *RSPtr=NULL;

   /* allocate space for the table description and initialize it */
   table_ptr=(TableDescription *)malloc(sizeof(TableDescription));
   memset(table_ptr,0,sizeof(TableDescription));

   /* make name into fully-qualified name, if it already isn't */
/*   error=FILENAME_RESOLVE_(table_name,(short)strlen(table_name),
                           FullTableName,(short)sizeof(FullTableName),
                           &fullname_length);
   FullTableName[fullname_length]=NULL;
   if(error){
      printf("%s File System error %d returned from FILENAME_RESOLVE_\n",
             g_errstr,error);
      free(table_ptr);
      return(NULL);
      }
*/

   /* allocate space for NOMAD specific information (used later) */
   table_ptr->NomadInfoPtr=(NomadInfo *)malloc(sizeof(NomadInfo));
   memset(table_ptr->NomadInfoPtr,0,sizeof(NomadInfo));

   /* allocate space for table's info and fill it in with data */
   table_ptr->TableInfoPtr=GetTableInfo(hdbc,table_name,FALSE,RSPtr);
   TPtr=table_ptr->TableInfoPtr;
   if(TPtr==NULL) {
      FreeTableDesc(table_ptr);
      return(NULL);
   }

   /* set other info values about the table */
/*   switch(result.filetype){
      case 1: TPtr->Organization=RELATIVE; break;
      case 2: TPtr->Organization=ENTRY_SEQ; break;
      case 0: // 0 mean unstructured file which we default to key-seq
      case 3: TPtr->Organization=KEY_SEQ; break;
      }
*/

/*>>>>might need to set additional NomadInfo values here */

   /* find required columns to use for key, zerosum, abort and... */
   /* ...last process id columns */
   *RSPtr=FindRequiredColumns(table_ptr);
   if(*RSPtr!=NULL){
      FreeTableDesc(table_ptr);
      return(NULL);
      }
   return(table_ptr);
   } /* end: GetExistingTableDesc() */

/***********************************************************************
** InitializeTableDesc()
**
** This function will allocate the TableDescription structure and all its
** substructures based upon the inputs specified.
************************************************************************/
TableDescription *InitializeTableDesc(short ColumnCount,short KeyColCount,
                                      short PartitionCount,
                                      short IndexCount,short IndexColumnCount,
                                      short IndexPartitionCount)
{
   TableDescription *TablePtr;

   /*>>>> These are here to prevent warning messages and will be */
   /*>>>> removed when indexes are fully supported */
   IndexCount=0;
   IndexColumnCount=0;
   IndexPartitionCount=0;

   TablePtr=(TableDescription *)malloc(sizeof(TableDescription));

   TablePtr->TableInfoPtr=InitializeTableInfo(ColumnCount,KeyColCount);

   TablePtr->NomadInfoPtr=(NomadInfo *)malloc(sizeof(NomadInfo));
   memset(TablePtr->NomadInfoPtr,0,sizeof(NomadInfo));

   return(TablePtr);
   } /* end: InitializeTableDesc() */

/***********************************************************************
** RandomNumericType()
**
** This function will return a random SQL data type.
************************************************************************/
short RandomNumericType(void)
{
   switch(RANDOM_NUM0(7)){
      case 0:return(TYPE_NUMERIC);
      case 1:return(TYPE_SMALLINT);
      case 2:return(TYPE_INT);
      case 3:return(TYPE_BIGINT);
      case 4:return(TYPE_FLOAT);
      case 5:return(TYPE_REAL);
      case 6:return(TYPE_DOUBLE);
      case 7:return(TYPE_DECIMAL);
      }

   /* not that we'll ever get here but, it does get rid of a warning */
   return(TYPE_SMALLINT);

   } /* end: RandomNumericType() */


/***********************************************************************
** RandomNonDateTimeType()
**
** This function will return a random SQL data type that is NOT a
** datetime or interval data type.
************************************************************************/
short RandomNonDateTimeType(void)
{
   switch(RANDOM_NUM0(9)){
      case 0:return(TYPE_CHAR);
      case 1:return(TYPE_VARCHAR);
      case 2:return(TYPE_NUMERIC);
      case 3:return(TYPE_SMALLINT);
      case 4:return(TYPE_INT);
      case 5:return(TYPE_BIGINT);
      case 6:return(TYPE_FLOAT);
      case 7:return(TYPE_REAL);
      case 8:return(TYPE_DOUBLE);
      case 9:return(TYPE_DECIMAL);
      }

   /* not that we'll ever get here but, it does get rid of a warning */
   return(TYPE_SMALLINT);

   } /* end: RandomNonDateTimeType() */


/***********************************************************************
** FillTableDesc()
**
** This function will randomly fill in all the information needed in the
** TableDescription structure.
************************************************************************/
void FillTableDesc(TableDescription *TablePtr)
{
   TableInfo *TPtr;
   KeyDef *KPtr;
   ColumnInfo *CPtr;
   short i,j;
   short temp;
   short AbortColumn;
   short ZerosumColumn;
   short LastIdColumn;
   short Column[SQL_MAX_COLUMNS];
   short ColumnCount;
   short KeyLengthMax;
   short KeyLength;
   short ActualKeyColCount;

   TPtr=TablePtr->TableInfoPtr;

   /* build a list of all columns */
   for(i=0;i<TPtr->NumOfCol;i++) Column[i]=i;
   ColumnCount=TPtr->NumOfCol;

   /* if entry seq. or relative table then the key column is always */
   /* added by the system and is a system key and always column 0 */
   /* need to adjust the column count to allow for the addition of */
   /* a system key and still keep the same column count */
   if(TPtr->Organization==ENTRY_SEQ || TPtr->Organization==RELATIVE_TABLE){
      TPtr->KeyType=SYSTEM_KEY;
      ColumnCount--;
      }

   else {
      /* NOMAD cannot work with a key seq. table that has only a system */
      /* key so, make the key type either primary or clustering */
      if(RANDOM_T_OR_F) {
         TPtr->KeyType=PRIMARY_KEY;
         KeyLengthMax=255;
         }
      else {
         TPtr->KeyType=CLUSTERING_KEY;
         KeyLengthMax=247;
         }
      }

   /* Randomly pick a column to be a numeric data type for the abort column */
   temp=RANDOM_NUM0(ColumnCount-1);
   AbortColumn=Column[temp];
   CPtr=TPtr->ColPtr+AbortColumn;
   CPtr->DataType=RandomNumericType();

   /* if type is NUMERIC, DECIMAL, or PIC then make sure the length */
   /* and/or scale is set to a value NOMAD can use */
   if((CPtr->DataType==TYPE_NUMERIC)||(CPtr->DataType==TYPE_DECIMAL)){
      CPtr->DataTypeLen=RANDOM_RANGE(5,18);
      CPtr->DataTypeScale=0;
      }

   /* remove that column number from the list of column choices */
   for(i=temp;i+1<ColumnCount;i++) Column[i]=Column[i+1];
   ColumnCount--;

   /* Randomly pick a column to be a numeric data type for zerosum column */
   temp=RANDOM_NUM0(ColumnCount-1);
   ZerosumColumn=Column[temp];
   CPtr=TPtr->ColPtr+ZerosumColumn;
   CPtr->DataType=RandomNumericType();

   /* if type is NUMERIC, DECIMAL, or PIC then make sure the length */
   /* and/or scale is set to a value NOMAD can use */
   if((CPtr->DataType==TYPE_NUMERIC)||(CPtr->DataType==TYPE_DECIMAL)){
      CPtr->DataTypeLen=RANDOM_RANGE(5,18);
      CPtr->DataTypeScale=0;
      }

   /* remove that column number from the list of column choices */
   for(i=temp;i+1<ColumnCount;i++) Column[i]=Column[i+1];
   ColumnCount--;

   /* Randomly pick a column to be a numeric data type for last-id column */
   temp=RANDOM_NUM0(ColumnCount-1);
   LastIdColumn=Column[temp];
   CPtr=TPtr->ColPtr+LastIdColumn;
   CPtr->DataType=RandomNonDateTimeType();

   /* if type is NUMERIC, DECIMAL, PIC, CHAR, VCHAR, or PICX then make */
   /* sure the length and/or scale is set to a value NOMAD can use */
   if((CPtr->DataType==TYPE_NUMERIC)||
      (CPtr->DataType==TYPE_DECIMAL)||
      (CPtr->DataType==TYPE_CHAR)||
      (CPtr->DataType==TYPE_VARCHAR)){

      CPtr->DataTypeLen=RANDOM_RANGE(5,18);
      CPtr->DataTypeScale=0;
      }

   /* remove that column number from the list of column choices */
   for(i=temp;i+1<ColumnCount;i++) Column[i]=Column[i+1];
   ColumnCount--;

   /* if a key seq. table then we have some work to do to set up the */
   /* key field that NOMAD will use to keep track of records with */
   if(TPtr->Organization==KEY_SEQ){

      /* assign the key columns so that none of the three columns just picked */
      /* will be used as part of the key.  First, set up at least one */
      /* column of the key to meet NOMAD's requirements */
      /* make sure one of the key columns is a non-datetime type */
      KPtr=TPtr->KeyPtr;
      temp=RANDOM_NUM0(ColumnCount-1);
      KPtr->ColNum=Column[temp];
      CPtr=TPtr->ColPtr+(KPtr->ColNum);
      CPtr->DataType=RandomNonDateTimeType();
      for(j=temp;j+1<ColumnCount;j++) Column[j]=Column[j+1];
      ColumnCount--;
      KPtr++;

      /* if type is NUMERIC or DECIMAL, then make sure the length */
      /* and/or scale is set to a value NOMAD can use */
      if((CPtr->DataType==TYPE_NUMERIC)||
         (CPtr->DataType==TYPE_DECIMAL)||
         (CPtr->DataType==TYPE_CHAR)||
         (CPtr->DataType==TYPE_VARCHAR)){

         CPtr->DataTypeLen=RANDOM_RANGE(5,18);
         CPtr->DataTypeScale=0;
         }

      KeyLength=(short)CPtr->DataTypeLen;

      /* Now pick the rest of the key columns randomly */
      /* loop until we have the number of key columns we wanted or until */
      /* we run out of columns to choose from */
      ActualKeyColCount=1;
      i=1;
      while(KeyLengthMax!=(TPtr->KeyType==PRIMARY_KEY ? 255 : 247) &&
            (i<TPtr->KeyColCount) && (ColumnCount!=0)){
         temp=RANDOM_NUM0(ColumnCount);
         KPtr->ColNum=Column[temp];

         CPtr=TPtr->ColPtr+(KPtr->ColNum);
         FillColumnInfo(CPtr);

         /* see if this key column will make the total key length exceed */
         /* the maximum key length.  If it doesn't then we can use this one */
         /* for part of the key.  If it does, then randomly make up another */
         /* set of column information until we get one we can use */
         while(KeyLength+(CPtr->DataTypeLen) > KeyLengthMax){

            /* clear column info */
            memset(CPtr,-1,sizeof(ColumnInfo));
            CPtr->CName[0]          = NULL;
            CPtr->Literal           = NULL;
            CPtr->CHeading[0]       = NULL;

            /* Randomly create new column info */
            FillColumnInfo(CPtr);
            }
         ActualKeyColCount++;
         KeyLength+=(short)CPtr->DataTypeLen;

         /* remove it from the list of column choices */
         for(j=temp;j+1<ColumnCount;j++) Column[j]=Column[j+1];
         ColumnCount--;

         KPtr++;
         i++;
         } /* end: while */

      /* it might have been the case that we could not select the requested */
      /* number of key columns because the maximum key length would have */
      /* been exceeded no matter which combination of columns were chosen */
      /* So, we'll adjust the key column count here to be the actual count */
      TPtr->KeyColCount=ActualKeyColCount;

      } /* end: if KEY_SEQ */

   /* Now just fill in the TableInfo part.  The NomadInfo */
   /* will be filled in later by CreateSQLTable() */
   FillTableInfo(TablePtr->TableInfoPtr);

   } /* end: FillTableDesc() */


/***********************************************************************
** FillTable()
**
** This function will insert the specified number of records into an SQL
** table.  The table will be emptied first, before records are inserted.
************************************************************************/
short FillTable(TableDescription *TablePtr)
{
   NomadInfo *NPtr;
   TableInfo *TPtr;
	ColumnInfo *pCol;
   ReturnStatus *RSPtr;
   long record_num=0;
   char parm_string[80];
   char fields[80];
   short i;
   long record_count;
	RETCODE rc;
	HSTMT hstmt;
   char command_line[SQL_MAX_COMMAND_LENGTH];
	short abort_flag;
	short zerosum_value;
	short last_process_id_column;

   NPtr=TablePtr->NomadInfoPtr;
   TPtr=TablePtr->TableInfoPtr;
	hstmt=TablePtr->hstmt;

   /* if there are any records in the table to delete, then try to */
   /* delete them because we must start with a clean table */
   sprintf(command_line,"DELETE FROM %s",TPtr->TableName);

	rc=SQLExecDirect(hstmt,command_line,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecDirect")){
      printf("%s return code=%d on %s\n",g_errstr,rc,command_line);
		LogAllErrors(NULL,NULL,hstmt);
		if(rc!=SQL_SUCCESS_WITH_INFO) return(FAILURE);
		}

   /*>>>need to handle the case of an entry sequenced file which we */
   /*>>>can not delete from.  Maybe check if it has any records in it */
   /*>>>so, for now we'll just ignore any errors */

   /* next, fill SQL tables with random inserts */

   /* allocate record bitmaps for each table to keep track of which */
   /* records have been written */
   NPtr->BitmapPtr=QACreateBitmap(NPtr->max_records);
   if(NPtr->BitmapPtr==NULL){
      LogMsg(ERRMSG+LINEAFTER,
             "unable to allocate space for table's bitmap\n");
      return(FAILURE);
      }

   /* build the SQL INSERT statement */
   if(strcmp(TPtr->ColPtr[0].CName,"SYSKEY")==0){
      strcpy(fields,"SYSKEY,*");
      }
   else strcpy(fields,"*");
   sprintf(command_line,"INSERT INTO %s (%s) VALUES(?p0",
           TPtr->TableName,fields);
   for(i=1;i<TPtr->NumOfCol;i++){
      sprintf(parm_string,",?p%d",i);
      strncat(command_line,parm_string,6);
      }
   strncat(command_line,")",2);
gTrace=1;

	rc=SQLPrepare(hstmt,command_line,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLPrepare")){
		LogAllErrors(NULL,NULL,hstmt);
      return(FAILURE);
      }

   /* are we going to fill the table with random inserts? */
   if(NPtr->InitialFillMethod==FILLRANDOMLY){

   	if(gTrace){
         LogMsg(0,"   -- filling table %s randomly with %ld records\n",
                TPtr->TableName,NPtr->InitialRecordCount);
         }

      /* randomly fill table with records */
      for(record_count=0;record_count<NPtr->InitialRecordCount;record_count++){

         /* randomly choose a record number which has not been chosen before */
         record_num=FindNextBit(BIT_OFF,NPtr->BitmapPtr,
                       LongRand(NPtr->max_records),CIRCULAR_SEARCH);

         /* if no unused records remain then something is wrong */
         if(record_num<0)return(FAILURE);

         /* fill each field with random data appropriate to its type */
         /* randomly fill values into all columns */
			RSPtr=BindAndFillAllParams(hstmt,TPtr);
			if(RSPtr!=NULL){
				LogMsg(ERRMSG+LINEAFTER,
					"couldn't generate random data values for all columns\n"
					"probable cause: row contains an unsupported data type\n"
					"I will continue, inserting the row as is\n");
				FreeReturnStatus(RSPtr);
				}

         /* set key-column(s) */
			RSPtr=SetKeyColumnValue2(TablePtr,record_num);
			if(RSPtr!=NULL){
				LogMsg(ERRMSG+LINEAFTER,
					"couldn't set data value for all key columns\n"
					"probable cause: row contains an unsupported data type\n"
					"I will continue, inserting the row as is\n");
				FreeReturnStatus(RSPtr);
				}

			/* set abort-column */
			abort_flag=0;
			pCol=&(TPtr->ColPtr[NPtr->abort_column]);
			rc=SQLBindParameter(hstmt,(short)(NPtr->abort_column+1),SQL_PARAM_INPUT,SQL_C_SHORT,
				pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
				&abort_flag,1,NULL);
			if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
				LogAllErrors(NULL,NULL,hstmt);
				if(gDebug) assert(FALSE);
				return(FAILURE);
				}

			/* set zerosum-column */
			zerosum_value=0;
			pCol=&(TPtr->ColPtr[NPtr->zerosum_column]);
			rc=SQLBindParameter(hstmt,(short)(NPtr->zerosum_column+1),SQL_PARAM_INPUT,SQL_C_SHORT,
				pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
				&zerosum_value,0,NULL);
			if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
				LogAllErrors(NULL,NULL,hstmt);
				if(gDebug) assert(FALSE);
				return(FAILURE);
				}

         /* set last process id column */
			last_process_id_column=0;
			pCol=&(TPtr->ColPtr[NPtr->last_process_id_column]);
			rc=SQLBindParameter(hstmt,(short)(NPtr->last_process_id_column+1),SQL_PARAM_INPUT,SQL_C_SHORT,
				pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
				&last_process_id_column,0,NULL);
			if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
				LogAllErrors(NULL,NULL,hstmt);
				if(gDebug) assert(FALSE);
				return(FAILURE);
				}

			/* EXECUTE the previously prepared INSERT statement */
			rc=SQLExecute(hstmt);
			if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecute")){
				LogAllErrors(NULL,NULL,hstmt);
				assert(FALSE);
				if(rc!=SQL_SUCCESS_WITH_INFO) return(FAILURE);
            }

         /* once sucessfully inserted (or hit allowable error) then mark bit... */
         /* ...in bitmap for this table */
			SetBit(BIT_ON,NPtr->BitmapPtr,record_num);
         }/* end: for */

      } /* end: if random inserts */

   /* fill the table with sequential inserts starting at record zero */
   else {

      if(gTrace){
         LogMsg(0,"   %s\n"
                "   -- filling table %s sequentially starting with 0 for %ld records\n",
                TPtr->TableName,command_line,NPtr->InitialRecordCount);
         }

      for(record_count=0;i<NPtr->InitialRecordCount;record_count++){

         /* fill each field with random data appropriate to its type */
         /* randomly fill values into all columns */
			RSPtr=BindAndFillAllParams(hstmt,TPtr);
			if(RSPtr!=NULL){
				LogMsg(ERRMSG+LINEAFTER,
					"couldn't generate random data values for all columns\n"
					"probable cause: row contains an unsupported data type\n"
					"I will continue, inserting the row as is\n");
				FreeReturnStatus(RSPtr);
				}

         /* set key-column(s) */
			RSPtr=SetKeyColumnValue2(TablePtr,i);
			if(RSPtr!=NULL){
				LogMsg(ERRMSG+LINEAFTER,
					"couldn't set data value for all key columns\n"
					"probable cause: row contains an unsupported data type\n"
					"I will continue, inserting the row as is\n");
				FreeReturnStatus(RSPtr);
				}

			/* set abort-column */
			abort_flag=0;
			pCol=&(TPtr->ColPtr[NPtr->abort_column]);
			rc=SQLBindParameter(hstmt,(short)(NPtr->abort_column+1),SQL_PARAM_INPUT,SQL_C_SHORT,
				pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
				&abort_flag,1,NULL);
			if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
				LogAllErrors(NULL,NULL,hstmt);
				if(gDebug) assert(FALSE);
				return(FAILURE);
				}

			/* set zerosum-column */
			zerosum_value=0;
			pCol=&(TPtr->ColPtr[NPtr->zerosum_column]);
			rc=SQLBindParameter(hstmt,(short)(NPtr->zerosum_column+1),SQL_PARAM_INPUT,SQL_C_SHORT,
				pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
				&zerosum_value,0,NULL);
			if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
				LogAllErrors(NULL,NULL,hstmt);
				if(gDebug) assert(FALSE);
				return(FAILURE);
				}

         /* set last process id column */
			last_process_id_column=0;
			pCol=&(TPtr->ColPtr[NPtr->last_process_id_column]);
			rc=SQLBindParameter(hstmt,(short)(NPtr->last_process_id_column+1),SQL_PARAM_INPUT,SQL_C_SHORT,
				pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
				&last_process_id_column,0,NULL);
			if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
				LogAllErrors(NULL,NULL,hstmt);
				if(gDebug) assert(FALSE);
				return(FAILURE);
				}

			/* EXECUTE the previously prepared INSERT statement */
			rc=SQLExecute(hstmt);
			if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecute")){
				LogAllErrors(NULL,NULL,hstmt);
				if(rc!=SQL_SUCCESS_WITH_INFO) return(FAILURE);
            }

         /* once sucessfully inserted (or hit allowable error) then mark bit... */
         /* ...in bitmap for this table */
			SetBit(BIT_ON,NPtr->BitmapPtr,i);
         }
      }

   /* perform an UPDATE STATISTICS on the table, mainly to get rid of */
   /* that annoying warning from SQL about no statistics available */
   /* whenever anyone accesses the table */
   sprintf(command_line,"UPDATE STATISTICS FOR TABLE %s ON EVERY COLUMN",
           TPtr->TableName);
   rc=SQLExecDirect(hstmt,command_line,SQL_NTS);
   if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecDirect")){
	   printf("return code=%d on %s\n",rc,command_line);
	   LogAllErrors(NULL,NULL,hstmt);
       if(rc!=SQL_SUCCESS_WITH_INFO) return(FAILURE);
	   }

   return(SUCCESS);

   } /* end: FillTable() */


/***********************************************************************
** CreateSQLTable()
**
** This function creates the SQL tables (and some day indexes and views)
** which don't already exist and will be used by the processes.
************************************************************************/
short CreateSQLTable(TableDescription *table_ptr)
{
   char command_line[SQL_MAX_COMMAND_LENGTH];
   char *StringPtr;
   NomadInfo *NPtr;
   TableInfo *TPtr;
   TableInfo *TempTPtr;
   ReturnStatus *RSPtr;
	RETCODE rc;
	HENV henv;
	HDBC hdbc;
	HSTMT hstmt;
   short table_num;


   NPtr=table_ptr->NomadInfoPtr;
   TPtr=table_ptr->TableInfoPtr;
   RSPtr=NULL;
	henv=table_ptr->henv;
	hdbc=table_ptr->hdbc;
	hstmt=table_ptr->hstmt;

   printf("NOMAD: creating SQL table '%s'\n",TPtr->TableName);

   /* First, make sure any old SQL tables are deleted */
   /* handle the case where NOPURGEUNTIL and SECURE */
   /* are set so that we can't drop the tables */
/*   sprintf(command_line,"ALTER TABLE %s SECURE 'OOOO' "
           "NOPURGEUNTIL 01 JAN 1980",TPtr->Tname);
   blank_pad(command_line,SQL_MAX_COMMAND_LENGTH);
   exec sql EXECUTE IMMEDIATE :command_line;
   if((sqlcode!=0)&&(sqlcode!=SQL_TABLE_NOT_FOUND)){
      //>>> handle error somehow
      sql_error();
      }
*/
   // now drop the tables (ignore errors since we don't care if table are there or not)
   sprintf(command_line,"DROP TABLE %s",TPtr->TableName);
	rc=SQLExecDirect(hstmt,command_line,SQL_NTS);

   sprintf(command_line,"DROP TABLE %sV",TPtr->TableName);
	rc=SQLExecDirect(hstmt,command_line,SQL_NTS);

   /* handle creation like an existing table */
   if(strlen(NPtr->like_name)!=0){
      sprintf(command_line,"CREATE TABLE %s LIKE %s",
              TPtr->TableName,NPtr->like_name);
		rc=SQLExecDirect(hstmt,command_line,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecDirect")){
         printf("%s return code=%d on %s\n",g_errstr,rc,command_line);
			LogAllErrors(henv,hdbc,hstmt);
			return(FAILURE);
			}
      }

   /* handle creation of a new table from scratch */
   else {

      StringPtr=BuildCreateTableString(TPtr);
      if(strlen(StringPtr)==0) return(FAILURE);
      strncpy(g_CommandLine,StringPtr,sizeof(g_CommandLine));
		rc=SQLExecDirect(hstmt,g_CommandLine,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecDirect")){
         printf("%s return code=%d\n",g_errstr,rc);
			LogAllErrors(henv,hdbc,hstmt);
			if(gDebug) assert(FALSE);
         FormatForSQLCI(StringPtr);
			return(FAILURE);
			}
      free(StringPtr);
   }

	// get info about table we just created
	if(TPtr->Organization==KEY_SEQ){
		TempTPtr=GetTableInfo(hdbc,TPtr->TableName,FALSE,&RSPtr);
		}
	else{
		TempTPtr=GetTableInfo(hdbc,TPtr->TableName,TRUE,&RSPtr);
		}

	FreeTableInfo(TPtr);
	TPtr=TempTPtr;
	table_ptr->TableInfoPtr=TempTPtr;

	RSPtr=FindRequiredColumns(table_ptr);
	if(RSPtr!=NULL){
		printf("ReturnType=%d  ReturnCode=%d\n%s\n%s\n",
				 RSPtr->ReturnType,RSPtr->ReturnCode,
				 RSPtr->Message1,RSPtr->Message2);
		return(FAILURE);
		}

	/* add the table name to the list (if it's already in... */
	/* ...the list then only its number is returned) */
	table_num=add_table(TPtr->TableName);
	if(table_num<0) {
		printf("%s Problem with table '%s'\n",g_errstr,TPtr->TableName);
		return(FAILURE);
	}

   return(SUCCESS);

   } /* end: CreateSQLTable() */
