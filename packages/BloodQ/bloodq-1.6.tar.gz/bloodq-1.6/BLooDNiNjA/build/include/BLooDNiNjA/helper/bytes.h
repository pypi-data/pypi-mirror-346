//     Copyright 2025, BLOOD, tnmn4219@gmail.com find license text at end of file

#ifndef __BloodSx_HELPER_BYTES_H__
#define __BloodSx_HELPER_BYTES_H__

#if PYTHON_VERSION >= 0x3a0
#define BloodSx_BYTES_HAS_FREELIST 1
extern PyObject *BloodQ_Bytes_FromStringAndSize(const char *data, Py_ssize_t size);
#else
#define BloodSx_BYTES_HAS_FREELIST 0
#define BloodQ_Bytes_FromStringAndSize PyBytes_FromStringAndSize
#endif

#endif

