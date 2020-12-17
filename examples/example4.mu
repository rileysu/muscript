std = import 'std';

Type = {
  print: Function,
  string: String
};

constructor = @str {
  return (Type {
    print = @{ std.print str; return str; },
    string = 'Hello World!'
  });
};


o = constructor 'Test World!';
std.print o;
o.print ();

modifier = {
  print = @str { std.print str; return str; }
};

std.print 'Before';
std.print o;
std.print modifier;


o = o modifier;


std.print 'After';
std.print o;


std.print 'Out';
o.print 'Second Test!';
