//     Copyright 2025, BLOOD, tnmn4219@gmail.com find license text at end of file

#ifndef __BloodSx_HELPER_BYTEARRAYS_H__
#define __BloodSx_HELPER_BYTEARRAYS_H__

BloodSx_MAY_BE_UNUSED static PyObject *BYTEARRAY_COPY(PyThreadState *tstate, PyObject *bytearray) {
    CHECK_OBJECT(bytearray);
    assert(PyByteArray_CheckExact(bytearray));

    PyObject *result = PyByteArray_FromObject(bytearray);

    if (unlikely(result == NULL)) {
        return NULL;
    }

    return result;
}

#endif


