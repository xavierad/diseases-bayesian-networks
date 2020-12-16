# import probability

class MDProblem:
    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet () to create the Bayesian network.
        
        load(fh)

        # probability.BayesNet()
        pass

    def solve(self):
        # Place here your code to determine the maximum likelihood
        # solution returning the solution disease name and likelihood.
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
    # return diseases, symptoms, exams, results, probs


if __name__ == "__main__":
    import sys

    fh = open(sys.argv[1])
    MDProblem(fh)
