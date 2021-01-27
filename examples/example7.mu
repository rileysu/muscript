io = import 'io';

Tree = [Integer | Tree, ...];

tree1: Tree = [1, [1, 2]];
tree2: Tree = [1, [1, [2.2]]];

io.print Tree;
