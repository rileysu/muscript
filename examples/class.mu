eq = import 'eq';
ctrl = import 'control';

// Self uses the object stack to find the appropriate object

Graph = @x {

  return {
    verticies: [x],
    edges: [[x, x]],
    add_vertex: x -> self,
    add_edge: x -> x -> self,
    neighbours: x -> [x]
  };
}

//If the object is assimilated then there is no need to coalesce it with the type?
//Return type of the function checks the return type is correct

construct_graph: x -> Graph x = @{
  return {
    verticies = [],
    edges = [],
    add_vertex = @x {
      return (self { verticies = self.verticies [x] });
    },
    add_edge = @x {
      return @y {
        return (self { edges = self.edges [[x, y]] });
      }
    },
    neighbours = @x {
      ctrl.for_each (self.edges) @{
        ...
      };
      return ...
    }
  };
};
