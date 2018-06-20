from gen import Generation
import pickle

generation = Generation()
i=0
while(1):
    print("GENERATION -> ",i+1,end='')
    generation.survive()
    generation.breed_and_mutate()
    i+=1
