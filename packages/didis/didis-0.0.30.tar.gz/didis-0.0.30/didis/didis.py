#!/usr/bin/python3

# DIDIS - Desy ITk Database Interaction Script -- DESY's very own framework for interacting with the ITk Production Database
# Based on itkdb: https://gitlab.cern.ch/atlas-itk/sw/db/itkdb
# Created: 2021/11/17, Updated: 2022/01/24
# Written by Maximilian Felix Caspar, DESY HH

import sys

import didis.didis as dd
import didis.batch as ddb

from loguru import logger
import argh
import os
import json
import itkdb
import mimetypes
import six


def authenticate():
    "Check the DB login for this session."
    try:
        # Get the Pixel project contents to show that there is a connection
        client = itkdb.Client()
        client.get('listComponents', json={
            'project': 'P', 'pageInfo': {'pageSize': 32}})
        logger.info("Authentification successful")
    except itkdb.exceptions.ResponseException as e:
        logger.error(e)
        logger.error("Wrong or missing login credentials")
        logger.info(
            "Set environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2")
    except Exception as e:
        logger.error(e)


@argh.arg('-v', '--value', nargs='+', type=str)
def lookup(project: "ATLAS Project" = 'S',
           subProject: "ATLAS Subproject" = "SE",
           lookupKey: "Key that corresponds to VALUE" = 'serialNumber',
           value: "Values to look up (can be a list)" = None,
           componentType: "Type of component" = 'BT',
           returnResults: "Return lookup results (useful if not used from CLI)" = False,
           printJSON: "PrettyPrint the component JSON" = False):
    "Look up a component or list of components in the DB."

    try:
        if value is None:
            value = []
        if isinstance(value, six.string_types):
            # Using six to get the correct string type regardless of the python version
            value = [value]
        client = itkdb.Client()
        components = client.get('listComponents', json={
                                'project': project, "componentType": componentType, "subproject": subProject})
        results = {}
        logger.info(f"Looking up {lookupKey} = {value}")
        for i, comp in enumerate(components):
            if value != []:
                # If no input is given, show all components of this type
                if comp[lookupKey] in value:
                    logger.info(
                        f"Found {lookupKey} = {comp[lookupKey]}: {comp['code']}")
                    results[comp[lookupKey]] = comp
            else:
                # Search for the ones that fit the criteria
                logger.info(f"Found {lookupKey} = {comp[lookupKey]}: {comp['code']}")
                results[str(comp[lookupKey])] = comp
        if printJSON:
            for k in results:
                print(json.dumps(results[k], indent=1))
        if returnResults or __name__ != '__main__':
            return results
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")

def lookup_component(componentID: "Component identifier or ATLAS serial number",
                    componentType: "Component Type only needed if ID is serialNumber" = '',
                    returnResults: "Return lookup results (useful if not used from CLI)" = False,
                    printJSON: "PrettyPrint the component JSON" = False):
    """ Lookup full information from database """

    if componentID.startswith('20US'): # e.g. '20USECL9000023' and not '6f40312bc3204c2bd037741d7ac48a18'
            dCL = dd.lookup(value=[componentID], componentType=componentType)
            # print(json.dumps(dCL, indent=1))
            componentID = dCL[list(dCL.keys())[0]]['code']
    try:
        logger.info(f"Getting slots for component {componentID}")
        client = itkdb.Client()
        result = client.get('getComponent', json={'component': componentID})
        if printJSON:
            print(json.dumps(result, indent=1))
        if returnResults or __name__ != '__main__':
            return result
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")

