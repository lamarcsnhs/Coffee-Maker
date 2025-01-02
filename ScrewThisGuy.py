import time
import sys
import RPi.GPIO as GPIO
import json 
import threading
import traceback
from GmailAPI import Gmail_API as g
import OrderParser as o
import grounds
import Arm
import Pully
import Sensor


from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate
from drinks import drink_list, drink_options
max_stages = 3

GPIO.setmode(GPIO.BCM)



FLOW_RATE = 60.0/100.0

class Bartender(MenuDelegate): 
    

    def __init__(self):
        print("Initializing...")
        #Pully.reset()
        #Pully.up()
        self.possibleDrinks = drink_list
        self.running = False
        # load the pump configuration from file
        self.pump_configuration = Bartender.readPumpConfiguration()
        # GPIO.setup(6, GPIO.OUT, initial=GPIO.HIGH)
        for pump in self.pump_configuration.keys():
            #Finding the pin numbers per pump and seting up the GPIO
            if not self.pump_configuration[pump]['pin'] == 21:
                GPIO.setup(self.pump_configuration[pump]["pin"], GPIO.OUT, initial=GPIO.HIGH)
            #elif not self.pump_configuration[pump]['pin'] == 6:
                # GPIO.setup(self.pump_configuration[pump]["pin"], GPIO.OUT, initial=GPIO.LOW)
                # time.sleep(2)
                #print("asdffdsfsdfsdafdsa")
            else:    
                GPIO.setup(self.pump_configuration[pump]["pin"], GPIO.OUT, initial=GPIO.LOW)
            

        print("Done initializing")

    @staticmethod
    def readPumpConfiguration():
        return json.load(open('/home/lamarcsnhscoffee/Desktop/Coffee-MakerV.2/Coffee-Maker/pump_config.json')) # what value do we want the grinder to manage? (trent)

    def newDay(self):
        waitTime = 20
        pumpThreads = []

        # cancel any button presses while the drink is being made
        # self.stopInterrupts()
        self.running = True

        for pump in self.pump_configuration.keys():
            pump_t = threading.Thread(target=self.pour, args=(self.pump_configuration[pump]["pin"], waitTime))

            if self.pump_configuration[pump]["pin"]==21 or self.pump_configuration[pump]["pin"]==23:
                continue
            pumpThreads.append(pump_t)

        # start the pump threads
        for thread in pumpThreads:
            thread.start()

        # start the progress bar
        #self.progressBar(waitTime)

        # wait for threads to finish
        for thread in pumpThreads:
            thread.join()

        # show the main menu
        #self.menuContext.showMenu()

        # sleep for a couple seconds to make sure the interrupts don't get triggered
        time.sleep(2)

        # reenable interrupts
        # self.startInterrupts()
        self.running = False      

    # def clean(self):
    #     waitTime = 60
    #     pumpThreads = []

    #     # cancel any button presses while the drink is being made
    #     # self.stopInterrupts()
    #     self.running = True

    #     for pump in self.pump_configuration.keys():
    #         pump_t = threading.Thread(target=self.pour, args=(self.pump_configuration[pump]["pin"], waitTime))
    #         if self.pump_configuration[pump]["pin"]==21 or self.pump_configuration[pump]["pin"]==23:
    #             continue
    #         pumpThreads.append(pump_t)

    #     # start the pump threads
    #     for thread in pumpThreads:
    #         thread.start()

    #     # start the progress bar
    #     #self.progressBar(waitTime)

    #     # wait for threads to finish
    #     for thread in pumpThreads:
    #         thread.join()

    #     # show the main menu
    #     #self.menuContext.showMenu()

    #     # sleep for a couple seconds to make sure the interrupts don't get triggered
    #     time.sleep(2)

    #     # reenable interrupts
    #     # self.startInterrupts()
    #     self.running = False
    def clean(self, ingredients, stage):
        self.running = True

        maxTime = 0
        #pumpThreads = []

        for ing in ingredients.keys():
            for stuff in self.pump_configuration.keys():
                if ing == self.pump_configuration[stuff]["type"]:
                    if stuff == "solenoid":
                        solenoidInUse = stuff.pump_configuration["pin"]
                        GPIO.output(solenoidInUse, GPIO.LOW)
                    elif stuff == "pump":
                        waitTime = ingredients[ing] * FLOW_RATE
                        if (waitTime > maxTime):
                            maxTime = waitTime
                            self.pour(self.pump_configuration[stuff]["pin"], waitTime)
                        GPIO.output(solenoidInUse, GPIO.HIGH)
        self.running = False

    def displayMenuItem(self, menuItem):
        print(menuItem.name)

    def pour(self, pin, waitTime):
        print("pour pin", pin)
        if pin == 21:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(waitTime)
            GPIO.output(pin, GPIO.LOW)
        else:
            if not pin == 23:
                GPIO.output(pin, GPIO.LOW)
                time.sleep(waitTime)
                GPIO.output(pin, GPIO.HIGH)
            if pin == 23:
                time.sleep(5)
                Pully.down()
                GPIO.output(pin, GPIO.LOW)
                time.sleep(waitTime)
                GPIO.output(pin, GPIO.HIGH)
                Pully.up()


    def makeDrink(self, ingredients, stage):

        print(f"makeDrink called with stage {stage}")
    # Rest of your code...
