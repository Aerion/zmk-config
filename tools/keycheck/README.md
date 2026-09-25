# Five-minute keyboard check

Run from this repository on the Mac:

```sh
python3 tools/keycheck/server.py
```

Open <http://127.0.0.1:8765/> in Safari or Chrome. The server listens only on
the local machine. Keep that tab focused. Select **M3 MacBook Air** or **BT60**,
then complete **Plain**, **Shift**, **Right Option**, **Right Option + Shift**,
**Fn / Raise**, and **Dead accents**. Plain includes the MacBook's physical
F1–F12 row (with this Mac's standard-function-key setting). The other three
typing levels check every printable position; Fn / Raise checks every active
binding. In Fn / Raise, the keyboard diagram displays the expected action at
each mapped position on either keyboard, including arrows, page keys and media.
Each correct event advances immediately. The page shows the
next physical position and expected output. **Previous** retries a step. If
the key produces a different event, choose **Mark failed & continue**; the
report records both expected output and the last received event. **Skip without
result** is for a key the browser cannot observe. The current run survives a
page refresh. **Copy report** includes failures and skips across all parts
completed in this browser tab.

For volume, playback and the context menu, use **I observed the action** when
the action works but no keyboard event reaches the tester. The report records
these separately from event-checked passes and unresolved skips. macOS may
report Print Screen as F13; the tester accepts that name. Fn + the two bracket
positions should report F14 and F15 on both keyboards.

Select **FR-OSS Arrows** as the macOS input source before either run. For the
MacBook, enable the corresponding Karabiner complex modification. For the BT60,
connect it by USB after flashing and leave Karabiner device modification off.
Use only the selected keyboard during a run; the browser cannot tell which
physical keyboard sent an ordinary key.

The small native observer compiles into `tools/keycheck/.build/` on first run
and receives macOS media events, including volume and playback. Grant Input
Monitoring if macOS asks, then restart the server. Its connection state is
shown at the bottom of the page. When unavailable, media actions can still
pass if the browser receives a media key event; otherwise **Skip** leaves an
explicit unresolved item. If the action visibly works, use **I observed the
action** instead. Volume and playback may actually change during the
test. The observer does not save or transmit key events; the HTTP page and
event stream are bound to `127.0.0.1`.

Fn itself is tested through its actions because it emits no ordinary key
event. MacBook Touch ID cannot be validated as a keyboard event. The BT60's
Bluetooth profile keys are inactive while BLE
is disabled. Bootloader and reset are omitted from the automatic run because
they disconnect the board; check them separately when flashing.

The test verifies received key and character events. It cannot guarantee that
a system action had the intended side effect (for example, that audio was
playing when Play/Pause was pressed). Check any skipped action in Karabiner
EventViewer or the target app.

If the MacBook key above Tab yields `<` instead of `²`, open Karabiner Settings
→ **Devices** → **Apple Internal Keyboard / Trackpad** and enable **Swap ISO
layout-specific keys**. The virtual keyboard type should already be **ISO**.
Then retry both positions: above Tab should give `²`, and beside left Shift
should give `<`. Once confirmed, record the resulting Karabiner configuration
in chezmoi so the setting follows the Mac to other machines.
