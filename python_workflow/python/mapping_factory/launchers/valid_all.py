import os
import sys
import traceback
import json
import xmltodict

from mapping_factory.validator.validator import Validator
from mapping_factory.launchers import data_dir

base_path = os.path.dirname(os.path.realpath(__file__)) 


validator = Validator(os.path.join(data_dir
                                   , "schemas"
                                   , "vodml_lite.xsd"))


# Open a file
sample_path = os.path.join(data_dir
                         , "mapping_components")
dirs = os.listdir( sample_path )

# This would print all the files and directories
for file in dirs:
    if not file.endswith(".xml"):
        continue
    sample_file = os.path.join(sample_path, file)
   
    try:
        validator.validate_file(sample_file)
        print(file + ' is Valid')
        with open(sample_file, 'r') as f:
            my_xml = f.read()     
            with open(sample_file.replace(".xml", ".json"), 'w') as jsonfile:
                jsonfile.write(json.dumps(xmltodict.parse(my_xml)
                                          , indent=2, sort_keys=True))
    except :
        print(file + ' is not Valid')
        traceback.print_exc()    
        sys.exit(1)                                  
    
        