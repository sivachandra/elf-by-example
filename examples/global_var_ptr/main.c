int global_int = 12345;
int *global_int_ptr = &global_int;

int global_func() {
  return *global_int_ptr - 12345;
}

int main() {
  return global_func();
}
