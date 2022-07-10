"""
Role Assignment simulator script based on MQTT
install Paho MQTT Client using the following
pip install paho-mqtt


"""


import json
import random
import time
import paho.mqtt.client as mqtt


device_token = "ROLE_ASSIGNMENT"        #giving a human readable device ID

username = ""

password = ""

role_topic_1 = "/truck/truckRole/1"   #for getting the data related to role assignment of Truck 1
role_topic_2 = "/truck/truckRole/2"   #for getting the data related to role assignment of Truck 1
role_topic_3 = "/truck/truckRole/3"   #for getting the data related to role assignment of Truck 1
role_topic_4 = "/truck/truckRole/4"   #for getting the data related to role assignment of Truck 1
assigned_role_topic = "/truck/truckRole/assigned"

truck1Role =""
truck2Role=""
truck3Role=""
truck4Role=""

truck1MasterCount = 0
truck2MasterCount = 0
truck3MasterCount = 0
truck4MasterCount = 0

numberOfTrucks =4
truckResponseReceived =0

payload =""
payloadJson = ""
newPayload = False

"""
Function: for connecting to MQTT server with subscriptions
Callback function: executed when msg is being received on the subscribed topic
"""


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global newPayload       #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    global payload          #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    print(msg.topic+" "+str(msg.payload))
    payload = str(msg.payload)
    newPayload = True
    print("newPayload : " + str (newPayload))

