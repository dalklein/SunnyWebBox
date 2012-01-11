#!/usr/bin/env python
# version: 0.2
# date:    2012-01-10
# author:  Joerg Raedler joerg@j-raedler.de
# license: BSD
# purpose: make RPC to a Sunny WebBox, a monitoring system for solar plants
#
# http://www.sma.de/en/produkte/monitoring-systems/sunny-webbox.html
#
# Use the class SunnyWebBox in your code or run this file as a script to test
# the class. First parameter is the hostname or IP of the box. A password can 
# be provided with an optional second parameter.
#
# Example: python SunnyWebBox.py 123.123.123.123 "foobar"
#
# Documentation on the RPC API can be found here:
#
# http://files.sma.de/dl/2585/SWebBoxRPC-BEN092713.pdf
#

import json, httplib, hashlib

class Counter:
    """generate increasing numbers with every call - just for convenience"""
    def __init__(self, start=0):
        self.i = start
    def __call__(self):
        i = self.i
        self.i += 1
        return i


class SunnyWebBox(object):
    """
    Class to make RPC to a 'Sunny WebBox', a monitoring system for solar plants
    """
    
    def __init__(self, host='1.2.3.4', password=''):
        self.host = host
        if password:
            self.pwenc = hashlib.md5(password).hexdigest()
        else:
            self.pwenc = ''
        self.conn  = httplib.HTTPConnection(self.host)
        self.count = Counter()

    def newRequest(self, name='GetPlantOverview', withPW=False, **params):
        """return a new rpc request structure (dictionary)"""
        r = {'version': '1.0', 'proc': name, 'format': 'JSON'}
        r['id'] = str(self.count())
        if withPW:
            r['passwd'] = self.pwenc
        if params:
            r['params'] = params
        return r
            
    def _rpc(self, request):
        """send an rpc request as JSON object via http and read the result"""
        js = json.dumps(request)
        self.conn.request('POST', '/rpc', "RPC=%s" % js)
        response = json.loads(self.conn.getresponse().read())
        if response['id'] != request['id']:
            raise Exception('RPC answer has wrong id!')
        return response['result']
        
    def printOverview(self):
        """print a short overview of the plant data"""
        for v in self.getPlantOverview():
            print("%15s (%15s): %s %s" % 
                (v['name'], v['meta'], v['value'], v['unit']))
        
    # wrapper methods for the RPC functions
        
    def getPlantOverview(self):
        res = self._rpc(self.newRequest('GetPlantOverview'))
        return res['overview']
        
    def getDevices(self):
        res = self._rpc(self.newRequest('GetDevices'))
        return res['devices']

    def getProcessDataChannels(self, deviceKey):
        res = self._rpc(self.newRequest('GetProcessDataChannels', device=deviceKey))
        return res[deviceKey]

    def getProcessData(self, channels):
        res = self._rpc(self.newRequest('GetProcessData', devices=channels))
        # reorder data structure: {devKey: {dict of channels}, ...}
        return {l['key']: l['channels'] for l in res['devices']}
        
    def getParameterChannels(self, deviceKey):
        res = self._rpc(self.newRequest('GetParameterChannels', withPW=True, device=deviceKey))
        return res[deviceKey]

    def getParameter(self, channels):
        res = self._rpc(self.newRequest('GetParameter', withPW=True, devices=channels))
        # reorder data structure: {devKey: {dict of channels}, ...}
        return {l['key']: l['channels'] for l in res['devices']}
        
    def setParameter(self, *args):
        raise Exception('Not yet implemented!')


if __name__ == '__main__':
    
    import sys

    pw = ''
    ip = sys.argv[1]
    if len(sys.argv) > 2:
        pw = sys.argv[2]
    
    swb = SunnyWebBox(ip, password=pw)

    print '###### Overview:'
    swb.printOverview()
    
    for d in swb.getDevices():
        devKey = d['key']
        print "\n  #### Device %s (%s):" % (devKey, d['name'])
        
        print "\n    ## Process data:"
        channels = swb.getProcessDataChannels(devKey)
        data = swb.getProcessData([{'key':devKey, 'channels':channels}])
        for c in data[devKey]:
           print("      %15s (%15s): %s %s" % 
               (c['name'], c['meta'], c['value'], c['unit']))

               
        print "\n    ## Parameters:"
        channels = swb.getParameterChannels(devKey)
        data = swb.getParameter([{'key':devKey, 'channels':channels}])
        for c in data[devKey]:
            print("      %15s (%15s): %s %s" % 
                (c['name'], c['meta'], c['value'], c['unit']))
