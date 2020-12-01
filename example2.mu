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
  std.print 'Should run!';
  return x;
  std.print 'Not supposed to run';
};

closure = @{
  val = 1;

  return @{
    val = i.add val 1;
    std.print val;
  };
};

inc = closure ();

inc ();
inc ();
inc ();
