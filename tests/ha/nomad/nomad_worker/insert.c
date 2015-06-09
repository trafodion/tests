#include "defines.h"
#include "include.h"
#include "ODBCcommon.h"
#include "bitlib.h"
#include "table.h"
#include "struct.h"
#include "globals.h"
#include "sqlutil.h"
#include "sqlutil2.h"

/*************************************************************************
** Function: do_insert()
**
** Randomly selects a record or subset of sequential records to be
** inserted into the specified table and then attempts to insert them.
*************************************************************************/
short do_insert(table_description *tab_ptr,Bitmap *bmap_ptr,long record_count,Boolean abort_flag)
{
   short zerosum_value;
   short last_zerosum_value_inserted;
   long zerosum_total;
   long i;
   ReturnStatus *RSPtr;
   long record_num;
   long last_record_num;
   long last_record_num_inserted;
   long stop_record_num;
   long records_in_block;
   char parm_string[80];
   char fields[80];
   char command_line[SQL_MAX_COMMAND_LENGTH];
	TableInfo *pTable;
	ColumnInfo *pCol;
	ColumnInfo *pCol2;
	HENV	henv;
	HDBC	hdbc;
	HSTMT	hstmt;
	char	szSqlState[10];
	SQLINTEGER	NativeError;
	char	szErrorMsg[SQL_MAX_ERROR_MSG];
	short	cbErrorMsgMax;
	short cbErrorMsg;
	RETCODE rc;
	Boolean UpdateZeroSumNeeded;

	cbErrorMsgMax=SQL_MAX_ERROR_MSG;
	pTable=tab_ptr->pTable;
	henv=tab_ptr->henv;
	hdbc=tab_ptr->hdbc;
	hstmt=tab_ptr->hstmt;
   zerosum_total=0;
	UpdateZeroSumNeeded=FALSE;

	LogMsg(NONE,"\n");

	/* search bitmap for a full block of the right size */
   record_num=FindNextBitBlock(BIT_OFF,bmap_ptr,
                               LongRand((long)tab_ptr->max_records-1),
                               CIRCULAR_SEARCH,
                               record_count,&records_in_block);
LogPrintf("***DEBUG: requested size=%lu, actual size=%lu, max_records=%lu\n"
		,record_count,records_in_block,tab_ptr->max_records);
   /* if no places to insert into then nothing can be done */
   if(record_num==BIT_NOT_FOUND) {
      if(gTrace){
         LogMsg(NONE,"No empty places to insert.\n");
         if(gDebug){
         	 LogMsg(NONE,"Terminating program because debug flag was set.\n");
         	 LogMsg(NONE,"Current transactions will abort.\n");
         	 assert(FALSE);
         }
      }
      return(0);
   }

   /* check if the bitblock was the size requested or if it was smaller */
   /* if smaller then change the <record_count> to the records in the bitblock */
   if(record_count>records_in_block){
      record_count=records_in_block;
      }

   LogMsg(TIMESTAMP+INFOMSG,"Inserting %lu records starting from %lu\n",
   		record_count,record_num);

   /* build and PREPARE the SQL INSERT statement used for all inserts */
   /* >>>need to modify this if ALTER ADD COLUMN is ever supported */

   /* build the SQL INSERT statement */
   if(strcmp(pTable->ColPtr[0].CName,"SYSKEY")==0){
      strcpy(fields,"SYSKEY,*");
      }
   else strcpy(fields,"*");
   sprintf(command_line,"INSERT INTO %s (%s) VALUES(?p1",
           pTable->TableName,fields);
   for(i=1;i<pTable->NumOfCol;i++){
      sprintf(parm_string,",?p%ld",i+1);
      strncat(command_line,parm_string,6);
      }
   strncat(command_line,")",2);

   if(gTrace&&TRACE_SQL){
      LogMsg(0,"   %s\n",command_line,record_num,record_count);
      }

	rc=SQLPrepare(hstmt,command_line,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLPrepare")){
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }

   /* determine if block of records wraps */
   stop_record_num=-1;
   last_record_num=record_num+record_count-1;
   if(last_record_num>tab_ptr->max_records-1){

      /* block wraps so, two groups of inserts will need to be done */
      stop_record_num=last_record_num-tab_ptr->max_records;
      LogMsg(DEBUGMSG,"block wraps: stop_record_num=%lu\n",stop_record_num);
      for(i=0;i<=stop_record_num;i++){

         /* randomly fill values into all columns */
			RSPtr=BindAndFillAllParams(hstmt,pTable);
			if(RSPtr!=NULL){
				LogMsg(ERRMSG+LINEAFTER,
					"couldn't generate random data values for all columns\n"
					"probable cause: row contains an unsupported data type\n"
					"I will continue, inserting the row as is\n");
				FreeReturnStatus(RSPtr);
				}

         /* set key-column(s) */
			RSPtr=SetKeyColumnValue(tab_ptr,i);
			if(RSPtr!=NULL){
				LogMsg(ERRMSG+LINEAFTER,
					"couldn't set data value for all key columns\n"
					"probable cause: row contains an unsupported data type\n"
					"I will continue, inserting the row as is\n");
				FreeReturnStatus(RSPtr);
				}

         /* set abort-column */
			pCol=&(pTable->ColPtr[tab_ptr->abort_column]);
			rc=SQLBindParameter(hstmt,(short)(tab_ptr->abort_column+1),SQL_PARAM_INPUT,SQL_C_CHAR,
				pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
				&abort_flag,1,NULL);
			if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
				LogAllErrors(henv,hdbc,hstmt);
				if(gDebug) assert(FALSE);
				return(FAILURE);
				}

         /* set zerosum-column */
         zerosum_value=500-RANDOM_NUM0(1000);
         zerosum_total+=(long)zerosum_value;
			pCol=&(pTable->ColPtr[tab_ptr->zerosum_column]);
			rc=SQLBindParameter(hstmt,(short)(tab_ptr->zerosum_column+1),SQL_PARAM_INPUT,SQL_C_SHORT,
				pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
				&zerosum_value,0,NULL);
			if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
				LogAllErrors(henv,hdbc,hstmt);
				if(gDebug) assert(FALSE);
				return(FAILURE);
				}

         /* set last process id column */
         /*>>> need to find a good way to figure out <last_process_id> */
			pCol=&(pTable->ColPtr[tab_ptr->last_process_id_column]);
			*(pCol->Value.pInteger)=0;

         if(gTrace&&TRACE_SQL) {
            LogMsg(0,"   KEY=%d, ABORT=%d, ZEROSUM=%d\n",
                   i,abort_flag,zerosum_value);
            }

			/* EXECUTE the previously prepared INSERT statement */
			rc=SQLExecute(hstmt);
			if((rc!=SQL_SUCCESS)&&(rc!=SQL_SUCCESS_WITH_INFO)){
				SQLError(NULL,NULL,hstmt,szSqlState,&NativeError,
					szErrorMsg,cbErrorMsgMax,&cbErrorMsg);
				// allow duplicate keys error
				if(NativeError==SQL_DUPLICATE_KEY_ERROR) {
					zerosum_total-=(long)zerosum_value;
					}
				else{
					CHECKRC(SQL_SUCCESS,rc,"SQLExecute");
					LogMsg(ERRMSG,szErrorMsg);
					LogAllErrors(henv,hdbc,hstmt);
					return(FAILURE);
					}
				}
			else{
				if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecute")){
					LogAllErrors(henv,hdbc,hstmt);
					if(rc!=SQL_SUCCESS_WITH_INFO) return(FAILURE);
					}
            last_record_num_inserted=i;
            last_zerosum_value_inserted=zerosum_value;
				UpdateZeroSumNeeded=TRUE;
            }

         /* once sucessfully inserted (or hit allowable error) then mark bit... */
         /* ...in bitmap for this table */
			SetBit(BIT_ON,bmap_ptr,i);
         }

      last_record_num=tab_ptr->max_records-1;
      }

   /* loop for each record to be inserted */
   if(gDebug){
   	LogMsg(DEBUGMSG,"inserting from %lu to %lu\n",record_num,last_record_num);
   }
   for(i=record_num;i<=last_record_num;i++){

      /* randomly fill values into all columns */
		RSPtr=BindAndFillAllParams(hstmt,pTable);
		if(RSPtr!=NULL){
			LogMsg(ERRMSG+LINEAFTER,
				"couldn't generate random data values for all columns\n"
				"probable cause: row contains an unsupported data type\n"
				"I will continue, inserting the row as is\n");
			FreeReturnStatus(RSPtr);
			}

      /* set key-column(s) */
		RSPtr=SetKeyColumnValue(tab_ptr,i);
		if(RSPtr!=NULL){
			LogMsg(ERRMSG+LINEAFTER,
				"couldn't set data value for all key columns\n"
				"probable cause: row contains an unsupported data type\n"
				"I will continue, inserting the row as is\n");
			FreeReturnStatus(RSPtr);
			}

      /* set abort-column */
		pCol=&(pTable->ColPtr[tab_ptr->abort_column]);
		rc=SQLBindParameter(hstmt,(short)(tab_ptr->abort_column+1),SQL_PARAM_INPUT,SQL_C_CHAR,
			pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
			&abort_flag,1,NULL);
		if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
			LogAllErrors(henv,hdbc,hstmt);
			if(gDebug) assert(FALSE);
			return(FAILURE);
			}

		/* set zerosum-column */
		zerosum_value=500-RANDOM_NUM0(1000);
		zerosum_total+=(long)zerosum_value;
		pCol=&(pTable->ColPtr[tab_ptr->zerosum_column]);
		rc=SQLBindParameter(hstmt,(short)(tab_ptr->zerosum_column+1),SQL_PARAM_INPUT,SQL_C_SHORT,
			pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
			&zerosum_value,0,NULL);
		if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
			LogAllErrors(henv,hdbc,hstmt);
			if(gDebug) assert(FALSE);
			return(FAILURE);
			}

		/* set last process id column */
		/*>>> need to find a good way to figure out <last_process_id> */
		pCol=&(pTable->ColPtr[tab_ptr->last_process_id_column]);
		*(pCol->Value.pInteger)=0;

      if(gTrace&&TRACE_SQL) {
         LogMsg(0,"   KEY=%d, ABORT=%d, ZEROSUM=%d\n",
				i,abort_flag,zerosum_value);
         }

      /* EXECUTE the previously prepared statement */
		rc=SQLExecute(hstmt);
		if((rc!=SQL_SUCCESS)&&(rc!=SQL_SUCCESS_WITH_INFO)){
			SQLError(NULL,NULL,hstmt,szSqlState,&NativeError,
				szErrorMsg,cbErrorMsgMax,&cbErrorMsg);
			// allow duplicate keys error
			if(NativeError==SQL_DUPLICATE_KEY_ERROR) {
				zerosum_total-=(long)zerosum_value;
				}
			else{
				CHECKRC(SQL_SUCCESS,rc,"SQLExecute");
				LogMsg(ERRMSG,szErrorMsg);
				LogAllErrors(henv,hdbc,hstmt);
				return(FAILURE);
				}
			}
      else{
			if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecute")){
				LogAllErrors(henv,hdbc,hstmt);
				if(rc!=SQL_SUCCESS_WITH_INFO) return(FAILURE);
				}
         last_record_num_inserted=i;
         last_zerosum_value_inserted=zerosum_value;
			UpdateZeroSumNeeded=TRUE;
         }

      /* once sucessfully inserted (or hit allowable error) then mark bit... */
      /* ...in bitmap for this table */
		SetBit(BIT_ON,bmap_ptr,i);
      }

   /* Do UPDATE of last record inserted to adjust the zerosum column, if needed. */
	if(UpdateZeroSumNeeded){

		/* subtract out last zerosum_value since it is the record that will */
		/* be updated with the zerosum_total */
		zerosum_total-=(long)last_zerosum_value_inserted;
		zerosum_total=-zerosum_total;

		pCol=&(pTable->ColPtr[tab_ptr->zerosum_column]);
		pCol2=&(pTable->ColPtr[tab_ptr->key_column_used]);
		sprintf(command_line,"UPDATE %s SET %s=?p1 WHERE %s=?p2",
			pTable->TableName,pCol->CName,pCol2->CName);

		rc=SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_LONG,
			pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
			&zerosum_total,0,NULL);
		if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
			LogAllErrors(henv,hdbc,hstmt);
			if(gDebug) assert(FALSE);
			return(-1);
			}

		rc=SQLBindParameter(hstmt,2,SQL_PARAM_INPUT,SQL_C_LONG,
			pCol2->pTypeInfo->SQLDataType,pCol2->DataTypeLen,0,
			&last_record_num_inserted,0,NULL);
		if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
			LogAllErrors(henv,hdbc,hstmt);
			if(gDebug) assert(FALSE);
			return(-1);
			}

      if(gTrace&&TRACE_SQL) {
			LogMsg(NONE,"   Parameter1=%ld    Parameter2=%ld\n",zerosum_total,last_record_num_inserted);
			LogMsg(NONE,"   %s\n",command_line);
			}

		rc=SQLExecDirect(hstmt,command_line,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecDirect")){
			LogAllErrors(henv,hdbc,hstmt);
			return(FAILURE);
			}
		}

   return(SUCCESS);
   }


