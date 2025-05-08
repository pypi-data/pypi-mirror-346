#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "pm_encrypt.h"

static PyObject* py_encrypt(PyObject *self, PyObject *args) {
    const char *input;
    const char *key;
    Py_ssize_t input_len, key_len;

    if (!PyArg_ParseTuple(args, "y#y#", &input, &input_len, &key, &key_len))
        return NULL;

    unsigned char *buffer = malloc(input_len);
    if (!buffer) return PyErr_NoMemory();
    memcpy(buffer, input, input_len);

    Encrypt(buffer, (unsigned char *)key, input_len);

    PyObject *result = PyBytes_FromStringAndSize((char *)buffer, input_len);
    free(buffer);
    return result;
}

static PyObject* py_decrypt(PyObject *self, PyObject *args) {
    const char *input;
    const char *key;
    Py_ssize_t input_len, key_len;

    if (!PyArg_ParseTuple(args, "y#y#", &input, &input_len, &key, &key_len))
        return NULL;

    unsigned char *buffer = malloc(input_len);
    if (!buffer) return PyErr_NoMemory();
    memcpy(buffer, input, input_len);

    Decrypt(buffer, (unsigned char *)key, input_len);

    PyObject *result = PyBytes_FromStringAndSize((char *)buffer, input_len);
    free(buffer);
    return result;
}

static PyMethodDef PMMethods[] = {
    {"Encrypt", py_encrypt, METH_VARARGS, "Encrypt data with key"},
    {"Decrypt", py_decrypt, METH_VARARGS, "Decrypt data with key"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pm_module = {
    PyModuleDef_HEAD_INIT,
    "PM", NULL, -1, PMMethods
};

PyMODINIT_FUNC PyInit_PM(void) {
    return PyModule_Create(&pm_module);
}
