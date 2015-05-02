#ifndef _TEST_STRUCT_
#define _TEST_STRUCT_
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>


typedef int newtype;


struct TestStruct {
    /* Basic primitive types */
    _Bool bool_val;

    char char_val;
    signed char schar_val;
    unsigned char uchar_val;

    short short_val;
    unsigned short ushort_val;

    int int_val;
    unsigned int uint_val;

    long long_val;
    unsigned long ulong_val;

    float float_val;
    double double_val;
    long double ldouble_val;

    long long longlong_val;
    unsigned long long ulonglong_val;

    /* Likely to be typedefs */
    newtype newtypeval;
    intmax_t intmax_t_val;
    size_t size_t_val;

    /* C99 sized types */
    int8_t int8_t_val;
    uint8_t uint8_t_val;
    int16_t int16_t_val;
    uint16_t uint16_t_val;
    int32_t int32_t_val;
    uint32_t uint32_t_val;
    int64_t int64_t_val;
    uint64_t uint64_t_val;

    int_least8_t int_least8_t_val;
};


typedef float FLOAT32;
typedef int INT;


struct TestStructWithTypedefs
{
    FLOAT32 float_val;
    INT int_val;
};


typedef struct 
{
    char char_val;
    long long_val;

} TypedefStruct;


/* We currently ignore typedef struct names */
typedef struct _unused_name_
{
    char char_val;
    long long_val;

} TypedefStruct2;


typedef struct 
{
    float float_val;
    TypedefStruct nested1;

} StructWithSub;


typedef struct
{
    TypedefStruct nested1;
    StructWithSub nested;
    
} StructWithDoubleSub;


struct WithNested {
    char not_nested;
    struct NestedStruct {
        float float_val;
    } nested;
};

struct WithNamelessNested {
    char not_nested;
    struct {
        float float_val;
    } nested;
};

#endif
