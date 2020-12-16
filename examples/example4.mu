std = import 'std';

Type = { a: Integer, b: Decimal };

o: Type = Type { a = 1, b = 2.2 };


std.print Type;
std.print { a = 1, b = 2.2 };
std.print o;

std.print (Integer '123');
