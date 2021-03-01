o = {
  a = 1,
  modify = @{
    return $ self { a = 0 };
  }
};

log o.a;

o = o.modify ();
o = o.modify ();
log o.a;
