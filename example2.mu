std = import 'std';
i = import 'integer';

add = @x {
  out = std.if (std.is_equal 10 x) @{
    return 'Worked!';
  } @{
    std.print x;
    return (add (i.add x 1));
  };

  return out;
};

identity = @x {
  return x;
};

closure = @{
  val = 1;

  return @{
    val = i.add val 1;
    std.print val;
  };
};

std.print (identity 'Hello World!');
