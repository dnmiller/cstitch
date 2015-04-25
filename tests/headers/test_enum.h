#ifndef _TEST_ENUM_H_
#define _TEST_ENUM_H_

#define ENUM_VAL_0  (5)

enum TestEnum {
    TEST_ENUM_1,
    TEST_ENUM_2,
    TEST_ENUM_3
};


typedef enum {
    TEST_TYPEDEF_ENUM_1,
    TEST_TYPEDEF_ENUM_2,
    TEST_TYPEDEF_ENUM_3,
    TEST_TYPEDEF_ENUM_4
} TYPEDEF_ENUM;


enum OutOfOrderEnum {
    OUT_ENUM_1 = -100,
    OUT_ENUM_2 = 0,
    OUT_ENUM_3 = 100,
    OUT_ENUM_4 = -1,
    OUT_ENUM_5 = 0
};


enum RefEnum {
    REF_ENUM_1 = OUT_ENUM_2,
    REF_ENUM_2 = 5,
    REF_ENUM_3 = TEST_TYPEDEF_ENUM_2
};


enum {
    ANON_ENUM_1 = 0,
    ANON_ENUM_2,
    ANON_ENUM_3 = ENUM_VAL_0    // Make sure preprocessor substitution works
};

#endif
