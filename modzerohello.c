#include <string.h>
#include "py/runtime.h"

STATIC mp_obj_t mod_zerohello_helloworld(void) {
    const char *sentence = "Hello from zero!\n";
    return mp_obj_new_str(sentence, (mp_uint_t)strlen(sentence), false);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(mod_zerohello_helloworld_obj, mod_zerohello_helloworld);

STATIC const mp_map_elem_t mp_module_zerohello_globals_table[] = {
    { MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_zerohello) },
    { MP_OBJ_NEW_QSTR(MP_QSTR_helloworld), (mp_obj_t)&mod_zerohello_helloworld_obj },
};

STATIC MP_DEFINE_CONST_DICT(mp_module_zerohello_globals, mp_module_zerohello_globals_table);

const mp_obj_module_t mp_module_zerohello = {
    .base = { &mp_type_module },
    .name = MP_QSTR_zerohello,
    .globals = (mp_obj_dict_t*)&mp_module_zerohello_globals,
};
