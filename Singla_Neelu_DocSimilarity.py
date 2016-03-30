import os
import itertools
import sys

def get_LHS(signature, threshold_value, no_of_hashes_for_minhashing ):
    factors=[]
    i=1
    while i<= no_of_hashes_for_minhashing:
        if no_of_hashes_for_minhashing%i==0:
            factors.append([i,no_of_hashes_for_minhashing/i])
        i=i+1

    distance={}
    counter=0
    for factor in factors:
        val=(1/float(factor[0]))**(1/float(factor[1]))
        if val<threshold_value:
            distance[counter]=threshold_value-val
        counter = counter+1

    min=99999999
    dvalue=0
    for i in distance:
        if distance[i]<min:
            min=distance[i]
            dvalue=i

    hashing_bucket={}
    indexed_value=0
    starting_counter=indexed_value
    for i in range(factors[dvalue][0]):
        hashing_bucket[i]={}
        for bn in range(20000):
            hashing_bucket[i][bn]=[]

        for document in signature:
            row_values=[]
            index=0
            indexed_value=int(starting_counter)
            while index <factors[dvalue][1]:
                row_values.append(signature[document][indexed_value]*(index+1))
                index= index + 1
                indexed_value = indexed_value + 1

            sum=0
            for val in row_values:
                sum+=val
            bnr=sum % 20000
            if hashing_bucket[i][bnr]:
                hashing_bucket[i][bnr].append(document)
            else:
                hashing_bucket[i][bnr]=[document]

        starting_counter+=factors[dvalue][1]

    data_formed_by_LHS=set()
    for bo in range(factors[dvalue][0]):
        for bn in range(20000):
            if len(hashing_bucket[bo][bn])>1:
                pairs_formed=itertools.combinations(hashing_bucket[bo][bn],2)
                for combination in pairs_formed:
                    data_formed_by_LHS.add(tuple(combination))

    data_formed_by_LHS=sorted(data_formed_by_LHS)
    for item in data_formed_by_LHS:
        print(item)


def get_jakard_similarity_for_min_hashing(signature, no_of_hashes_for_minhashing):
    pairs_formed= itertools.combinations(signature, 2)
    for document in pairs_formed:
        sum=0
        for i in range(no_of_hashes_for_minhashing):
            if signature[document[0]][i]==signature[document[1]][i]:
                sum=sum+1.0

        val=float(sum)/float(no_of_hashes_for_minhashing)
        print("Jaccard Similarity between "+ document[0] + " and "+ document[1]+":"+ str(val))

def get_min_hashing_signature(list_of_shingles, no_of_hashes_for_minhashing ):
    signature={}
    set_with_all_shingles=set()
    for document in list_of_shingles:
        set_with_all_shingles=set_with_all_shingles | set(list_of_shingles[document])
    set_with_all_shingles=sorted(set_with_all_shingles)

    list_of_hash_functions={}
    for index in range(1, no_of_hashes_for_minhashing+1):
        list_of_hash_functions[index]=[]
        for indexed_value in range(len(set_with_all_shingles)):
            list_of_hash_functions[index].append((index*indexed_value+1) % len(set_with_all_shingles))

    matrix={}
    for document in list_of_shingles:
        matrix[document]=[]
        for w in set_with_all_shingles:
            if w in list_of_shingles[document]:
                matrix[document].append(1)
            else:
                matrix[document].append(0)

    for document in matrix:
        signature[document]=[]
        val=0
        for index in range(no_of_hashes_for_minhashing):
            signature[document].append(999999999)
        for hash in list_of_hash_functions:
            for indexed_value in range(len(matrix[document])):
                if matrix[document][indexed_value]==1:
                    temp_list=[signature[document][hash-1],list_of_hash_functions[hash][indexed_value]]
                    signature[document][val]=min(temp_list)
            val= val+ 1
    return signature

def get_jakard_similarity(list_of_shingles):
    pairs_formed= itertools.combinations(list_of_shingles, 2)
    for documents in pairs_formed:
        intersection_value= len(set(list_of_shingles[documents[0]]).intersection(list_of_shingles[documents[1]]))
        union_value=len(list_of_shingles[documents[0]])+len(list_of_shingles[documents[1]])- intersection_value
        percentage=float(intersection_value)/float(union_value)
        print("Jaccard Similarity between " +  documents[0] + " and " + documents[1] + ":" + str(percentage))


def create_shingles(all_documents, shingle_type, size_of_shingle_window):
    shingles_dictionary={}
    for doc in all_documents:
        if shingle_type=="char":
             file1= open(doc)
             data= file1.read()
             doc_shingles=[]
             i=0
             j=size_of_shingle_window
             while j <= len(data) :
                print(data[i:j])
                if data[i:j] not in doc_shingles:
                    doc_shingles.append(data[i:j])
                j = j+1
                i = i +1

             shingles_dictionary[doc]=doc_shingles

        elif shingle_type=="word":
            file= open(doc)
            data= file.read().split()
            doc_shingles=[]
            i=0
            j=size_of_shingle_window
            while j <= len(data) :
                if "".join(data[i:j]) not in doc_shingles:
                    doc_shingles.append("".join(data[i:j]))
                j = j+1
                i = i +1

            shingles_dictionary[doc]=doc_shingles

    for doc_name in shingles_dictionary:
        print("No of Shingles in File " +  doc_name + ":" + str(len(shingles_dictionary[doc_name])))
    return shingles_dictionary

if __name__=='__main__':
	folder_path_containing_docs=sys.argv[1]
	size_of_shingle_window=int(sys.argv[2])
	shingle_type=sys.argv[3]
	no_of_hashes_for_minhashing=int(sys.argv[4])
	threshold_value=float(sys.argv[5])

all_documents=[]
for file in os.listdir(folder_path_containing_docs):
    if file.endswith(".txt"):
        all_documents.append(folder_path_containing_docs+"\\"+file)


list_of_shingles= create_shingles(all_documents, shingle_type, size_of_shingle_window)
print("")
get_jakard_similarity(list_of_shingles)
print("")
print("Min-Hash Signature for the Documents")
signature = get_min_hashing_signature(list_of_shingles, no_of_hashes_for_minhashing )
for document in signature:
	print(document+ ": "+ str(signature[document]))
print("")
get_jakard_similarity_for_min_hashing(signature, no_of_hashes_for_minhashing)
print("")
print("Candidate Pairs obtained using LSH")
get_LHS(signature, threshold_value, no_of_hashes_for_minhashing )