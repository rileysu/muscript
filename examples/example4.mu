std = import 'std';

Type = { a: Integer, b: Decimal };

o: Type; 
o = { a = 1, b = 2.2 };
o = o { a = 2 };
o = o { a = 2.2 };

std.print o;
