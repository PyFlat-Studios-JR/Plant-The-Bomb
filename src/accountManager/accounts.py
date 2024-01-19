import src.crypto as crypto
import os, json, random, hashlib

import src.accountManager.statregister as stats

SCTX = stats.getStatContext()
class userContent():
    def __init__(self, usr_or_json: str, pwd: str | None = None):
        self.times = {}
        if not pwd:
            self.loadFromJSON(usr_or_json)
        else:
            self.usr = usr_or_json
            self.pwd = pwd
            self.completedlevels = []
            self.times = {}

    def is_level_completed(self, filename):
        content = open(filename,"rb").read()
        hash = hashlib.sha256(content).hexdigest()
        return hash in self.completedlevels
    def mark_as_completed(self, filename, time = None, haswon=True):
        content = open(filename,"rb").read()
        hash = hashlib.sha256(content).hexdigest()
        if hash not in self.completedlevels:
            self.completedlevels.append(hash)
        if hash not in SCTX.data["levels_completed"]:
            SCTX.data["levels_completed"][hash] = {"name":filename, "amount":0}
        if hash not in SCTX.data["levels_played"]:
            SCTX.data["levels_played"][hash] = {"name":filename, "amount":0}
        if hash not in SCTX.data["time_spent_levels"]:
            SCTX.data["time_spent_levels"][hash] = {"name":filename, "amount":0}
        SCTX.data["levels_played"][hash]["amount"] += 1
        SCTX.data["levels_played_total"] += 1

        if time:
            d2,h2,M2,s2,m2 = time
            t1 = self.times[hash]
            ticks_2 = m2
            ticks_2 += s2 *1000
            ticks_2 += M2 * 60 * 1000
            ticks_2 += h2 * 60 * 60 * 1000
            ticks_2 += d2 * 24 * 60 * 60 * 1000
            SCTX.data["time_spent_levels"][hash]["amount"] += ticks_2
            SCTX.data["time_spent_levels_total"] += ticks_2
            if not haswon:
                return
            SCTX.data["levels_completed"][hash]["amount"] += 1
            SCTX.data["levels_completed_total"] += 1
            if hash in self.times:
                ticks_1 = int(t1.split(".")[1])
                ticks_1 += int(t1.split(":")[0]) * 1000
                ticks_1 += int(t1.split(":")[1]) * 60 *  1000
                ticks_1 += int(t1.split(":")[2]) * 60*60*1000
                ticks_1 += int(t1.split(":")[3].split(".")[0]) * 60 *60*  1000*24
                if ticks_2 < ticks_1:
                    time = "{}:{}:{}:{}.{}".format(*time)
                    self.times[hash] = time
    def loadFromJSON(self, jason:str):
        dc: dict = json.loads(jason)
        self.usr = dc["user"]
        self.pwd = dc["password"]
        self.completedlevels = dc["levels"]
        if "times" in dc:
            self.times = dc["times"]
        else:
            self.times = {}
        if "stats" in dc:
            SCTX.load(dc["stats"])
        else:
            SCTX.load()
    def get_time(self, level):
        content = open(level,"rb").read()
        hash = hashlib.sha256(content).hexdigest()
        if hash in self.completedlevels:
            if hash in self.times:
                return self.times[hash]
        return "-"
    def dumptoJSOM(self):
        a = {}
        a["user"] = self.usr
        a["password"] = self.pwd
        a["levels"] = self.completedlevels
        a["times"] = self.times
        a["stats"] = SCTX.data
        return json.dumps(a)
    def create_recovery_code(self):
        data = json.loads(open("saves/recovery/backupcodebase.json").read())
        usrhash = crypto.sha256(self.usr+"this_is_a_salt_:_)_._._.")
        rccodeset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        rccode = ""
        for i in range (6):
            rccode += rccodeset[random.randint(0,len(rccodeset)-1)]
        data[usrhash] = crypto.encode(self.pwd,rccode)
        print(f"Created recovery code for {self.usr}. Your one-time recovery code is {rccode}")
        open("saves/recovery/backupcodebase.json","w").write(json.dumps(data))
class userManager():
    def __init__(self) -> None:
        #setup required folder structure on init
        if not os.path.isdir("saves"):
            os.mkdir("saves")
        if not os.path.isdir("saves/recovery"):
            os.mkdir("saves/recovery")
        if not os.path.isfile("saves/recovery/backupcodebase.json"):
            open("saves/recovery/backupcodebase.json", "w").write("{}")
        self.user_content: userContent | None = None
        #user content structure:
        #name: user name as string
        #pass: user password
        #completedlevels: [hash]
        #ok, thats it
    def loginUser(self, username: str, pwd: str):
        usr_filename = "saves/"+ crypto.sha256(username+"this_is_a_salt_:_)_._._.") + ".ptbsav"
        if not os.path.isdir("saves"):
            os.mkdir("saves")
        if not os.path.isfile(usr_filename):
            return 1 #user does not exist!
        with open(usr_filename, "r") as file:
            content: str = file.read()
        decrypted_content: str | None = crypto.decode(content, "_another_salt"+pwd+".._.._salty_yummy_.._..")
        if not decrypted_content:
            return 2 #content decode error
        self.user_content = userContent(decrypted_content)
        return 0 # all okay :)
    def createUser(self, username: str, pwd: str):
        usr_filename = "saves/"+ crypto.sha256(username+"this_is_a_salt_:_)_._._.") + ".ptbsav"
        if not os.path.isdir("saves"):
            os.mkdir("saves")
        if os.path.isfile(usr_filename):
            return 1 #user does exist!
        self.user_content = userContent(username, pwd)
        encrypted_content = crypto.encode(self.user_content.dumptoJSOM(), "_another_salt"+pwd+".._.._salty_yummy_.._..")
        with open(usr_filename,"w") as file:
            file.write(encrypted_content)
        return 0
    def saveData(self):
        if self.user_content:
            username = self.user_content.usr
            pwd = self.user_content.pwd
            usr_filename = "saves/"+ crypto.sha256(username+"this_is_a_salt_:_)_._._.") + ".ptbsav"
            e = crypto.encode(self.user_content.dumptoJSOM(),"_another_salt"+pwd+".._.._salty_yummy_.._..")
            open(usr_filename, "w").write(e)
            print("Saved data successfully!")
if __name__ == "__main__":
    print("Should not initialize accounts.py as main. Exited!")
    os.sys.exit(-1)
_ACCOUNTS = None
def getAccountContext():
    global _ACCOUNTS
    if _ACCOUNTS == None:
        _ACCOUNTS = userManager()
    return _ACCOUNTS