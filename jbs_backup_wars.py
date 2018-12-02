#!/usr/bin/env python
"""
Script para realizar un backup de todas las app
deployadas en jboss eap 7+ en modo domain

"""

import xml.etree.ElementTree as et
import subprocess

jboss_home  = "/opt/jboss-eap-7.1/domain/configuration/"
backup_dest = "/path/to/backup_folder/"
deploy_home = "/opt/jboss-eap-7.1/domain/data/content/"
tree        = et.parse(jboss_home + "domain.xml")
root        = tree.getroot()
deploy_tag  = root[6]


if deploy_tag.getchildren():
  for child_tag in range( len(deploy_tag.getchildren())):
      deploy_name = deploy_tag[child_tag].get("name")
      deploy_name = deploy_name if ".war" in deploy_name else deploy_name + ".war"
      deploy_hash = deploy_tag[child_tag][0].get("sha1")
      path_to_content = deploy_home + deploy_hash[0:2] + "/" + deploy_hash[2:] + "/content"
      subprocess.call("cp " + path_to_content + " " + backup_dest + deploy_name, shell=True)
