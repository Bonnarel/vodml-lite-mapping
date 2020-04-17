#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from lxml import etree

from mappingfactory.transform import  MappingGenerator
from mapping_factory.launchers import data_dir
            
def main():
    mapping_generator = MappingGenerator()
    mapping_generator.parse_vodml_file(
        filename=(data_dir + "/models/cab_msd.vo-dml.xml"),
        model='cab_msd')
    mapping_generator.resolve_inheritance();
    mapping_generator.resolve_constaints();
    #root_object_id = 'cube:DataProduct'
    mapping_generator.root_object_id = 'cab_msd:Source'
    
    mapping_generator.concrete_classes = { 
                                         "cab_msd:Source.associatedData": ["cab_msd:WebEndpoint"
                                                                 , "cab_msd:VOModelInstance"
                                                                 #, "cab_sdm:cabsdmInstance" stack overflow
                                                                 ],
                                         
                                         "cab_msd:Source.parameter": ["meas:GenericMeasure"],
                                         
                                         #"cube:MeasurementAxis.measure": ["ts:PhotometricMeasure", "meas:StdTimeMeasure"]
                                         # , "ts:PhotometricCoord": ["ts:Magnitude", "meas:Time"]
                                          }

    
 
    #mapping_generator.concrete_classes = {}
    #mapping_generator.concrete_types={}
    mapping_generator.generate_mapping()
    
    for ac in mapping_generator.mapped_abstract_classes :
        print("Abstract class mapped " + ac)
        for sc in mapping_generator.get_sub_classes(ac):
            abstract = ""
            if  mapping_generator.object_types[sc].abstract == True:
                abstract = "Abstract "
            print("   " + abstract + sc)
            if abstract != "":
                for sc2 in mapping_generator.get_sub_classes(sc):
                    print("       " + sc2)
               
    for ac in mapping_generator.mapped_abstract_types :
        print("Abstract type mapped " + ac)
        for sc in mapping_generator.get_sub_types(ac):
            print("   " + sc)
    #parse_vodml_file(filename="/home/michel/workspace/vo-datamodels/provenance/vo-dml/xml/ProvenanceDM.vo-dml.xml", model='provenance')
    #root_object_id = 'provenance:provenance.Entity'
    #print(root_object_id)
    #generate_mapping()

    root = etree.fromstring(mapping_generator.xml_string + "\n")
    print((etree.tostring(root, pretty_print=True)).decode("utf-8") )
if __name__ == "__main__":
    main()   
    sys.exit()   
        
    