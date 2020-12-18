std = import 'std';
ctrl = import 'control';

false = 0;
true = 1;

a = false;

val = 'Hello';

matcher: Function = @arg {
  ctrl.match arg [
    [String, @str {
      std.print ('This is a string: ' str);
    }],
    [Integer, @x {
      std.print ('This is an integer: ' (String x));
    }],
    [[1, 2, Integer], @l {
      std.print ('This is some list: ' (String l));
    }],
    [Any, @x {
      std.print ('This was not caught by anything else: ' (String x));
    }]
  ];
};

matcher 'String';
matcher 42;
matcher [1, 2, 42];
matcher <'Something else!', 1>;

f = @{
  std.print b;
};

b = 'Defined after func';

f ();
