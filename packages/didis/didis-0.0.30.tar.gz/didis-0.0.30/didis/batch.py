#!/usr/bin/python3

# DIDIS - Desy ITk Database Interaction Script -- DESY's very own framework for interacting with the ITk Production Database
# Based on itkdb: https://gitlab.cern.ch/atlas-itk/sw/db/itkdb
# Created: 2021/11/17, Updated: 2022/02/15
# Written by Maximilian Felix Caspar, DESY HH

from loguru import logger
import argh
import json
import six
import os
import docx2pdf
import collections

import datetime as dt
import pandas as pd
import didis.didis as dd
from docxtpl import DocxTemplate


def register(excelFile: "Excel file containing the component data",
             componentType: "Type of component" = "THERMALFOAMSET",
             project: "ATLAS Project" = "S",
             subProject: "ATLAS Subproject" = "SE",
             institution: "Institute doing the registration" = "DESYHH",
             subType: "Component Subtype" = "THERMALFOAMSET_PETAL",
             lambdaFunction: "Function that modifies the df (takes the df as argument, returns the modified df)" = None,
             sheetName: "Name or number of the excel sheet to process" = 0
             ):
    "Registering components from an excel file."
    if isinstance(excelFile, str):
        df = pd.read_excel(excelFile, header=1, sheet_name=sheetName)
    elif isinstance(excelFile, pd.DataFrame):
        df = excelFile
    else:
        print('Your excelFile was of bad type: ', type(excelFile))
    print(df)
    # If a transformation Function is given, this will be used
    if lambdaFunction is not None:
        df = lambdaFunction(df)
        logger.info("Modified the dataframe")
        assert isinstance(df, pd.DataFrame)
        print(df)
    # Loop over the rows
    for i, r in df.iterrows():
        JSON = {}
        JSON['institution'] = institution
        JSON['componentType'] = componentType
        JSON['project'] = project
        JSON['subproject'] = subProject
        JSON['type'] = subType

        Properties = {}
        Batches = {}
        # Loop over the columns in the row
        for i, k in enumerate(r.keys()):
            if k == "serialNumber":
                JSON["serialNumber"] = r[k]
            elif k == "alternativeIdentifier":
                JSON["alternativeIdentifier"] = r[k]
                JSON["serialNumber"] = None
            elif k.startswith("B_"):
                Batches[k[2:]] = r[k]
            else:
                Properties[k] = r[k]
        JSON['properties'] = Properties
        if Batches != {}:
            JSON["batches"] = Batches
        dd.register(JSON)


