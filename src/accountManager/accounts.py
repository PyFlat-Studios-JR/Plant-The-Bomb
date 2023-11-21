import src.crypto as crypto
import os
class userManager():
    def __init__(self) -> None:
        self.user_content: str | None = None
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
        self.user_content = decrypted_content
        return 0 # all okay :)
    def createUser(self, username: str, pwd: str):
        usr_filename = "saves/"+ crypto.sha256(username+"this_is_a_salt_:_)_._._.") + ".ptbsav"
        if not os.path.isdir("saves"):
            os.mkdir("saves")
        if os.path.isfile(usr_filename):
            return 1 #user does exist!
        encrypted_content = crypto.encode("PTB IS A COOL GAME! THERE IS NO DATA HERE!", "_another_salt"+pwd+".._.._salty_yummy_.._..")
        with open(usr_filename,"w") as file:
            file.write(encrypted_content)
        return 0
if __name__ == "__main__":
    print("Should not initialize accounts.py as main. Exited!")
    os.sys.exit(-1)