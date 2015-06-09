#ifndef __RTNSTATH      /* this prevents multiple copies of this... */
#define __RTNSTATH      /* ...include file from being #included... */

/*
   ReturnType - defines.

      used to specify the reason why the ReturnStruct block was returned.
      following are the values reserved by the UTILITY routines. it is
      recommened that USER defined values be restricted to the range:
      10000-10999.
*/
#define RT_OK                  0      /* no problem                    */
#define RT_WARNING             20000  /* warning returned to caller    */
#define RT_PROGRAMERR          20001  /* program detected an error     */
#define RT_PROCEDUREERR        20002  /* guardian procedure call       */
                                      /*   returned error              */
#define RT_INFO                20003  /* informational message returned*/
                                      /*   by caller                   */
#define RT_MALLOC              20004  /* call to malloc() failed       */
#define RT_SQL                 20005  /* SQL error or warning occurred */
#define RT_ODBC                20006  /* ODBC error occurred           */
#define RT_LAST                32767  /* this is the highest value a   */
                                      /*   ReturnType define can have  */
                                      /*   and is here mainly to remind*/
                                      /*   those who add to this file  */
                                      /*   not to go beyond 32767      */
/*
   ReturnStatusCode - defines.

      used to specify the reason why the ReturnStatus block cound not
      be allocated properly.  All of these are basically errors that
      should not happen.
*/
#define RSC_MALLOC0            1      /* One of several malloc() calls */
#define RSC_MALLOC1            2      /*   failed.                     */
#define RSC_MALLOC2            3
#define RSC_MALLOC3            4
#define RSC_VSPRINTF_OVERFLOW  5      /* There was a buffer overflow   */
                                      /* some portion of memory has    */
                                      /* been overwritten. Might effect*/
                                      /* further execution of program  */

/*
   ReturnStatus defines a ReturnStatus block. A ReturnStatus block
   is used to return status information to the caller of a procedure.
*/
typedef struct ReturnStatus ReturnStatus;
struct ReturnStatus {
   int ReturnType;                    /* type of return status         */
                                      /*  see "ReturnType - defines"   */
                                      /*  for reserved type values     */
   int ReturnCode;                    /* return code                   */
   char *Message1;                    /* pointer to return message 1   */
   char *Message2;                    /* pointer to return message 2   */
   ReturnStatus *NextPtr;             /* pointer to next return struct */
};


/*
   external routines
*/
extern ReturnStatus *BuildReturnStatusChain (int ReturnType,
                                             int ReturnCode,
                                             ReturnStatus *NextPtr,
                                             char *Message1,
                                             char *Message2,
                                             ... );
extern ReturnStatus *BuildReturnStatus (int ReturnType,
                                        int ReturnCode,
                                        char *Message1,
                                        char *Message2,
                                        ... );
#define BuildReturnStatusOK BuildReturnStatus(RT_OK,0,NULL,NULL)
#define BuildReturnStatusMALLOC BuildReturnStatus(RT_MALLOC,0,NULL,NULL)
extern void FreeReturnStatus(ReturnStatus *RSPtr);
extern int GetReturnStatusCode(void);

#endif
