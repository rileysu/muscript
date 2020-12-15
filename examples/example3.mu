std = import 'std';
list = import 'list';

a = [1, 2, 3];
b = [1, 2, 3, ...];

std.print (list.get a 1);
std.print (list.set a 3 1);

std.print (list.get b 10);
std.print (list.set b 3 4);
