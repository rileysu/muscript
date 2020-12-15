std = import 'std';
list = import 'list';

a: [Integer, Integer, Integer] = [1, 2, 3];
a = [4, 5, 6];

b: [Integer, ...] = [1, 2, 3];
b = [1, 2, 3, 4, 5];
b = [...];

c: [Integer, Decimal, ...] = [1, 1.1, 2, 2.2];
c = [1];
c = [...];

d: 1 = 1;
e: 2.2 = 2.3;

std.print a;
std.print b;
std.print c;
