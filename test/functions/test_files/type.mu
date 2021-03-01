a: Function = @{ return (); };
log a;

b: Integer -> Integer = @x { return x; };
log b;
log $ b 1;

c: Integer -> Integer -> Integer = @x {
  return @y {
    return y;
  };
};
log c;
log $ c 1 2;
