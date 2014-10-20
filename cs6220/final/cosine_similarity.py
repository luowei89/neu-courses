import re, math
from collections import Counter

# copied from nltk.corpus.stopwords['english']
stopwords = [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now']
WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text.lower())
    return Counter([w for w in words if w not in stopwords])

def cosine_similarity(text1,text2):
    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)
    return get_cosine(vector1, vector2)

if __name__ == '__main__':
	text1 = 'Sub-50nm CMOS technologies are affected by significant variability, which causes power and performance variations among nominally similar cores in MPSoC platforms. This undesired heterogeneity threatens execution predictability and energy efficiency. We propose two techniques to allocate sets of barrier-synchronized tasks. The first technique models allocation as an ILP and achieves optimal results, but requires an offline solver. The second technique adopts a two-stage heuristic approach, and it can be adapted to work online. We tested our approach on the virtual prototype of a next-generation industrial multicore platform. Experimental results demonstrate that our approach minimizes deadline violations while increasing energy efficiency.'
	text2 = 'The complexity and physical distribution of modern active safety, chassis, and powertrain automotive applications requires the use of distributed architectures. Complex functions designed as networks of function blocks exchanging signal information are deployed onto the physical HW and implemented in a SW architecture consisting of a set of tasks and messages. The typical configuration features priority-based scheduling of tasks and messages and imposes end-to-end deadlines. In this work, we present and compare formulations and procedures for the optimization of the task allocation, the signal to message mapping, and the assignment of priorities to tasks and messages in order to meet end-to-end deadline constraints and minimize latencies. Our formulations leverage worst-case response time analysis within a mixed integer linear optimization framework and are compared for performance against a simulated annealing implementation. The methods are applied for evaluation to an automotive case study of complexity comparable to industrial design problems.'

	print cosine_similarity(text1,text2)