def attach(file: "Path of the file to upload",
           component: "Component code or ATLAS SN",
           title: "Title of the file" = "",
           description: "A file description" = "",
           filetype: "File MIME type (sript can usually guess this)" = None,
           supressURL: "Sometimes the upload only works without url" = False,
           eos: "Use eos instead of uploading to DB" = False):
    "Attach a file to a component in the DB."
    try:
        if not eos:
            client = itkdb.Client(use_eos=eos )
            if filetype is None:
                # If you can't be bothered to look up the MIME type,
                # we'll look it up for you :)
                filetype = mimetypes.guess_type(file)
            data = {
                'component': component,
                'title': title,
                'description': description,
                'type': 'file',
                'url': file,
            }
            # Sometimes the upload only works without url
            if supressURL: data.pop('url', None)
            # Get attachment data
            attachment = {'data': (os.path.basename(
                file), open(file, 'rb'), filetype)}

            client.post('createComponentAttachment',
                        data=data, files=attachment)
        else:
            client = itkdb.Client(use_eos=eos)
            data = {
                "component": component,
                "title": title,
                "description": description,
                "url": file,
                "type": "file",
                "filename" : os.path.basename(file)
            }
            with open(file, "rb") as fpointer:
                files = {"data": itkdb.utils.get_file_components({"data": fpointer})}
                response = client.post("createComponentAttachment", data=data, files=files)

        logger.info(f"Attached file {file} to {component}")
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def register(component: "Component to register (path to .json file or dict)"):
    "Register a new component"
    if isinstance(component, str) and os.path.isfile(component):
        logger.info(f"Loading component definition from file {component}")
        with open(component) as jsonFile:
            component = json.load(jsonFile)
            jsonFile.close()
    elif isinstance(component, dict):
        logger.info("Component definition was passed as a dict")
    else:
        logger.error(f"Unrecognised input {component}")
        return
    try:
        client = itkdb.Client()
        client.post('registerComponent', json=component)
        logger.info(f"Registered new component")
    except Exception as e:
        logger.error(e)
        logger.error(
            f"Unable to register component in the DB, is the format correct?")


def tests(componentType: "Type of component" = "BT",
          project: "ATLAS Subproject" = 'S',
          returnResults: "Return available tests (useful if not used from CLI)" = False):
    "Get a list of available tests for a component."
    logger.info(f"Polling for test types for {componentType}")
    try:
        client = itkdb.Client()
        out = client.get("listTestTypes", json={
            'project': project, "componentType": componentType})
        logger.info("Test type and required results:")
        result = {}
        for i, test in enumerate(out):
            result[test['code']] = test
            if not returnResults:
                print(test['code'], ":", test['name'])
                for p in test['parameters']:
                    print("  ", p['code'], ":", p['name'])
        if returnResults or __name__ != '__main__':
            return result
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def get_stage(lookupValue: "Value to look up (must be unique in the DB!)",
              project: "ATLAS Subproject" = 'S',
              lookupKey: "Key that corresponds to VALUE" = 'serialNumber',
              componentType: "Type of component" = 'BT'):
    "Look up production stage for a component."
    from loguru import logger
    logger.info(f"Getting component from the DB")
    component = dd.lookup(project=project, lookupKey=lookupKey, value=[
        lookupValue], componentType=componentType, returnResults=True)
    if len(component) == 0:
        logger.error(
            "No components that match the criteria were found in the DB")
        raise LookupError
    elif len(component) > 1:
        logger.error(
            "More than 1 component that match the criteria was found")
        raise LookupError
    component = component[lookupValue]
    return component['currentStage']['code']


def set_stage(lookupValue: "Value to look up (must be unique in the DB!)",
              stage: "Production stage to set",
              project: "ATLAS Project" = 'S',
              subProject: "ATLAS Subproject" = "SE",
              lookupKey: "Key that corresponds to VALUE" = 'serialNumber',
              componentType: "Type of component" = 'BT',
              comment: "Reason for production stage change" = ""):
    'Set production stage for a component. Ex: didis stage "20USECP9000050" "" componentType="COOLING_PIPE"????'
    logger.info(f"Getting component from the DB")
    component = lookup(project=project, subProject=subProject, lookupKey=lookupKey, value=[
                       lookupValue], componentType=componentType, returnResults=True)
    if len(component) == 0:
        logger.error(
            "No components that match the criteria were found in the DB")
        raise LookupError
    elif len(component) > 1:
        logger.error(
            "More than 1 component that match the criteria was found")
        raise LookupError
    component = component[lookupValue]
    if stage == "":
        logger.info(
            f"Current production stage: {component['currentStage']['code']}")
        if __name__ != '__main__':
            return component['currentStage']['code']
        else:
            return
    client = itkdb.Client()
    data = {
        'component': component['code'],
        'stage': stage,
    }
    if comment != "":
        data['comment'] = comment
    try:
        client.post('setComponentStage', data=data)
        logger.info(f"Set stage to {stage}")
    except Exception as e:
        logger.error(e)
        logger.error(
            f"DB error, is {stage} a valid stage for {componentType}?")


def stage(*args, **kwargs):
    return set_stage(*args, **kwargs)

def get_type_stages(componentType: "Type of component" = 'BT',
                    project: "ATLAS Project" = 'S',
                    subProject: "ATLAS Subproject" = "SE"):
    """ Get all available stages for a component type
        Args:
            componentType (Type of component, optional): _description_. Defaults to 'BT'.
        Returns:
            stages: list of stages of this component type
    """
    client = itkdb.Client()
    component_type = client.get('getComponentTypeByCode', json={'project': project, 'code': componentType})
    stages = [stage['code'] for stage in component_type['stages']]

    return stages

