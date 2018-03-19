from pyhooked import Hook, KeyboardEvent, MouseEvent
import sys, os

def handle_events(args):

    if isinstance(args, KeyboardEvent):

        if args.key_code == 13:
            sys.stdout.write( '\r\n' )
        else:
            if args.key_code > 45 and args.key_code < 91:
                sys.stdout.write( chr(args.key_code) )
            else:
                sys.stdout.write( args.key_code )

    if isinstance(args, MouseEvent):
        print args.mouse_x, " :  ", args.mouse_y



hk = Hook()
hk.handler = handle_events
hk.hook()