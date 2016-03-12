from multiprocessing import Process
from xml.dom import minidom
import wget
import os
from dbSchema import drop_cpe_collection, db_insert
from dbSchema import db_insert_bulk, get_cpes_count
import zipfile
import glob

cpe_latest_zip = 'http://static.nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip'

def extract_cpe_zip(cpe_latest_xml_zip):
    with zipfile.ZipFile(cpe_latest_xml_zip, "r") as z:
        z.extractall(".")

# Remove downloaded filesand temporary files
def cleanup():
    for current in glob.glob(os.path.join('.', '*.xml')):
        os.remove(current)
    for current in glob.glob(os.path.join('.', '*.zip')):
        os.remove(current)
    for current in glob.glob(os.path.join('.', '*.tmp')):
        os.remove(current)

def update_cpe_db():
    drop_cpe_collection()
    get_cpe_data(download_cpe_xml_zip(cpe_latest_zip))
    cleanup()

# Download CPE Update definitions
def download_cpe_xml_zip(cpe_latest_url):
    # Cleanup before downloads
    cleanup()
    cpe_latest_xml_zip = wget.download(cpe_latest_url, bar=wget.bar_adaptive)
    extract_cpe_zip(cpe_latest_xml_zip)
    cpe_latest_xml = "official-cpe-dictionary_v2.3.xml"
    return cpe_latest_xml

def make_post(cpe_uri_string):
    row = {}
    cpe_string = cpe_uri_string
    cpe_string_components = cpe_string.split(":")
    row['cpe_full_uri'] = cpe_string
    row['cpe_uri_begin'] = cpe_string_components[0]
    row['cpe_schema'] = cpe_string_components[1]
    row['cpe_part'] = cpe_string_components[2]
    row['cpe_vendor'] = cpe_string_components[3]
    row['cpe_product'] = cpe_string_components[4]
    row['cpe_version'] = cpe_string_components[5]
    row['cpe_update'] = cpe_string_components[6]
    row['cpe_edition'] = cpe_string_components[7]
    row['cpe_language'] = cpe_string_components[8]
    row['cpe_sw_edition'] = cpe_string_components[9]
    row['cpe_target_sw'] = cpe_string_components[10]
    row['cpe_target_hw'] = cpe_string_components[11]
    row['cpe_other'] = cpe_string_components[12]
    return row

# Read XML and add records into database
def get_cpe_data(cpe_latest_xml):
    print("[+] Extracting")
    xmldoc = minidom.parse(cpe_latest_xml)
    cpe_2_3_items = xmldoc.getElementsByTagName('cpe-23:cpe23-item')
    print("[+] Extraction done!")
    cpe_items_to_db = list()
    for cpe_2_3_item in cpe_2_3_items:
        # Temporay holder before bulk inserts
        cpe_items_to_db.append(make_post(cpe_2_3_item.attributes['name'].value))
    # Bulk Insert Call
    records = db_insert_bulk(cpe_items_to_db)
    # Uncomment the below to print mongo document ids
    # print(records)

if __name__ == "__main__":
    update_cpe_db()
