from distutils.core import setup
import py2exe

includes = ["encodings", "encodings.*"]    

options = {"py2exe":
    {"compressed": 1, 
     "optimize": 2,
     "ascii": 1,
     "includes":includes,
     "bundle_files": 1 
     }
    }
setup(     
    version = "1.0.0.0",  
    description = "sendmail",  
    name = "sendmail", 	
    options = options,      
    zipfile=None,
    console=['sendmail.py']
    # console=[{"script": "hello.py", "icon_resources": [(1, "Circle.ico")] }]
    )
	
# setup(console=['UpdateDPServerFile.py'])