def skeleton(test: "Type of test",
             componentType: "Type of component" = "BT",
             project: "ATLAS Project" = 'S',
             returnResults: "Return available tests (useful if not used from CLI)" = False):
    "Genereate a test skeleton for a given test. Otput is either as JSON to the CLI or as a dict as a return value."
    allTests = tests(componentType=componentType,
                     project=project, returnResults=True)
    if not test in allTests:
        logger.error(f"Unable to find {test} for {componentType}")
    skeleton = {
        'runNumber': '0-0',
        'component': None,
        'results':
        {
        },
        'properties':
        {
        },
        'passed': False,
        'problems': False,
        'testType': test,
        'institution': None
    }

    for v in allTests[test]["properties"]:
        skeleton["properties"][v["code"]] = None
    for v in allTests[test]["parameters"]:
        skeleton["results"][v["code"]] = None

    if returnResults or __name__ != '__main__':
        return skeleton
    else:
        print(json.dumps(allTests[test], indent=1))


def upload(result: "Results from the test (path to .json file or dict)"):
    "Upload a test result to the DB."
    if isinstance(result, str) and os.path.isfile(result):
        logger.info(f"Loading test result from file {result}")
        with open(result) as jsonFile:
            result = json.load(jsonFile)
            jsonFile.close()
    elif isinstance(result, dict):
        logger.info("Test result was passed as a dict")
    else:
        logger.error(f"Unrecognised input {result}")
        return success
    try:
        client = itkdb.Client()
        client.post('uploadTestRunResults', json=result)
        logger.info(
            f"Uploaded {result['testType']} results for {result['component']} to the DB")
        success = True
    except Exception as e:
        logger.error(e)
        logger.error(f"Unable to upload result to DB, is the format correct?")
        success = False

    return success


def testruns(cid: "Component ID",
             returnResults: "Return lookup results (useful if not used from CLI)" = False,
             printJSON: "PrettyPrint the component JSON" = False):
    "Look up all test results associated with a component ID."
    try:
        logger.info(f"Looking up tests in CID = {cid}")
        client = itkdb.Client()
        runs = client.get('listTestRunsByComponent', json={'component': cid})
        results = {}
        for i, testres in enumerate(runs):
            logger.info(
                f"Found {testres['testType']['name']} with ID = {testres['id']}")
            results[testres['id']] = testres
        if printJSON:
            for k in results:
                print(json.dumps(results[k], indent=1))
        if returnResults or __name__ != '__main__':
            return results
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def testfile(file: "Path of the file to upload",
             testrun: "Test run code",
             title: "Title of the file" = "",
             description: "A file description" = "",
             filetype: "File MIME type (script can usually guess this)" = None,
             supressURL: "Sometimes the upload only works without url" = False,
             eos: "Use eos instead of uploading to DB" = False):
    "Attach a file to a testrun in the DB."
    try:
        client = itkdb.Client(use_eos=eos )
        if filetype is None:
            # If you can't be bothered to look up the MIME type,
            # we'll look it up for you :)
            filetype = mimetypes.guess_type(file)
        data = {
            'testRun': testrun,
            'title': title,
            'description': description,
            'type': 'file',
            'url': file,
        }
        # Sometimes the upload only works without url
        if supressURL: data.pop('url', None)
        # Get attachment data
        attachment = {'data': (os.path.basename(
            file), open(file, 'rb'), filetype)}

        client.post('createTestRunAttachment',
                    data=data, files=attachment)
        logger.info(f"Attached file {file} to {testrun}")
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def assemble(parent:     "Parent component identifier (ATLAS SN or alternative ID)",
             child:      "Child component identifier (ATLAS SN or alternative ID)",
             parentAID:  "Parent identifier is an alternative ID" = False,
             childAID:   "Child identifier is an alternative ID" = False,
             slot:       "Target component slot id" = None,
             properties: "Properties collection (dict or .json file)" = None):
    "Assemble a component"
    if isinstance(properties, str) and os.path.isfile(properties):
        logger.info(f"Loading properties from file {properties}")
        with open(properties) as jsonFile:
            properties = json.load(jsonFile)
            jsonFile.close()
    elif isinstance(properties, dict):
        logger.info("Properties where passed as a dict")
    elif properties is None:
        logger.info("No properties given")
    else:
        logger.error(f"Unrecognised input {properties}")
        return
    try:
        data = {
            "parent": parent,
            "child": child,
            "alternativeIdentifierParent": parentAID,
            "alternativeIdentifierChild": childAID,
            "properties": properties
        }
        if slot is not None:
            data["slot"] = slot
        client = itkdb.Client()
        client.post('assembleComponent', json=data)
        logger.info(f"Assembled components {parent} and {child}")
    except Exception as e:
        logger.error(e)
        logger.error(
            f"Unable to assemble component in the DB, is the format correct?")


