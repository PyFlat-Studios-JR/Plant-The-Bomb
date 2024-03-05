import time


class compilerError(Exception):
    def __init__(self, msg="UNSPECIFIED", line=0, ecode=0):
        super().__init__(msg)
        self.ms = msg
        self.line = line
        self.ecode = ecode
    def get(self):
        return (self.line,self.ecode,self.ms)
class log:
    def __init__(self) -> None:
        self.logs = []

    def add_log(self, log):
        self.logs.append(f"[{time.time()}]" + log)

    def write_log(self, file):
        s = ""
        for log in self.logs:
            s += log + "\n"
        with open(file, "w") as file:
            file.write(s)


class util:
    def validateCommandLength(attrs, minlength, line):
        if len(attrs) < minlength:
            raise compilerError(
                f"Line {line} Compiler Error [002]: Short command. Expected >={minlength}, got {len(attrs)}", line, 2
            )

    def validateInteger(data, maxlength, line, logfile):
        try:
            i = int(data)
        except ValueError:
            try:
                i = int(data, 16)
                logfile.add_log(
                    f"WARNING [{line}]: Used hex as integer conversion for {data}. This is not recommended."
                )
            except ValueError:
                raise compilerError(
                    f"Line {line} Compiler Error [003]: Invalid integer Conversion of value {data}", line, 3
                )
        if i > maxlength:
            raise compilerError(
                f"Line {line} Compiler Error [004]: Maximum integer length exceeded. Exspected <= {maxlength}, got {i}", line, 4
            )
        if i < 0:
            raise compilerError(
                f"Line {line} Compiler Error [005]: Integer too small. Exspected >0, got {i}", line, 5
            )
        return i

    def validateEnum(data, enum, line, blacklisted=[]):
        if data not in enum:
            raise compilerError(
                f"Line {line} Compiler Error [001]: invalid Enum. Expected {enum}, got {data}.", line, 1
            )
        if data in blacklisted:
            raise compilerError(
                f"Line {line} Compiler Error [006]: Blacklisted value. The value {data} is blacklisted for {enum}. The blacklist is {blacklisted}", line, 6
            )
        for i in range(len(enum)):
            if enum[i] == data:
                return i
        raise compilerError(f"Line {line} Compiler Error [999]: Impossible", line, 999)

    def byte(i: int, l: int):
        return i.to_bytes(l, "big")


