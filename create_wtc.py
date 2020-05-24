import sys
from java.util import Properties
from java.io import FileInputStream
from java.io import File


domainProps = Properties()

def get_instance_property(instancetype, instanceNumber, propName):
        # read PARAMETER;  if PARAMETER="" try to overwrite with default. Note that the default parameter has "x" instead of number
        print '\n'+instancetype+'.'+instanceNumber+'.'+propName

        concreateValue = domainProps.getProperty(instancetype+'.'+instanceNumber+'.'+propName,"")
        if len(concreateValue) == 0:
                concreateValue = domainProps.getProperty(instancetype+'.x.'+propName,"")  # read default !!

        return concreateValue


def createAllWTCServer(myfile):
  try:
    print 'Connect to weblogic ....'
    #TODO change the user, password, IP and PORT values
    connect('user','password','IP:PORT') 
 

    print 'File: '+ myfile
    
    input = FileInputStream(myfile)
    domainProps.load(input)
    input.close()
    print 'File readed: '+ myfile

    totalWTCServer = domainProps.getProperty('wtc.amountserver')
    print 'totalWTCServer= '+ totalWTCServer
      


    print 'Creating ['+totalWTCServer+'] WTC servers'
    edit()
    startEdit()
    i=1
    while (i <= int(totalWTCServer)) :

        try:
            print '+++++++++++++++++++++++++'
            print 'Creando config: '+str(i)
            print '+++++++++++++++++++++++++'

            cd('/')
            wtc_name               = get_instance_property('wtc.server',str(i), 'name');
            wtc_targetmanagedserver= get_instance_property('wtc.server',str(i), 'targetmanagedserver');
            wtc_localdomainname    = get_instance_property('wtc.server',str(i), 'localtuxdomain.name');
            wtc_access_point       = get_instance_property('wtc.server',str(i), 'localtuxdomain.access_point');
            wtc_access_point_id    = get_instance_property('wtc.server',str(i), 'localtuxdomain.access_point_id');
            wtc_connection_policy  = get_instance_property('wtc.server',str(i), 'localtuxdomain.connection_policy');
            wtc_nwaddr = get_instance_property('wtc.server',str(i), 'localtuxdomain.nw_addr');

            print 'create WTC server:' + wtc_name
            cmo.createWTCServer(wtc_name)

            #print 'change to WTC server'
            cd ('/WTCServers/'+wtc_name)

            #print 'cmo.addTarget'
            cmo.addTarget(getMBean('/Servers/'+wtc_targetmanagedserver))

            print 'create local domain configuration ' +wtc_localdomainname

            cmo.createWTCLocalTuxDom(wtc_localdomainname)
            cd ('WTCLocalTuxDoms/'+wtc_localdomainname)
            cmo.setAccessPoint(wtc_access_point)
            cmo.setAccessPointId(wtc_access_point_id)
            cmo.setNWAddr(wtc_nwaddr)
            cmo.setConnectionPolicy(wtc_connection_policy)

            print 'create remote tux domains'
            totalWTCRemoteDomains=get_instance_property('wtc.server',str(i), 'amountremotedomains')
            
            #print 'init Conf Remote domain'
            r=1
            while (r <= int(totalWTCRemoteDomains)) :

                print 'Conf Remote domain' + str(r)
                print '+++++++++++++++++++++++++'
                remotetuxdomain_name = get_instance_property('wtc.server',str(i), 'remotetuxdomain.'+str(r)+'.name');
                remotetuxdomain_access_point = get_instance_property('wtc.server',str(i), 'remotetuxdomain.'+str(r)+'.access_point');
                remotetuxdomain_access_point_id = get_instance_property('wtc.server',str(i), 'remotetuxdomain.'+str(r)+'.access_point_id');
                remotetuxdomain_local_access_point = get_instance_property('wtc.server',str(i), 'remotetuxdomain.'+str(r)+'.local_access_point');
                remotetuxdomain_nw_addr = get_instance_property('wtc.server',str(i), 'remotetuxdomain.'+str(r)+'.nw_addr');
                remotetuxdomain_federation_url = get_instance_property('wtc.server',str(i), 'remotetuxdomain.'+str(r)+'.federation_url');
                remotetuxdomain_federation_name = get_instance_property('wtc.server',str(i), 'remotetuxdomain.'+str(r)+'.federation_name');
                remotetuxdomain_connection_policy  = get_instance_property('wtc.server',str(i), 'remotetuxdomain.'+str(r)+'.connection_policy');


                print 'create remote tux domain: '+wtc_name
                cd ('/WTCServers/'+wtc_name)

                cmo.createWTCRemoteTuxDom(remotetuxdomain_name)
                cd ('WTCRemoteTuxDoms/'+remotetuxdomain_name)
                cmo.setAccessPoint(remotetuxdomain_access_point)
                cmo.setAccessPointId(remotetuxdomain_access_point_id)
                cmo.setLocalAccessPoint(remotetuxdomain_local_access_point)
                cmo.setNWAddr(remotetuxdomain_nw_addr)
                cmo.setFederationName(remotetuxdomain_federation_name)
                cmo.setFederationURL(remotetuxdomain_federation_url)
                cmo.setConnectionPolicy(remotetuxdomain_connection_policy)

                r = r+1

            print 'create WTC imports:'
            totalWTCRImports=get_instance_property('wtc.server',str(i), 'amountimports')

            r=1
            while (r <= int(totalWTCRImports)) :
                import_name = get_instance_property('wtc.server',str(i), 'import.'+str(r)+'.name');
                import_resource_name = get_instance_property('wtc.server',str(i), 'import.'+str(r)+'.resource_name');
                import_remote_name = get_instance_property('wtc.server',str(i), 'import.'+str(r)+'.remote_name');
                import_local_access_point   = get_instance_property('wtc.server',str(i), 'import.'+str(r)+'.local_access_point');
                import_remote_access_point  = get_instance_property('wtc.server',str(i), 'import.'+str(r)+'.remote_access_point');

                # create WTC import
                cd ('/WTCServers/'+wtc_name)
                cmo.createWTCImport(import_name)
                cd ('WTCImports/'+import_name)
                cmo.setRemoteName(import_remote_name)
                cmo.setLocalAccessPoint(import_local_access_point)
                cmo.setResourceName(import_resource_name)
                cmo.setRemoteAccessPointList(import_remote_access_point)

                r = r+1

            # create WTC exports
