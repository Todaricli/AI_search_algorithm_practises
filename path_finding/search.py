class SearchProblem(object):
    """A search problem consists of:
    * a start node
    * a neighbours function that gives the neighbours of a node
    * a specification of a goal
    * a (optional) heuristic function.
    The methods must be overridden to define a search problem."""

    def start_node(self):
        """returns start node"""
        raise NotImplementedError("start_node")  # abstract method

    def is_goal(self, node):
        """is True if node is a goal"""
        raise NotImplementedError("is_goal")  # abstract method

    def get_neighbours(self, node):
        """returns a list of the arcs for the neighbours of node"""
        raise NotImplementedError("neighbours")  # abstract method

    def heuristic(self, n):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""
        return 0


class Arc(object):
    """An arc has a from_node and a to_node node and a (non-negative) cost"""

    def __init__(self, from_node, to_node, cost=1, action=""):
        assert cost >= 0, ("Cost cannot be negative for" +
                           str(from_node) + "->" + str(to_node) + ", cost: " + str(cost))
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost
        self.action = action

    def __repr__(self):
        """string representation of an arc"""
        return str(self.from_node) + " --> " + str(self.to_node)


class Path(object):
    """A path is either a node or a path followed by an arc"""

    def __init__(self, initial, arc=None):
        """initial is either a node (in which case arc is None) or
        a path (in which case arc is an object of type Arc)"""
        self.initial = initial
        self.arc = arc
        if arc is None:
            self.cost = 0
        else:
            self.cost = initial.cost + arc.cost

    def end(self):
        """returns the node at the end of the path"""
        if self.arc is None:
            return self.initial
        else:
            return self.arc.to_node

    def nodes(self):
        """enumerates the nodes for the path.
        This starts at the end and enumerates nodes in the path backwards."""
        current = self
        while current.arc is not None:
            yield current.arc.to_node
            current = current.initial
        yield current.initial

    def initial_nodes(self):
        """enumerates the nodes for the path before the end node.
        This starts at the end and enumerates nodes in the path backwards."""
        if self.arc is not None:
            for nd in self.initial.nodes(): yield nd  # could be "yield from"

    def __len__(self):
        """Returns the length of the path, which is the number of arcs plus one"""
        length = 0
        current = self
        while current.arc is not None:
            length += 1
            current = current.initial
        return length  # Adding 1 for the initial node

    def __lt__(self, other):
        """Compare this path with another path to determine if this path is less than the other path."""
        return self.cost < other.cost

    def __repr__(self):
        """returns a string representation of a path"""
        if self.arc is None:
            return str(self.initial)
        elif self.arc.action:
            return f"{self.initial}\n   --{self.arc.action}--> {self.arc.to_node}"
        else:
            return f"{self.initial} --> {self.arc.to_node}"


class Searcher(object):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    This does depth-first search unless overridden
    """

    def __init__(self, problem):
        """creates a searcher from a problem
        """
        self.max_frontier_length = 1
        self.problem = problem
        self.initialize_frontier()
        self.num_expanded = 0
        self.add_to_frontier(Path(problem.start_node()))

    def initialize_frontier(self):
        """intialises frontier as a list"""
        self.frontier = []

    def empty_frontier(self):
        """returns True if frintier is empty"""
        return self.frontier == []

    def add_to_frontier(self, path):
        self.frontier.append(path)

    def search(self):
        """returns (next) path from the problem's start node
        to a goal node. 
        Returns None if no path exists.
        """
        while not self.empty_frontier():

            self.path = self.frontier.pop()
            self.num_expanded += 1
            if self.problem.is_goal(self.path.end()):  # solution found
                self.solution = self.path  # store the solution found
                return self.path
            else:
                neighbours = self.problem.get_neighbours(self.path.end())
                for arc in neighbours:
                    self.add_to_frontier(Path(self.path, arc))
                self.max_frontier_length = max(self.max_frontier_length, len(self.frontier))



