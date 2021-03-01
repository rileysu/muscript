io = import 'io';
ctrl = import 'control';

ctrl.while @{ return 0; } @{
  return ();
};
