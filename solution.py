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
        
        T, F = True, False
        cpl = []
        
        for t in range(self.T):
            for disease in self.diseases:
                if t == 0:
                    cpl.append((disease + str(t), '', 0.5))
                else:
                    #Add all the parents from the current disease node
                    parents = disease + str(t-1) + ' '
                    already_in_list_disease = [disease]
                    for s_disease in self.symptoms.values():
                        if disease in s_disease:
                            for x in s_disease:
                                if x not in already_in_list_disease:
                                    parents = parents + x + str(t-1) + ' '
                                    already_in_list_disease.append(x)                        
                    
                    nparents = len(already_in_list_disease)
                    cpd_dict = {}
                    truth_table = list(product([T, F],repeat=nparents))
                    for row in truth_table:                        
                        if row[0] == F:
                            cpd_dict[row] = 0
                        else:
                            if not any(row[1:]):
                                cpd_dict[row] = 1
                            else:
                                cpd_dict[row] = float(self.prob)                


                    cpl.append((disease + str(t), parents[:-1], cpd_dict))

        # to add result childs to corresponding diseases at corresponding time-step
        for t, exam in enumerate(self.results):
            for code in exam.keys():
                disease = self.exams[code]['disease'] # to get the disease corresponding to exam
                tpr = self.exams[code]['tpr'] # to get the corresponding tpr
                fpr = self.exams[code]['fpr'] # to get the corresponding fpr

                parent =  disease + str(t) # at time-step t, the disease is parent of the exam result
                cpl.append((code+str(t), parent, {T:tpr, F:fpr}))     
        
        return cpl


    def solve(self):
        # Place here your code to determine the maximum likelihood
        # solution returning the solution disease name and likelihood.
        # Use probability.elimination_ask () to perform probabilistic
        # inference .        

        test_results = {}
        for t, exams in enumerate(self.results):
            for exam, value in exams.items():
                if value == 'T':
                    test_results[exam+str(t)] = True
                else:
                    test_results[exam+str(t)] = False

        prob = {}
        final_probability = {}
        for disease in self.diseases:
            prob[disease] = probability.elimination_ask(disease + str(self.T - 1), test_results, self.MDnet).show_approx('{:.8g}')
            final_probability[disease] = float(prob[disease].split()[-1:][0])

        disease = max(final_probability, key=final_probability.get)
        likelihood = final_probability[disease]
        
        # print(disease, likelihood)
        return disease, likelihood

    


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
                exams[code] = {'disease':string[2], 'tpr':float(string[3]), 'fpr':float(string[4])} 
                
            # Retrievement of exams results
            elif string[0] == 'M':
                codes = string[1::2]
                values = string[2::2]
                results.append(dict(x for x in zip(codes,values)))
                T += 1 # to get the total time

            # Retrievement of propagation probabilities
            elif string[0] == 'P':
                prob = string[1]
    
    return diseases, symptoms, exams, results, prob, T


# if __name__ == "__main__":
#     import sys

#     fh = open(sys.argv[1])
#     MDProblem(fh).solve()
