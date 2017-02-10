'''
Created on 10 feb 2017

@author: Conny
'''
class DeviceTable(object):
    '''
    classdocs
    '''

    @staticmethod  
    def getHtml(devices):
        code=""
        html="""<div class="table-responsive"><table class="table table-striped">
                    <thead>
                            <tr>
                              <th>#</th>
                              <th>ID</th>
                              <th>IP</th>
                              <th>CORE</th>
                              <th>MEMORY</th>
                              <th>DISK</th>
                              <th>ARCH</th>
                              <th>CMD</th>
                            </tr>
                    </thead>
                    <tbody>
                     %s
                    </tbody>
                </table></div>
                  <form action="add_node" method="post" >
                   <label> Hostname: </label><input type="text" name="add_node_id">
                   <button type="submit" class="btn btn-default btn-lg"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>
                </form> 
            """
        i=0
        for dev in devices['node_templates'] :
            i=i+1
            code=code+"""<tr>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                          
                        </tr>
            """ % (str(i),devices['node_templates'][dev]['id'],devices['node_templates'][dev]['device_type'])
        
        return html % code