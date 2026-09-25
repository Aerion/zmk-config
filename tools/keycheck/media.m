#import <AppKit/AppKit.h>
#import <CoreGraphics/CoreGraphics.h>
#include <stdio.h>

// macOS posts media controls as NX_SYSDEFINED events, subtype 8. The key type
// lives in data1's upper word; 0xA in the next byte denotes key down.
static void received(NSEvent *event) {
    if (event.subtype != 8) return;
    unsigned int data = (unsigned int)event.data1;
    unsigned int key = data >> 16;
    unsigned int state = (data >> 8) & 0xff;
    if (state != 0x0a) return;
    const char *name = NULL;
    switch (key) {
        case 0: name = "up"; break;
        case 1: name = "down"; break;
        case 7: name = "mute"; break;
        case 16: name = "play"; break;
        case 17: name = "next"; break;
        case 18: name = "prev"; break;
    }
    if (name) {
        printf("{\"type\":\"media\",\"key\":\"%s\"}\n", name);
        fflush(stdout);
    }
}

int main(void) {
    @autoreleasepool {
        id monitor = [NSEvent addGlobalMonitorForEventsMatchingMask:NSEventMaskSystemDefined
                                                         handler:^(NSEvent *event) { received(event); }];
        if (!monitor) {
            fputs("Could not install macOS media event monitor\n", stderr);
            return 1;
        }
        puts("{\"type\":\"ready\"}");
        fflush(stdout);
        [[NSRunLoop currentRunLoop] run];
    }
    return 0;
}