# The callback for when the client receives a CONNACK response from the server for truck 1
def on_connect_truck1(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(role_topic_1)

# The callback for when a PUBLISH message is received from the server for truck 1
def on_message_truck1(client, userdata, msg):
    global newPayload       #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    global payload          #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    print(msg.topic+" "+str(msg.payload))
    payload = str(msg.payload)
    newPayload = True
    print("newPayload : " + str (newPayload))

# The callback for when the client receives a CONNACK response from the server for truck 2
def on_connect_truck2(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(role_topic_2)

# The callback for when a PUBLISH message is received from the server for truck 2
def on_message_truck2(client, userdata, msg):
    global newPayload       #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    global payload          #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    print(msg.topic+" "+str(msg.payload))
    payload = str(msg.payload)
    newPayload = True
    print("newPayload : " + str (newPayload))

# The callback for when the client receives a CONNACK response from the server for truck 3
def on_connect_truck3(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(role_topic_3)

# The callback for when a PUBLISH message is received from the server for truck 3
def on_message_truck3(client, userdata, msg):
    global newPayload       #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    global payload          #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    print(msg.topic+" "+str(msg.payload))
    payload = str(msg.payload)
    newPayload = True
    print("newPayload : " + str (newPayload))

# The callback for when the client receives a CONNACK response from the server for truck 4
def on_connect_truck4(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(role_topic_4)

# The callback for when a PUBLISH message is received from the server for truck 4
def on_message_truck4(client, userdata, msg):
    global newPayload       #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    global payload          #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    print(msg.topic+" "+str(msg.payload))
    payload = str(msg.payload)
    newPayload = True
    print("newPayload : " + str (newPayload))

def handling_payload ():
    global payloadJson
    global truckResponseReceived,truck1MasterCount,truck2MasterCount,truck3MasterCount,truck4MasterCount
    print("Handling Payload: " + payload)
    payload2 = payload[2:(len(payload) - 1)] #making a substring to make it a valid JSON from the received msg i.e. b'{"tok": "SLAVE_TRUCK_1", "ts": 1653744036, "speed": 44, "direction": "RIGHT"}'
    print("payload2 after making substring is : " + payload2)
    payloadJson = json.loads(payload2)
    print(payloadJson['truckID'])
    print(payloadJson['masterCount'])
    if payloadJson['truckID'] == "TRUCK_1":
        truck1MasterCount = payloadJson['masterCount']
        truckResponseReceived = truckResponseReceived +1
    elif payloadJson['truckID'] == "TRUCK_2":
        truck2MasterCount = payloadJson['masterCount']
        truckResponseReceived = truckResponseReceived + 1
    elif payloadJson['truckID'] == "TRUCK_3":
        truck3MasterCount = payloadJson['masterCount']
        truckResponseReceived = truckResponseReceived + 1
    elif payloadJson['truckID'] == "TRUCK_4":
        truck4MasterCount = payloadJson['masterCount']
        truckResponseReceived = truckResponseReceived + 1


"""
End of Function
"""

# main Code Starts from here

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

clientTruck1 = mqtt.Client()
clientTruck1.on_connect = on_connect_truck1
clientTruck1.on_message = on_message_truck1

clientTruck2 = mqtt.Client()
clientTruck2.on_connect = on_connect_truck2
clientTruck2.on_message = on_message_truck2

clientTruck3 = mqtt.Client()
clientTruck3.on_connect = on_connect_truck3
clientTruck3.on_message = on_message_truck3

clientTruck4 = mqtt.Client()
clientTruck4.on_connect = on_connect_truck4
clientTruck4.on_message = on_message_truck4

clientTruck1.subscribe(role_topic_1)
clientTruck2.subscribe(role_topic_2)
clientTruck3.subscribe(role_topic_3)
clientTruck4.subscribe(role_topic_4)

client.username_pw_set(username, password)
client.connect("broker.hivemq.com", 1883, 60)

clientTruck1.username_pw_set(username, password)
clientTruck1.connect("broker.hivemq.com", 1883, 60)

clientTruck2.username_pw_set(username, password)
clientTruck2.connect("broker.hivemq.com", 1883, 60)

clientTruck3.username_pw_set(username, password)
clientTruck3.connect("broker.hivemq.com", 1883, 60)

clientTruck4.username_pw_set(username, password)
clientTruck4.connect("broker.hivemq.com", 1883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
#client.loop_forever()

client.loop_start()
clientTruck1.loop_start()
clientTruck2.loop_start()
clientTruck3.loop_start()
clientTruck4.loop_start()



###############################################################


try:
    while True:

        if truckResponseReceived == numberOfTrucks:
            print("Response of all the trucks Received")
            timeStamp = time.localtime(time.time())
            timeStampString= str (timeStamp.tm_hour)+ ":" + str(timeStamp.tm_min)+":"+str(timeStamp.tm_sec)
            if ((truck1MasterCount > 0 ) & (truck1MasterCount > truck2MasterCount) & (truck1MasterCount > truck3MasterCount) & (truck1MasterCount > truck4MasterCount)):
                truck1Role="MASTER"
                truck2Role = "SLAVE_1"
                truck3Role = "SLAVE_2"
                truck4Role = "SLAVE_3"
            elif ((truck2MasterCount > 0 ) & (truck2MasterCount > truck1MasterCount) & (truck2MasterCount > truck3MasterCount) & (truck2MasterCount > truck4MasterCount)):
                truck2Role="MASTER"
                truck1Role = "SLAVE_1"
                truck3Role = "SLAVE_2"
                truck4Role = "SLAVE_3"
            elif ((truck3MasterCount > 0 ) & (truck3MasterCount > truck2MasterCount) & (truck3MasterCount > truck1MasterCount) & (truck3MasterCount > truck4MasterCount)):
                truck3Role="MASTER"
                truck1Role = "SLAVE_1"
                truck2Role = "SLAVE_2"
                truck4Role = "SLAVE_3"
            elif ((truck4MasterCount > 0 ) & (truck4MasterCount > truck2MasterCount) & (truck4MasterCount > truck3MasterCount) & (truck4MasterCount > truck1MasterCount)):
                truck4Role="MASTER"
                truck1Role = "SLAVE_1"
                truck2Role = "SLAVE_2"
                truck3Role = "SLAVE_3"
            truck_data = {
                "truckID": device_token,
                "ts": timeStampString,
                "truck1Role": truck1Role,
                "truck2Role": truck2Role,
                "truck3Role": truck3Role,
                "truck4Role": truck4Role,
            }
            json_string = json.dumps(truck_data)
            # print(truck_data)
            print("Payload for RoleAssignment truck is: ")
            print(json_string)
            client.publish(assigned_role_topic, json_string)
            client.publish(assigned_role_topic, json_string)
            client.publish(assigned_role_topic, json_string)
            break

        print("newPayload status in while loop: " + str(newPayload))
        if (newPayload == True):
            print("New Payload Received")
            handling_payload()
            newPayload = False
        time.sleep(10)

except KeyboardInterrupt():
    print("Press Ctrl-C to terminate while statement")
    pass






