std = import 'std';

f = @x {
  std.print x;
};

identity = @x {
  out = x;
}

std.print 'Hello World!';

std.print (identity 'Hello World 2');
