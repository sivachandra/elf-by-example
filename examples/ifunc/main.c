
int DEFAULT_RETURN_VALUE = 0;
int SPECIAL_RETURN_VALUE = 111;

int my_special_ifunc() {
  return SPECIAL_RETURN_VALUE;
}

typedef int (*MyIFuncType)();

MyIFuncType my_ifunc_resolver() {
  return my_special_ifunc;
}

int my_ifunc() __attribute__ ((ifunc ("my_ifunc_resolver")));

int main() {
  return my_ifunc();
}
