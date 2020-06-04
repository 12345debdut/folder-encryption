from os import path,listdir,mkdir
import base64
import io
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
print("Please enter the password to encrypt:")
password_provided = input() # This is input in the form of a string
password = password_provided.encode() # Convert to type bytes
salt = b'\x86\xd8)P\x81\xc7g\x82\xf1p\x8f"\xa77\x08V' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
print("Enter your directory path to encrypt: ")
filepath=input()
print("Enter the path where to store newly created files: ")
newpath=input()
print("Enter your folder name to store encrypted file: ")
newfolder=input()
# print("Enter the name of the new folder")
# newfolder=input()
# print("Enter where to save the file? please give absolute path")
# newfilepath=input()
try:
    def fileencryption(pathdir,filename,newpath=""):
        f=open(path.join(pathdir,filename),'rb')
        message = base64.b64encode(f.read())
        f.close()
        f = Fernet(key)
        encrypted = f.encrypt(message)
        f=open(path.join(newpath,filename),'wb')
        f.write(encrypted)
        f.close()
        print("Encryption successfull of file {}".format(path.join(newpath,filename)))
    def direncryption(pathdir,dirname,newpath=""):
        files=listdir(pathdir)
        print("Encrypting the directory {}".format(newpath))
        for item in files:
            if path.isdir(path.join(pathdir,item)):
                if(path.isdir(path.join(newpath,item))):
                    pass
                else:
                    mkdir(path.join(newpath,item))
                direncryption(path.join(pathdir,item),item,path.join(newpath,item))
            else:
                fileencryption(pathdir,item,newpath)
    if(len(password)>0 and len(filepath)>0 and len(newpath)>0):
        if(path.isdir(path.join(newpath,newfolder))):
            print("A folder with this name is still exist. do you want to procceed?(y/n)")
            res=input()
            if(res.lower()=="y" or res.lower()=="yes"):
                pass
            else:
                sys.exit()
        else:
            mkdir(path.join(newpath,newfolder))
        direncryption(filepath,path.basename(filepath),path.join(newpath,newfolder))
    else:
        print("Enter all the informations all are required feild...")
except Exception as e:
    print(e)