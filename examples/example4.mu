std = import 'std';

o = { a = 1, b = 2 };
o = o { a = 2 };

std.print o;
