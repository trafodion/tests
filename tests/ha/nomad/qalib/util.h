#ifndef __UTILH      /* this prevents multiple copies of this... */
#define __UTILH      /* ...include file from being #included... */

/************************************************************************
** UTIL.H
**
** This is the header file for all functions in UTIL.C
*************************************************************************/
#define TRUE  1
#define FALSE 0

#undef NULL				// redefine NULL to prevent compiler warnings
#define NULL '\0'

/* Use these as generic return values for functions */
#define SUCCESS 0
#define FAILURE -555       /* because I like fives, ok? */

/* Random TRUE or FALSE */
#define RANDOM_T_OR_F  (rand()%2)

/* Random number from 1 up to and including <x> */
#define RANDOM_NUM1(x) (rand()%(x)+1)

/* Random number from 0 up to and including <x> */
#define RANDOM_NUM0(x) (rand()%(x+1))

/* Random number from <x> up to and including <y> */
#define RANDOM_RANGE(x,y) ((rand()%(y+1-x))+x)

/* RANDOM is used as a parameter in many DP2 QA functions to notify the */
/* function code to choose a random value for the given parameter */
#define RANDOM  -1


#define MAX_FILENAME_LENGTH  500
#define MAX_FILENAME_LEN     MAX_FILENAME_LENGTH

typedef int Boolean;           /* use this if the value is TRUE or FALSE */

extern void blank_pad(char *,size_t);
extern char *remove_char(char *,unsigned int);
#define remove_blanks(x) remove_char(x,' ')
extern char *toupper_s(char *);
extern char *fget_s(char *,int,FILE *);
extern char *get_s(char *);
extern long LongRand(long range);
extern long LongRandRange(long min, long max);
extern int sysnn(char *SystemName);
extern char *RandomString(int length);
extern char *atoh(char *InStrPtr,int InStrLen);
extern void *HexStrToBytes(char *HexStrPtr);
extern void FormatHexOutput( char *In, char *Out, long Length );


#endif
