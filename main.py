from gen import Generation


generation = Generation()
i=0
while(1):
    print("GENERATION ",i)
    generation.survive()
    generation.breed_and_mutate()
    i+=1
