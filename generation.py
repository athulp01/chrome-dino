import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from network import Genome
import pickle
import copy


class Generation:
    def __init__(self):
        try:
            file = open("netData.pkl",'rb')
            self.genomes = pickle.load(file)
            print("Loading from the previous state")
        except:
            print("Creating new genomes")
            self.genomes = [Genome() for i in range(12)]

        self.fittest = []
        self.loosers = []

        self.browser = webdriver.Chrome()
        self.browser.get("chrome://dino")
        self.canvas = self.browser.find_element_by_id('t')
        self.canvas.send_keys(Keys.SPACE)

    def survive(self):
        for i,genome in enumerate(self.genomes):
            while(1):
                try:
                    ypos = (self.browser.execute_script('return Runner.instance_.horizon.obstacles[0].yPos'))
                    dist = (self.browser.execute_script('return Runner.instance_.horizon.obstacles[0].xPos')) - 24
                    speed = (self.browser.execute_script('return Runner.instance_.currentSpeed'))
                except:
                    dist=0
                    speed=0
                    ypos =0

                output = genome.out(dist/1000,ypos/100,speed/10)   #normalizing input
                #print(output)

                if(np.argmax(output) == 1):
                    self.canvas.send_keys(Keys.ARROW_UP)              #jump
                else:
                    if(np.argmax(output) == 2):
                        self.canvas.send_keys(Keys.ARROW_DOWN)          

                if self.browser.execute_script('return Runner.instance_.crashed') == True:
                    genome.fitness = int(self.browser.execute_script('return Runner.instance_.distanceRan'))
                    self.browser.execute_script('Runner.instance_.restart()')
                    break

        self.genomes.sort(key=lambda x: x.fitness, reverse=True)
        self.fittest = self.genomes[:4]
        self.loosers = self.genomes[4:]
        print(" Fitness = ", self.fittest[0].fitness)
        self.genomes = self.fittest


    def breed_and_mutate(self):
        while len(self.genomes) < 8:                    #breeding among the fittest
            g1 = np.random.choice(self.fittest)
            g2 = np.random.choice(self.fittest)
            self.genomes.append(self.cross_over(self.mutate(g1), self.mutate(g2)))
        while len(self.genomes) < 12:                   #breeding the fittest with the loosers
            g1 = np.random.choice(self.fittest)
            g2 = np.random.choice(self.loosers)
            self.genomes.append(self.cross_over(self.mutate(g1),self.mutate(g2)))

    def cross_over(self, g1, g2):
        new_genome = copy.deepcopy(g1)
        other_genome = copy.deepcopy(g2)
        for j in range(0,3):
            cut_loc = int(len(new_genome.w1[j])*np.random.uniform(0, 1))        #cutting at random position
            for i in range(cut_loc):
                new_genome.w1[j][i],g2.w1[j][i] = g2.w1[j][i], new_genome.w1[j][i]

        for j in range(0,6):
            cut_loc = int(len(new_genome.w2[j])*np.random.uniform(0, 1))        #cutting at random position
            for i in range(cut_loc):
                new_genome.w2[j][i],g2.w2[j][i] = g2.w2[j][i], new_genome.w2[j][i]
        return new_genome

    def mutate_weights(self, weights):
        if np.random.uniform(0, 1) < 0.2:
            print("An individual is mutated")
            return weights * (np.random.uniform(0, 1) - 0.5) * 3 + (np.random.uniform(0, 1) - 0.5)
        else:
            return 0

    def mutate(self,g):
        new_genome = copy.deepcopy(g)
        new_genome.w1 += self.mutate_weights(new_genome.w1)
        new_genome.w2 += self.mutate_weights(new_genome.w2)
        return new_genome



