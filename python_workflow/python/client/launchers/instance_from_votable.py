'''
Created on 6 avr. 2020

@author: laurentmichel
'''
import re, os
import xmltodict

from schema.validator.validator import Validator
from client.inst_builder.json_mapping_builder import JsonMappingBuilder
from client.inst_builder.instancier import Instancier
from client.launchers import logger, data_dir

class InstanceFromVotable:
    '''
    Translates the mapping block of the inputy VOTable in dictionary where all mapping elements 
    names are replaced with attribute values
    '''
    def __init__(self, votable_path):
        '''
        Constructor
        :param votable_path: VOTAble path
        :type votable: string
        '''
        self.votable_path = votable_path
        self.vodml_block = None

    def _extract_vodml_block(self):
        '''
        Stores in an intern field the VODML block as a string
        Raise an exception in case of failure
        '''
        logger.info("extract vodml block from %s", self.votable_path)
        with open(self.votable_path) as xml_file:
            self.vodml_block =re.search(r'<VODML>((.|\n)*?)</VODML>', xml_file.read()).group() 
        
        if self.vodml_block is None :
            raise Exception("No vodml block found")
        logger.info("VODML found")
        
    def _validate_vodml_block(self):
        '''
        Validates the VODML block against the mapping schema
        Raise an exception in case of failure
        '''
        validator = Validator(os.path.join(data_dir
                                   , "schemas"
                                   , "vodml_lite.xsd"))
        if validator.validate_string(self.vodml_block) is True:
            logger.info("VODML block is valid")
            self.json_block = xmltodict.parse(self.vodml_block)
        else:
            logger.error("VODML block is not valid")
            raise Exception("VODML block is not valid")
        
    def _build_instance(self):
        '''
        Translate the VODML block into dict
        '''
        builder = JsonMappingBuilder(json_dict=self.json_block)

        builder.revert_sets("GLOBALS",
                                         default_key='globals')
        #self.builder.revert_compositions("COMPOSITION")
        builder.revert_sets("TEMPLATES",
                                         default_key='root')
        builder.revert_array()
        builder.revert_compositions("COMPOSITION")
        builder.revert_elements("INSTANCE")
        builder.revert_elements("VALUE")
        builder.revert_elements("MODEL")

        self.json_vodml_block = builder.json
        logger.info("JSON VODML block built")
        

    def _populate_instance(self, resolve_refs=False):
        '''
        Set the dict with the real values
        :param resolve_refs: Flag for resolving the cross-reference in the mapping. 
                             if true, instance references are replaced with a copy 
                             of the referenced instance
        :type resolve_refs: boolean
        '''
        self._instancier = Instancier(self.votable_path
                                  , json_inst_dict=self.json_vodml_block)
        self._instancier.set_element_values(resolve_refs=resolve_refs)
        self._instancier.set_array_values()
        self._instancier.map_columns()
        logger.info("VODML instance created")

    def build_instance(self, resolve_refs=False):
        '''
         This is the public class that must be invoked from outside
         It does the checking and build the model instance that is hosted by 
         an Instancier instance
        :param resolve_refs: Flag for resolving the cross-reference in the mapping. 
                             if true, instance references are replaced with a copy 
                             of the referenced instance
        :type resolve_refs: boolean
        :return : An Instancier the contains the dictionary representation of the model 
                  in addition to some getters 
        :rtype: Instancier instance
        '''
        logger.info("Build in memory instance")

        self._extract_vodml_block()
        self._validate_vodml_block()
        self._build_instance()
        self._populate_instance(resolve_refs=resolve_refs)
        return self._instancier


    
