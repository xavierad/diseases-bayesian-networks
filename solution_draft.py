import probability

class MDProblem:
    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability . BayesNet () to create the Bayesian network .
        pass

    def solve(self):
        # Place here your code to determine the maximum likelihood
        # solution returning the solution disease name and likelihood .
        # Use probability . elimination_ask () to perform probabilistic
        # inference .        
        return (disease, likelihood)






def load(f):      
    """ Input: file object f (opened)
        Ouput: None
        Description: Loads a problem from a (opened) file object f. Here we assign the initial 
        and goal states as such we retrieve all useful values from f to solve the problem."""
    
    # Some auxiliar lists and dictionaries
    diseases = []
    symptoms = {}
    exams = {}
    results = {}
    probs = []

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
                exams[code] = string[2] # assigning the disease
                exams[code]['tpr'] = string[3] # assigning TPR
                exams[code]['fpr'] = string[4] # assigning FPR

            # Retrievement of exams results
            elif string[0] == 'M':
                codes = string[1::2]
                values = string[2::2]
                results = dict(x for x in zip(codes,values))

            # Retrievement of propagation probabilities
            elif string[0] == 'P':
                probs = string[1]

    return diseases, symptoms, exams, results, probs