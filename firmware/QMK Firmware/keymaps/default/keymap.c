#include QMK_KEYBOARD_H

#define ENCODER_MAP_ENABLE

bool encoder_mode = false;
uint8_t volume_level = 50;
uint8_t brightness_level = 50;

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
[0] = LAYOUT(
KC_ESC, KC_F1, KC_F2, KC_F3, KC_F4, KC_F5, KC_F6, KC_F7, KC_F8, KC_F9, KC_F10, KC_F11, KC_F12,
KC_GRV, KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7, KC_8, KC_9, KC_0, KC_MINS, KC_BSPC,
KC_TAB, KC_Q, KC_W, KC_E, KC_R, KC_T, KC_Y, KC_U, KC_I, KC_O, KC_P, KC_LBRC, KC_BSLS,
KC_CAPS, KC_A, KC_S, KC_D, KC_F, KC_G, KC_H, KC_J, KC_K, KC_L, KC_SCLN, KC_QUOT, KC_ENT,
KC_LSFT, KC_Z, KC_X, KC_C, KC_V, KC_B, KC_N, KC_M, KC_COMM, KC_DOT, KC_SLSH, KC_NO, KC_RSFT,
KC_PSCR, KC_NO, KC_NO, KC_PAUS, KC_LEFT, KC_EQL, KC_NO, KC_NO, KC_RGHT, KC_DOWN, KC_RBRC, KC_NO, KC_UP,
KC_LCTL, KC_LGUI, KC_LALT, KC_NO, KC_NO, KC_SPC, KC_NO, KC_NO, KC_RALT, KC_NO, KC_APP, KC_RCTL, KC_NO
)
};

// ---------- ENCODER ----------
bool encoder_update_user(uint8_t index, bool clockwise) {
    if (!encoder_mode) {
        tap_code(clockwise ? KC_VOLU : KC_VOLD);
        volume_level = clockwise ? volume_level + 2 : volume_level - 2;
    } else {
        tap_code(clockwise ? KC_BRIU : KC_BRID);
        brightness_level = clockwise ? brightness_level + 2 : brightness_level - 2;
    }
    return false;
}

// ---------- BUTTON ----------
bool encoder_button_user(uint8_t index, bool pressed) {
    if (pressed) {
        encoder_mode = !encoder_mode;
    }
    return true;
}

#ifdef OLED_ENABLE

void draw_bar(uint8_t level) {
    uint8_t bars = level / 10;
    for (int i = 0; i < 10; i++) {
        oled_write(i < bars ? "|" : ".", false);
    }
}

bool oled_task_user(void) {

    oled_set_cursor(0, 0);
    oled_write_ln("RHENIUM", false);

    oled_set_cursor(0, 1);
    oled_write_ln("------------", false);

    if (!encoder_mode) {
        oled_set_cursor(0, 2);
        oled_write_ln("VOLUME", false);

        oled_set_cursor(0, 3);
        draw_bar(volume_level);
    } else {
        oled_set_cursor(0, 2);
        oled_write_ln("BRIGHT", false);

        oled_set_cursor(0, 3);
        draw_bar(brightness_level);
    }

    return false;
}

#endif