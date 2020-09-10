from __future__ import absolute_import
import os, pdb, requests, logging, time, json
import requests
from collections import OrderedDict, Mapping
from StringIO import StringIO
import unittest as test
from copy import deepcopy

from nistoar.testing import *
from nistoar.pdr.publish.midas3 import customize
from nistoar.pdr import exceptions as exc
from nistoar.pdr import utils
from nistoar.pdr.publish.midas3 import service as mdsvc
from nistoar.pdr.publish.midas3 import customize
from nistoar.pdr.preserv.bagit import builder as bldr
from nistoar.pdr.preserv.bagit.bag import NISTBag

testdir = os.path.dirname(os.path.abspath(__file__))
simsrvrsrc = os.path.join(testdir, "sim_cust_srv.py")
custport = 9091
custbaseurl = "http://localhost:{0}/draft/".format(custport)

datadir = os.path.join( os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                        "preserv", "data" )

loghdlr = None
rootlog = None
def setUpModule():
    global loghdlr
    global rootlog
    ensure_tmpdir()
#    logging.basicConfig(filename=os.path.join(tmpdir(),"test_builder.log"),
#                        level=logging.INFO)
    rootlog = logging.getLogger()
    loghdlr = logging.FileHandler(os.path.join(tmpdir(),"test_publishing.log"))
    loghdlr.setLevel(logging.DEBUG)
    loghdlr.setFormatter(logging.Formatter(bldr.DEF_BAGLOG_FORMAT))
    rootlog.addHandler(loghdlr)
    rootlog.setLevel(logging.DEBUG)

    svcarch = os.path.join(tmpdir(), "simcust")
    os.mkdir(svcarch)
    startService(svcarch)

def tearDownModule():
    global loghdlr
    if loghdlr:
        if rootlog:
            rootlog.removeHandler(loghdlr)
        loghdlr = None
    svcarch = os.path.join(tmpdir(), "simcust")
    stopService(svcarch)
    rmtmpdir()

def startService(archdir):
    srvport = custport
    tdir = os.path.dirname(archdir)
    pidfile = os.path.join(tdir,"simsrv"+str(srvport)+".pid")
    
    cmd = "uwsgi --daemonize {0} --plugin python --http-socket :{1} " \
          "--wsgi-file {2} --pidfile {3} --set-ph archive_dir={4} "   \
          "--set-ph auth_key=SECRET" 
    cmd = cmd.format(os.path.join(tdir,"simsrv.log"), srvport,
                     os.path.join(simsrvrsrc), pidfile, archdir)
    os.system(cmd)
    time.sleep(0.5)

def stopService(archdir):
    srvport = custport
    pidfile = os.path.join(os.path.dirname(archdir),"simsrv"+str(srvport)+".pid")
    cmd = "uwsgi --stop {0}".format(pidfile)
    os.system(cmd)
    time.sleep(1)

