# AirScape WHF interface
[AirScape](https://airscapefans.com) has a collection of connected whole house fans.  They can be controlled via their app, but also have a published API.  This project is an interface to control their fans locally via the REST API on the fan.

API is documented [here](https://blog.airscapefans.com/archives/gen-2-controls-api)

## Invocation
Import into your code and create a `airscape.Fan` object

```python
import airscape
fan = airscape.Fan('192.168.1.10', 5)
```
Constructor takes 2 arguments.  The IP or hostname (if you DNS registered your fan) and the timeout for communicating with the fan.

The timeout is optional and has a default value of 5.

### Fan Control
The fan has 3 attributes to control:
* on/off
* speed
* timer
```python
>>> fan.is_on
False
>>> fan.is_on = True
>>> fan.is_on
True
>>> fan.speed
2
>>> fan.speed = 5
>>> fan.speed
5
>>> fan.add_time()

```

The speed can also be controled in incrememnts instead of setting directly
```python
>>> fan.speed
3
>>> fan.speed_up()
>>> fan.speed
4
>>> fan.slow_down()
>>> fan.speed
3
```
