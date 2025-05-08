"""
patlang.py

Author: Marijn van Tricht
Date: 2025-04-17
Description:
    Pattern language, contains:
    String
    List (& List.Variable)
    Tree (& Tree.Variable)
"""

# Copyright 2025 Marijn van Tricht
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#------------------------------------------------------------------------------#
#                                                                              #
# String                                                                       #
#                                                                              #
#------------------------------------------------------------------------------#

class String(str):
    """
    a patlang String
    """
    
    def __new__(cls, value = ""):
        """
        new Pattern (String) with value, because string is immutable
        """ 
        pat = super().__new__(cls, value)
        pat.variables = dict()
        return pat

    def __getitem__(self, key):
        return self.variables[key]
    
    def __setitem__(self, key, value):
        self.variables.pop(key, None)
        self.variables[key] = value

    def __add__(self, other):
        pat = String(super().__add__(other))
        pat.variables = self.variables
        if isinstance(other, String):
            pat.variables.update(other.variables)
        return pat

    def __eq__(self, other, strict=True):
        if not strict:
            return str(self) == str(other)
        if isinstance(other, String):   
            return repr(self) == repr(other)
        return False
    
    def __str__(self):
        out = super().__str__()
        variables = dict(self.variables)
        
        for key in variables:
            out = out.replace(str(key), str(variables[key]))
            
        return out

    def __contains__(self, key):
        if isinstance(key, str):
            if (key in str(self)):
                return True
            elif (key in self.variables):
                return True
        elif isinstance(key, String):
            if (str(key) in str(self)):
                return True
            elif (key in self.variables):
                return True
        return False

    def __repr__(self):
        out = super().__repr__()
        variables = dict(self.variables)
        
        for key in variables:
            out = out.replace(
                str(key), repr(key) + ":" + repr(variables[key]))
            
        return out

    def flush(self):
        variables = dict(self.variables)
        
        for key in variables:
            for otherKey in variables:
                if key != otherKey:
                    variables[otherKey] = variables[otherKey].replace(
                        str(key), str(self.variables[key]))
                    
        self.variables = variables

    # for compatiblity accross other patlang types
    def setItem(self, key, value):
        """
        set 'static' item
        """
        # cannot replace in self, because string is immutable
        self.setVariable(key, value)

    # for compatiblity accross other patlang types
    def getItem(self, key):
        """
        get static item
        """  
        if key in self:
            return key

    # for compatiblity accross other patlang types
    def setVariable(self, key, value):
        """
        set variable item
        """ 
        self[key] = value

    # for compatiblity accross other patlang types
    def getVariable(self, key):
        """
        get variable item
        """  
        return self[key]

    def split(self, separator=" ", maxsplit=-1):
        """
        split, but return a patlang List type
        """
        pass

    def toList(self, flattend=True, sep="", endline=""):
        """
        convert to patlang List
        """ 
        S = super().__str__()
        L = [List(S)]

        dictovaries = dict(self.variables)

        if sep != "": dictovaries.update({sep:""});
        if endline != "": dictovaries.update({endline:""});
        
        for key in dictovaries:
            Lint = [List()]
            for l in L:
                for item in l:
                    if not isinstance(item, List.Variable):
                        if key in item:
                            items = item.split(key)
                            for idx, item in enumerate(items):
                                if idx > 0:
                                    if key in self.variables:
                                        Lint[-1].append(List.Variable(key, self.variables[key]))
                                        nk = self.variables[key]
                                        while nk in self.variables:
                                            Lint[-1].setVariable(key, List.Variable(nk, self.variables[nk]))
                                            nk = self.variables[nk]
                                    elif key == endline:
                                        Lint.append(List())
                                if item != '':
                                    Lint[-1].append(item)
                        else:
                            Lint[-1].append(item)
                    else:
                        Lint[-1].append(item)

            if len(Lint) > 1:
                L = []
                for l in Lint:
                    L.append(l.copy())
            else:
                L = [Lint[-1].copy()]

        if len(L) > 1:
            return L
        else:
            return L[0]

    def toTree(self, flattend=True):
        """
        convert to patlang Tree
        """ 
        L = self.toList(flattend)
        return L.toTree(flattend)

#------------------------------------------------------------------------------#
#                                                                              #
# List                                                                         #
#                                                                              #
#------------------------------------------------------------------------------#

