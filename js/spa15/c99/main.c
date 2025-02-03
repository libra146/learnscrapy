#include "wasm.h"
#include <stdio.h>
#include <stdlib.h>
void w2c_wasi__snapshot__preview1_proc_exit(struct w2c_wasi__snapshot__preview1*, u32){};

w2c_Wasm instance;//全局可用

void init_wasm(){
    wasm_rt_init();
    wasm2c_Wasm_instantiate(&instance, NULL);
}

char* encrypt(const char* a1,const char* a2){
    u32 str_len1 = strlen(a1) + 1;
    u32 ptr1 = w2c_Wasm_stackAlloc(&instance,str_len1);
    memcpy(w2c_Wasm_memory(&instance)->data + ptr1, a1, str_len1);
    u32 str_len2 = strlen(a2) + 1;
    u32 ptr2 = w2c_Wasm_stackAlloc(&instance,str_len2);
    memcpy(w2c_Wasm_memory(&instance)->data + ptr2, a2, str_len2);
    u32 out_ptr = w2c_Wasm_encrypt(&instance,ptr1, ptr2);
    char* out_str = (char *)malloc(128);
    memcpy(out_str, w2c_Wasm_memory(&instance)->data + out_ptr, 128);
    w2c_Wasm_stackRestore(&instance,ptr1);
    w2c_Wasm_stackRestore(&instance,ptr2);
    return out_str;
}

// 用于释放 encrypt 函数分配内存的函数
void free_encrypt_result(char* result) {
    free(result);
}

int main() {
    init_wasm();
    char* a1 = "/api/movie";//为了测试，先写死
    printf("%s\n", a1);
    char* a2 = "1738565280";
    printf("%s\n", a2);

    char* out_str=encrypt(a1,a2);

    printf("%s\n",out_str);
    free(out_str);

    return 0;
}
