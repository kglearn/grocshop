from passlib.context import CryptContext

passwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPasswd(password: str):
    return passwdContext.hash(password)

def verifyPasswd(plainPasswd, hashPasswd):
    return passwdContext.verify(plainPasswd, hashPasswd)

def intersection(lst1, lst2):
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3