class List(list):
    """
    a patlang List
    """

    def __init__(self, *args):
        """
        Init a Pattern (list) with *args
        """
        self.variables = dict()
        super().__init__(args)
        
    def __getitem__(self, key, flattend = True):
        """
        will return a nested (if flattend) variable (if key is variable) or item whose name is matching the key
        """            
        if isinstance(key, slice):
            items = super().__getitem__(key)
            newPat = List()
            for item in items:
                newPat.append(item)
            return newPat

        if isinstance(key, List.Variable):
            return self.getVariable(key.name, flattend)
        else:
            return self.getItem(key, flattend)

    def __setitem__(self, key, value, flattend = True):
        """
        will set a nested (if flattend) variable (if key is variable) or item whose name is matching the key
        """
        if isinstance(key, List.Variable):
            self.setVariable(key.name, value, flattend)
        else:
            self.setItem(key, value, flattend)

    def __add__(self, other):
        pat = self.copy()
        if type(other) is List:
            pat.extend(other)
        else:
            pat.append(other)
        return pat

    def __iadd__(self, other):
        """
        return __add__
        """
        return self.__add__(other)

    def __sub__(self, other):
        return (self.copy()).__isub__(other)

    def __isub__(self, other):
        """
        return __sub__
        """
        for i in range(len(self)-1, -1, -1):
            print(list.__getitem__(self,i), i)
            if list.__getitem__(self,i) == other:
                del self[i:i+1]
            elif (isinstance(list.__getitem__(self,i), List.Variable)
                  and isinstance(other, List.Variable)):
                if list.__getitem__(self,i).name == other.name:
                    del self[i:i+1]
            elif isinstance(list.__getitem__(self,i), List):
                item = list.__getitem__(self,i)
                item -= other
        return self

    def __contains__(self, key, flattend=True):
        """
        if __getitem__ returns a valid item, this returns True
        """
        if self.__getitem__(key, flattend):
            return True
        return False
    
    def __str__(self):
        """
        return serialized string of self
        """
        return "" + "".join(map(str, self)) + ""

    def __repr__(self):
        """
        return serialized repr of self
        """
        return "[" + ",".join(map(repr, self)) + "]"

    def _copy(self, newList):
        """
        private copy, because self_type cannot be given as default argument
        """
        for item in self:
            if hasattr(item, "copy"):
                newList.append(item.copy())
            else:
                newList.append(item)
        return newList

    def copy(self):
        """
        returns a copy of self as Pattern(self)
        """ 
        return self._copy(List())

    def setItem(self, key, value, flattend=True):
        """
        set static item
        """ 
        for index, item in enumerate(self):
            if item == key:
                super().__setitem__(index, value)
            else:
                if isinstance(item, List) and flattend:
                    item[key] = value

    def getItem(self, key, flattend=True):
        """
        get static item
        """  
        for item in self:
            if item == key:
                return item
            else:
                if isinstance(item, List) and flattend:
                    n = item[key]
                    if n: return n;

    def setVariable(self, key, value, flattend=True):
        """
        set variable item
        """

	# This should logically be a dict of variables that can be updated and
        # keeps reference instead of duplicate variables inside the patterns
        # right?
        
        # There is a good reason to not do that:
        # Variables should stick with previous values assigned, even if they
        # have the same name, because otherwise, which one is true?, both may be
        # true.
        
        # For example (what if classnames are lateron combined into a file which
        # may be a List itself. Updating the variables is a consious decision of
        # the desiginer/coder, use:
        # setVariable(getVariable().name, getVariable().value) or use flush(key)

        # or should one not use flatten at that point?
        
        for item in self:
            if type(item) is List.Variable:
                if item.name == key:
                    item.clear()
                    if type(value) is List:
                        item.extend(value)
                    else:
                        item.append(value)
                elif flattend:
                    item.setVariable(key, value)
            elif isinstance(item, List) and flattend:
                item.setVariable(key, value)

    def getVariable(self, key, flattend=True):
        """
        get variable item
        """

        # which variable? it returns just the first and that may be a flaw.
         
        for item in self:
            if type(item) is List.Variable:
                if item.name == key:
                    return item
                elif flattend:
                    n = item.getVariable(key)
                    if n: return n;
            elif isinstance(item, List) and flattend:
                n = item.getVariable(key)
                if n: return n;

    def flush(self, key, flattend=True):
        """
        updating variables and values (no garanteed success)
        """
        var = getVariable(key, flattend)
        setVariable(var.name, var.value, flattend)

    def toTree(self, flattend=True):
        """
        convert to patlang Tree
        """            
        Tbase = Tree()
        T = Tbase
        for item in self:
            if isinstance(item, List.Variable):
                T = T[Tree.Variable(item.name, item.toTree().value)]
            elif isinstance(item, List) and flattend:
                nTbase = T 
                for x in item.toTree():
                    nT = nTbase
                    for y in x:
                        nT = nT[y]
            else:
                T = T[item]
        return Tbase

    def toString(self, flattend=True, sep="", endline=""):
        """
        convert to patlang String
        """
        def _toString(lst, flattend):
            S = ""
            variables = dict()
            for i, item in enumerate(lst):
                if isinstance(item, List.Variable):
                    S += item.name
                    s, nv = _toString(item, flattend)
                    variables.update({item.name : s})
                    variables.update(nv)
                elif isinstance(item, List) and flattend:
                    s, nv = _toString(item, flattend)
                    S += s
                    if len(lst) != 1:
                        S += endline
                    variables.update(nv)
                else:
                    S += item
                    if i != (len(lst)-1):
                        S += sep
            return S, variables

        S = String()
        s, nv = _toString(self, flattend)
        S += s.strip()
        S.variables.update(nv)
        return S

