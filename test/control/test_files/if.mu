ctrl = import 'control';

ctrl.if 0 @{
  log 0; 
} @{
  log 1;
};

ctrl.if 1 @{
  log 1; 
} @{
  log 0;
};

ctrl.if 0 @{
  log 0;
} $ ctrl.elif 1 @{
  log 1;
} @{
  log 0;
};

ctrl.if 0 @{
  log 0;
} $ ctrl.elif 0 @{
  log 0;
} $ ctrl.elif 1 @{
  log 1;
} @{
  log 0;
};

ctrl.if 0 @{
  log 0;
} $ ctrl.elif 0 @{
  log 0;
} $ ctrl.elif 0 @{
  log 0;
} @{
  log 1;
};

ctrl.if 0 @{
  log 0;
} $ ctrl.elonly 1 @{
  log 1;
};
