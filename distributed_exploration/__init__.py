# -*- coding: utf-8 -*-
"""
Multithreading exploration of parameters
"""

def list_tensor_product(*args):
    import numpy as np
    
    aux = np.meshgrid(*args);
    ret = []
    for a in aux:
        ret.append(a.flatten())
        
    return ret

def chunks(L, n):
    return [L[i::n] for i in range(n)]
    
def explore_thread(function,arg_dict,nthreads=1,postpro=None):

    """
    The function should be called as function(**arguments), with arguments been made from arg_dict
    postpro function could be passes to executed with the output of function
    """
    
    from threading import Thread  
        
    nvalues = len(arg_dict.values()[0])
    
    responses= []
    
    class worker(Thread):
        def __init__ (self,jj):
            Thread.__init__(self)
            self.jj = jj
            
        def run(self):
            jj = self.jj
            
            for j in jj:
                
               
                arguments = {key:val[j] for key,val in arg_dict.iteritems() }
                            
                X = function( **arguments )
                
                resp = {}
                resp['args'] = arguments
                resp['ix']=j

                if postpro:
                    resp['out']= postpro(X)
                else:
                    resp['out']= X
                
                responses.append(resp)

    if nthreads>nvalues:
        nthreads = nvalues


    chunks_list = chunks( range(nvalues),nthreads )
 
    thr = range(nthreads)
    for k in xrange(nthreads):
        jj = chunks_list[k]
        thr[k] = worker(jj)
        thr[k].start()
        
    for k in xrange(nthreads):   
        thr[k].join()
        
    return responses
