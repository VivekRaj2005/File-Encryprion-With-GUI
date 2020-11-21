from flask import *
import os
import shutil
import sqlite3
# import subprocess
import random

# CONSTANTS
mainLink = "/Main"
encodeLink = "/Encode"
decodeLink = "/Decode"
exitLink = "/Exit"
resetLink = "/Reset"
Generate_New_Hash_Map_link = "/GNHM"
fti = "/FTI"

# Helper Functions
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def GetMultipleDecryption(listobj):
    val = []
    for obj in listobj:
        val.append(GetDecodeEncryption(obj, "Hash_Map"))
    return val


def STRTOLIST(String) -> []:
    return String.split("\n")


def LISTTOTEXT(listobj):
    if listobj is None:
        return None
    FileWriter("Val_Print.file", "STOPPED:18")
    FileWriter("CONSTANTS", len(listobj))
    if len(listobj) == 0:
        return []
    rt_val = ""
    for x in range(len(listobj) - 1):
        rt_val += f"{listobj[x]}\n"
    rt_val += f"{listobj[len(listobj) - 1]}"

    return rt_val


def GetMultipleEncryption(listobj):
    val = []
    ret = False
    for obj in listobj:
        bol = GetEncryption(obj, "Hash_Map")
        if bol is False:
            FileWriter("fIN_cONTENT", "Please RETRY")
            ret = True
        else: 
            val.append(GetEncryption(obj, "Hash_Map"))
    if ret is False:
        return val
    else:
        return None


def ReadFile(path) -> []:
    if os.path.exists(path):
        # if path.split(".")[1] == "txt":
        file = open(path, 'r')
        rt_val = []
        while True:
            response = file.readline()
            if response == "":
                break
            else:
                rt_val.append(response.replace("\n", ""))
        file.close()
        return rt_val
        # else: 
        # return []
    else: 

        return []


def GenerateSampleSpace(): 
    FileWriter("sample_space", "qwertyuiopasdfgh\"jklzxcvbnm1234567890{}:-+_=<>?!@#$%^&*.()[]\\|;\'/QWERTYUIOPASDFGHJKLZXCVBNM ")


def FileWriter(file, content):
    if content is None:
        return
    if os.path.exists(f"{file}.file"):
        os.remove(f"{file}.file")
    with open(f'{file}.txt', 'w') as fileRead:
        fileRead.write(f"{content}")
    shutil.copy(f'{file}.txt', f'{file}.file')
    os.remove(f"{file}.txt")


def Reset():
    files = ["Hash_Map.file", "content.file", "sample_space.file"]
    for file in files:
        if os.path.exists(file):
            os.remove(file)
    quit(0)


def FileReader(file) -> str:
    shutil.copy(f'{file}.file', f'{file}.txt')
    with open(f'{file}.txt', 'r') as fileRead:
        content = fileRead.readline()
    os.remove(f"{file}.txt")
    return content


def removeChar(char, string) -> str:
    rt_val = ""
    for chars in string:
        if char != chars:
            rt_val += chars
    return rt_val


def GenerateHashTable():
    sample_space = FileReader("sample_space")
    sample = sample_space
    rt_val = ""

    for x in range(len(sample) - 1):
        if len(sample_space) == 0:
            break
        FileWriter("Err_Print", len(sample_space))
        char = random.choice(sample_space)
        rt_val += f"{char}||"
        sample_space = removeChar(char, sample_space)

    rt_val += sample_space[0]
    FileWriter("Hash_Map", rt_val)


def LoadSample(hash_map) -> []:
    read = FileReader(hash_map)
    set_char = read.split("||")
    return set_char


def WriteEncryption(string, hash_map):
    sample = LoadSample(hash_map)
    rt_val = ""
    for x in range(len(string) - 1):
        char = string[x]
        rt_val += f"{str(sample.index(char))}||"
    char = string[len(string) - 1]
    rt_val += f"{str(sample.index(char))}"
    FileWriter("content", rt_val)


