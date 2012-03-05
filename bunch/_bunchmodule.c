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
Bunch_setattro(PyObject *self, PyObject *_k, PyObject *_v)
{
    /* Python code is:
    
        try:
            object.__getattribute__(self, k)                 # 1)
        except AttributeError:
            try:
                self[k] = v                                  # 2)
            except:
                raise AttributeError(k)                      # 3)
        else:
            object.__setattr__(self, k, v)                   # 4)
    */
    
    char *k = PyString_AsString(_k);
    
    PyObject *__builtin__ = PyImport_AddModule("__builtin__");
    PyObject *object = PyObject_GetAttrString(__builtin__, "object"); /* New ref */
    
    /* 1) Try getting ahold of an attribute first ..
    */
    PyObject *ret = PyObject_CallMethod(object, "__getattribute__", "Os", self, k); /* New ref */
    Py_XDECREF(object);
    
    PyObject *err_occurred = PyErr_Occurred();
    
    if(err_occurred) {
        Py_XDECREF(ret);
        if(PyErr_ExceptionMatches(PyExc_AttributeError)) {
        
            /* 2) .. ignore AttributeError and attempt to insert a key .. */
            PyErr_Clear();
            int set_item_result = PyDict_SetItem(self, _k, _v);
            if(set_item_result == 0) {
                return 0;
            }
            else {
                /* 3) .. give up with an AttributeError */
                (void)PyErr_Format(PyExc_AttributeError, "\%s", k);
                return -1;
            }
        }
        else {
            return -1;
        }
    }
    else {
        return 0;
    }
}

/* 
    __getattr__
*/
static PyObject *
Bunch_getattro(PyObject *self, PyObject *_k)
{
    /* Python code is:
    
        try:
            return object.__getattribute__(self, k)          # 1)
        except AttributeError:
            try:
                return self[k]                               # 2)
            except KeyError:
                raise AttributeError(k)                      # 3)
    */
    
    char *k = PyString_AsString(_k);
    
    PyObject *__builtin__ = PyImport_AddModule("__builtin__");
    PyObject *object = PyObject_GetAttrString(__builtin__, "object");
    
    /* 1) Try getting ahold of an attribute first ..
    */
    PyObject *ret = PyObject_CallMethod(object, "__getattribute__", "Os", self, k); /* New ref */
    Py_XDECREF(object);
    
    PyObject *err_occurred = PyErr_Occurred();
    
    if(err_occurred) {
        Py_XDECREF(ret);
        if(PyErr_ExceptionMatches(PyExc_AttributeError)) {
        
            /* 2) .. ignore AttributeError and see if there's a key of that name .. */
            PyErr_Clear();
            PyObject *item = PyDict_GetItem(self, _k); /* Borrowed ref */
            if(item != NULL) {
                Py_INCREF(item);
                return item;
            }
            else {
                /* 3) .. give up with an AttributeError */
                (void)PyErr_Format(PyExc_AttributeError, "\%s", k);
                return NULL;
            }
        }
        else {
            return NULL;
        }
    }
    else {
        return ret;
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
    0,                       /* tp_getattr */
    0,                       /* tp_setattr */
    0,                       /* tp_compare */
    0,                       /* tp_repr */
    0,                       /* tp_as_number */
    0,                       /* tp_as_sequence */
    0,                       /* tp_as_mapping */
    0,                       /* tp_hash */
    0,                       /* tp_call */
    0,                       /* tp_str */
    (getattrofunc)Bunch_getattro,                       /* tp_getattro */
    (setattrofunc)Bunch_setattro,                       /* tp_setattro */
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
    if (PyType_Ready(&BunchType) < 0) {
        return;
    }

    m = Py_InitModule3("_bunch", NULL, "Bunch module (C implementation)");
    if (m == NULL) {
        return;
    }

    Py_INCREF(&BunchType);
    PyModule_AddObject(m, "Bunch", (PyObject *) &BunchType);
}
