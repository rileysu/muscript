a = 1;

mutate: () -> () = @{
  a = 2;
};

mutate ();
log a;