/*************************************************************************
** Function: do_vsbb_insert()
**
** Randomly selects a subset of sequential records to be
** inserted into the specified table and then attempts to insert them.
**
** NOTE: perhaps provide another version of this function which uses the
**       DM^ SQL-filesystem procedures to do VSBB inserts
*************************************************************************/
/*
short do_vsbb_insert(tab_ptr,bmap_ptr,record_count,abort_flag)
exec sql begin declare section;
table_description *tab_ptr;
exec sql end declare section;
bitmap *bmap_ptr;
short record_count;
boolean abort_flag;
{
   // item code for SQLCAGETINFOLIST
   #define NUMBER_OF_ROWS_PROCESSED  20

   long zerosum_total;
   char *key_column_name;
   long record_num;
   long records_in_block;
   char dup_insert_table[MAX_FILENAME_LEN];
   char fields[80];
   char *StringValuePtr;
   char FormatLine[SQL_MAX_COMMAND_LENGTH];
   exec sql begin declare section;
   char command_line[SQL_MAX_COMMAND_LENGTH];
   exec sql end declare section;
   short item_list[1];
   struct{
      long rows_processed;
      } results;


   zerosum_total=0;
   abort_flag=abort_flag;

   // search bitmap for an empty block of the right size
   // we'll start searching from record zero of the table (not the...
   //...best choice but, we need to do that since we only search until...
   //...the end of the bitmap.  If we searched the bitmap circularly then...
   //...we could start at a random place)
   record_num=find_next_bitblock(BIT_OFF,bmap_ptr,tab_ptr->max_records,
                                 0,SEARCH_UNTIL_END,
                                 record_count,&records_in_block);

   // if no records left to insert then nothing can be done
   if(record_num==BIT_NOT_FOUND){
      if(gTrace) LogMsg(0,"   No empty places to VSBB insert into.\n");
      return(0);
      }

   // check if the bitblock was the size requested or if it was smaller
   // if smaller then change the <record_count> to the records in the bitblock
   if(record_count>records_in_block){
      record_count=records_in_block;
      }

   // build the SQL INSERT statement used for VSBB inserts
   key_column_name=tab_ptr->name_ptr[tab_ptr->key_column_used];
   sprintf(dup_insert_table,"%sV",tab_ptr->table_name);

   switch(tab_ptr->file_type){
      case ENTRY_SEQ:
      case KEY_SEQ:
         strcpy(fields,"*");
         break;
      case RELATIVE_TABLE:
         strcpy(fields,"SYSKEY,*");
         break;
      }

   strcpy(FormatLine,"INSERT INTO %s (%s) (SELECT %s FROM %s WHERE %s>=");

   StringValuePtr=SetColumnValueString(tab_ptr->sqlda_ptr,
                  tab_ptr->key_column_used,record_num);
   strcat(FormatLine,StringValuePtr);
   free(StringValuePtr);

   strcat(FormatLine," AND %s<=");

   StringValuePtr=SetColumnValueString(tab_ptr->sqlda_ptr,
                  tab_ptr->key_column_used,record_num+record_count-1);
   strcat(FormatLine,StringValuePtr);
   free(StringValuePtr);

   strcat(FormatLine," FOR BROWSE ACCESS)");

   sprintf(command_line,FormatLine,
           tab_ptr->table_name,fields,fields,dup_insert_table,
           key_column_name,key_column_name);

   if(gTrace){
      LogMsg(0,"   %s\n"
             "   -- starting with %ld for %d records\n",
             command_line,record_num,record_count);
      }

   blank_pad(command_line,SQL_MAX_COMMAND_LENGTH);

   //>>> need to do something to randomly set the zerosum and abort
   //>>> column values from the table we're inserting from

   exec sql EXECUTE IMMEDIATE :command_line;

   //>>>what happens when some records are inserted and then a
   //>>>duplicate key error is encountered??  ANSWER: the partially
   //>>>inserted records remain, unless it is aborted
   if(sqlcode!=0) {
      // adjust <record_count> to show actual number of records inserted
      item_list[0]=NUMBER_OF_ROWS_PROCESSED;
      SQLCAGETINFOLIST((short *)&sqlca,item_list,1,(short *)&results,
                       (short)sizeof(results));
      record_count=results.rows_processed;
      if(sqlcode!=SQL_DUPLICATE_KEY_ERROR){
         if(EvaluateSQLError(SQL_INSERT_VSBB,tab_ptr)!=0) return(-1);
         }
      }

   // once sucessfully inserted (or hit allowable error) then mark bits...
   // ...in bitmap for this table
   set_bitblock(BIT_ON,bmap_ptr,record_num,tab_ptr->max_records,
                record_count);

   return(0);
   }

*/
