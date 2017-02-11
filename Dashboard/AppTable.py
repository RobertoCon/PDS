'''
Created on 11 feb 2017

@author: Conny
'''
import yaml
class AppTable(object):
    '''
    classdocs
    '''

    @staticmethod  
    def getHtml(apps):
        code=""
        html="""<div class="table-responsive"><table class="table table-striped">
                    <thead>
                            <tr>
                              <th>#</th>
                              <th>ID</th>
                              <th>IMAGE</th>
                              <th>HOST</th>
                              <th>PORT</th>
                              <th>QUOTA</th>
                              <th>BOOT</th>
                              <th>STATE</th>
                              <th>CMD</th>
                            </tr>
                    </thead>
                    <tbody>
                     %s
                    </tbody>
                </table></div>
                  <form action="add_app" method="post" >
                   <label> App Model: </label><br>
                   <textarea name="add_app_model" rows="5" cols="40"></textarea><br>
                   <button type="submit" class="btn btn-default btn-lg"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>
                </form> 
            """
        i=0 
        
        for app in apps['node_templates'] :
            i=i+1
            a={'node_templates':{}}
            a['node_templates'][app]=apps['node_templates'][app]
            code=code+"""<tr>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                        </tr>
            """ % (str(i),apps['node_templates'][app]['instance'],\
                   apps['node_templates'][app]['artifacts']['image']['file'],\
                   apps['node_templates'][app]['requirements']['host']['node'],\
                   apps['node_templates'][app]['properties']['ports']['in_port']['protocol']+":"+str(apps['node_templates'][app]['properties']['ports']['in_port']['target']),\
                   str(apps['node_templates'][app]['requirements']['host']['cpu_quota']),\
                   apps['node_templates'][app]['requirements']['host']['bootstrap'],\
                   apps['node_templates'][app]['requirements']['host']['state'],\
                   '<form action="remove_app" method="post" >\
                   <button type="submit" name="remove_app_model" value="'+yaml.dump(a)+\
                   '"  class="btn btn-default btn-lg"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button>\
                   </form>'+\
                   '<form action="start_app" method="post" >\
                   <button type="submit" name="start_app_model" value="'+yaml.dump(a)+\
                   '"  class="btn btn-default btn-lg"><span class="glyphicon glyphicon-play" aria-hidden="true"></span></button>\
                   </form>'+\
                   '<form action="stop_app" method="post" >\
                   <button type="submit" name="stop_app_model" value="'+yaml.dump(a)+\
                   '"  class="btn btn-default btn-lg"><span class="glyphicon glyphicon-stop" aria-hidden="true"></span></button>\
                   </form>'+\
                   '<form action="update_app" method="post" >\
                   <button type="submit" name="update_app_model" value="'+yaml.dump(a)+\
                   '"  class="btn btn-default btn-lg"><span class="glyphicon glyphicon-sort" aria-hidden="true"></span></button>\
                   </form>')
        
        return html % code