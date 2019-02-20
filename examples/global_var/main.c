int musl_global = 12345;

int musl_func() {
  return musl_global - 12345;
}

int main() {
  return musl_func();
}
