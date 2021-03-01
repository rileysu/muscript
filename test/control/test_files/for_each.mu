ctrl = import 'control';

a = [1, 2, 3, 4];
b = <1, 2, 3, 4>;

ctrl.for_each a @x {
  log x;
};

ctrl.for_each b @x {
  log x;
};
