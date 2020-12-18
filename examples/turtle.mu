std = import 'std';
int = import 'integer';
ctrl = import 'control';

Turtle = {
  print: Function,
  move_x: Function,
  move_y: Function
};

construct_turtle: Function = @{
  pos_x: Integer = 0;
  pos_y: Integer = 0;

  return (Turtle {
    print = @{
      std.print ('Turtle is at pos_x: ' (String pos_x));
      std.print ('Turtle is at pos_y: ' (String pos_y));
    },
    move_x = @move {
      pos_x = int.add pos_x move;
      return pos_x;
    },
    move_y = @move {
      pos_y = int.add pos_y move;
      return pos_y;
    }
  });
};

turtle1 = construct_turtle ();

turtle1.move_x 2;
turtle1.print ();
