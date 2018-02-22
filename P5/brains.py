import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None

  def handle_event(self, message, details):

    if self.state is 'idle':

      if message == 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state == 'curious':

      if message == 'timer':
        # chase down that slug who bumped into us
        if self.target:
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
    
class SlugBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None
    self.has_resources = False
    self.harvest_amount = 0.1

  # state is a string
  # target can be either a string or an (x,y) tuple
  def set_state(self, state, target):
    self.state = state
    self.body.set_alarm(1)
    try:
        if state == 'moving':
            self.target = target
            self.body.go_to(self.target)
        elif state == 'idle':
            self.body.stop()
        else:
            self.target = self.body.find_nearest(target)
            self.body.follow(self.target)
    except ValueError:
        self.body.stop()
        self.state = 'idle'

  def handle_event(self, message, details):   
    if message == 'order':
        if type(details) is tuple:
            self.set_state('moving', details)
        
        elif type(details) is str:
            if details == 'i':
                self.set_state('idle', None)
            
            elif details == 'a':
                self.set_state('attacking', 'Mantis')
                
            elif details == 'h':
                if self.has_resources:
                    self.set_state('harvesting', 'Nest')
                else:
                    self.set_state('harvesting', 'Resource')
          
            elif details == 'b':
                self.set_state('building', 'Nest')
                
    elif message == 'timer':    
        if self.state == 'attacking':
            self.set_state('attacking', 'Mantis')
        
        elif self.state == 'moving':
            self.set_state('moving', self.target)
        
        elif self.state == 'harvesting':
            if self.has_resources:
                self.set_state('harvesting', 'Nest')
            else:
                self.set_state('harvesting', 'Resource')
            
    elif message == 'collide':
        self.target = details['who']
        if self.body.amount < 0.5 and self.state is not 'fleeing':
            self.set_state('fleeing', 'Nest')
        
        elif details['what'] == 'Mantis' and self.state == 'attacking':
            self.target.amount -= 0.07
        
        elif details['what'] == 'Nest':
            if self.state == 'building':
                self.target.amount += self.harvest_amount * 0.01
                if self.target.amount >= 1.0:
                    self.state = 'idle'
            elif self.state == 'fleeing':
                self.body.amount += 0.05
                if self.body.amount >= 1.0:
                    self.state = 'idle'
            elif self.state == 'harvesting' and self.has_resources:
                self.has_resources = False
                self.set_state('harvesting', 'Resource')
        
        elif details['what'] == 'Resource' and self.state == 'harvesting' and not self.has_resources:
            self.target.amount -= self.harvest_amount
            self.has_resources = True
            self.set_state('harvesting', 'Nest')