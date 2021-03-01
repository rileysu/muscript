o = {
  state = 0,

  sub_o = {
    state = 1,

    f = @{
      return $ self;
    }
  },

  f = @{
    return $ self;
  }
};

ex1 = o.f ();
ex2 = o.sub_o.f ();

log ex1.state;
log ex2.state;
