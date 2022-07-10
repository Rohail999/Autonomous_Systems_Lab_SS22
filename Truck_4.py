"""
Truck 2 simulator script based on MQTT
install Paho MQTT Client using the following
pip install paho-mqtt

Version 2
TimeStamp is Converted from Epoch to H:M:S
Master gets the data of all the slaves
This version Handles the Payload missing issue
as for each topic separate client is being made and
for each client separate event handlers are made.
So data from subscribed topics doesn't miss at all.
Publishing frequency of all the trucks is same
10 seconds
GPS feature is added in Mater Truck so it gets the latitude and
longitude of at the start of script.
"""


import json
import random
import time
import paho.mqtt.client as mqtt
import math


master_topic = "/truck/masterTruck"
slave1_topic = "/truck/slaveTruck/1"
slave2_topic= "/truck/slaveTruck/2"
slave3_topic = "/truck/slaveTruck/3"
role_topic = "/truck/truckRole/4"   #for publishing the data related to role assignment of Truck 4
assigned_role_topic = "/truck/truckRole/assigned"

device_token = "TRUCK_4"        #giving a human readable device ID
role=""
roleDefined = False

username = ""
password = ""

distanceFromDestination = 9
sensors = 3
random_speed = [30,31,32,33,34,35,40,41,42,43,44,45,46,47,48,49,50]
random_direction = ["LEFT","STOPPED-OBSTACLE DETECTED-CHANGING LANE","RIGHT","FORWARD","REVERSE","FORWARD","LEFT","STOPPED-OBSTACLE DETECTED-CHANGING LANE","FORWARD","REVERSE","RIGHT","STOPPED-OBSTACLE DETECTED-CHANGING LANE","FORWARD","LEFT"]
random_destination =["51.708283675540855, 8.772094256081514", "51.71567491719658, 8.740284213603493","51.72254389850122, 8.74670739525771","51.73079511494316, 8.765293447104725","51.73152320563492, 8.73577362447226"]

payload =""
payloadJson = ""
newPayload = False

observedTruck= (distanceFromDestination,sensors)
distanceDataSet=[4,6,7,5,8]
sensorsDataSet=[3,7,8,5,8]
roleDataSet =["SLAVE","MASTER","MASTER","SLAVE","MASTER"]
k=3
result =[0,0,0,0,0]
masterCount = 0
slaveCount = 0


speedSlave= 10
directionSlave = "FORWARD"
FollowedTS = 0
distanceFromFrontTruck =10
publishTimeDelay = 10
publishMasterTimeDelay = 10
publishSlave1TimeDelay =12
publishSlave2TimeDelay=14
publishSlave3TimeDelay=16


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


