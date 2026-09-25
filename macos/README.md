# Match the BT60 and M3 MacBook Air

## How to install on the Mac

- Install **chezmoi** and **Karabiner-Elements**. Grant the permissions
  Karabiner requests.
- Sync your chezmoi source, then run `chezmoi apply`. This copies
  `FR-OSS-Arrows.keylayout` to `~/Library/Keyboard Layouts/`,
  `karabiner.json` to `~/.config/karabiner/`, and
  `bt60-fn-on-macbook.json` to
  `~/.config/karabiner/assets/complex_modifications/`.
- In **System Settings → Keyboard → Text Input → Edit → Input Sources**, add
  **FR-OSS Arrows**. Log out and back in if it is missing. Keep French-PC
  available until you have tested the new layout.
- In **System Settings → Keyboard → Keyboard Shortcuts → Function Keys**,
  enable **Use F1, F2, etc. keys as standard function keys**.
- In **Karabiner-Elements → Virtual Keyboard**, select **ISO**. In **Devices**,
  leave modification enabled for the built-in keyboard and disable it for
  the BT60. If the key above Tab types `<` rather than `²`, enable **Swap ISO
  layout-specific keys** for the built-in keyboard.
- In **Karabiner-Elements → Complex Modifications**, check that **Match BT60
  Control and Raise actions on the built-in MacBook keyboard** is enabled.
  If it is absent, use **Add predefined rule** to enable it.
- Run the [keyboard tester](../tools/keycheck/README.md) on each keyboard.

## What this installs

Both keyboards use the same FR-OSS Arrows text layout after login. It keeps
FR-OSS characters and dead keys, except for these printable shortcuts:

| Right Option + Shift + | Character |
| --- | --- |
| O | ↑ |
| K | ← |
| L | ↓ |
| M | → |

The MacBook rule maps Caps to Control and mirrors the BT60 Fn shortcuts for
navigation, media, F1–F12, F14/F15, Delete and ². The MacBook's own
function row and arrow keys remain available. BT60 Adjust, Bluetooth,
bootloader and reset actions are not mapped to the MacBook.

Fn + P sends Print Screen, which appears as F13 in a browser and currently
changes brightness on this Mac. The legacy Application Menu key may have no
effect in macOS apps.

To undo the Mac changes, select French-PC as the input source and disable the
Karabiner rule. BT60 firmware is built and flashed separately.
