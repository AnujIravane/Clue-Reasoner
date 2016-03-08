import subprocess

def testKb(clauses):
    maxVar = 0
    for clause in clauses:
        for literal in clause:
            maxVar = max(abs(literal),maxVar)
    out = open('query.cnf','w')
    print >> out, 'c This DIMACS format CNF file was generated by SATSolver.py'
    print >> out, 'c Do not edit.'
    print >> out, 'p cnf',maxVar,len(clauses)
    for clause in clauses:
        for literal in clause:
            print >> out,literal,
        print >> out,'0'
    out.close();
    ##process = subprocess.Popen('zchaff query.cnf',stdout=subprocess.PIPE,shell=True)
    ##process.wait()
    ##stdout = process.stdout
    #stdout,stderr = process.communicate()
    #print stdout
    ##result = stdout.read().split()
    result1 = subprocess.check_output('~/Downloads/zchaff64/zchaff ~/hwk03/clue/query.cnf',shell=True)
    result = result1.split()
    ##stdout.close()
    it = iter(result)
    try:
        while it.next() != 'RESULT:':
            pass
        answer = it.next()
        if answer == 'SAT':
            return True
        elif answer == 'UNSAT':
            return False
        else:
            print "Error: SAT/UNSAT not indicated in query.cnf."
            return False
    except StopIteration:
            print "Error: Unexpected file end in query.cnf."
            return False


def testLiteral(literal,clauses):
    kb = clauses + [[literal]]
    if not testKb(kb):
        return False

    kb = clauses + [[-literal]]
    if not testKb(kb):
        return True

    return None

if __name__ == '__main__':
    clauses = [[-1,-2],[2 ,1],[-2,-3],[3,2],[-3,-1],[-3, -2],[1,2,3]]
    print 'Knowledge base is satisfiable:',testKb(clauses)
    print 'Is Cal a truth-teller?',
    result = testLiteral(3,clauses)
    if result==True:
        print 'Yes.'
    elif result==False:
        print 'No.'
    else:
        print 'Unknown.'
