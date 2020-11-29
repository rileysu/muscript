o = {
  a: Integer = 1,
  b: Decimal = 1.2,
  c: List = [1, 2, 3],
  d: Set = <1, 2, 3>
};

f: { a: Integer, b: Integer } -> Integer = @{
  return (add a b);
};

print (f { a = o.a, b = 2 });
