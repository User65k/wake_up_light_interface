import socket, logging
from threading import Thread
from time import sleep
"""
uses a socket to adjust my GLOBO lamp.
Shows how to use the actions folder.
"""

def set_lamp(brightness, redval):
    """
    Adjust lamp to certain color and brightness
    """

    code = (brightness*16+redval).to_bytes(1, byteorder="big")
    try:
        buz = socket.socket()
        buz.connect(('127.0.0.1', 1337))
        logging.debug("send %r"%(code,))
        buz.send(code)
        buz.close()
    except Exception:
        logging.exception("send error")

def parse_args(args):
    l = args.find(" ")
    shine = args
    cool = args
    if l!=-1:
        cool = args[l+1:]
        shine = args[:l]
    
    shine = int(shine)
    cool = int(cool)
    return (shine, cool)

class dimThread(Thread):
    def __init__(self, args):
        Thread.__init__(self)
        self.args = args

    def run(self):
        shine, cool = parse_args(self.args)

        set_lamp(1,15)

        #brigten every min
        for l in range(1,15):
            sleep(shine)
            set_lamp(l,15)

        #now get colder
        for r in range(1,15):
            sleep(cool)
            set_lamp(15,15-r)

def prerun(args):
    """
    Args: see main

    return: minutes to trigger this action before the alarm rings
    """
    shine, cool = parse_args(args)
    #lamp should be brigt at alarm time, so brigten should happen before
    #shine is in seconds and there are 15 steps
    return ((shine * 15)+1)/60

def main(args):
    """
    Args: rise cool

    rise: delay between a step while rising
    cool: delay between a step of cooling (after rise is done)
    """
    t = dimThread(args)
    t.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main("2 1")
