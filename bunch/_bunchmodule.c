/*
    MIT License
    (c) 2012 Dariusz Suchojad <dsuch at gefira.pl>
*/

#include <Python.h>

#ifndef _BUNCH_SUCCESS
#define _BUNCH_SUCCESS 0
#endif

typedef struct {
    PyDictObject HEAD;
} Bunch;

static PyMethodDef Bunch_methods[] = {
    {NULL,	NULL},
};

static int
Bunch_init(Bunch *self, PyObject *args, PyObject *kwds)
{
    if (PyDict_Type.tp_init((PyObject *)self, args, kwds) < 0)
        return -1;
    return 0;
};

/* 
    __setattr__
*/
static int
Bunch_setattr(PyObject *self, char *name, PyObject *value)
{
    int result = 0;
    
    result = PyDict_SetItemString(self, name, value);
    if(result == _BUNCH_SUCCESS) {
        return _BUNCH_SUCCESS;
    }
    else {
        (void)PyErr_Format(PyExc_AttributeError, "(Bunch_setattr) \%s", name);
        return -1;
    }
}

/* 
    __getattr__
*/
static PyObject *
Bunch_getattr(PyObject *self, const char *name)
{
    PyObject *_name = NULL;
    PyObject *_attr = NULL;

    _name = PyString_FromString(name);
    if(_name == NULL) {
        (void)PyErr_Format(PyExc_MemoryError, "(Bunch_getattr) Could not create PyString from char *");
        return NULL;
    }
    
    _attr = PyObject_GenericGetAttr(self, _name);
    Py_XDECREF(_name);
    
    if(_attr != NULL) {
        return _attr;
    }
    else {
        _attr = PyDict_GetItemString(self, name);
        if(_attr == NULL) {
            (void)PyErr_Format(PyExc_AttributeError, "(Bunch_getattr) \%s", name);
            return NULL;
        }
        return _attr;
    }
}


static PyTypeObject BunchType = {
    PyObject_HEAD_INIT(NULL)
    0,                       /* ob_size */
    "bunch._bunch.Bunch",           /* tp_name */
    sizeof(Bunch),           /* tp_basicsize */
    0,                       /* tp_itemsize */
    0,                       /* tp_dealloc */
    0,                       /* tp_print */
    (getattrfunc)Bunch_getattr,           /* tp_getattr */
    (setattrfunc)Bunch_setattr,           /* tp_setattr */
    0,                       /* tp_compare */
    0,                       /* tp_repr */
    0,                       /* tp_as_number */
    0,                       /* tp_as_sequence */
    0,                       /* tp_as_mapping */
    0,                       /* tp_hash */
    0,                       /* tp_call */
    0,                       /* tp_str */
    0,                       /* tp_getattro */
    0,                       /* tp_setattro */
    0,                       /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
      Py_TPFLAGS_BASETYPE | Py_TPFLAGS_DICT_SUBCLASS,   /* tp_flags */
    0,                       /* tp_doc */
    0,                       /* tp_traverse */
    0,                       /* tp_clear */
    0,                       /* tp_richcompare */
    0,                       /* tp_weaklistoffset */
    0,                       /* tp_iter */
    0,                       /* tp_iternext */
    Bunch_methods,           /* tp_methods */
    0,                       /* tp_members */
    0,                       /* tp_getset */
    0,                       /* tp_base */
    0,                       /* tp_dict */
    0,                       /* tp_descr_get */
    0,                       /* tp_descr_set */
    0,                       /* tp_dictoffset */
    (initproc)Bunch_init,    /* tp_init */
    0,                       /* tp_alloc */
    0,                       /* tp_new */
};

PyMODINIT_FUNC
init_bunch(void)
{
    PyObject *m;

    BunchType.tp_base = &PyDict_Type;
    if (PyType_Ready(&BunchType) < 0)
        return;

    m = Py_InitModule3("_bunch", NULL, "Bunch module (C implementation)");
    if (m == NULL)
        return;

    Py_INCREF(&BunchType);
    PyModule_AddObject(m, "Bunch", (PyObject *) &BunchType);
}
