import serial

from dout_common import get_do_request, set_do_request

with serial.Serial("/dev/ttyACM0",timeout=0.1) as doboard:

    doboard.write(set_do_request(1, 1, 1))
    response = doboard.readall()
    print(response)