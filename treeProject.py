def result(nodes):
    res = []
    for node in nodes:
        res.append(node.leafValue)
    return res


def AND(nodes):
    return min(result(nodes))

def OR(nodes):
  return max(result(nodes))

def arithmeticMean(nodes,bound):
    value = result(nodes)
    avg = sum(value)/len(value)
    if avg% 0.5 ==0 and bound=="UPPER":
        return avg+0.5
    elif avg% 0.5 ==0 and bound=="LOWER":
        return avg-0.5
    else:
        return round(avg)

def weightedMean(nodes,weights,bound):
    value = result(nodes)
    small = []
    large = []
    currentMean = 0
    valueWeights = dict(zip(value, weights))
    for key in valueWeights:
        if valueWeights[key]=="SMALL":
            small.append(key)
        else:
            large.append(key)

    if len(small)!=0:
        if len(small)==1:
            currentSmall=small[0]
        else:
            currentSmall = sum(small)/2
            if currentSmall%0.5==0 and bound=="UPPER":
                currentSmall+=0.5
            elif currentSmall%0.5==0 and bound=="LOWER":
                currentSmall-=0.5
            else:
                currentSmall=round(currentSmall)
    if len(large)!=0:
        if len(large)==1:
            currentLarge=large[0]
        else:
            currentLarge = sum(large)/2
            if currentLarge%0.5==0 and bound=="UPPER":
                currentLarge+=0.5
            elif currentLarge%0.5==0 and bound=="LOWER":
                currentLarge-=0.5
            else:
                currentLarge=round(currentLarge)

    if len(large)!=0 and len(small)!=0:
        if currentSmall==3 and currentLarge==1:
            if bound == "UPPER":
                currentMean=3
            elif bound=="LOWER":
                currentMean=2
        elif currentSmall==1 and currentLarge==2:
            currentMean=2
        elif currentSmall==1 and currentLarge==3:
            if bound=="UPPER":
                currentMean=2
            elif bound=="LOWER":
                currentMean=1
    elif len(large)!=0:
        return currentLarge
    else:
        return currentSmall
    return currentMean
class AggregationError(Exception):
    pass

class BoundError(Exception):
    pass

class LeafError(Exception):
    pass