@argh.arg('-v', '--value', nargs='+', type=str)
def ship(value: "Values to look up (can be a list)" = None,
         project: "ATLAS Project" = 'S',
         subProject: "ATLAS Subproject" = "SE",
         lookupKey: "Key that corresponds to VALUE" = 'serialNumber',
         componentType: "Type of component" = 'BT',
         name: "Name of the shipment." = "DESY Bus Tape Shipment",
         sender: "Sender of the shipment" = "DESYHH",
         recipient: "Recipient of the shipment" = "AVS",
         trackingNumber: "Tracking number" = None,
         shippingService: "Shipping service" = None,
         shippmentType: "Shipment Type (domestic | intraContinental | continental)" = "intraContinental",
         status: "Current status of the shipment" = "prepared",
         comments: "Comments" = None,
         cocTemplate: "Template DOCX for the certificate of conformity" = "templates/CoCTemplate.docx",
         slTemplate: "Template DOCX for the shipping slip" = "templates/SLTemplate.docx",
         configFile: "Config File for the pdf generation" = "pdfconfig.json",
         currentStage: "Current stage of the component to ship" = None,
         dryRun: "Dry Run without creating a shipment in DB" = True,
         path: "Output path for the shipping papers" = ".",
         generatePDFs: "Generate PDFs from the docx files (requires Windows + a Word installation)" = False
         ):
    "Ship items to another institution and generate packaging slips."

    print('Starting to prepare ~~~')

    def getProperty(component, property):
        "Helper function to get an arbitrary property from a DB object."
        print(component, property)
        properties = component["properties"]
        for p in properties:
            if p["code"] == property:
                return p["value"]
        return '-'

    def getDate(component):
        "Helper function to get the manufacturing date from a DB object."
        return getProperty(component, "MANUFACTURING_DATE")

    print(value)

    if value is None:
        value = []
    if isinstance(value, six.string_types):
        # Using six to get the correct string type regardless of the python version
        value = [value]

    # Get components from DB
    components = dd.lookup(project=project,
                           subProject=subProject,
                           lookupKey=lookupKey,
                           value=value,
                           componentType=componentType,
                           returnResults=True)

    codes = [components[key]["code"] for key in value]

    # Load jinja templates
    cocTemplate = DocxTemplate(cocTemplate)
    slTemplate = DocxTemplate(slTemplate)

    # Load config file with
    config = json.load(open(configFile, 'r'))[componentType]

    # Initialize jinja context
    context = {"shipping_items_coc": [{"serial": c["serialNumber"], "date": getDate(c), "posnr": i+1, "comment": "-/-", "cols": []} for i, c in enumerate(components.values())],
               "col_labels_coc": [c["HEADER"] for c in config["TEST_DATA_COC"].values()] + [c["HEADER"] for c in config["PROPERTIES_COC"].values()],
               "shipping_items_sl": [{"serial": c["serialNumber"], "date": getDate(c), "posnr": i+1, "comment": "-/-", "cols": []} for i, c in enumerate(components.values())],
               "col_labels_sl": [c["HEADER"] for c in config["TEST_DATA_SL"].values()],
               "location": config["DATA"]["LOCATION"],
               "responsible": config["DATA"]["RESPONSIBLE"],
               "part_description": config["DATA"]["DESCRIPTION"],
               "drawing_number": config["DATA"]["DRAWING_NUMBER"],
               "part_name": config["DATA"]["NAME"],
               "date": dt.date.today().strftime("%d.%m.%Y")}

    # Fill context for both templates
    logger.info("Getting test data from the database")
    for index, c in enumerate(codes):
        # Getting test runs for component
        tests = dd.testruns(c, returnResults=True)
        # Filter only test results for current stage (if user requires it)
        tests = {t: tests[t] for t in tests if (
            currentStage is None or tests[t]["stage"]["code"] == currentStage)}
        testCodes = [tests[t]['testType']['code'] for t in tests]

        # Figure out if there are duplicates
        if len(set(testCodes)) < len(testCodes):
            duplicateTests = [item for item, count in collections.Counter(
                testCodes).items() if count > 1]
            logger.warning("Found duplicate tests," +
                           str(duplicateTests) + ", using latest instances")
            for duplicateTest in duplicateTests:
                # Remove duplicate tests from the dict
                dtKeys = [t for t in tests if tests[t]
                          ["testType"]["code"] == duplicateTest]
                testDates = [tests[t]["date"] for t in dtKeys]
                # Select latest instance
                latestIndex = testDates.index(max(testDates))
                for i in range(len(dtKeys)):
                    if i != latestIndex:
                        del tests[dtKeys[i]]
            # Update test codes
            testCodes = [tests[t]['testType']['code'] for t in tests]

        # COC loop
        for requiredTest in config["TEST_DATA_COC"]:
            found = False
            for t, c in zip(tests.keys(), testCodes):
                if c == requiredTest:
                    dbTest = dd.testresult(t)
                    if "FIELD" in config["TEST_DATA_COC"][c]:
                        # If it has a field set, get it from the result
                        for r in dbTest["results"]:
                            if config["TEST_DATA_COC"][c]["FIELD"] == r["code"]:
                                value = r["value"]
                                if isinstance(value, list) and len(value) == 1:
                                    value = value[0]
                                if isinstance(value, float):
                                    if value < 1e-2:
                                        value = "{:.02e}".format(value)
                                    else:
                                        value = "{:.02f}".format(value)
                                context["shipping_items_coc"][index]["cols"].append(
                                    value)
                                found = True
                    else:
                        # Find out whether test has passed
                        passed = dbTest["passed"]
                        problems = dbTest["problems"]
                        remark = " with remarks" if problems else ""
                        if passed:
                            context["shipping_items_coc"][index]["cols"].append(
                                "Passed" + remark)
                            found = True
                        else:
                            context["shipping_items_coc"][index]["cols"].append(
                                "Failed" + remark)
                            found = True
            if not found:
                # Test was not found in DB
                context["shipping_items_coc"][index]["cols"].append("N/A")

        # CoC property loop
        for property in config["PROPERTIES_COC"]:
            component = list(components.values())[index]
            value = getProperty(
                component, config["PROPERTIES_COC"][property]["FIELD"])
            context["shipping_items_coc"][index]["cols"].append(value)

        # SL loop
        for requiredTest in config["TEST_DATA_SL"]:
            found = False
            for t, c in zip(tests.keys(), testCodes):
                if c == requiredTest:
                    dbTest = dd.testresult(t)
                    if "FIELD" in config["TEST_DATA_SL"][c]:
                        # If it has a field set, get it from the result
                        for r in dbTest["results"]:
                            if config["TEST_DATA_SL"][c]["FIELD"] == r["code"]:
                                value = r["value"]
                                context["shipping_items_sl"][index]["cols"].append(
                                    value)
                                found = True
                    else:
                        # Find out whether test has passed
                        passed = dbTest["passed"]
                        problems = dbTest["problems"]
                        remark = " with remarks" if problems else ""
                        if passed:
                            context["shipping_items_sl"][index]["cols"].append(
                                "Passed" + remark)
                            found = True
                        else:
                            context["shipping_items_sl"][index]["cols"].append(
                                "Failed" + remark)
                            found = True
            if not found:
                # Test was not found in DB
                context["shipping_items_sl"][index]["cols"].append("N/A")

    renderTimestamp = dt.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")

    logger.info("Rendering templates")
    # Render context to the docx templates
    cocTemplate.render(context)
    cocTemplate.save(os.path.join(path, f"{renderTimestamp}_COC.docx"))
    slTemplate.render(context)
    slTemplate.save(os.path.join(path, f"{renderTimestamp}_SL.docx"))

    # Generate pdfs
    if generatePDFs:
        docx2pdf.convert(os.path.join(path, f"{renderTimestamp}_COC.docx"))
        docx2pdf.convert(os.path.join(path, f"{renderTimestamp}_SL.docx"))

    # Create shipment in the DB
    if not dryRun:
        dd.ship(codes, name=name, sender=sender, recipient=recipient, trackingNumber=trackingNumber,
                shippingService=shippingService, type=shippmentType, status=status, comments=comments)
    else:
        # Generate python command for shipment creation
        logger.info("Create the shipment using:")
        print(f"dd.ship({codes}, name={name}, sender={sender}, recipient={recipient}, trackingNumber={trackingNumber}, shippingService={shippingService}, type={shippmentType}, status={status}, comments={comments})")


def main():
    parser = argh.ArghParser()
    parser.add_commands([register, ship])
    parser.dispatch()


if __name__ == '__main__':
    main()
