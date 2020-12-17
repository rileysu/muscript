std = import 'std';

a = {
  a = 1,
  b = 2.2,
  c = 'Hello'
};

b = {
  b = 3.3
};

o = a;

std.print o;

o = o b;

std.print o;
