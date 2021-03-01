ctrl = import 'control';

true = 1;
false = 0;
Bool = true | false;

loop0 = true;
loop1 = true;
loop2 = true;
loop3 = true;

cond: () -> Bool = @{
  return $ ctrl.if loop0 @{
    return true;
  } $ ctrl.elif loop1 @{
    return true;
  } $ ctrl.elif loop2 @{
    return true;
  } $ ctrl.elif loop3 @{
    return true;
  } @{
    return false;
  };
};

ctrl.while cond @{
  log 0;

  ctrl.if loop0 @{
    loop0 = false;
  } $ ctrl.elif loop1 @{
    loop1 = false;
  } $ ctrl.elif loop2 @{
    loop2 = false;
  } $ ctrl.elonly loop3 @{
    loop3 = false;
  };
};

log 1;