class TestMIDAS3PublishingServiceDraft(test.TestCase):

    testsip = os.path.join(datadir, "midassip")
    midasid = '3A1EE2F169DD3B8CE0531A570681DB5D1491'
    wrongid = '333333333333333333333333333333331491'
    arkid = "ark:/88434/mds2-1491"
    defcfg = {
        'customization_service': {
            'auth_key': 'SECRET',
            'service_endpoint': custbaseurl,
            'merge_convention': 'midas1',
            'updatable_properties': [ "title", "topic", "theme", "authors", "_editStatus" ]
        }
    }

    def setUp(self):
        self.tf = Tempfiles()
        self.workdir = self.tf.mkdir("publish")
        self.upldir = os.path.join(self.testsip, "upload")
        self.revdir = os.path.join(self.testsip, "review")
        self.nrddir = os.path.join(self.workdir, "nrdserv")
        self.svc = mdsvc.MIDAS3PublishingService(self.defcfg, self.workdir,
                                                 self.revdir, self.upldir)
        self.client = customize.CustomizationServiceClient(self.defcfg['customization_service'])

    def tearDown(self):
        self.svc.wait_for_all_workers(300)
        requests.delete(custbaseurl, headers={'Authorization': 'Bearer SECRET'})
        self.tf.clean()

    def test_ctor(self):
        self.assertTrue(os.path.isdir(self.svc.workdir))
        self.assertTrue(os.path.isdir(self.svc.mddir))
        self.assertTrue(os.path.isdir(self.svc.nrddir))
        self.assertTrue(os.path.isdir(self.svc.podqdir))
        self.assertTrue(os.path.isdir(self.svc.storedir))
        self.assertTrue(os.path.isdir(self.svc._schemadir))
        self.assertTrue(self.svc._custclient)

    def test_start_customization_for(self):
        podf = os.path.join(self.revdir, "1491", "_pod.json")
        pod = utils.read_json(podf)
        bagdir = os.path.join(self.svc.mddir, self.midasid)

        self.assertTrue(not self.client.draft_exists(self.midasid))
        self.svc.start_customization_for(pod)
        self.assertTrue(self.client.draft_exists(self.midasid))

        self.svc.end_customization_for(self.midasid)
        self.assertTrue(not self.client.draft_exists(self.midasid))

    def test_start_customization_for_emptypod(self):
        self.assertTrue(not self.client.draft_exists(self.midasid))
        with self.assertRaises(ValueError):
            self.svc.start_customization_for({})
        self.assertTrue(not self.client.draft_exists(self.midasid))

    def test_start_customization_for_minpod(self):
        bagdir = os.path.join(self.svc.mddir, self.midasid)
        pod = {"identifier": self.midasid}
        self.assertTrue(not self.client.draft_exists(self.midasid))
        
        self.svc.start_customization_for(pod)
        self.assertTrue(self.client.draft_exists(self.midasid))

        self.svc.end_customization_for(self.midasid)
        self.assertTrue(not self.client.draft_exists(self.midasid))

    def test_get_customized_pod(self):
        podf = os.path.join(self.revdir, "1491", "_pod.json")
        pod = utils.read_json(podf)
        bagdir = os.path.join(self.svc.mddir, self.midasid)
        bmddir = os.path.join(bagdir, "metadata")
        nerdf = os.path.join(bmddir, "nerdm.json")
        annotf = os.path.join(bmddir, "annot.json")
        self.assertTrue(not os.path.exists(nerdf))
        self.assertTrue(not os.path.exists(annotf))

        self.assertTrue(not self.client.draft_exists(self.midasid))
        self.svc.start_customization_for(pod)
        self.assertTrue(self.client.draft_exists(self.midasid))
        self.assertTrue(os.path.exists(nerdf))
        self.assertTrue(not os.path.exists(annotf))
        nerdm = utils.read_json(nerdf)
        self.assertNotEqual(nerdm.get('title'), "Goobers!")

        pod = self.svc.get_pod(self.midasid)
        self.assertNotEqual(pod['title'], "Goobers!")
        pod = self.svc.get_customized_pod(self.midasid)
        self.assertNotEqual(pod['title'], "Goobers!")
        resp = requests.patch(custbaseurl+self.midasid, json={"title": "Goobers!"},
                              headers={'Authorization': 'Bearer SECRET'})
        self.assertEqual(resp.status_code, 201)

        pod = self.svc.get_pod(self.midasid)
        self.assertNotEqual(pod['title'], "Goobers!")
        pod = self.svc.get_customized_pod(self.midasid)
        self.assertEqual(pod['title'], "Goobers!")
        self.assertEqual(pod['_editStatus'], "in progress")

        resp = requests.patch(custbaseurl+self.midasid,
                              json={"_editStatus": "done",
                                    "authors": [{"fn": "Enya",
                                                 "affiliation": [
                                                     {"title": "NIST", "subunits": ["MML", "ODI"], "dept":"SDG"},
                                                     "UMD"
                                                 ]
                                                },
                                                "Madonna"]},
                              headers={'Authorization': 'Bearer SECRET'})
        self.assertEqual(resp.status_code, 201)
        pod = self.svc.get_customized_pod(self.midasid)
        self.assertEqual(pod['title'], "Goobers!")
        self.assertEqual(pod['_editStatus'], "done")
        self.assertEqual(pod['identifier'], self.midasid)
        self.assertNotIn('authors', pod)

        self.svc.end_customization_for(self.midasid)
        self.assertTrue(not self.client.draft_exists(self.midasid))
        self.assertTrue(os.path.isfile(nerdf))
        self.assertTrue(os.path.isfile(annotf))

        pod = self.svc.get_pod(self.midasid)
        self.assertEqual(pod['title'], "Goobers!")

        nerdm = utils.read_json(nerdf)
        self.assertEqual(nerdm['title'], "Goobers!")
        self.assertNotIn('authors', nerdm)
        nerdm = utils.read_json(annotf)
        self.assertIn('authors', nerdm)
        self.assertEqual(len(nerdm['authors']), 1)
        self.assertEqual(nerdm['authors'][0]['fn'], "Enya")
        self.assertEqual(nerdm['authors'][0]['@type'], "foaf:Person")
        self.assertIn('affiliation', nerdm['authors'][0])
        self.assertEqual(len(nerdm['authors'][0]['affiliation']), 1)
        self.assertEqual(nerdm['authors'][0]['affiliation'][0]['title'], "NIST")
        self.assertEqual(nerdm['authors'][0]['affiliation'][0]['@type'], "org:Organization")
        self.assertEqual(nerdm['authors'][0]['affiliation'][0]['@id'], "ror:05xpvk416")
        self.assertIn('subunits', nerdm['authors'][0]['affiliation'][0])
        self.assertEqual(nerdm['authors'][0]['affiliation'][0]['subunits'], ["MML","ODI"])
        self.assertNotIn('title', nerdm)

        # ensure that @type has DataPublication in it
        self.assertIn('@type', nerdm)
        self.assertIn('nrdp:DataPublication', nerdm.get('@type'))

        nerdf = os.path.join(self.nrddir, self.midasid+".json")
        self.assertTrue(os.path.isfile(nerdf))
        nerdm = utils.read_json(nerdf)
        self.assertEqual(nerdm['title'], "Goobers!")
        self.assertIn('authors', nerdm)
        self.assertIn('nrdp:DataPublication', nerdm.get('@type', []))

        # test add an author
        self.assertEqual(len(nerdm['authors']), 1)
        pod = self.svc.get_pod(self.midasid)
        self.svc.start_customization_for(pod)
        authors = nerdm['authors']
        authors.append({"fn": "Madonna"})
        resp = requests.patch(custbaseurl+self.midasid,
                              json={"_editStatus": "done", "authors": authors},
                              headers={'Authorization': 'Bearer SECRET'})
        self.svc.end_customization_for(self.midasid)
        nerdm = utils.read_json(annotf)
        self.assertEqual(len(nerdm['authors']), 2)
        self.assertIn('@type', nerdm)
        self.assertIn('nrdp:DataPublication', nerdm.get('@type'))

        # test removal of authors
        pod = self.svc.get_pod(self.midasid)
        self.svc.start_customization_for(pod)
        resp = requests.patch(custbaseurl+self.midasid,
                              json={"_editStatus": "done", "authors": []},
                              headers={'Authorization': 'Bearer SECRET'})
        self.svc.end_customization_for(self.midasid)
        nerdm = utils.read_json(annotf)
        self.assertIn('@type', nerdm)
        self.assertNotIn('nrdp:DataPublication', nerdm.get('@type'))
        

    TAXONURI = "https://www.nist.gov/od/dm/nist-themes/v1.0"

    def test_get_customized_pod_wtopic(self):

        podf = os.path.join(self.revdir, "1491", "_pod.json")
        pod = utils.read_json(podf)
        bagdir = os.path.join(self.svc.mddir, self.midasid)

        self.assertTrue(not self.client.draft_exists(self.midasid))
        self.svc.start_customization_for(pod)
        self.assertTrue(self.client.draft_exists(self.midasid))

        resp = requests.patch(custbaseurl+self.midasid,
                              json={"topic": [{"@type": "Concept", "scheme": self.TAXONURI,
                                               "tag": "Bioscience: Genomics" }]},
                              headers={'Authorization': 'Bearer SECRET'})

        self.assertEqual(resp.status_code, 201)
        pod = self.svc.get_customized_pod(self.midasid)
        self.assertEqual(pod['identifier'], self.midasid)

        self.assertIn('theme', pod)
        self.assertNotEqual(len(pod['theme']), 0);
        self.assertEqual(pod['theme'][-1], "Bioscience-> Genomics")

    def test_get_customized_pod_wtheme(self):

        podf = os.path.join(self.revdir, "1491", "_pod.json")
        pod = utils.read_json(podf)
        bagdir = os.path.join(self.svc.mddir, self.midasid)

        self.assertTrue(not self.client.draft_exists(self.midasid))
        self.svc.start_customization_for(pod)
        self.assertTrue(self.client.draft_exists(self.midasid))

        resp = requests.patch(custbaseurl+self.midasid,
                              json={"theme": ["Bioscience: Genomics"]},
                              headers={'Authorization': 'Bearer SECRET'})

        self.assertEqual(resp.status_code, 201)
        pod = self.svc.get_customized_pod(self.midasid)
        self.assertEqual(pod['identifier'], self.midasid)

        self.assertIn('theme', pod)
        self.assertNotEqual(len(pod['theme']), 0);
        self.assertEqual(pod['theme'][-1], "Bioscience-> Genomics")

    def test_get_customized_minnpod(self):
        bagdir = os.path.join(self.svc.mddir, self.midasid)
        pod = {"identifier": self.midasid}
        self.assertTrue(not self.client.draft_exists(self.midasid))
        
        self.svc.start_customization_for(pod)
        self.assertTrue(self.client.draft_exists(self.midasid))

        pod = self.svc.get_customized_pod(self.midasid)
        self.assertEqual(pod['title'], "")
        resp = requests.patch(custbaseurl+self.midasid, json={"title": "Goobers!"},
                              headers={'Authorization': 'Bearer SECRET'})
        self.assertEqual(resp.status_code, 201)

        pod = self.svc.get_pod(self.midasid)
        self.assertNotEqual(pod['title'], "Goobers!")
        pod = self.svc.get_customized_pod(self.midasid)
        self.assertEqual(pod['title'], "Goobers!")
        self.assertEqual(pod['_editStatus'], "in progress")


if __name__ == '__main__':
    test.main()

        
        
