io = import 'io';

a = 1.1;

double: Integer -> Integer -> Decimal = @int {
  return @dec {
    return 2.2;
  };
};

io.print (double 1 1);

f: Function = @x {
  return x;
};

f_int: Integer -> Integer = f;
f_dec: Decimal -> Decimal = f_int;

io.print (f_int 1);
io.print (f_dec 1.1);

b = a;
c = b;
d = c;

io.print d;