def property(componentID: "Component identifier or ATLAS serial number",
             property: "Property code",
             value: "Target value "):
    "Change a component property"
    try:
        client = itkdb.Client()
        data = {
            'component': componentID,
            'code': property,
            'value': value
        }

        client.post('setComponentProperty', data=data)
        logger.info(f"Changed property {property} of {componentID} to {value}")
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def comment(identifier: "ID for the comment to be attached to (can be a ATLAS serial number in case of a component)",
            comment: "Comment to attach (can also be an array)",
            isTest: "If you want to attach to test instead of component" = False):
    "Attach a comment to a component or test"
    try:
        if isinstance(comment, str):
            comment = [comment]
        assert isinstance(comment, list)

        # Workaround for a very annoying bug in the db
        if len(comment) == 1:
            comment += [""]

        if isTest:
            data = {
                "testRun": identifier,
                "comments": comment
            }
            client = itkdb.Client()
            client.post('createTestRunComment', data=data)
        else:
            data = {
                "component": identifier,
                "comments": comment
            }
            client = itkdb.Client()
            client.post('createComponentComment', data=data)

        logger.info(f"Attached comment(s) to {identifier}")
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def ship(components: "Component codes",
         name: "Name of the shipment" = "DESY Shipment",
         sender: "Sender of the shipment" = "DESYHH",
         recipient: "Recipient of the shipment" = "AVS",
         trackingNumber: "Tracking number" = None,
         shippingService: "Shipping service" = None,
         type: "Shipment Type (domestic | intraContinental | continental)" = "intraContinental",
         status: "Current status of the shipment" = "prepared",
         comments: "Comments" = None):
    """Ship components to another institute."""
    try:
        client = itkdb.Client()
        if isinstance(components, str):
            components = [components]
        assert isinstance(components, list)

        data = {
            "sender": sender,
            "name": name,
            "recipient": recipient,
            "type": type,
            "shipmentItems": components}

        if trackingNumber is not None:
            data["trackingNumber"] = trackingNumber
        if shippingService is not None:
            data["shippingService"] = shippingService
        if comments is not None:
            data["comments"] = comments

        print(data)

        client.post('createShipment', data=data)

        logger.info(f"Shipped {components} to {recipient}")
    except Exception as e:
        logger.error(e)
        if len(components) == 1:
            logger.info(
                "This is probably a DB bug, check if your shipment was created using the web interface.")
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def testresult(tid: "Test ID",
               returnResults: "Return lookup results (useful if not used from CLI)" = False,
               printJSON: "PrettyPrint the component JSON" = False):
    "Look up a test result for a given test ID."
    try:
        logger.info(f"Looking up tests TID = {tid}")
        client = itkdb.Client()
        result = client.get('getTestRun', json={'testRun': tid})
        if printJSON:
            print(json.dumps(result, indent=1))
        if returnResults or __name__ != '__main__':
            return result
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")

def get_slots(componentID: "Component identifier or ATLAS serial number",
              returnResults: "Return lookup results (useful if not used from CLI)" = False):
    """Get child component slots."""
    try:
        logger.info(f"Getting slots for component {componentID}")
        client = itkdb.Client()
        result = client.get('getComponent', json={'component': componentID})
        children = result["children"]
        logger.info(f"Found {len(children)} child component slots")
        for i, c in enumerate(children):
            type = c["type"]["code"]
            id = c["id"]
            logger.info(f"Slot {i}: {type} in {id}")
        if returnResults or __name__ != '__main__':
            return children
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")

