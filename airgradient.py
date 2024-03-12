#!/usr/bin/env python3
"""
Polyglot v3 node server Example 1
Copyright (C) 2021 Robert Paauwe

MIT License
"""
import udi_interface
import sys
import time
import json
import requests

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom
polyglot = None
Parameters = None
n_queue = []
count = 0

'''
TestNode is the device class.  Our simple counter device
holds two values, the count and the count multiplied by a user defined
multiplier. These get updated at every shortPoll interval
'''
class TestNode(udi_interface.Node):
    id = 'test'
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},   # node server status
        {'driver': 'GV1', 'value': 0, 'uom': 0},       # location id
        {'driver': 'GV2', 'value': 0, 'uom': 145},       # location name
        {'driver': 'GV3', 'value': 0, 'uom': 56},       # serial no
        {'driver': 'GV4', 'value': 0, 'uom': 122},     # pm1
        {'driver': 'GV5', 'value': 0, 'uom': 122},     # pm2.5
        {'driver': 'GV6', 'value': 0, 'uom': 122},     # pm10
        {'driver': 'GV7', 'value': 0, 'uom': 0},       # pm0.3 count
        {'driver': 'CLITEMP', 'value': 0, 'uom': 4},   # ambient temp
        {'driver': 'CLIHUM', 'value': 0, 'uom': 51},   # relative humidity
        {'driver': 'CO2LVL', 'value': 0, 'uom': 54},   # co2
        {'driver': 'GV8', 'value': 0, 'uom': 0},       # tvoc
        {'driver': 'GV9', 'value': 0, 'uom': 0},       # tvoc index
        {'driver': 'GV10', 'value': 0, 'uom': 0},      # nox index
        {'driver': 'GV11', 'value': 0, 'uom': 131},      # wifi
        {'driver': 'GV12', 'value': 0, 'uom': 56},      # ledMode
        {'driver': 'GV13', 'value': 0, 'uom': 56},     # timestamp
        {'driver': 'GV14', 'value': 0, 'uom': 0},      # firmware version
    ]

    def noop(self):
        LOGGER.info('Discover not implemented')

    commands = {'DISCOVER': noop}

'''
node_queue() and wait_for_node_event() create a simple way to wait
for a node to be created.  The nodeAdd() API call is asynchronous and
will return before the node is fully created. Using this, we can wait
until it is fully created before we try to use it.
'''
def node_queue(data):
    n_queue.append(data['address'])

def wait_for_node_event():
    while len(n_queue) == 0:
        time.sleep(0.1)
    n_queue.pop()

'''
Read the user entered custom parameters. In this case, it is just
the 'multiplier' value.  Save the parameters in the global 'Parameters'
'''
def parameterHandler(params):
    global Parameters

    Parameters.load(params)


'''
This is where the real work happens.  When we get a shortPoll, increment the
count, report the current count in GV0 and the current count multiplied by
the user defined value in GV1. Then display a notice on the dashboard.
'''
def poll(polltype):
    global count
    global Parameters

    if 'shortPoll' in polltype:
        if Parameters['Token'] is None:
            LOGGER.debug("INVALID PARAMETER TOKEN!! See notice.")
            LOGGER.error("INVALID PARAMETER TOKEN!! See notice.")
            polyglot.Notices['token'] = "Missing AirGradient Token. Please configure it in CustomParams as 'Token'."
            return

        node = polyglot.getNode('my_address')
        if node is not None:
            count += 1
            token = Parameters['Token']
            response_API = requests.get(f'https://api.airgradient.com/public/api/v1/locations/measures/current?token={token}')
            if response_API.status_code is not 200:
                LOGGER.debug("Could not find a connection with airgradient API. Got error code {}".format(response_API))
                LOGGER.error("Could not find a connection with airgradient API. Got error code {}".format(response_API))
                polyglot.Notices['request'] = 'HTTP Request failed for api.airgradient.com'
                return
            parse_json = json.loads(response_API.text)
            index = 0
            if Parameters['Index'] == None:
                LOGGER.debug("Index was not set prior. It has been defaulted to 0.")
                polyglot.Notices['index'] = 'No index was set so it has been defaulted to 0.'
            else:
                index = int(Parameters['Index'])
            try:
                data = parse_json[index]
            except IndexError:
                LOGGER.debug("Index error. Out of bounds.")
                LOGGER.error("Invalid index.")
                polyglot.Notices['error'] = 'Could not parse the data pulled.'
                return
            except:
                LOGGER.debug("Probably a ValueError. Something is wrong with the index or data. Received: {} from the API".format(parse_json))
                LOGGER.error("Something went wrong.")
                polyglot.Notices['error'] = 'Could not parse the data pulled.'
                return
            # debugging purposes
            # polyglot.Notices['data'] = 'Successfully pulled data from the AirGradient API ({})'.format(count)
            node.setDriver('GV1', 0, True, True, 145, data['locationId'])
            node.setDriver('GV2', 0, True, True, 145, data['locationName'])
            node.setDriver('GV3', 0, True, True, 145, data['serialno'])
            node.setDriver('GV4', data['pm01'], True, True)
            node.setDriver('GV5', data['pm02'], True, True)
            node.setDriver('GV6', data['pm10'], True, True)
            node.setDriver('GV7', data['pm003Count'], True, True)
            node.setDriver('CLITEMP', 0, True, True, 145, data['atmp'])
            node.setDriver('CLIHUM', 0, True, True, 145, data['rhum'])
            node.setDriver('CO2LVL', 0, True, True, 145, data['rco2'])
            node.setDriver('GV8', 0, True, True, 145, data['tvoc'])
            node.setDriver('GV9', 0, True, True, 145, data['tvocIndex'])
            node.setDriver('GV10', 0, True, True, 145, data['noxIndex'])
            node.setDriver('GV11', 0, True, True, 145, data['wifi'])
            node.setDriver('GV12', 0, True, True, 145, data['ledMode'])
            node.setDriver('GV13', 0, True, True, 145, data['timestamp'])
            node.setDriver('GV14', 0, True, True, 145, data['firmwareVersion'])
'''
When we are told to stop, we update the node's status to False.  Since
we don't have a 'controller', we have to do this ourselves.
'''
def stop():
    nodes = polyglot.getNodes()
    for n in nodes:
        nodes[n].setDriver('ST', 0, True, True)
    polyglot.stop()


if __name__ == "__main__":
    try:
        polyglot = udi_interface.Interface([])
        polyglot.start()

        Parameters = Custom(polyglot, 'customparams')

        # subscribe to the events we want
        polyglot.subscribe(polyglot.CUSTOMPARAMS, parameterHandler)
        polyglot.subscribe(polyglot.ADDNODEDONE, node_queue)
        polyglot.subscribe(polyglot.STOP, stop)
        polyglot.subscribe(polyglot.POLL, poll)

        # Start running
        polyglot.ready()
        polyglot.setCustomParamsDoc()
        polyglot.updateProfile()

        '''
        Here we create the device node.  In a real node server we may
        want to try and discover the device or devices and create nodes
        based on what we find.  Here, we simply create our node and wait
        for the add to complete.
        '''
        node = TestNode(polyglot, 'my_address', 'my_address', 'AirGradient')
        polyglot.addNode(node)
        wait_for_node_event()

        # Just sit and wait for events
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
        

