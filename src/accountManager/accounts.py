import src.crypto as crypto
import os, json, random, hashlib
class userContent():
    def __init__(self, usr_or_json: str, pwd: str | None = None):
        if not pwd:
            self.loadFromJSON(usr_or_json)
        else:
            self.usr = usr_or_json
            self.pwd = pwd
            self.completedlevels = []
    def is_level_completed(self, filename):
        content = open(filename,"rb").read()
        hash = hashlib.sha256(content).hexdigest()
        return hash in self.completedlevels
    def mark_as_completed(self, filename):
        content = open(filename,"rb").read()
        hash = hashlib.sha256(content).hexdigest()
        if hash not in self.completedlevels:
            self.completedlevels.append(hash)
    def loadFromJSON(self, jason:str):
        dc: dict = json.loads(jason)
        self.usr = dc["user"]
        self.pwd = dc["password"]
        self.completedlevels = dc["levels"]
    def dumptoJSOM(self):
        a = {}
        a["user"] = self.usr
        a["password"] = self.pwd
        a["levels"] = self.completedlevels
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