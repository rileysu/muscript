func1 = @{ return 1; };
log func1;
func2 = @{ return 2; };
log func2;
func3 = @{ return 3; };
log func3;
func4 = @{ return 4; };
log func4;
func5 = @{ return 5; };
log func5;

a = func1 func2 func3;
log a;

b = func1 (func2 func3) (func4 func5);
log b;
