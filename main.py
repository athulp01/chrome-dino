from generation import Generation
import pickle

gen = Generation()
i=0
while(1):
    print("GENERATION -> ",i+1,end='')
    gen.survive()
    gen.breed_and_mutate()
    i+=1
