import numpy as np

def calc_entropy(probabilities):

    if probabilities != 0:
        return -probabilities * math.log2(p)
    else:
        return 0

def calc_info_gains(data, feature):

    loss = 0
    values = []

    for instance in data:
        if instance[feature] not in values:
            values.append(instance[feature])

    for value in values:

        sublist_feature = [x for x in x[feature] == value]

        frequency = {}
        total = 0

        for instance in sublist_feature:
            if i[-1] in frequency.keys():
                frequency[instance[-1]] += 1
            else:
                frequency[instance[-1]] = 1;

            total += 1

        for key in frequency.keys():
            frequency[key] = frequency[key] / total

        entropy = calc_entropy(frequency)

        loss = (len(sublist_feature) / len(data)) * entropy

    return loss

def make_tree(data, feature):

    if len(data) == 0:
        return 0

    targets = [x[-1] for x in data]
    test_targets = np.full_like(targets, targets[0])
    if np.array_equal(targets, test_targets):
        return targets[0]

    else:
        node = ID3()

        gains = np.zeros(len(feature))

        for i in range(len(feature)):
            gains[i] = calc_info_gains(data, feature)

        smallest_value = np.argmin(gains)
        new_feature = feature[smallest_value]
        value = [x[new_feature] for x in data]
        values = set(value)

        node.attribute = new_feature

        for v in values:
            d = [x for x in data if x[new_feature] == v]
            f = copy.deepcopy(feature)
            f.remove(new_feature)

            sub_tree = make_tree(d, f)

            node.branches[v] = sub_tree

        return node

class DecisionTreeClassifier:

    def __init__(self):
        self.data = ""
        self.target = ""
        self.root = ""


    def fit_data(self, data, target):
        self.train_data(data, target)

    def train_data(self, data, target):
        self.data = data
        self.target = target

        target = target.reshape(-1, 1)
        data_target = np.append(data, target, axis=1)

        feature = []

        for i in range(self.data.shape[1]):
            feature.append(i);

        self.root = make_tree(data_target, feature)

        self.print_tree(self.root, 0)

    def predict_data(self, data):

        predict = []

        for i in data:
            predict.append(self.look_tree(i, self.root))

        return predict

    def traverse_tree(self, i, node):

        if i[node.attribute] not in node.branches.keys():
            return 0

        tree_branch = node.branches[i[node.attribute]]

        if isinstance(tree_branch, ID3):
            return self.traverse_tree(i, tree_branch)
        else:
            return node.branches[i[node.attribute]]



    def print_tree(self, node, node_level):


        if isinstance(node, ID3):
            print("Node: ", node.attr_index)
            print("Children: ")
            for key, v in node.branches.items():
                print(key, ": ")
                self.print_tree(v, node_level + 1)

        else:
            print(node)

class ID3:

    def __init__(self):
        self.attribute = 0
        self.branches = {}