class A {
public:
  A();
  ~A();

private:
  int i = 0;
};

A::A() {
  i++;
}

A::~A() {
  i--;
}

A global_a;

int main() {
  return 0;
}
