from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
import board
import time
import busio
import adafruit_ssd1306

keyboard = KMKKeyboard()

# ---------------- MATRIX ----------------
keyboard.row_pins = (
    board.GP16, board.GP17, board.GP18,
    board.GP19, board.GP20, board.GP21, board.GP22
)

keyboard.col_pins = (
    board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8,
    board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13, board.GP14
)

# ⚠️ If keys don't work, switch this
keyboard.diode_orientation = DiodeOrientation.COL2ROW
# keyboard.diode_orientation = DiodeOrientation.ROW2COL


# ---------------- OLED ----------------
i2c = busio.I2C(scl=board.GP27, sda=board.GP26)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)

# Fix orientation (very common issue)
oled.rotate(2)


# ---------------- BOOT ----------------
def boot_logo():
    oled.fill(0)
    oled.text("RHENIUM", 30, 8, 1)
    oled.text("READY", 40, 18, 1)
    oled.show()
    time.sleep(1.2)

boot_logo()


# ---------------- STATS ----------------
start_time = time.monotonic()
keypress_count = 0
last_key = ""
last_oled_update = 0


def get_wpm():
    elapsed = time.monotonic() - start_time
    if elapsed == 0:
        return 0
    return int((keypress_count / 5) / (elapsed / 60))


# ---------------- KEY HANDLING (FIXED) ----------------
keyboard._orig_process_key = keyboard.process_key

def process_key(key, is_pressed, int_coord):
    global keypress_count, last_key

    if is_pressed:
        keypress_count += 1
        last_key = str(key).replace("KC.", "")

    # IMPORTANT: pass back to KMK
    return keyboard._orig_process_key(key, is_pressed, int_coord)

keyboard.process_key = process_key


# ---------------- OLED RENDER (FAST) ----------------
def render_oled():
    oled.fill(0)

    # Key (top row)
    oled.text("K:" + last_key[:6], 0, 0, 1)

    # WPM (bottom row)
    oled.text("WPM:" + str(get_wpm()), 0, 16, 1)

    oled.show()


# ---------------- THROTTLED UPDATE ----------------
def after_matrix_scan(*args):
    global last_oled_update

    now = time.monotonic()

    # Update at ~5 FPS (no lag)
    if now - last_oled_update > 0.2:
        last_oled_update = now
        render_oled()

keyboard.after_matrix_scan = after_matrix_scan


# ---------------- KEYMAP ----------------
keyboard.keymap = [[
    KC.ESC, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5, KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12,
    KC.GRV, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS, KC.BSPC,
    KC.TAB, KC.Q, KC.W, KC.E, KC.R, KC.T, KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC, KC.BSLS,
    KC.CAPS, KC.A, KC.S, KC.D, KC.F, KC.G, KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT, KC.ENTER,
    KC.LSHIFT, KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N, KC.M, KC.COMM, KC.DOT, KC.SLSH, KC.NO, KC.RSHIFT,
    KC.PSCR, KC.NO, KC.NO, KC.PAUSE, KC.LEFT, KC.EQL, KC.NO, KC.NO, KC.RIGHT, KC.DOWN, KC.RBRC, KC.NO, KC.UP,
    KC.LCTRL, KC.LGUI, KC.LALT, KC.NO, KC.NO, KC.SPACE, KC.NO, KC.NO, KC.RALT, KC.NO, KC.APP, KC.RCTRL, KC.NO
]]


# ---------------- START ----------------
if __name__ == '__main__':
    keyboard.go()