class WeightError(Exception):
    pass

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None
        self.nodes = 0
        self.leafValue = None
        self.counter = 0
        self.agg_op = None
        self.bound = None
        self.values = {'LOW':1,'MEDIUM':2,'HIGH':3}
        self.weights = []
        self.weightBound = None
    def add_children(self, no_of_children):
        for i in range(1, no_of_children + 1):
            new_node = TreeNode(self.name + str(i))
            new_node.parent = self
            self.children.append(new_node)

    def set_nodes(self, no_of_children):
        self.nodes = no_of_children

    def iter_children(self):
        if self.nodes == 0:
            if len(self.children)==0:
                while True:
                    try:
                        inputValue = input("It is a leaf. Please enter the value of leaf low, medium, high:").strip().upper()
                        if inputValue not in ['LOW','MEDIUM','HIGH']:
                            raise LeafError
                        else:
                            break
                    except:
                        print("Please type any one of the three options")
                self.leafValue = self.values[inputValue]
            else:
                #apply aggregation operator on self.children
                if self.agg_op == 'AND':
                    self.leafValue=AND(self.children)
                elif self.agg_op == 'OR':
                    self.leafValue=OR(self.children)
                elif self.agg_op == 'ARITHMETIC MEAN':
                    self.leafValue=arithmeticMean(self.children,self.bound)
                elif self.agg_op == 'WEIGHTED MEAN':
                    self.leafValue = weightedMean(self.children,self.weights,self.weightBound)
            if self.parent is None:
                if self.leafValue == 1:
                    return "LOW"
                elif self.leafValue == 2:
                    return "MEDIUM"
                elif self.leafValue == 3:
                    return "HIGH"
                else:
                    print(self.leafValue)
            elif self.parent.counter == self.parent.nodes-1:
                    self.parent.nodes=0
                    return self.parent.iter_children()
            else:
                self.parent.counter+=1
                return self.parent.iter_children()
        else:
            while True:
                try:
                    children_count = int(input("Enter number of children of " + self.children[self.counter].name+":"))
                    break
                except ValueError:
                    print("Please enter an integer")
            while True:
                if children_count<=10:
                    if children_count!=0:
                        while True:
                            try:
                                self.children[self.counter].agg_op = input("Choose your aggregation operator: AND, OR, Arithmetic Mean or Weighted mean:").strip().upper()
                                if self.children[self.counter].agg_op not in ['AND','OR','ARITHMETIC MEAN','WEIGHTED MEAN']:
                                    raise AggregationError
                                else:
                                    break
                            except AggregationError:
                                print("Please type one of the four options")
                        if self.children[self.counter].agg_op=='ARITHMETIC MEAN':
                            while True:
                                try:
                                    self.children[self.counter].bound = input("Which bound would you want in case of uncertainty? Upper or Lower? ").strip().upper()
                                    if self.children[self.counter].bound not in ['UPPER','LOWER']:
                                        raise BoundError
                                    else:
                                        break
                                except:
                                    print("Please type one of the two options")

                    self.children[self.counter].add_children(children_count)
                    self.children[self.counter].set_nodes(children_count)
                    if self.children[self.counter].agg_op == 'WEIGHTED MEAN':
                        while True:
                            try:
                                self.children[self.counter].bound = input("Which bound would you want in case of uncertainty?Upper or Lower?").strip().upper()
                                if self.children[self.counter].bound not in ["UPPER","LOWER"]:
                                    raise BoundError
                                else:
                                    break
                            except BoundError:
                                print("Please type any one of the options")
                        for i in range(children_count):
                            while True:
                                try:
                                    weights = input("Choose Weight for "+self.children[self.counter].children[i].name+"Small or Large:").strip().upper()
                                    if weights not in ["SMALL","LARGE"]:
                                        raise WeightError
                                    break
                                except WeightError:
                                    print("Please type any one of the two options")

                            self.children[self.counter].weights.append(weights)
                    break
                else:
                    children_count = int(input("There can only be 10 children for max. Enter number of children of "+ self.children[self.counter].name+"again:"))
            return self.children[self.counter].iter_children()

root = TreeNode("X")
while True:
    try:
        no_of_children = int(input("Enter number of children:"))
        break
    except ValueError:
        print("Please enter an integer")
while True:
    if no_of_children<=10:
        root.add_children(no_of_children)
        root.set_nodes(no_of_children)
        while True:
            try:
                root.agg_op = input("Choose your aggregation operator: AND,OR,ARITHMETIC MEAN or WEIGHTED MEAN:").strip().upper()
                if root.agg_op not in ['AND','OR','ARITHMETIC MEAN','WEIGHTED MEAN']:
                    raise AggregationError
                else:
                    break
            except:
                print("Please type one of the four options")
        if root.agg_op == "ARITHMETIC MEAN":
            while True:
                try:
                    root.bound = input(
                        "Which bound would you want in case of uncertainty? Upper or Lower? ").strip().upper()
                    if root.bound not in ['UPPER', 'LOWER']:
                        raise BoundError
                    else:
                        break
                except:
                    print("Please type one of the two options")
        elif root.agg_op == "WEIGHTED MEAN":
            while True:
                try:
                    root.bound = input(
                        "Which bound would you want in case of uncertainty?Upper or Lower?").strip().upper()
                    if root.bound not in ["UPPER", "LOWER"]:
                        raise BoundError
                    break
                except BoundError:
                    print("Please type any one of the two options")
            for i in range(no_of_children):
                while True:
                    try:
                        weights = input(
                            "Choose Weight for " + root.children[i].name + "Small or Large:").strip().upper()
                        if weights not in ["SMALL", "LARGE"]:
                            raise WeightError
                        break
                    except WeightError:
                        print("Please type any one of the two options")
                root.weights.append(weights)

        print(root.iter_children())
        break
    else:
        no_of_children = int(input("There can be only 10 children for maximum. Enter number of children again:"))

