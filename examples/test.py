import zipfile
import os

def zip_file(event):
    input = event.get["files"]
    
    