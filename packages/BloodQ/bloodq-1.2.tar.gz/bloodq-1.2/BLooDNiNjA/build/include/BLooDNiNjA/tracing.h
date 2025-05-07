//     Copyright 2025, BLOOD, tnmn4219@gmail.com find license text at end of file

#ifndef __BloodSx_TRACING_H__
#define __BloodSx_TRACING_H__

/* Stupid tracing, intended to help where debugging is not an option
 * and to give kind of progress record of startup and the running of
 * the program.
 */

#ifdef _BloodSx_TRACE

#define BloodSx_PRINT_TRACE(value)                                                                                      \
    {                                                                                                                  \
        puts(value);                                                                                                   \
        fflush(stdout);                                                                                                \
    }
#define BloodSx_PRINTF_TRACE(...)                                                                                       \
    {                                                                                                                  \
        printf(__VA_ARGS__);                                                                                           \
        fflush(stdout);                                                                                                \
    }

#else
#define BloodSx_PRINT_TRACE(value)
#define BloodSx_PRINTF_TRACE(...)

#endif

#if defined(_BloodSx_EXPERIMENTAL_SHOW_STARTUP_TIME)

#if defined(_WIN32)

#include <windows.h>
static void inline PRINT_TIME_STAMP(void) {
    SYSTEMTIME t;
    GetSystemTime(&t); // or GetLocalTime(&t)
    printf("%02d:%02d:%02d.%03d:", t.wHour, t.wMinute, t.wSecond, t.wMilliseconds);
}
#else
static void inline PRINT_TIME_STAMP(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);

    time_t now_time = tv.tv_sec;
    struct tm *now_tm = localtime(&now_time);

    char tm_buf[64];
    strftime(tm_buf, sizeof(tm_buf), "%Y-%m-%d %H:%M:%S", now_tm);
    printf("%s.%03ld ", tm_buf, tv.tv_usec / 1000);
}
#endif

#define BloodSx_PRINT_TIMING(value)                                                                                     \
    {                                                                                                                  \
        PRINT_TIME_STAMP();                                                                                            \
        puts(value);                                                                                                   \
        fflush(stdout);                                                                                                \
    }

#else

#define BloodSx_PRINT_TIMING(value) BloodSx_PRINT_TRACE(value)

#endif

#endif