#            totalWTCRExports=get_instance_property('wtc.server',str(i), 'amountexports')

#           r=1
#           while (r <= int(totalWTCRExports)) :
#               export_name  = get_instance_property('wtc.server',str(i), 'export.'+str(r)+'.name');
#               export_resource_name    = get_instance_property('wtc.server',str(i), 'export.'+str(r)+'.resource_name');
#               export_remote_name      = get_instance_property('wtc.server',str(i), 'export.'+str(r)+'.remote_name');
#               export_local_access_point   = get_instance_property('wtc.server',str(i), 'export.'+str(r)+'.local_access_point');
#               export_ejbname  = get_instance_property('wtc.server',str(i), 'export.'+str(r)+'.ejbname');
#
#               # create WTC export
#               cd ('/WTCServers/'+wtc_name)
#               cmo.createWTCExport(export_name)
#               cd ('WTCExports/'+export_name)
#               cmo.setRemoteName(export_remote_name)
#               cmo.setLocalAccessPoint(export_local_access_point)
#               cmo.setResourceName(export_resource_name)
#               cmo.setEJBName(export_ejbname)
#
#               r = r+1
                
            print 'WTC Server: ',wtc_name,', has been created Successfully !!!'

        except:
            dumpStack()
            print '***** CANNOT CREATE WTC-Server with the Name : ' , wtc_name ,' !'
            print ''

        i = i + 1
    save()
    activate()
    disconnect()
  except:
    print 'Exception while creating WTC server !'
    stopEdit()
    dumpStack()
    disconnect()

createAllWTCServer ("osb_wtc.properties")