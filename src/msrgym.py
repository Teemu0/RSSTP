from internal import Internal
from external import External

class robot_arm:
    
    def __init__(self, joints_n : int, arm_lengths : float, obstacles : list, initial_position: int, goal_position: tuple, actions):
        """Create a robot arm with charactersitics passed in arguments
        
        Args:
            joints_n (int): number of joints : int : > 0
            arm_lengths (float): arm lenghts : float (TODO: List<float> with size n)
            obstacles (list): list of obstacles in the form [[x1,y1], radius_1, ..., [x_n,y_n], radius_n]
            initial_position (int): initial position of arm in degress : int 0-359 (TODO: List<int> with size n)
            goal_position (tuple): desired point for the arm to reach in coordinates [x,y] (TODO: in degrees?)
            actions (_type_): list of initial possible actions in the form [(0, 1, ... n)]
        """

        self.ext = External(joints_n, initial_position, arm_lengths, obstacles, goal_position)
        self.int = Internal(actions)

    def update_position(self, action : int):
        """ Update position of robot arm through an action from the possible actions set in the constructor

        Args:
            action (int): e.g. 0 = left 1 = right 
        """
        if self.int.transition(action) >= 0:
            self.ext.update(action)

            print("Updated position: " + str(self.get_arm_position()) + " Internal state after update: " + str(self.get_current_internal_state()))

            if self.is_desired_position_reached():
                print("Home positon reached")

    def get_arm_position(self):
        """ Get current arm position

        Returns:
            tuple(int, float): The position of the arm in degrees and coordinates (for end point of arm)
        """
        return self.ext.get_position()

    def is_desired_position_reached(self):
        """ Check whether the set desired position has been reached by the hand.

        Returns:
            int: 0 or 1 (acts as bool)
        """
        return self.ext.get_sensory_data()

    def get_current_internal_state(self):
        """ Get the current internal state

        Returns:
            int: Current state
        """
        return self.int.get_current_state()
        
    # Helper functions
    def split_node(self, n):
        """ Split node n into two nodes, duplicating transitions.

        Args:
            n (int): Node number to split

        Returns:
            NDArray (on success): Resulting matrix after split

            or

            int (on failure): a -1 showing that some matrix validation has failed
        """
        return self.int.split(n)

    def merge_nodes(self, n, m):
        """ Merge nodes 1 and 2 by removing columns and rows n,m and creating one row and column with taking the union of the two nodes

        Args:
            n (int): node 1
            m (int): node 2

        Returns:
            NDArray (on success): Resulting matrix after merge

            or

            int (on failure): a -1 showing that some matrix validation has failed
        """
        return self.int.merge(n, m)

    def add_connection_between_nodes(self, n, m, k):
        """Create a connection between node 1 and 2 through action k.

        Args:
            n (int): node 1
            m (int): node 2
            k (int): action

        Returns:
            NDArray (on success): Resulting matrix after add

            or

            int (on failure): a -1 showing that some matrix validation has failed
        """
        return self.int.add(n, m, k)

    def delete_conection_between_nodes(self, n, m, k):
        """Delete a connection between node 1 and 2 of action k.

        Args:
            n (int): node 1
            m (int): node 2
            k (int): action

        Returns:
            NDArray (on success): Resulting matrix after deletion

            or
            
            int (on failure): a -1 showing that some matrix validation has failed
        """
        return self.int.delete(n,m,k)
    


