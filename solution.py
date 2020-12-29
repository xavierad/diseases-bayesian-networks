import probability
from itertools import product

#Work done by Guilherme Atanásio, nº87013, and Xavier Dias, nº 87136.

class MDProblem:
    """
    MDProblem is a class that contains a method to build a list of child-parents with the corresponding conditional probability table to
    the Bayes network and a method to solve the problem with variable elimination algorithm.
    """
    def __init__(self, fh):
        """
        Input: a opened file header object
        Description: initializes a MDProblem object by loading the file content and creating the corresponding bayesian network.
        """
        
        # loading the the file
        self.diseases, self.symptoms, self.exams, self.results, self.prob, self.T = load(fh)

        # creating the bayesian network
        self.MDnet = probability.BayesNet(self.getChildParentsList())
        

    def getChildParentsList(self):
        """ Input: none.
            Output: a child-parents list (cpl), a list of tuples.
            Description: this method returns a list of tuples, where each tuple contains the node, the parents and the corresponding
            conditional probabilities table (cpt). Initially, at the first time-step, the probability of a patient having a disease 
            is 0.5. For the the remaining time-steps, the cpts of each node is constrained by the propagation law. A cpt is a dictionary
            for nodes with parents. Otherwise it's only a probability value. 
        """

        T, F = True,  False
        
        # the returning child-parents list
        cpl = []
        
        # for each time-step add all the parents of each disease node
        for t in range(self.T):
            for disease in self.diseases:
                if t == 0: # since the first node has no parents
                    cpl.append((disease + str(t), '', 0.5))
                else:
                    parents = disease + str(t-1) + ' '  # the list of parents of the current disease
                    already_in_list_disease = [disease] # a list to make sure that the parent diseases are not repeated
                    for s_disease in self.symptoms.values():
                        if disease in s_disease:        # go over the list of symptoms and check if the disease is part of it
                            for x in s_disease:         # if True, take every other disease with that sympthom
                                if x not in already_in_list_disease: # except the ones that are already in the list
                                    parents = parents + x + str(t-1) + ' '
                                    already_in_list_disease.append(x)                        
                    
                    # to build the cpt dictionary it's necessary to build the truth table, made with product() function
                    # where it receives a list of values to be and the number of collumns of the table.
                    nparents = len(already_in_list_disease)
                    cpt_dict = {}
                    truth_table = list(product([T, F], repeat=nparents)) # generate all the combinations of True and False

                    # for each combination of True and False
                    for row in truth_table:                   
                        if row[0] == F:       # from rule 1: if we didn't have a disease at time t, we won't have it at time t+1
                            cpt_dict[row] = 0 # therefore the probability is 0.
                        else:
                            if not any(row[1:]):   # from rule 3: if we have a disease at time t and don't have any other disease with sharing sympthoms
                                cpt_dict[row] = 1  # at time t+1, then the probability of having that disease (at t+1) is 1.
                            else:
                                cpt_dict[row] = float(self.prob)  # from rule 2: if at time t we had a disease, at t+1 the probability of having it is              
                                                                  # the propagation probability, in case we have another disease with the sharing sympthoms

                    cpl.append((disease + str(t), parents[:-1], cpt_dict))

        # to add exam result childs to corresponding diseases at the corresponding time-step
        for t, exam in enumerate(self.results):
            for code in exam.keys():
                disease = self.exams[code]['disease'] # to get the disease corresponding to exam
                tpr = self.exams[code]['tpr'] # to get the corresponding tpr
                fpr = self.exams[code]['fpr'] # to get the corresponding fpr

                parent =  disease + str(t) # at time-step t, the disease is parent of the exam result
                cpl.append((code+str(t), parent, {T:tpr, F:fpr})) # tpr and fpr are the conditional probabilities (tpr = P(result | disease))
        
        return cpl


    def solve(self):
        """ Input: None.
            Output: The disease with the highest likelihood of being true and it's likelihood.
            Description: From the results of the exams, a dictionary is created where each key is an (exam + its respective timestamp)
            and the value, the respective result (True or False). After this, this dictionary is used to compute the probability of having
            each disease on the last timestamp, using the provided probability.elimination_ask function, and then, the one with the highest
            likelihood is choosen and returned.
        """

        # turn the test results in a single dictionary with the correct timestamp for each exam
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
            # compute the likelihood of having each disease on the last timestamp
            prob[disease] = probability.elimination_ask(disease + str(self.T - 1), test_results, self.MDnet).show_approx('{:.8g}')
            
            # take the last word from the string (the true value) and turn it into a float.
            final_probability[disease] = float(prob[disease].split()[-1:][0])

        disease = max(final_probability, key=final_probability.get) # take the disease with the maximum likehood
        likelihood = final_probability[disease]
        
        return disease, likelihood

    


def load(f):      
    """ Input: file object f (opened)
        Ouput: A list of diseases, a dictionary of symptoms, dictionary of exams, a list 
        of results, the propagation probability (prob), and the maximum timestep T.
        Description: Loads a problem from a (opened) file object f. All the useful information is retrieved and saved.
    """
    
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
