'''
Created on 10 feb 2017

@author: Conny
'''
import yaml
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
                              <th>TYPE</th>
                              <th>LOCATION</th>
                              <th>HOST</th>
                              <th>CMD</th>
                            </tr>
                    </thead>
                    <tbody>
                     %s
                    </tbody>
                </table></div>
                  <form action="add_device" method="post" >
                   <label> Device Model: </label><br>
                   <textarea name="add_device_model" rows="5" cols="40"></textarea><br>
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
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                          
                        </tr>
            """ % (str(i),devices['node_templates'][dev]['id'],devices['node_templates'][dev]['device_type'],devices['node_templates'][dev]['location'],devices['node_templates'][dev]['requirements']['host'],\
                   '<form action="remove_device" method="post" >\
                   <button type="submit" name="remove_device_model" value="'+\
                   yaml.dump(devices['node_templates'][dev])    +\
                   '"  class="btn btn-default btn-lg"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button>\
                   </form>')
        
        return html % code