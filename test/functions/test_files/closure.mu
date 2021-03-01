f: Integer -> () -> Integer = @a {
  return @{
    return a; 
  };
};

f1 = f 1;

log $ f1 ();
