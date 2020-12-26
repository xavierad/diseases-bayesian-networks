import probability
from itertools import product, combinations

class MDProblem:
    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet () to create the Bayesian network.
        
        # loading the the file
        self.diseases, self.symptoms, self.exams, self.results, self.prob, self.T = load(fh)

        # creating the bayesian network
        self.MDnet = probability.BayesNet(self.getChildParentsList())
        

    # maybe improve this algorithm....
    def getChildParentsList(self):
        cpl = []        
        aux_diseases = {d:[] for d in self.diseases}
        prob_init = 1
        
        edges = []
        for diseases in self.symptoms.values():
            edges += list(combinations(diseases,2))
        
        print(f'\nedges {edges}')
        
        for edge in edges:
            # make the first disease as parent
            parent = edge[0]
            if aux_diseases[parent] == []:
                aux_diseases[parent] = ''

            if aux_diseases[edge[1]] == '':
                aux_diseases[edge[1]] = [parent]
            else:
                aux_diseases[edge[1]].append(parent)

        values = [True, False]
        for disease in aux_diseases.keys():      

            nparents = len(aux_diseases[disease])            
            if nparents > 1:
                string = ''
                for d in aux_diseases[disease]:
                    if string == '':
                        string += d
                    else:
                        string += ' ' + d

                aux_diseases[disease] = [string]

                cpd_dict = {}
                truthTable = list(product(values,repeat=nparents))
                for row in truthTable:
                    cpd_dict[row] = prob_init
                aux_diseases[disease].append(cpd_dict)

            elif nparents == 1:
                cpd_dict = {}
                cpd_dict[True] = prob_init
                cpd_dict[False] = 1- prob_init
                aux_diseases[disease].append(cpd_dict)

            else:
                aux_diseases[disease] = [aux_diseases[disease]]
                aux_diseases[disease].append(prob_init)

        # print(aux_diseases)
        cpl = [tuple([k]+v) for k, v in aux_diseases.items()] 
        
        print(f'\ncpl {cpl}')        
        
        return cpl


    def solve(self):
        # Place here your code to determine the maximum likelihood
        # solution returning the solution disease name and likelihood.
        # Use probability.elimination_ask () to perform probabilistic
        # inference .        
        # for time in self.T:


        prob = probability.elimination_ask('covid', dict(flu=True, common_cold=True), self.MDnet).show_approx()
        print(prob)

        # return (disease, likelihood)

    


def load(f):      
    """ Input: file object f (opened)
        Ouput: None
        Description: Loads a problem from a (opened) file object f. Here we assign the initial 
        and goal states as such we retrieve all useful values from f to solve the problem."""
    
    # Some auxiliar lists and dictionaries
    diseases = []
    symptoms = {}
    exams = {}
    results = []
    prob = []
    T = 0

    # Beginnig of reading the file
    info = f.readlines()
    for line in info:
        string = line.split()
        if string != []:
            # Retrievement of all values correspondent to diseases
            if string[0] == 'D':
                # storing all diseases
                diseases = string[1:] 

            # Retrievement of all values correspondent to symptoms
            elif string[0] == 'S':
                code = string[1]
                symptoms[code] = string[2:] #assigning all diseases to the symptom

            # Retrievement of all values correspondent to exams
            elif string[0] == 'E':
                code = string[1]        
                exams[code] = {'d':string[2], 'tpr':string[3], 'fpr':string[4]} 

            # Retrievement of exams results
            elif string[0] == 'M':
                codes = string[1::2]
                values = string[2::2]
                results.append(dict(x for x in zip(codes,values)))
                T += 1 # to get the total time

            # Retrievement of propagation probabilities
            elif string[0] == 'P':
                prob = string[1]
    
    print(f'Diseases: {diseases}\nSymptoms: {symptoms}\nExams: {exams}\nResults: {results}\nProb: {prob}\nT = {T}')
    return diseases, symptoms, exams, results, prob, T


if __name__ == "__main__":
    import sys

    fh = open(sys.argv[1])
    MDProblem(fh).solve()
