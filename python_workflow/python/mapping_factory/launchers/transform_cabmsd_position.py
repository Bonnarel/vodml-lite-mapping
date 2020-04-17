#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from lxml import etree

from mapping_factory.factory.transform import  MappingGenerator
from mapping_factory.launchers import data_dir

            
def main():
    mapping_generator = MappingGenerator()
    mapping_generator.parse_vodml_file(filename=(data_dir + "/models/cab_msd.vo-dml.xml"), 
                                       model='cab_msd')
    mapping_generator.resolve_inheritance();
    mapping_generator.resolve_constaints();
    #root_object_id = 'cube:DataProduct'
    mapping_generator.root_object_id = 'cab_msd:STCSphericalSkyPosition'
    
    mapping_generator.concrete_classes = {
        "coords:SpaceFrame.refPosition": ["coords:StdRefLocation"],
        "coords:Coordinate.coordSys": ["coords:SpaceSys"],
        "coords:PhysicalCoordSys.frame": ["coords:SpaceFrame"],
        "coords:PhysicalCoordSys.coordSpace": ["coords:SphericalCoordSpace"]
        }

    mapping_generator.concrete_types={
        "coords:Point.axis1": "ivoa:RealQuantity",
        "coords:Point.axis2": "ivoa:RealQuantity",
        "coords:Point.axis3": "ivoa:RealQuantity",
        "coords:ContinuousAxis.domainMin": "ivoa:RealQuantity",
        "coords:ContinuousAxis.domainMax": "ivoa:RealQuantity",
        "meas:Error.statError": "meas:Symmetrical",
        "meas:Error.sysError": "meas:Symmetrical",
        "coords:SpaceFrame.refPosition": "coords:StdRefLocation"
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
        
    