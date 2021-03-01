ctrl = import 'control';

a = 1;

ctrl.match a [
  [Integer, @x { log 1; }],
  [Integer, @{ log 0; }],
  [Decimal, @{ log 0; }]
];

ctrl.match a [
  [Decimal, @x { log 0; }],
  [Decimal, @{ log 0; }],
  [Integer, @{ log 1; }]
];

ctrl.match a [
  [Decimal, @{ log 0; }],
  [Any, @{ log 1; }]
];

b = [1, 2.0, 'Three'];
c = <1, 2.0, 'Three'>;

ctrl.match b [
  [[Any, Any, Integer], @{ log 0; }],
  [[2.0, 1], @{ log 0; }],
  [[1, 2.0, Any], @{ log 1; }]
];

ctrl.match c [
  [<Integer, Decimal>, @{ log 0; }],
  [<Integer, String>, @{ log 0; }],
  [<Integer, Decimal, String>, @{ log 1; }]
];
