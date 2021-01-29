O = {
  int: Integer,
  dec: Decimal,
  list: [Integer, ...],
  fun: Integer -> Integer,
  otherobj: {
    a: Integer,
    b: Integer
  }
};

o: O = {
  int = 1,
  dec = 1.1,
  list = [1, 2, 3],
  fun = @x { return x; },
  otherobj = { a = 1, b = 2 }
};

log o.fun;
log o;
