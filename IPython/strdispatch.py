from IPython.hooks import CommandChainDispatcher
import IPython.hooks

import re

class StrDispatch(object):
    """ Dispatch (lookup) a set of strings / regexps for match """
    def __init__(self):
        self.strs = {}
        self.regexs = {}
    def add_s(self, s, obj, priority= 0 ):
        """ Adds a target 'string' for dispatching """
        
        chain = self.strs.get(s, CommandChainDispatcher())
        chain.add(obj,priority)
        self.strs[s] = chain

    def add_re(self, regex, obj, priority= 0 ):
        """ Adds a target regexp for dispatching """
        
        chain = self.regexs.get(regex, CommandChainDispatcher())
        chain.add(obj,priority)
        self.regexs[regex] = chain

    def dispatch(self, key):
        """ Get a seq of Commandchain objects that match key """
        if key in self.strs:
            yield self.strs[key]
        
        for r, obj in self.regexs.items():
            if re.match(r, key):
                yield obj
            else: 
                #print "nomatch",key
                pass
            

    def __repr__(self):
        return "<Strdispatch %s, %s>" % (self.strs, self.regexs)
    def flat_matches(self, key):
        """ Yield all 'value' targets, without priority """
        for val in self.dispatch(key):
            for el in val:
                yield el[1] # only value, no priority
        return
         

def test():
    d = StrDispatch()
    d.add_s('hei',34, priority = 4)
    d.add_s('hei',123, priority = 2)
    print  list(d.dispatch('hei'))
    d.add_re('h.i', 686)
    print list(d.flat_matches('hei'))

if __name__ == '__main__':
    test()    