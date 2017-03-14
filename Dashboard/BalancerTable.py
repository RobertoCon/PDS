'''
Created on 08 mar 2017

@author: Conny
'''
import yaml
class BalancerTable(object):
    '''
    classdocs
    '''

    @staticmethod  
    def getHtml(balancers):
        code=""
        html="""<div class="table-responsive"><table class="table table-striped">
                    <thead>
                            <tr>
                              <th>#</th>
                              <th>ID</th>
                              <th>HOST</th>
                              <th>ALGORITHM</th>
                              <th>PROTOCOL</th>
                              <th>IP</th>
                              <th>PORT</th>
                              <th>CMD</th>
                            </tr>
                    </thead>
                    <tbody>
                     %s
                    </tbody>
                </table></div>
                  <form action="add_balancer" method="post" >
                   <label> Balancer Model: </label><br>
                   <textarea name="add_balancer_model" rows="5" cols="40"></textarea><br>
                   <button type="submit" class="btn btn-default btn-lg"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>
                </form> 
            """
        i=0 
        for source in balancers['node_templates'] :
            for balancer in balancers['node_templates'][source] :
                i=i+1
                a={'node_templates':{}}
                a['node_templates'][balancer]=balancers['node_templates'][source][balancer]
                code=code+"""<tr>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                            </tr>
                """ % (str(i),balancers['node_templates'][source][balancer]['name'],\
                       balancers['node_templates'][source][balancer]['host'],\
                       balancers['node_templates'][source][balancer]['properties']['algorithm'],\
                       balancers['node_templates'][source][balancer]['properties']['ports']['in_port']['protocol'],\
                       balancers['node_templates'][source][balancer]['capabilities']['clients']['ip_address'],\
                       str(balancers['node_templates'][source][balancer]['properties']['ports']['in_port']['target']),\
                       '<table><tr><td><form action="remove_balancer" method="post">\
                       <button type="submit" name="remove_balancer_model" value="'+yaml.dump(a)+\
                       '"  class="btn btn-default btn-lg"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button>\
                       </form></td></tr></table>')
        
        return html % code