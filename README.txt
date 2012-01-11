
===============================
 SunnyWebBox - RPC with Python
===============================

Introduction
------------

**This software is not much tested and should be used with care!**

The `Sunny WebBox`_ (made by SMA Solar Technology) is a monitoring system for 
solar plants which offers RPC (remote procedure calls) to access the data of 
the box. These calls are made of JSON objects which are transported by HTTP.

This python module provides a class that can be used to communicate with a 
Sunny WebBox. You can use the class SunnyWebBox in your own code. A small 
sample program is used if you run the module as a script. The first parameter 
is the hostname or IP of the box. A password can be provided with an optional 
second parameter.

    Example: python SunnyWebBox.py 123.123.123.123 "foobar"

There's no documentation yet. You should try to read and understand the code of 
the class and the sample program to get an idea of the data structures.

The RPC API is documented here:
    
    http://files.sma.de/dl/2585/SWebBoxRPC-BEN092713.pdf

License and Author
------------------

License: `BSD License`_

Author:  Joerg Raedler joerg@j-raedler.de


.. _`Sunny WebBox`: http://www.sma.de/en/products/monitoring-systems/sunny-webbox.html
.. _`BSD License`: http://www.opensource.org/licenses/bsd-license.php
