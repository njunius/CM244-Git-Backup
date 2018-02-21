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

  def set_fleeing(self):
    self.state = 'fleeing'
    try:
        self.target = self.body.find_nearest('Nest')
        self.body.go_to(self.target)
    except ValueError:
        self.body.stop()
        self.state = 'idle'
        
  def set_attacking(self):
    self.body.set_alarm(1)
    self.state = 'attacking'
    try:
        self.target = self.body.find_nearest('Mantis')
        self.body.follow(self.target)
    except ValueError:
        self.body.stop()
        self.state = 'idle'

  def set_harvesting(self):
    self.body.set_alarm(1)
    self.state = 'harvesting'
    if not self.has_resources:
        try:
            self.target = self.body.find_nearest('Resource')
            self.body.go_to(self.target)
        except ValueError:
            self.body.stop()
            self.state = 'idle'
    else:
        try:
            self.target = self.body.find_nearest('Nest')
            self.body.go_to(self.target)
        except ValueError:
            self.body.stop()
            self.state = 'idle'
            
  def set_building(self):
    self.state = 'building'
    
    try:
        self.target = self.body.find_nearest('Nest')
        self.body.go_to(self.target)
    except ValueError:
        self.body.stop()
        self.state = 'idle'

  def handle_event(self, message, details):   
    if message == 'order':
        if type(details) is tuple:
            self.body.go_to(details)
            self.body.set_alarm(1)
            self.state = 'moving'
        
        elif type(details) is str:
            if details == 'i':
                self.body.stop()
                self.body.set_alarm(1)
                self.state = 'idle'
            
            elif details == 'a':
                self.set_attacking()
                
            elif details == 'h':
                self.set_harvesting()
          
            elif details == 'b':
                self.set_building()
                
    elif message == 'timer':    
        if self.state == 'attacking':
            self.set_attacking()
            
        elif self.state == 'harvesting':
            self.set_harvesting()
            
    elif message == 'collide':
        self.target = details['who']
        if self.body.amount < 0.5 and self.state is not 'fleeing':
            self.set_fleeing()
        
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
                self.set_harvesting()
        
        elif details['what'] == 'Resource' and self.state == 'harvesting' and not self.has_resources:
            self.target.amount -= self.harvest_amount
            self.has_resources = True
            self.set_harvesting()