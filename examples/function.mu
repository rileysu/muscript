std = import 'std';

double: Integer -> Decimal -> Decimal = @int {
  return @dec {
    return 2.2;
  };
};

std.print (double 1 2.2);
