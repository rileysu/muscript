direction = {
  up = 0,
  down = 1
};
Direction = direction.up | direction.down;

constructor = @{ 
  state: Direction = direction.up;

  return {
    set_up = @{
      state = direction.up;
    },
    set_down = @{
      state = direction.down;
    },
    get_state = @{
      return state;
    }
  };
};

o1 = constructor ();
o2 = constructor ();

o1.set_up ();
log $ o1.get_state ();

o2.set_down ();
log $ o2.get_state ();

o1.set_up ();
log $ o2.get_state ();
