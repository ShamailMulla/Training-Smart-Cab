import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""
    success=0.0

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.actions=[None, 'left', 'right', 'forward']
        self.success = 0.0
        self.total = 0.0
        self.Q={}

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.gamma = 0.1 #discount
        self.l_rate = 0.8 #alpha
        self.curr_action = None
        #self.prev_action = None
        self.prev_q = 50
        self.curr_q = None
        self.policy = None
        self.prev_rew = 0.0
        self.new_rew = 0.0
        self.total_rew = 0.0
        self.r=0.0
        self.action=None
        self.total = self.total+1

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        

        # TODO: Update state
        #self.state={'light': 'green', 'oncoming': None, 'left': None, 'right': None}
        #self.state = (("lights", inputs['light']), ('oncoming', inputs['oncoming']), ('right', inputs['right']), ('left', inputs['left']), ("waypoint", self.next_waypoint))
        self.state = (("light", inputs['light']), ('oncoming', inputs['oncoming']), ('right', inputs['right']), ('left', inputs['left']), ("waypoint", self.next_waypoint))
        # TODO: Select action according to your policy
        #reward = self.env.act(self, action)
        #self.action = action     
        
        self.curr_state = self.state
        best_q = -999
        for a in self.actions:            
            # Execute action and get reward
            reward = self.env.act(self, a)
            self.action = a
            #reward = self.env.act(self, action)
            # TODO: Learn policy based on state, action, reward
            self.total_rew = self.total_rew + reward
            self.curr_q = (reward + (self.gamma**self.total)*self.prev_q)
            self.prev_rew = self.new_rew
            if self.curr_q > best_q:
                best_q = self.curr_q
                best_a = a
            if (self.state, best_a) not in self.Q.keys():
                self.Q[(self.state, best_a)] = best_q
        self.curr_q = (1-self.l_rate)*(self.prev_q) + self.l_rate*(self.curr_q)
        self.prev_q = self.l_rate*(self.curr_q)
        action=best_a
        if self.env.done:
            self.success = self.success + 1
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
        self.prev_action = self.curr_action
        self.prev_rew = self.total_rew
        
        self.print_success()

    def print_success(self):
        print "Success value: ",format(float(self.success/self.total))
    
def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.001, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

if __name__ == '__main__':
    run()
    
    
