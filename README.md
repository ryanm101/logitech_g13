# G13 userspace Driver - Python

## TODO
*   Actions on Keypress
*   LCD Updates
*   Decode all Keypresses
    *   MouseKeys
    *   Joystick
*   write c kernel module to send interrupt directly to system pipe
*   listenfordata is infinate while loop, needs to be cleaned up to allow for clean exit

## Done
*   detect if LCD light is on
*   basic test for unittests
*   Decode Keypresses
    *   LCDKeys
    *   MKeys
    *   GKeys