def find_family( componentID: "Component identifier or ATLAS serial number",
                  componentType: "Component Type only needed if ID is serialNumber" = '',
                  returnResults: "Return lookup results (useful if not used from CLI)" = False,
                  printLogger: "Print some debugging info, if needed" = False,
                  printJSON: "PrettyPrint the component JSON" = False,
                  onlyChildren: "Return a dict with only children" = False,
                  onlyParents:  "Return a dict with only parents" = False):
    """Find component family.

        Returns:
            { 'parents':{id:{'type' : ...,
                             'serialNumber': ...,
                             'alternativeIdentifier': ...}
              'children': {id:{'type' : ...,
                               'serialNumber': ...,
                               'alternativeIdentifier': ...}}    
    """

    if componentID.startswith('20US'): # e.g. '20USECL9000023' and not '6f40312bc3204c2bd037741d7ac48a18'
        dCL = dd.lookup(value=[componentID], componentType=componentType)
        componentID = dCL[list(dCL.keys())[0]]['code']

    try:
        if printLogger: logger.info(f"Getting slots for component {componentID}")
        client = itkdb.Client()
        result = client.get('getComponent', json={'component': componentID})
        
        dic_family = {'parents':{},'children':{}}
        if onlyChildren: dic_family = {'children':{}}
        if onlyParents:  dic_family = {'parents':{}}

        for relative in dic_family.keys():
            d_relative = result[ relative ]
            try:
                if printLogger: logger.info(f"Found {len(d_relative)} {relative} component slots")
                for i, fam_member in enumerate(d_relative):
                    id       = fam_member["id"]
                    if isinstance(fam_member["type"], dict):
                        type = fam_member["type"]["code"]
                    else:
                        type = fam_member["componentType"]["code"]
                    if printLogger: logger.info(f"Slot {i}: {type} in {id}")
                    if isinstance(fam_member['component'], dict):
                        dic_family[relative].update({id:{
                                            'type' : type,
                                            'serialNumber': fam_member['component']['serialNumber'],
                                            'alternativeIdentifier': fam_member['component']['alternativeIdentifier'] }})
                    else:
                        dic_family[relative].update({id: None})
            except:
                logger.info(f"Found {d_relative} {relative} component slots")
                dic_family.update( {relative: {}} )
            if onlyChildren or onlyParents:
                dic_family = dic_family[relative]
        if printJSON:
            print(json.dumps(dic_family, indent=1))
        if returnResults or __name__ != '__main__':
            return dic_family
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")
    # return dic_family

def find_children(componentID: "Component identifier or ATLAS serial number",
                  componentType: "Component Type only needed if ID is serialNumber" = '',
                  returnResults: "Return lookup results (useful if not used from CLI)" = False,
                  printJSON: "PrettyPrint the component JSON" = False):
    """Find component children."""
    # can be deprecated and replaced by find_family
    if componentID.startswith('20US'): # e.g. '20USECL9000023' and not '6f40312bc3204c2bd037741d7ac48a18'
            dCL = dd.lookup(value=[componentID], componentType=componentType)
            # print(json.dumps(dCL, indent=1))
            componentID = dCL[list(dCL.keys())[0]]['code']

    try:
        logger.info(f"Getting slots for component {componentID}")
        client = itkdb.Client()
        result = client.get('getComponent', json={'component': componentID})
        children = result["children"]
        dic_children = {}
        logger.info(f"Found {len(children)} child component slots")
        for i, child in enumerate(children):
            type = child["type"]["code"]
            id = child["id"]
            logger.info(f"Slot {i}: {type} in {id}")
            if isinstance(child['component'], dict):
                dic_children.update({id:{'type' : type,
                                    'serialNumber':child['component']['serialNumber'],
                                    'alternativeIdentifier': child['component']['alternativeIdentifier'] }})
            else:
                dic_children.update({id: None})
        if printJSON:
            print(json.dumps(dic_children, indent=1))
        if returnResults or __name__ != '__main__':
            return dic_children
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")

    return dic_children

def get_slots(componentID: "Component identifier or ATLAS serial number",
              returnResults: "Return lookup results (useful if not used from CLI)" = False):
    """Get child component slots."""
    try:
        logger.info(f"Getting slots for component {componentID}")
        client = itkdb.Client()
        result = client.get('getComponent', json={'component': componentID})
        children = result["children"]
        logger.info(f"Found {len(children)} child component slots")
        for i, c in enumerate(children):
            type = c["type"]["code"]
            id = c["id"]
            logger.info(f"Slot {i}: {type} in {id}")
        if returnResults or __name__ != '__main__':
            return children
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def main():
    parser = argh.ArghParser()
    parser.add_commands([authenticate, register, lookup,
                        attach, tests, get_stage, set_stage,
                        skeleton, upload, testruns,
                        testfile, assemble, property,
                        comment, ship, testresult, get_slots])
    parser.dispatch()


if __name__ == '__main__':
    main()
