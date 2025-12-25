import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_displayio_ssd1306 import SSD1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler

# Sorry but I had school work too I cant spent time to do this so I gave AI it  took me 5 mins 

keyboard = KMKKeyboard()

layers = Layers()
keyboard.modules.append(layers)

encoder = EncoderHandler()
keyboard.modules.append(encoder)


keyboard.col_pins = (
    board.GP6, board.GP7, board.GP8, board.GP9, board.GP10,
    board.GP11, board.GP12, board.GP13, board.GP14, board.GP15,
    board.GP16, board.GP17, board.GP18, board.GP19, board.GP20
)

keyboard.row_pins = (
    board.GP0, board.GP1, board.GP4,
    board.GP5, board.GP26, board.GP27
)

keyboard.diode_orientation = keyboard.DIODE_COL2ROW



encoder.pins = (
    (board.GP21, board.GP22, None),  
)

encoder.map = [
    ((KC.VOLD, KC.VOLU),),  
    ((KC.LEFT, KC.RIGHT),) 
]



displayio.release_displays()

i2c = board.I2C(scl=board.GP2, sda=board.GP3)

display_bus = displayio.I2CDisplay(
    i2c,
    device_address=0x3C
)

display = SSD1306(
    display_bus,
    width=128,
    height=64
)

splash = displayio.Group()
display.show(splash)

text = label.Label(
    terminalio.FONT,
    text="Layer 0",
    color=0xFFFFFF,
    x=0,
    y=10
)
splash.append(text)

def after_layer_change(old, new):
    text.text = f"Layer {new}"

keyboard.after_layer_change = after_layer_change



keyboard.keymap = [
   
    [
        KC.ESC, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5, KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12, KC.PSCR, KC.DEL,
        KC.GRV, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS, KC.EQL, KC.BSPC, KC.NO,
        KC.TAB, KC.Q, KC.W, KC.E, KC.R, KC.T, KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC, KC.RBRC, KC.BSLS, KC.NO,
        KC.CAPS, KC.A, KC.S, KC.D, KC.F, KC.G, KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT, KC.ENTER, KC.NO, KC.NO,
        KC.LSFT, KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N, KC.M, KC.COMM, KC.DOT, KC.SLSH, KC.RSFT, KC.UP, KC.NO, KC.NO,
        KC.LCTL, KC.LGUI, KC.LALT, KC.SPACE, KC.RALT, KC.FN1, KC.LEFT, KC.DOWN, KC.RIGHT, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO
    ],

 
    [
        KC.TRNS, KC.F13, KC.F14, KC.F15, KC.F16, KC.F17, KC.F18, KC.F19, KC.F20, KC.F21, KC.F22, KC.F23, KC.F24, KC.TRNS, KC.RESET,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.PGUP, KC.TRNS, KC.TRNS,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.HOME, KC.PGDN, KC.END, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ]
]



if __name__ == "__main__":
    keyboard.go()