# The callback for when the client receives a CONNACK response from the server for Master
def on_connect_master(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(master_topic)

# The callback for when a PUBLISH message is received from the server for Master
def on_message_master(client, userdata, msg):
    global newPayload       #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    global payload          #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    print(msg.topic+" "+str(msg.payload))
    payload = str(msg.payload)
    newPayload = True
    print("newPayload : " + str (newPayload))
# The callback for when the client receives a CONNACK response from the server for slave 1
def on_connect_slave1(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(slave1_topic)

# The callback for when a PUBLISH message is received from the server for slave 1
def on_message_slave1(client, userdata, msg):
    global newPayload       #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    global payload          #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    print(msg.topic+" "+str(msg.payload))
    payload = str(msg.payload)
    newPayload = True
    print("newPayload : " + str (newPayload))

# The callback for when the client receives a CONNACK response from the server for slave 2
def on_connect_slave2(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(slave2_topic)

# The callback for when a PUBLISH message is received from the server for slave 2
def on_message_slave2(client, userdata, msg):
    global newPayload       #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    global payload          #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    print(msg.topic+" "+str(msg.payload))
    payload = str(msg.payload)
    newPayload = True
    print("newPayload : " + str (newPayload))

# The callback for when the client receives a CONNACK response from the server for slave 3
def on_connect_slave3(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(slave3_topic)

# The callback for when a PUBLISH message is received from the server for slave 3
def on_message_slave3(client, userdata, msg):
    global newPayload       #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    global payload          #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    print(msg.topic+" "+str(msg.payload))
    payload = str(msg.payload)
    newPayload = True
    print("newPayload : " + str (newPayload))

# The callback for when the client receives a CONNACK response from the server for publishing the KNN algo for role
def on_connect_role(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(assigned_role_topic)

# The callback for when a PUBLISH message is received from the server for publishing the KNN algo and for getting the role
def on_message_role(client, userdata, msg):
    global newPayload       #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    global payload          #declaring it as global variable so that it can be used globally otherwise it will considered as another instance for this function only
    print(msg.topic+" "+str(msg.payload))
    payload = str(msg.payload)
    newPayload = True
    print("newPayload : " + str (newPayload))

def handling_payload ():
    global payloadJson
    global role,roleDefined,speedSlave,directionSlave,FollowedTS
    print("Handling Payload: " + payload)
    payload2 = payload[2:(len(payload) - 1)] #making a substring to make it a valid JSON from the received msg i.e. b'{"tok": "SLAVE_TRUCK_1", "ts": 1653744036, "speed": 44, "direction": "RIGHT"}'
    print("payload2 after making substring is : " + payload2)
    payloadJson = json.loads(payload2)

    if payloadJson['truckID'] == "ROLE_ASSIGNMENT":
        role =payloadJson['truck4Role']
        print("Role Defined : %s" %(role))
        roleDefined=True
    else:
        print(payloadJson['speed'])
        print(payloadJson['direction'])
        if role == "SLAVE_1":
            if payloadJson['truckRole'] == "MASTER":
                print(payloadJson['speed'])
                speedSlave = payloadJson['speed']
                print(payloadJson['direction'])
                directionSlave = payloadJson['direction']
                print(payloadJson['ts'])
                FollowedTS = payloadJson['ts']
        if role == "SLAVE_2":
            if payloadJson['truckRole'] == "SLAVE_1":
                print(payloadJson['speed'])
                speedSlave = payloadJson['speed']
                print(payloadJson['direction'])
                directionSlave = payloadJson['direction']
                print(payloadJson['ts'])
                FollowedTS = payloadJson['ts']
        if role == "SLAVE_3":
            if payloadJson['truckRole'] == "SLAVE_2":
                print(payloadJson['speed'])
                speedSlave = payloadJson['speed']
                print(payloadJson['direction'])
                directionSlave = payloadJson['direction']
                print(payloadJson['ts'])
                FollowedTS = payloadJson['ts']


#KNN classifier learning algorithm

def knn_classifier ():
    global observedTruck, distanceDataSet,sensorsDataSet,masterCount,slaveCount
    for i in range(len(roleDataSet)):
        print(i)
        # calculating Euclidean Distance
        result[i - 1] = math.sqrt(((observedTruck[0] - distanceDataSet[i - 1]) ** 2) + ((observedTruck[1] - sensorsDataSet[i - 1]) ** 2))

    # finding the minimum distance as k=3 so we will calculate/extract 3 minimum distance values
    print(result)
    firstMin = min(result)
    print("First Minimum Value is : %s" % (firstMin))
    firstMinIndex = result.index(firstMin)
    print("Index of First Minimum Value is : %s" % (firstMinIndex))
    result1 = result
    result1[firstMinIndex] = 1000
    print("Second List is : %s" % (result1))
    secMin = min(result1)
    print("Second Minimum value is : %s" % (secMin))
    secMinIndex = result1.index(secMin)
    print("Index of second Minimum Value is : %s" % (secMinIndex))
    result2 = result1
    result2[secMinIndex] = 1000
    print("Third List is : %s" % (result2))
    thirdMin = min(result2)
    print("Third Minimum Value is : %s" % (thirdMin))
    thirdMinIndex = result2.index(thirdMin)
    print("Index of third Minimum Value is : %s" % (thirdMinIndex))

    minIndicesList = [firstMinIndex, secMinIndex, thirdMinIndex]

    # Mapping the minimum distance value with roleDataSet, whether the 3 extracted values belongs to MASTER or SLAVE
    for i in minIndicesList:
        if roleDataSet[i] == "MASTER":
            masterCount = masterCount + 1
        elif roleDataSet[i] == "SLAVE":
            slaveCount = slaveCount + 1
        print(i)

    print("Master Count is : %s" % (masterCount))
    print("Slave Count is : %s" % (slaveCount))


"""
End of Function
"""

# main Code Starts from here

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

clientMaster = mqtt.Client()
clientMaster.on_connect = on_connect_master
clientMaster.on_message = on_message_master

clientSlave1 = mqtt.Client()
clientSlave1.on_connect = on_connect_slave1
clientSlave1.on_message = on_message_slave1

clientSlave2 = mqtt.Client()
clientSlave2.on_connect = on_connect_slave2
clientSlave2.on_message = on_message_slave2

clientSlave3 = mqtt.Client()
clientSlave3.on_connect = on_connect_slave3
clientSlave3.on_message = on_message_slave3

clientRole = mqtt.Client()
clientRole.on_connect = on_connect_role
clientRole.on_message = on_message_role

clientMaster.subscribe(master_topic)
clientSlave1.subscribe(slave1_topic)
clientSlave2.subscribe(slave2_topic)
clientSlave3.subscribe(slave3_topic)
clientRole.subscribe(assigned_role_topic)


client.username_pw_set(username, password)
client.connect("broker.hivemq.com", 1883, 60)

clientMaster.username_pw_set(username, password)
clientMaster.connect("broker.hivemq.com", 1883, 60)

clientSlave1.username_pw_set(username, password)
clientSlave1.connect("broker.hivemq.com", 1883, 60)

clientSlave2.username_pw_set(username, password)
clientSlave2.connect("broker.hivemq.com", 1883, 60)

clientSlave3.username_pw_set(username, password)
clientSlave3.connect("broker.hivemq.com", 1883, 60)

clientRole.username_pw_set(username, password)
clientRole.connect("broker.hivemq.com", 1883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
#client.loop_forever()

client.loop_start()
clientMaster.loop_start()
clientSlave1.loop_start()
clientSlave2.loop_start()
clientSlave3.loop_start()
clientRole.loop_start()

###############################################################

knn_classifier()
role_data = {
    "truckID": device_token,
    "ts": time.time(),
    "masterCount": masterCount,
}
json_string = json.dumps(role_data)
# print(truck_data)
print("Payload for Truck 4 is: ")
print(json_string)
client.publish(role_topic, json_string)


try:
    while True:

        while(roleDefined == False):
            print("Waiting for role to be defined")
            if (newPayload == True):
                print("New Payload Received")
                handling_payload()
                # so that the following code of this block gets executed one time
                if role == "MASTER":
                    destination = random.choice(random_destination)
                    clientMaster.unsubscribe(master_topic)  ##UnSubscribing from its own topic on which it will publish
                    publishTimeDelay = publishMasterTimeDelay
                elif role == "SLAVE_1":
                    clientSlave3.unsubscribe(slave3_topic)
                    clientSlave3.loop_stop()
                    clientSlave1.unsubscribe(slave1_topic)  ##UnSubscribing from its own topic on which it will publish
                    publishTimeDelay = publishSlave1TimeDelay
                elif role == "SLAVE_2":
                    clientMaster.unsubscribe(master_topic)
                    clientMaster.loop_stop()
                    clientSlave2.unsubscribe(slave2_topic)  ##UnSubscribing from its own topic on which it will publish
                    publishTimeDelay = publishSlave2TimeDelay
                elif role == "SLAVE_3":
                    clientSlave1.unsubscribe(slave1_topic)
                    clientSlave1.loop_stop()
                    clientSlave3.unsubscribe(slave3_topic)  ##UnSubscribing from its own topic on which it will publish
                    publishTimeDelay = publishSlave3TimeDelay
                newPayload = False
            time.sleep(10)
        print("Role defined to this Truck 4 is %s" %(role))
        timeStamp = time.localtime(time.time())
        timeStampString= str (timeStamp.tm_hour)+ ":" + str(timeStamp.tm_min)+":"+str(timeStamp.tm_sec)

        if role == "MASTER":
            truck_data = {
                "truckID": device_token,
                "truckRole": role,
                "ts": timeStampString,
                "speed": int(random.choice(random_speed)),
                "direction": random.choice(random_direction),
                "destination": destination,
            }
            json_string = json.dumps(truck_data)
            # print(truck_data)
            print("Payload for Truck 4 with Role : %s" % (role))
            print(json_string)
            client.publish(master_topic, json_string)
        if role == "SLAVE_1":
            truck_data = {
                "truckID": device_token,
                "truckRole": role,
                "ts": timeStampString,
                "speed": int(speedSlave),
                "direction": directionSlave,
                # "distanceFromMaster": int(random.choice(random_distance)),
                "distanceFromMaster": distanceFromFrontTruck,
                "masterFollowedTS": FollowedTS,
            }
            json_string = json.dumps(truck_data)
            # print(truck_data)
            print("Payload for Truck 4 with Role : %s" % (role))
            print(json_string)
            client.publish(slave1_topic, json_string)
        if role == "SLAVE_2":
            truck_data = {
                "truckID": device_token,
                "truckRole": role,
                "ts": timeStampString,
                "speed": int(speedSlave),
                "direction": directionSlave,
                # "distanceFromSlave1": int(random.choice(random_distance)),
                "distanceFromSlave1": distanceFromFrontTruck,
                "slave1FollowedTS": FollowedTS,
            }
            json_string = json.dumps(truck_data)
            # print(truck_data)
            print("Payload for Truck 4 with Role : %s" % (role))
            print(json_string)
            client.publish(slave2_topic, json_string)
        if role == "SLAVE_3":
            truck_data = {
                "truckID": device_token,
                "truckRole": role,
                "ts": timeStampString,
                "speed": int(speedSlave),
                "direction": directionSlave,
                # "distanceFromSlave2": int(random.choice(random_distance)),
                "distanceFromSlave2": distanceFromFrontTruck,
                "slave2FollowedTS": FollowedTS,
            }
            json_string = json.dumps(truck_data)
            # print(truck_data)
            print("Payload for Truck 4 with Role : %s" % (role))
            print(json_string)
            client.publish(slave3_topic, json_string)

        print("newPayload status in while loop: " + str(newPayload))
        if (newPayload == True):
            print("New Payload Received")
            handling_payload()
            newPayload = False
        time.sleep(publishTimeDelay)

except KeyboardInterrupt():
    print("Press Ctrl-C to terminate while statement")
    pass






