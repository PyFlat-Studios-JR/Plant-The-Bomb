VERSION = "1.0.0"
ARG_SHORT = r"\b(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\b"
ARG_LONG = r"\b(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]?[0-9]?[0-9]?|0)\b"
COORD = r"\b(2[0-4]|1?[0-9])\b"
def enum(args) -> str:
    r = "\\b("
    for element in args:
        r += element + "|"
    return r[:-1] + ")\\b"
START = "^"
END = "( +.*|$)"
COMMANDS = [
    f"^//{END}",
    f"{START}@ {enum(['on_step','on_collect','on_explode','on_destroy','on_init','on_tick'])} on {COORD} {COORD}{END}",
    f"{START}end{END}",
    f"{START}add {ARG_LONG} , {ARG_LONG} => {ARG_LONG}{END}",
    f"{START}subtract {ARG_LONG} , {ARG_LONG} => {ARG_LONG}{END}",
    f"{START}multiply {ARG_LONG} , {ARG_LONG} => {ARG_LONG}{END}",
    f"{START}divide {ARG_LONG} , {ARG_LONG} => {ARG_LONG}{END}",
    f"{START}set {ARG_LONG} = {ARG_SHORT}{END}",
    f"{START}reset {ARG_LONG}{END}",
    f"{START}store {enum(['player.health','player.bombs','player.range','player.dynamite','player.timed_bombs','player.damage','player.nukes'])} to {ARG_LONG}{END}",
    f"{START}set_item {enum(['player.health','player.bombs','player.range','player.dynamite','player.timed_bombs','player.damage','player.nukes'])} = {ARG_LONG}{END}",
    f"{START}win{END}",
    f"{START}loose{END}",
    f"{START}drawImage {ARG_LONG} on {ARG_LONG} {ARG_LONG}{END}",
    f"{START}drawRect on {ARG_LONG} {ARG_LONG} with color ( {ARG_LONG} {ARG_LONG} {ARG_LONG} ){END}",
    f"{START}clear {ARG_LONG} {ARG_LONG}{END}",
    f"{START}compare {ARG_LONG} {enum(['>', '<', '==', '<=', '>='])} {ARG_LONG} => {ARG_LONG}{END}",
    f"{START}jump {ARG_LONG} lines if {ARG_LONG}{END}",
    f"{START}setFlag {enum(['drop_items'])} = {ARG_SHORT}{END}",
    f"{START}tp to {ARG_LONG} {ARG_LONG}{END}",
    f"{START}jumpRelative {ARG_LONG} lines if {ARG_LONG}{END}",
    f"{START}createMemory{END}",
    f"{START}loadToMemory{END}",
    f"{START}loadFromMemory{END}",
    f"{START}randomNumber from {ARG_LONG} to {ARG_LONG} => {ARG_LONG}{END}",
    f"{START}loadFromPointer at {ARG_LONG} to {ARG_LONG}{END}",
    f"{START}storeToPointer value {ARG_LONG} to {ARG_LONG}{END}",
    f"{START}place_block {ARG_LONG}{END}",
    f"{START}show_text {ARG_LONG} using {enum(['mode_popup','mode_display'])}"
]