#!/usr/bin/env python
"""
Script para deployar app en jboss domain mode

Ejemplo:
    new deploy
    $ jbs_domain_deploy.py  /location/to/app.war  server-group-to-deploy  jbs_host

    replace
    $ jbs_domain_deploy.py  name-of-the-app  server-group-to-deploy  jbs_host

"""

import subprocess
import sys


def main():
    location     = sys.argv[1]              # ubicacion del war
    server_group = sys.argv[2]              # server-group al cual deployar 
    jbs_host     = sys.argv[3]              # jboss master node
    app_name = location.split('/')[-1]
    is_deploy, deploy_info = check_deploy(app_name, jbs_host)

    if is_deploy:
        if is_same_group(server_group, deploy_info):
            replace(location, jbs_host)           
        else:
            args = '--name=' + app_name
            deploy(args, server_group, jbs_host)      # assign de una app a otro server-group
    else:
        deploy(location, server_group, jbs_host)


def is_same_group(server_group, deploy_info):
    # retorna True si es el mismo server-group y False si no
    deploy_info = deploy_info.split("\n")[3:]
    for line in deploy_info:
        aux = line.split(' ',1)
        if server_group in aux and 'enabled' in aux[1].strip():
            return True
    return False 


def deploy(location, server_group, jbs_host):
    comando = './jboss-cli.sh --connect --controller=' + jbs_host + ':9999 --command="deploy ' + location + ' --server-groups=' + server_group + '"' 
    exit_status, output = jboss_cli(comando)
    exit(exit_status)


def replace(location, jbs_host):
    comando = './jboss-cli.sh --connect --controller=' + jbs_host + ':9999 --command="deploy ' + location + ' --force"'
    exit_status, output = jboss_cli(comando)
    exit(exit_status)
    

def check_deploy(app_name, jbs_host):
    """Checkea si la app ya esta deployada.
    
    Returns:
        retorna un tuple con un boolean del deploy y info-del deploy
        (True, output)
        (False, outpu)
    """
    comando = './jboss-cli.sh --connect --controller=' + jbs_host + ':9999 --command="deployment-info --name=' + app_name + '"' 
    exit_status, output = jboss_cli(comando)

    if 'enabled' in output:
        return (True, output)
    else:
        return (False, output)


def jboss_cli(comando):
    """  Ejecuta un comando en jboss-cli

    Returns:
        0 si termino sin errores, 1 si ocurrio algun error.
    """
    # workaround del bug de jboss-cli info:https://access.redhat.com/solutions/2333581
    try:
        output = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT)
        return (0, output)
    except Exception, e:
        output = str(e.output)
        return (1, output)


if __name__ == '__main__':
    main()