def GetEncryption(string, hash_map):
    sample = LoadSample(hash_map)
    rt_val = ""
    for x in range(len(string) - 1):
        char = string[x]
        try:
            sample.index(char)
            rt_val += f"{str(sample.index(char))}||"
        except Exception as e:
            FileWriter("Val_Print", str(e))
            if "is not in list" in str(e):
                text = str(FileReader("sample_space"))
                text += string[x]
                FileWriter("sample_space", text)
                GenerateHashTable()
                return False
        
    char = string[len(string) - 1]
    try:
        sample.index(char)
        rt_val += f"{str(sample.index(char))}"
    except Exception as e:
        if "is not in list" in str(e):
            text = str(FileReader("sample_space"))
            text += string[len(string) - 1]
            FileWriter("sample_space", text)
            GenerateHashTable()
            return False
    return rt_val


def GetDecodeEncryption(file, hash_map):
    sample = LoadSample(hash_map)
    rt_val = ""
    read = file
    space = read.split("||")
    for char in space:
        rt_val += str(sample[int(char)])
    return rt_val

def DecodeEncryption(file, hash_map):
    sample = LoadSample(hash_map)
    rt_val = ""
    read = FileReader(file)
    space = read.split("||")
    for char in space:
        rt_val += str(sample[int(char)])
    return rt_val


def Encoder():
    print("USE DEFAULT HASH MAP?[Y / N]")
    a = input(">>>")
    if a.lower() == "y":
        WriteEncryption(input("Enter content:"), "Hash_Map")
    else:
        a = input("Path")
        if os.path.exists(a) and ".file" in a:
            os.mkdir("Hash_Map")
            shutil.copy("Hash_Map.file", "Hash_Map\\Hash_Map.file")
            os.remove("Hash_Map.file")
            shutil.copy(a, "Hash_Map.file")
            WriteEncryption(input("Enter content:"), "Hash_Map")
            os.remove("Hash_Map.file")
            shutil.copy("Hash_Map\\Hash_Map.file", "Hash_Map.file")
            os.remove("Hash_Map\\Hash_Map.file")
            os.rmdir("Hash_Map")


def LoadClearer():
    try:
        os.system('cls')
        def clear(): os.system('cls')
        return clear
    except Exception as e:
        FileWriter("Error Log1", e)
    try:
        os.system("clear")
        def clear(): os.system('clear')
        return clear
    except Exception as e:
        FileWriter("Error Log2", e)



