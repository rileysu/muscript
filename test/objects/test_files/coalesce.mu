'Coalesce various things and use types to check';
a: {} = {} {};
log a;

b: { a = 1 } = {} { a = 1 };
log b;

c: { a = 3, b = 2 } = { a = 2 } { a = 1 } { a = 3, b = 2 };
log c;