class VariableList(List):
    """
    a Variable is a Pattern with a name
    """
    
    def __init__(self, name = "", *args):
        """
        Init a variable with a name
        Rest *args will init the pattern
        """
        super().__init__(*args)
        self.name = name

    def __repr__(self):
        """
        return serialized repr of self (including name)
        """
        return repr(self.name) + ":" + ",".join(map(repr, self))
    
    def copy(self):
        """
        returns a copy of self as Variable()
        """ 
        newVariable = List.Variable(self.name)
        return self._copy(newVariable)

# propper alias
List.Variable = VariableList

#------------------------------------------------------------------------------#
#                                                                              #
# Tree                                                                         #
#                                                                              #
#------------------------------------------------------------------------------#

class Tree():
    """
    Tree is a node to a 2D tree
    """

    def __init__(self, *args):
        self._lower_node = None
        self._next_node = None
        self.value = None
        if len(args) > 0: self._setmerge(*args);

    def _addnext(self, value):
        if self._next_node == None:
            self._next_node = Tree(value)
            return self._next_node
        else:
            if isinstance(value, Tree.Variable):
                if isinstance(self._next_node, Tree.Variable):
                    if self._next_node.name == value.name:
                        return self._next_node
            elif self._next_node.value == value:
                return self._next_node
            return self._next_node._addbelow(value)

    def _addbelow(self, value):
        if self._lower_node == None:
            self._lower_node = Tree(value)
            return self._lower_node
        else:
            if self._lower_node.value == value:
                return self._lower_node
            return self._lower_node._addbelow(value)

    def _setmerge(self, value, *args):
        node = self

        if node.value == None:
            node.value = value
        elif node.value == value:
            pass
        else:
            node = node._addbelow(value)
            
        for arg in args:
            node = node._addnext(arg)

        return node

    def _remove(self, value):
        """
        private func used by __sub__, returns a copy minus given value
        """
        # should be able to have inplace sub, but what about the first element
        # self cannot be reassigned
        # for now _remove returns a copy
        
        newTree = Tree()
        for path in self:
            T = newTree
            for item in path:
                if isinstance(value, Tree.Variable):
                    if isinstance(item, Tree.Variable):
                        if value != item.name:
                            T = T[item._remove(value)]
                        else:
                            continue
                        
                if isinstance(item, Tree):
                    if isinstance(value, Tree):
                        if item != value:
                            T = T[item._remove(value)]
                else:
                    if item != value:
                        T = T[item]
        return newTree

    def __eq__(self, other):
        if isinstance(other, Tree):
            for path in self:
                for otherpath in other:
                    for item, otheritem in zip(path, otherpath):
                        if item != otheritem:
                            return False
            return True
        return False
            
    def __getitem__(self, key):
        node = self._setmerge(key)
        if not node._next_node:
            node._addnext(None)
        return node._next_node

    def __setitem__(self, key, value):
        node = self._setmerge(key)
        node.value = value
        return node

    def __add__(self, other):
        n = self.copy()
        n._setmerge(other)
        return n

    def __iadd__(self, other):
        self._setmerge(other)
        return self
        
    def __sub__(self, other):
        return self._remove(other)

    def __contains__(self, value, flattend=True):
        lower_nodes = [self]
        while len(lower_nodes) > 0:
            node = lower_nodes.pop()
            while node != None:
                if node._lower_node:
                    lower_nodes.append(node._lower_node)
                    
                if isinstance(value, Tree.Variable):
                    if isinstance(node.value, Tree.Variable):
                        if value.name == node.value.name:
                            return True

                if isinstance(value, Tree):
                    if isinstance(node.value, Tree):
                        if value.value == node.value.value:
                            return True
                else:
                    if isinstance(node.value, Tree) and flattend:
                        if value in node.value:
                            return True
                    else:
                        if node.value == value:
                            return True

                node = node._next_node
        return False

    def __iter__(self):
        self.routes = [(self,[])]
        return self

    def __next__(self):
        if len(self.routes) > 0:
            node, path = self.routes.pop()
            while node != None:
                if node._lower_node != None:
                    self.routes.append((node._lower_node, list(path)))
                path.append(node)

                node = node._next_node
            L = List()
            L.extend([i.value for i in path if i.value != None])
            return L
        else:
            raise StopIteration
    
    def __str__(self):
        """
        return serialized string of self
        """
        out = ""
        for path in self:
            for item in path:
                if item != None:
                    out += str(item)

        return out

    def __repr__(self):
        """
        return serialized repr of self
        """
        out = []
        for path in self:
            l = []
            for item in path:
                l.append(repr(item))
            out.append("{" + ",".join(l) + "}")
        
        return "{" + ",".join(out) + "}"

    def _copy(self, newTree):
        """
        private copy, cause self_type cannot be as default argument
        """
        for path in self:
            T = newTree
            for item in path:
                if isinstance(item, Tree):
                    T = T[item.copy()]
                else:
                    T = T[item]
        return newTree

    def copy(self):
        return self._copy(Tree())

    def setItem(self, key, value, flattend=True):
        """
        set static item
        """
        lower_nodes = [self]
        while len(lower_nodes) > 0:
            node = lower_nodes.pop()
            while node != None:
                if node._lower_node:
                    lower_nodes.append(node._lower_node)

                if isinstance(node.value, Tree) and flattend:
                    node.value.setItem(key, value);
                else:
                    if node.value == key:
                        node.value = value

                node = node._next_node

    def getItem(self, key, flattend=True):
        """
        get static item
        """
        lower_nodes = [self]
        while len(lower_nodes) > 0:
            node = lower_nodes.pop()
            while node != None:
                if node._lower_node:
                    lower_nodes.append(node._lower_node)

                if isinstance(node.value, Tree) and flattend:
                    n = node.value.getItem(key);
                    if n: return n;
                else:
                    if node.value == key:
                        return node

                node = node._next_node

    def setVariable(self, key, value, flattend=True):
        """
        set variable item
        """
        for path in self:
            for item in path:
                if isinstance(item, Tree.Variable):
                    if item.name == key:
                        item.value = value
                if isinstance(item, Tree) and flattend:
                    item.setVariable(key, value, flattend)
        
    def getVariable(self, key, flattend=True):
        """
        get variable item
        """
        for path in self:
            for item in path:
                if isinstance(item, Tree.Variable):
                    if item.name == key:
                        return item.value
                if isinstance(item, Tree) and flattend:
                    n = item.getVariable(key, flattend)
                    if n: return n;

    def flush(self, key, flattend=True):
        """
        updating variables and values (no garanteed success)
        """
        var = getVariable(key, flattend)
        setVariable(var.name, var.value, flattend)

    def toList(self, flattend=True):
        """
        convert to patlang List (of patlang List) ..
        """
        if isinstance(self, Tree.Variable) and flattend:
            if isinstance(self.value, Tree.Variable) and flattend:
                return List.Variable(self.name, self.value.toList())
            return List.Variable(self.name, self.value)
            
        returnlist = List()
        for path in self:
            pathlist = List()
            for item in path:
                if isinstance(item, Tree) and flattend:
                    pathlist.append(item.toList(flattend))
                else:
                    pathlist.append(item)
            returnlist.append(pathlist)

        if len(returnlist) > 1:
            return returnlist
        else:
            return list.__getitem__(returnlist, 0)

    def toString(self, flattend=True):
        """
        convert to patlang String
        """ 
        L = self.toList(flattend)
        return L.toString(flattend)
    
class VariableTree(Tree):
    """
    a Variable is a Pattern with a name
    """
    
    def __init__(self, name = "", value = Tree(), *args):
        super().__init__(value, *args)
        self.name = name

    def __repr__(self):
        return repr(self.name) + ":" + repr(self.value)
    
    def copy(self):
        newVariable = Tree.Variable(self.name)
        return self._copy(newVariable)

# propper alias
Tree.Variable = VariableTree
