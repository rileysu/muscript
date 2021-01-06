io = import 'io';

o = {
  a = 1,
  b = 2.2,
  f = @ {
    io.print self.a;
  },
  otwo = {
    a = 2,
    b = 1.1,
    f = @ {
      io.print self.a;
    }
  }
};

o.f ();
o.otwo.f ();