class compiler:
    def __init__(self):
        self.comp_scripts = [
            None,
            self.compile_trigger,
            self.compile_end,
            self.compile_math,
            self.compile_math,
            self.compile_math,
            self.compile_math,
            self.compile_set,
            self.compile_reset,
            self.compile_get,
            self.compile_get,
            self.compile_end,
            self.compile_end,
            self.compile_drawimg,
            self.compile_rect,
            self.compile_clear,
            self.compile_comp,
            self.compile_jump,
            self.compile_flag,
            self.compile_tp,
            self.compile_jump,
            self.compile_downloadRAM,
            self.compile_toMemory,
            self.compile_toMemory,
            self.compile_rand,
            self.compile_ptr,
            self.compile_ptr,
            self.compile_reset,
            self.compile_text
        ]
        self.logfile = log()

    def getLineSize(self):
        ls = []

    def getEnumHelp(self, enum):
        enum = enum.lower()
        help = {"event": "No help here yet :("}
        try:
            return help[enum]
        except KeyError:
            return f"Hilfe für {enum} kann nicht abgerufen werden."

    def getCmdHelp(self, cmId):
        if type(cmId) == str:
            cmId = self.getCommandId(cmId)
        if type(cmId) != int:
            return f"Ungültige ID {cmId}"
        help = [
            "General: Konstante Zahlen sind maximal 8 Bit groß, Adressen bis zu 16 Bit. Die Speicherzellen haben kein größenlimit.\n Keine Zahlen dürfen 0 groß sein!!!"
            "@: Dieser Befehl stellt einen einstiegspunkt da. Nutzung:\n@ event on x y\nevent ist ein Enum. Für mehr info zu enums benutze getEnumHelp(enum).\n x und y sind die koordinaten des triggers und sind konstanten\nWenn das event ausgelöst wird, startet das script bei diesem Befehl.",
            "end: Dieser Befehl stoppt die Ausführung des aktuellen scripts.\n Wird end nicht aufgerufen, läuft das script auch über andere @ Anweisungen",
            "add: Dieser Befehl addiert 2 zahlen aus dem Speicher und speichert das Ergebnis.Syntax: \n add a , b => c\n a und b werden addiert und in c gespeichert",
            "subtract: Dieser Befehlt subtrahiert 2 Zahlen. Für mehr info, siehe getCmdHelp(3)\nAlle mathematikbefehle sind syntaktisch gleich",
            "multiply: Dieser Befehl multipliziert 2 Zahlen. Für mehr infor siehe getCmdHelp(3)\nAlle mathematikbefehle sind syntaktisch gleich",
            "divide: Dieser Befehl dividiert 2 Zahlen. Für mehr infor siehe getCmdHelp(3)\nAlle mathematikbefehle sind syntaktisch gleich.\nWICHTIG: Das teilen von Zahlen liefert IMMER eine ganzzahl.",
            "set: Dieser Befehlt speichert eine Konstante im speicher.\nset location = value\n",
            "reset: Dieser Befehl bewirkt set location = 0, da set location = 0 nicht verwendet werden DARF",
            "store: Dieser Befehl lädt einen wert (enum) vom spiel und speichert ihn.\nstore value to cell",
            "set_item: Dieser Befehl ändert einen Wert im SPiel.\nset_item value = cell",
            "win: wins the game, even if no enemys are present.\nwin",
            "loose: loose the game instantly.\nloose",
            "drawImage: draws an image to the screen.\ndrawImage image on x y => stor\nImage is the ID of an image in the game files. Custom images are supportet. x and y are the coords of the image.\nThe image ist stored to stor.\nDO NOT EDIT STOR. If stor is changed or deleted you won't be able to destroy the image",
            "drawRect on x y with color ( r g b ) => stor",
            "clear graphics\n graphics; adress of image",
        ]
        try:
            return help[cmId]
        except IndexError:
            return f"Hilfe für ID {cmId} konnte nicht abgerufen werden. Gültige IDs sind {0}-{len(help)-1}."

    def getCommandId(self, cmd):
        cm = {
            "@": 1,
            "end": 2,
            "add": 3,
            "subtract": 4,
            "multiply": 5,
            "divide": 6,
            "set": 7,
            "reset": 8,
            "store": 9,
            "set_item": 10,
            "win": 11,
            "loose": 12,
            "drawImage": 13,
            "drawRect": 14,
            "clear": 15,
            "compare": 16,
            "jump": 17,
            "setFlag": 18,
            "tp": 19,
            "jumpRelative": 20,
            "createMemory": 21,
            "loadToMemory": 22,
            "loadFromMemory": 23,
            "randomNumber": 24,
            "loadFromPointer": 25,
            "storeToPointer": 26,
            "place_block": 27,
            "show_text": 28
        }
        try:
            return cm[cmd]
        except KeyError:
            return False

    def getCommandString(self, cmd):
        cm = [
            None,
            "@",
            "end",
            "add",
            "subtract",
            "multiply",
            "divide",
            "set",
            "reset",
            "store",
            "set_item",
            "win",
            "loose",
            "drawImage",
            "drawRect",
            "clear",
            "compare",
            "jump",
            "setFlag",
            "tp",
            "jumpRelative",
            "createMemory",
            "loadToMemory",
            "loadFromMemory",
            "randomNumber",
            "loadFromPointer",
            "storeToPointer",
            "place_block",
            "show_text"
        ]
        try:
            return cm[cmd]
        except IndexError:
            return False

    def getCommandMask(self, cmd):
        ms = [
            "",
            "@ {} on {} {}",
            "end",
            "add {} , {} => {}",
            "subtract {} , {} => {}",
            "multiply {} , {} => {}",
            "divide {} , {} => {}",
            "set {} = {}",
            "reset {}",
            "store {1} to {0}",
            "set_item {1} = {0}",
            "win",
            "loose",
            "drawImage {2} on {0} {1}",
            "drawRect on {0} {1} with color ( {2} {3} {4} )",
            "clear {0} {1}",
            "compare {} {} {} => {}",
            "jump {} lines if {}",
            "setFlag {} = {}",
            "tp to {} {}",
            "jumpRelative {} lines if {}",
            "createMemory at {}",
            "loadToMemory at {} with index {} from {}",
            "loadFromMemory at {} with index {} to {}",
            "randomNumber from {} to {} => {}",
            "loadFromPointer at {} to {}",
            "storeToPointer value {} to {}",
            "place_block {}",
            "show_text {1} using {0}"
        ]
        try:
            return ms[cmd]
        except IndexError:
            return "ERROR:INVALID_COMMAND"

    def getEnum(self, cmd):
        ens = [
            None,
            [None, "on_init", "on_step", "on_collect", "on_explode", "on_destroy","on_tick"],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            [
                None,
                "player.health",
                "player.bombs",
                "player.range",
                "player.dynamite",
                "player.timed_bombs",
                "player.damage",
                "player.nukes",
            ],
            [
                None,
                "player.health",
                "player.bombs",
                "player.range",
                "player.dynamite",
                "player.timed_bombs",
                "player.damage",
                "player.nukes",
            ],
            None,
            None,
            None,
            None,
            None,
            [None, ">", "<", "==", "<=", ">="],
            None,
            [None, "drop_items"],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            [None, "mode_popup","mode_display"]
        ]
        return ens[cmd]

    def get_config(self, cmd):
        cc = [
            "",
            "§$$",
            "",
            "***",
            "***",
            "***",
            "***",
            "*$",
            "*",
            "*§",
            "*§",
            "",
            "",
            "***",
            "*****",
            "**",
            "*§**",
            "**",
            "§$",
            "**",
            "**",
            "*",
            "***",
            "***",
            "***",
            "**",
            "**",
            "*",
            "§*"
        ]
        return cc[cmd]

    def compile_trigger(self, attrs, line):
        util.validateCommandLength(attrs, 5, line)
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd, 1)
        events = [None, "on_init", "on_step", "on_collect", "on_explode", "on_destroy", "on_tick"]
        i = util.validateEnum(attrs[1], events, line, [None])
        result += util.byte(i, 1)
        x = util.validateInteger(attrs[3], 255, line, self.logfile)
        y = util.validateInteger(attrs[4], 255, line, self.logfile)
        result += util.byte(x, 1)
        result += util.byte(y, 1)
        return result
    def compile_ptr(self, attrs, line):
        util.validateCommandLength(attrs, 5, line)
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd,1)
        f = util.validateInteger(attrs[2],65535,line,self.logfile)
        t = util.validateInteger(attrs[4],65535,line,self.logfile)
        result += util.byte(f,2)
        result += util.byte(t,2)
        return result
    def compile_end(self, attrs, line):
        util.validateCommandLength(attrs, 1, line)
        cmd = self.getCommandId(attrs[0])
        return util.byte(cmd, 1)

    def compile_math(self, attrs, line):
        util.validateCommandLength(attrs, 6, line)
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd, 1)
        a = util.validateInteger(attrs[1], 65535, line, self.logfile)
        b = util.validateInteger(attrs[3], 65535, line, self.logfile)
        c = util.validateInteger(attrs[5], 65535, line, self.logfile)
        result += util.byte(a, 2)
        result += util.byte(b, 2)
        result += util.byte(c, 2)
        return result

    def compile_set(self, attrs, line):
        util.validateCommandLength(attrs, 4, line)
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd, 1)
        m = util.validateInteger(attrs[1], 65535, line, self.logfile)
        v = util.validateInteger(attrs[3], 255, line, self.logfile)
        result += util.byte(m, 2)
        result += util.byte(v, 1)
        return result

    def compile_reset(self, attrs, line):
        util.validateCommandLength(attrs, 2, line)
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd, 1)
        m = util.validateInteger(attrs[1], 65535, line, self.logfile)
        result += util.byte(m, 2)
        return result

    def compile_get(self, attrs, line):
        util.validateCommandLength(attrs, 4, line)
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd, 1)
        values = [
            None,
            "player.health",
            "player.bombs",
            "player.range",
            "player.dynamite",
            "player.timed_bombs",
            "player.damage",
            "player.nukes",
        ]
        i = util.validateEnum(attrs[1], values, line, [None])
        m = util.validateInteger(attrs[3], 65535, line, self.logfile)
        result += util.byte(m, 2)
        result += util.byte(i, 1)
        return result

    def compile_drawimg(self, attrs, line):
        # draw image on x y => stor
        util.validateCommandLength(attrs, 7, line)
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd, 1)
        x = util.validateInteger(attrs[3], 65535, line, self.logfile)
        y = util.validateInteger(attrs[4], 65535, line, self.logfile)
        i = util.validateInteger(attrs[1], 65535, line, self.logfile)
        result += util.byte(x, 2)
        result += util.byte(y, 2)
        result += util.byte(i, 2)
        return result

    def compile_rect(self, attrs, line):
        # drawRect on x y with color ( r g b ) => stor
        util.validateCommandLength(attrs, 13, line)
        mx = 65535
        x = util.validateInteger(attrs[2], mx, line, self.logfile)
        y = util.validateInteger(attrs[3], mx, line, self.logfile)
        r = util.validateInteger(attrs[7], mx, line, self.logfile)
        g = util.validateInteger(attrs[8], mx, line, self.logfile)
        b = util.validateInteger(attrs[9], mx, line, self.logfile)
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd, 1)
        result += util.byte(x, 2)
        result += util.byte(y, 2)
        result += util.byte(r, 2)
        result += util.byte(g, 2)
        result += util.byte(b, 2)
        return result

    def compile_clear(self, attrs, line):
        util.validateCommandLength(attrs, 2, line)
        x = util.validateInteger(attrs[1], 65535, line, self.logfile)
        y = util.validateInteger(attrs[2], 65535, line, self.logfile)
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd, 1)
        result += util.byte(x, 2)
        result += util.byte(y, 2)
        return result

    def compile_comp(self, attrs, line):
        # compare a o b => c
        util.validateCommandLength(attrs, 6, line)
        a = util.validateInteger(attrs[1], 65535, line, self.logfile)
        b = util.validateInteger(attrs[3], 65535, line, self.logfile)
        c = util.validateInteger(attrs[5], 65535, line, self.logfile)
        operands = [None, ">", "<", "==", "<=", ">="]
        o = util.validateEnum(attrs[2], operands, line, [None])
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd, 1)
        result += util.byte(a, 2)
        result += util.byte(o, 1)
        result += util.byte(b, 2)
        result += util.byte(c, 2)
        return result

    def compile_jump(self, attrs, line):
        # jump m lines if a
        util.validateCommandLength(attrs, 5, line)
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd, 1)
        j = util.validateInteger(attrs[1], 65535, line, self.logfile)
        c = util.validateInteger(attrs[4], 65535, line, self.logfile)
        result += util.byte(j, 2)
        result += util.byte(c, 2)
        return result
    def compile_flag(self, attrs, line):
        util.validateCommandLength(attrs, 4, line)
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd, 1)
        values = [None, "drop_items"]
        i = util.validateEnum(attrs[1], values, line, [None])
        result += util.byte(i, 1)
        v = util.validateInteger(attrs[3], 255, line, self.logfile)
        result += util.byte(v, 1)
        return result

    def accessCompilationScript(self, cmd):
        return self.comp_scripts[cmd]

    def compileCommand(self, cmd, attrs, line):
        return self.accessCompilationScript(cmd)(attrs, line)

    def compile_tp(self, attrs, line):
        util.validateCommandLength(attrs, 4, line)
        x = util.validateInteger(attrs[2], 65535, line, self.logfile)
        y = util.validateInteger(attrs[3], 65535, line, self.logfile)
        cmd = self.getCommandId(attrs[0])
        result = util.byte(cmd, 1)
        result += util.byte(x, 2)
        result += util.byte(y, 2)
        return result
    def compile_downloadRAM(self, attrs, line):
        util.validateCommandLength(attrs, 3, line)
        adress = util.validateInteger(attrs[2],65535,line,self.logfile)
        result = util.byte(self.getCommandId(attrs[0]),1)
        result += util.byte(adress,2)
        return result
    def compile_toMemory(self, attrs,line):
        util.validateCommandLength(attrs,8,line)
        location = util.validateInteger(attrs[2],65535,line,self.logfile)
        index = util.validateInteger(attrs[5],65535,line,self.logfile)
        source = index = util.validateInteger(attrs[7],65535,line,self.logfile)
        result = util.byte(self.getCommandId(attrs[0]),1)
        result += util.byte(location, 2)
        result += util.byte(index,2)
        result += util.byte(source, 2)
        return result
    def compile_rand(self, attrs, line):
        util.validateCommandLength(attrs,7,line)
        _min = util.validateInteger(attrs[2],65535,line,self.logfile)
        _max = util.validateInteger(attrs[4],65535,line,self.logfile)
        stor = util.validateInteger(attrs[6],65535,line,self.logfile)
        result = util.byte(self.getCommandId(attrs[0]),1)
        result += util.byte(_min,2)
        result += util.byte(_max,2)
        result += util.byte(stor,2)
        return result
    def compile_text(self, attrs, line):
        util.validateCommandLength(attrs, 4, line)
        text = util.validateInteger(attrs[1],65535,line,self.logfile)
        mode = util.validateEnum(attrs[3],[None,"mode_popup","mode_display"],line, [None])
        result = util.byte(self.getCommandId(attrs[0]),1)
        result += util.byte(mode, 1)
        result += util.byte(text,2)
        return result
    def compile(self, script: str, options="") -> bytes:
        self.logfile.add_log(f"Compiling started with options {options}")
        result = b"\x00"
        lines = script.split("\n")
        for i in range(len(lines)):
            line = lines[i]
            attrs = line.split(" ")
            cmd = self.getCommandId(attrs[0])
            if cmd == False:
                if "--disable_comment_warnings" not in options:
                    self.logfile.add_log(
                        f"WARNING Line {i} is not a valid command. Use --disable_comment_warnigns to remove this from the log."
                    )
                continue
            result += self.compileCommand(cmd, attrs, i)
        self.logfile.add_log(f"Compiling finished.")
        if "--write_log" in options:
            self.logfile.write_log("LOG " + str(time.time()) + ".log")
        self.logfile = log()
        return result

    def process_line(self, line: bytes, config):
        exl = 1
        for c in config:
            if c == "$" or c == "§":
                exl += 1
            elif c == "*":
                exl += 2
            else:
                raise ValueError("Invalid Config")
        if len(line) != exl:
            raise ValueError(
                f"Decompiler Error [006]: Length missmatch. Exspected {exl}, got {len(line)}"
            )
        chrs = [line[0]]
        line = line[1:]
        i = 0
        j = 0
        while i < len(config):
            if config[i] == "§" or config[i] == "$":
                chrs.append(line[j])
            elif config[i] == "*":
                chrs.append(256 * line[j] + line[j + 1])
                j += 1
            j += 1
            i += 1
        cmd = chrs.pop(0)
        for i in range(len(chrs)):
            if config[i] == "§":
                chrs[i] = self.getEnum(cmd)[chrs[i]]
        mask = self.getCommandMask(cmd)
        cmd = self.getCommandString(cmd)
        return mask.format(*tuple(chrs))

    def decompile(self, data: bytes) -> str:
        if data == b"\x00\r":
            return ""
        data = data[1:]
        lines = []
        result = ""
        i = 0
        while i < len(data):
            cmi = self.get_config(data[i])
            ll = 1
            for c in cmi:
                if c == "$" or c == "§":
                    ll += 1
                elif c == "*":
                    ll += 2
            lines.append(data[i : i + ll])
            i += ll
        for line in lines:
            result += self.process_line(line, self.get_config(line[0])) + "\n"
        result = result[:-1]
        return result


# Usage: a = compiler()
# a.comile(script: str, options: str="") -> bytes
# a.decomile(script: bytes) -> str
"""
script = "@ on_collect on 1 1\nset 0 = 20\ntp to 0 0\nend"
a = compiler()
print(a.compile(script))
print(a.decompile(a.compile(script, "--write_log")))
"""
