# Matching the BT60 and M3 MacBook Air

The `FR-OSS-Arrows.keylayout` managed by chezmoi is based on the KLFC-generated
`y-xkb-fr-oss.keylayout`. Its FR-OSS characters, dead keys and spacing remain
unchanged except for four Right Option + Shift positions:

| Physical key | Stock FR-OSS | This layout |
| --- | --- | --- |
| O | Œ | ↑ |
| K | Ï | ← |
| L | Ŀ | ↓ |
| M | Ö | → |

The layout is shared by the MacBook and the BT60 after login. Like stock
FR-OSS, it uses Option on either side for the AltGr level; the right Option
key is the intended typing habit. The original printable ← ↑ → on V/B/N are
still present. The MacBook's dedicated ² key gives ², ³ with Shift, and ¹
with Option. BT60 Fn + Tab sends that key's HID position. BT60 Escape stays
Escape, while Fn + Escape gives a backtick via Option + the `è` position.

## Install the text layout

Sync your chezmoi source and run `chezmoi apply` to install the layout under
`~/Library/Keyboard Layouts/`. Log out and back in if it does not immediately
appear. In System Settings → Keyboard → Text Input → Edit → Input Sources,
add **FR-OSS Arrows**. Keep French-PC
available as a fallback until both keyboards are tested. Choosing the source
changes text entry for both keyboards. It does not remap shortcuts or work at
the login screen for a user who has not logged in.

## Mirror Fn on the MacBook

The MacBook needs Karabiner-Elements for the Fn + letter, navigation and media
bindings. Install it, grant its requested macOS permissions, and set its
virtual keyboard type to ISO. In Karabiner's **Devices** tab, disable event
modification for the BT60; its existing macOS Alt/Command swap is specific to
that physical device. Leave modification enabled for the built-in keyboard.

The chezmoi source also installs `bt60-fn-on-macbook.json` under
`~/.config/karabiner/assets/complex_modifications/`. Enable the rule
**Match BT60 Control and Raise actions on the built-in MacBook keyboard** in
Complex Modifications. It also maps the MacBook Caps position to Control,
preserving that habit if Karabiner's virtual device bypasses the current
macOS per-device modifier setting.

The rule maps Fn + number row to F1–F12, Fn + Tab to ², Fn + Escape to a
backtick, and the BT60's navigation, media and editing positions to the same
key events. Bluetooth, reset and bootloader stay BT60-only. Print Screen,
Scroll Lock, Insert and Application Menu events are preserved; macOS apps may
ignore those legacy keys. The MacBook's own function row remains available.

## Check after setup

1. On each keyboard, check plain Escape, Caps/Control and Command beside Space.
2. In TextEdit, check `²`, `³`, `¹`, `é`, `œ`, `«`, `»`, one dead accent, and
   Right Option + Shift + O/K/L/M → `↑ ← ↓ →`.
3. Check BT60 and MacBook Fn + O/K/L/; navigation, Fn + Y/U/I volume, Fn +
   Z/X/C playback, Fn + Backspace forward delete, and Fn + 1/F1.
4. If Fn + Tab on the MacBook produces `<` instead of `²`, check Karabiner's
   virtual keyboard ISO setting and its **Swap ISO layout-specific keys**
   device option. Use EventViewer to verify the physical key codes.

The firmware file must be built and flashed separately. To revert the Mac
typing change, select French-PC again. Disable the Karabiner rule to revert
the Mac Fn mappings. The old BT60 firmware can be flashed again if needed.
