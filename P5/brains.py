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
    # TODO: IMPLEMENT THIS METHOD
    self.body = body
    self.state = 'idle'
    self.has_resources = False
    self.target = None
    self.harvest_amount = 0.1

  def set_attacking(self):
    self.body.set_alarm(1)
    self.state = 'attacking'
    try:
        self.body.follow(self.body.find_nearest('Mantis'))
    except ValueError:
        self.body.stop()
        self.state = 'idle'

  def set_harvesting(self):
    #self.body.set_alarm(1)
    self.state = 'harvesting'
    if not self.has_resources:
        try:
            self.body.go_to(self.body.find_nearest('Resource'))
        except ValueError:
            self.body.stop()
            self.state = 'idle'
    else:
        try:
            self.body.go_to(self.body.find_nearest('Nest'))
        except ValueError:
            self.body.stop()
            self.state = 'idle'
            
  def set_building(self):
    self.body.set_alarm(1)
    self.state = 'building'
    
    try:
        self.body.go_to(self.body.find_nearest('Nest'))
    except ValueError:
        self.body.stop()
        self.state = 'idle'

  def handle_event(self, message, details):
    # TODO: IMPLEMENT THIS METHOD
    #  (Use helper methods and classes to keep your code organized where
    #  approprioate.)
    
    if message == 'order':
        if type(details) is tuple:
            self.body.go_to(details)
            self.body.set_alarm(1)
            self.state = 'moving'
        
        elif type(details) is str:
            if details == 'i':
                self.body.stop()
                #self.body.set_alarm(1)
                self.state = 'idle'
            
            elif details == 'a':
                self.set_attacking()
                
            elif details == 'h':
                self.set_harvesting()
          
            elif details == 'b':
                self.set_building()
                
    elif message == 'timer':
        if self.body.amount < 0.5:
            self.state = 'fleeing'
            self.body.go_to(self.body.find_nearest('Nest'))
            
        elif self.state == 'attacking':
            self.set_attacking()

            
    elif message == 'collide':
        if details['what'] == 'Mantis' and self.state == 'attacking':
            target = details['who']
            target.amount -= 0.07
            self.set_attacking()
        
        elif details['what'] == 'Nest':
            target = details['who']
            if self.state == 'building':
                target.amount += self.harvest_amount * 0.01
                if target.amount >= 1.0:
                    self.body.stop()
                    self.state = 'idle'
            elif self.state == 'fleeing':
                self.body.amount += 0.05
                if self.body.amount >= 1.0:
                    self.body.stop()
                    self.state = 'idle'
            elif self.state == 'harvesting' and self.has_resources:
                self.has_resources = False
                self.set_harvesting()
        
        elif details['what'] == 'Resource' and self.state == 'harvesting' and not self.has_resources:
            target = details['who']
            target.amount -= self.harvest_amount
            self.has_resources = True
            self.set_harvesting()