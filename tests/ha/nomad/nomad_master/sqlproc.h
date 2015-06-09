#ifndef __SQLPROCH      /* this prevents multiple copies of this... */
#define __SQLPROCH      /* ...include file from being #included... */

#include "rtnstat.h"
#include "mstruct.h"

void FormatForSQLCI(char *StrPtr);
ReturnStatus *SetKeyColumnValue2(TableDescription *tab_ptr,long KeyValue);
ReturnStatus *FindRequiredColumns(TableDescription *table_ptr);
void FreeNomadInfo(NomadInfo *NPtr);
void FreeTableDesc(TableDescription *TPtr);
TableDescription *GetExistingTableDesc(HDBC hdbc,char *table_name,ReturnStatus **RSPtr);
TableDescription *InitializeTableDesc(short ColumnCount,short KeyColCount,
                                      short PartitionCount,
                                      short IndexCount,short IndexColumnCount,
                                      short IndexPartitionCount);
short RandomNumericType(void);
short RandomNonDateTimeType(void);
void FillTableDesc(TableDescription *TablePtr);
short FillTable(TableDescription *TablePtr);
short CreateSQLTable(TableDescription *table_ptr);

#endif