# cancel any button presses while the drink is being made
        # self.stopInterrupts()
        #The drink parameter is a string that represents the name of the drink being made 
        #ingredients is a dictionary where the keys are strings representing the names of the ingredients and the values are floats representing the amount of each ingredient required to make the drink.
        #For example a drink like half and half 50% coffee and 50% milk
        #Would have ingredients 'Coffee' : 50, 'Milk' :50

        if ingredients == "ESC":
            return "dumbass. enter a real drink"

        self.running = True

        maxTime = 0
        pumpThreads = []
        #This loop goes though each ingredient 
        for ing in ingredients.keys():
            #This loop looks though each pump in the pump config to see if there is one that matches the label of the ingredent we are attempting to add
            for pump in self.pump_configuration.keys(): 
                if ing == self.pump_configuration[pump]["value"]:
                    #This finds how long we should pour the drink for
                    waitTime = ingredients[ing] * FLOW_RATE
                    if (waitTime > maxTime):
                        maxTime = waitTime
                    #Bro really worte it weird for no reason but args is just the paramenters for the pour method
                    #So this opens a thread which goes to the pour method for each ingredient
                    #THE THREADS HAVENT STARTED YET
                    #Then it adds them to a list of not started threads 
                    #This is statement checks if the arm is in the correct place
                    #print("testing stage pin", self.pump_configuration[pump]["pin"])
                    #print('test stage', stage, ' ', self.pump_configuration[pump]["stage"])

                    if stage == self.pump_configuration[pump]["stage"]:
                     #   print("testing pin", self.pump_configuration[pump]["pin"])
  #                      if stage == 2 and ing == "Froth":
   #                         print("going down")
    #                        FrothArm.down()
                        pump_t = threading.Thread(target=self.pour, args=(self.pump_configuration[pump]["pin"], waitTime))
                        pumpThreads.append(pump_t)
     #                   print('We have made a thread')
      #                  if stage == 2 and ing == "Froth":
       #                         print("works2")
        #                        FrothArm.up()

                    
                        #add frother arm code here



        # start the pump threads
        for thread in pumpThreads:
            thread.start()

        # start the progress bar
        #I dont think we need this
        #self.progressBar(maxTime)

        # wait for threads to finish
        for thread in pumpThreads:
            thread.join()

        # show the main menu
        #Don't think we need this either 
        #self.menuContext.showMenu()


        # sleep for a couple seconds to make sure the interrupts don't get triggered
        time.sleep(2)

        # reenable interrupts
        # self.startInterrupts()
        self.running = False


 
    def run(self):
        self.startInterrupts()
        # main loop
        try:  
            while True:
                time.sleep(0.1)
            
        except KeyboardInterrupt:  
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
        GPIO.cleanup()           # clean up GPIO on normal exit 

        traceback.print_exc()

    def ChooseDrink(self, drinkName):
        for drink in self.possibleDrinks:
            if drink['name'] == drinkName:
                print(drink['ingredients'])
                return drink['ingredients']

orders = []

 
def CheckForOrder():
    ordered = True
    thing = g.checkMail()
    order = thing[0].lower()
    print(order)
    order = o.CheckTextVaildity(order)
    if order is not None and order[0] is not None:
        print('This is the order')
        print(order)
        return order
    else:
        d = 'Please choose from one of these drinks: '
        temp = []
        for drink in drink_list:
            temp.append(drink['name'])  
        d += ', '.join(temp)
        print(d)
        g.send_email_gmail(thing[1], None, d)
        print(thing[1])
        return CheckForOrder()




def orderThread():
    while True:
        o = CheckForOrder()
        print(o)
        orders.append(o)
        print(orders)




#SomethingNasty = {'Milk' : 1, 'Water' : 1}
#bartender.makeDrink(SomethingNasty)
#time.sleep(2)

#print('How many drinks do we want to make')
#drinkLimit = input()

#TODO: add condition for clean to not check orders
if __name__ == "__main__":
    bartender = Bartender()
    #bartender.clean()
    time.sleep(5)
    #bartender.newDay()
    d = []
    for drink in drink_list:
        d.append(drink['name'])  

    gettingOrders = threading.Thread(target=orderThread)
    gettingOrders.start()

    drinkcount = 0

    while True:
        print(orders)
        if len(orders) > 0:
            if (Sensor.doesCupExist(4)):
                stage = 1
                order = orders[0]
                orders.pop(0)
                Bartender.order_name = order
                # Unpack the tuple into drink_name and add_sweetener
                drink_name, add_sweetener = order

                if order == "clean":
                    bartender.clean()
                    Arm.reset()
                else:
                    # make sure the solenoids are off with a quick for loop here 
                    ingredients = bartender.ChooseDrink(drink_name)
                    if ingredients is None:
                        print(f"Drink '{drink_name}' not found.")
                        continue  # Skip to the next iteration
                    if add_sweetener and drink_name != "PSL":
                        sweetener_amount = {'Sweetener': 10}  # Adjust as necessary
                        ingredients.update(sweetener_amount)
                    # Proceed to make the drink
                    for stage in range(0, 5):
                        print(f"Processing stage {stage}")
                        try:
                            bartender.makeDrink(ingredients, stage)
                        except Exception as e:
                            print(f"Exception occurred during makeDrink at stage {stage}: {e}")
                            # Handle the exception as needed
                        # Call Arm.rotate(stage) based on your desired conditions
                        if stage == 2 or stage == 3:
                            print(f"Rotating arm at stage {stage}")
                            Arm.rotate(stage)
                        print("stage " + str(stage))
                    Arm.reset()


        time.sleep(1)

                



    #test2 = input()
    #If that works test this
    #test2 = bartender.ChooseDrink(test2)
    #print(test2)
    #bartender.makeDrink(test2)

    #If that works we just need to connect up the text API

    #If we want to clean the pumps attach water to them and run this code
    #bartender.clean()

    #WTF Does this code do?
    #bartender.buildMenu(drink_list, drink_options)
    #bartender.run()