class Server:
    def __init__(self):
        self.App = Flask(__name__)
        self.Login = False

    def run(self):
        @self.App.route("/", methods=["GET" ,"POST"])
        def Home():
            if os.path.exists("sample_space.file") is False:
                return redirect("/FTI/0")
            elif request.method == "GET":
                if self.Login:
                    redirect(url_for("Main"))
                return render_template("LOGIN.html")
            else:
                PASS = DecodeEncryption("ENCRYPTOR\\Password", "ENCRYPTOR\\Hash_Map")
                epass = request.form["Pass"]
                if PASS == epass:
                    return redirect(url_for("Main"))
                    self.Login = True
                else:
                    FileWriter("Val_Print", "FAIL")
                return render_template("LOGIN.html")

        @self.App.route(mainLink, methods=["GET"])
        def Main():
            if self.Login is False:
                    redirect(url_for("Home"))
            return render_template("MENU.html", encodeLink=encodeLink, 
                decodeLink=decodeLink, GNHML=Generate_New_Hash_Map_link, resetLink=resetLink, exitLink=exitLink)

        @self.App.route(decodeLink, methods=["GET", "POST"])
        def DecoderPage():
            if self.Login is False:
                    redirect(url_for("Home"))
            if request.method == "GET":
                return render_template("Decoder.html")
            else:
                FileWriter("Val_Print", request.form)
                file = request.form["File"]
                hs_file = request.form["HM-File"]

                if file == "":
                    file = "fIN_cONTENT.file"
                if hs_file == "":
                    hs_file = "Hash_Map.file"
                if os.path.exists(file):
                    FileWriter("fIN_cONTENT", LISTTOTEXT(GetMultipleDecryption(ReadFile(file))))
                else:
                    FileWriter("fIN_cONTENT", "PLEASE RETRY!")
                return redirect(url_for("Main"))

        @self.App.route(exitLink, methods=["GET", "POST"])
        def Quit():
            shutdown_server()
            return redirect(url_for("Home"))

        @self.App.route(resetLink, methods=["GET", "POST"])
        def Reset():
            if self.Login is False:
                    redirect(url_for("Home"))
            if request.method == "GET":
                return render_template("Reset.html")
            else:
                PASS = DecodeEncryption("ENCRYPTOR\\Password", "ENCRYPTOR\\Hash_Map")
                epass = request.form["Pass"]
                if PASS == epass:
                    ClearUp().Run()
                    return redirect(url_for("Home"))
                else:
                    return redirect(url_for("Reset"))

       
        @self.App.route(Generate_New_Hash_Map_link, methods=["GET", "POST"])
        def GNHM():
            if self.Login is False:
                    redirect(url_for("Home"))
            if request.method == "GET":
                return render_template("GNHM.html")
            else:
                PASS = DecodeEncryption("ENCRYPTOR\\Password", "ENCRYPTOR\\Hash_Map")
                epass = request.form["Pass"]
                if PASS == epass:
                    if os .path.exists("Hash_Map.file"):
                        os.remove("Hash_Map.file")
                    GenerateHashTable()
                    return redirect(url_for("Main"))
                else:
                    return redirect(url_for("GNHM"))

                

        @self.App.route(encodeLink, methods=["GET", "POST"])
        def EncoderPage():
            if self.Login is False:
                    redirect(url_for("Home"))
            if request.method == "GET":
                return render_template("Encoder.html")
            else:
                file = request.form["File"]
                if os.path.exists(file):
                    FileWriter("fIN_cONTENT", LISTTOTEXT(GetMultipleEncryption(ReadFile(file))))
                else:
                    FileWriter("fIN_cONTENT", "PLEASE RETRY!")
                return redirect(url_for("Main"))

        @self.App.route(f"{fti}/<int:num>", methods=["GET" ,"POST"])
        def FTI(num):
            if os.path.exists("sample_space.file"):
                return redirect(url_for("Home"))
            if num == 0:
                if request.method == "GET":
                    return render_template("FTI 0.html")
                else:
                    password = request.form["Pass"]
                    GenerateSampleSpace()
                    GenerateHashTable()
                    WriteEncryption(password, "Hash_Map")
                    os.mkdir("ENCRYPTOR")
                    shutil.copy("Hash_Map.file", "ENCRYPTOR\\Hash_Map.file")
                    shutil.copy("content.file", "ENCRYPTOR\\Password.file")
                    # os.remove("Hash_Map.file")
                    os.remove("content.file")
                    # os.remove("sample_space.file")
                    return redirect(url_for("Main"))

        self.App.run(debug=False)



class ClearUp:
    def __init__(self):
        self.files = [
            "Err_Print.file",
            "fIN_cONTENT.file",
            "Hash_Map.file",
            "sample_space.file",
            "CONSTANTS.file",
            "Val_Print.file",
            "Val_Print.file.file",
            "abcd.file",
            "ReadFile.file",
            "ENCRYPTOR\\Hash_Map.file",
            "ENCRYPTOR\\Password.file"
            ]
        self.dirs = [
            "ENCRYPTOR"
            ]

    def Remove(self, file):
        try:
            print(f"Removing: {file}")
            os.remove(file)
        except Exception as e:
            print(str(e))

    def RemoveDir(self, Dir):
        try:
            print(f"Removing: {Dir}")
            os.rmdir(Dir)
        except Exception as e:
            print(str(e))

    def Run(self):
        for file in self.files:
            self.Remove(file)
        for dir_ in self.dirs:
            self.RemoveDir(dir_)

Server().run()
