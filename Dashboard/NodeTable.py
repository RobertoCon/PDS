'''
Created on 06 feb 2017

@author: Conny
'''
class NodeTable(object):
    '''
    classdocs
    '''

    @staticmethod  
    def getHtml(nodes):
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
                </table></div>"""
        i=0
        for node in nodes['node_templates'] :
            i=i+1
            code=code+"""<tr>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                        </tr>
            """ % (str(i),node,nodes['node_templates'][node]['attributes']['public_address'],nodes['node_templates'][node]['capabilities']['host']['properties']['num_cpus'],nodes['node_templates'][node]['capabilities']['host']['properties']['mem_size'],nodes['node_templates'][node]['capabilities']['host']['properties']['disk_size'],nodes['node_templates'][node]['capabilities']['host']['properties']['os']['properties']['architecture'],"CMD")
        
        return html % code      