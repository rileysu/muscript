a = 0;

f = @{
  return @{
    return @{
      return @{
        a = 1;
      };
    };
  };
};

f () () () ();
log a;
