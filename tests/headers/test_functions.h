#ifndef _TEST_FUNCTIONS_
#define _TEST_FUNCTIONS_

/* Will use some structs and functions from time.h */
#include <time.h>

/* Static functions we're supposed to ignore. */
static void ignored(void);

/* Functions with no arguments or return type */
void dummy(void);

/* Function with no return type */
void no_ret(int);

/* Function with no arguments */
int no_args(void);

#if 0
/* Basic math */
float addf(float a, float b);

/* Don't include a name for one of them here. */
double addd(double, double b);

/* Don't include a name for either */
float subdf(double, float);

/* Dummy saxpy routine */
float saxpy(int n, float a, float *x, int inc_x, float *y, int inc_y);

/* What month is it? */
int get_month(const struct tm *);

/* What year is it? Include a name for the variable. */
int get_year(const struct tm *input);

#endif
#endif
