std = import std;

o = {
  a: Integer = 1,
  b: Decimal = 1.2,
  c: List = [1, 2, 3],
  d: Set = <1, 2, 3>
};

f: Integer -> Integer -> Integer = @a {
  o = { attr = 1 };
  out = add a b;
};

long_function 1 2.5 3. 'Hello' (compound 1 2);

std.print std.capitalise 'Hello World';
