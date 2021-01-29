o = {
  f = @x {
    return self;
  }
};

log o.f;
log o;
log (o.f ());
