std = import 'std';
ctrl = import 'control';

Type = Integer | Decimal;

a: Type = 1;
b: Type = 2.2;

matcher = @arg {
  return (ctrl.match arg [
    [Integer, @x {
      std.print 'Found Integer!';
      std.print x;
      return x;
    }],
    [Decimal, @x {
      std.print 'Found Decimal!';
      std.print x;
      return x;
    }]
  ]);
};

matcher a;
matcher b;
