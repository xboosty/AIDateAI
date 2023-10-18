import os

class Files:
    def __init__(self):
        # Get path root
        self.path_root = os.getcwd()
        print(self.path_root)
    
    def getPathRoot(self):
        return self.path_root
    
    def getConcatPathToRoot(self,path):
        if os.path.exists(os.path.join(self.path_root, path)):
            return os.path.join(self.path_root, path)
        else:
            print(f"The path {path} there is'nt.")
            
    def joinPath(self,pathX,pathY):
        return os.path.join(pathX, pathY)
    
    def createPathRoot(self,path):
        with open(str(path)+"\\path.txt","w") as f:
            f.write(path)