f = @{ return 0; };
ident = @x { return x; };

ho = @f {
  return $ f 1;
};

log $ ho ident;
