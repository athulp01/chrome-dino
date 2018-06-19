import numpy as np
import random
import cv2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from network import Genome
import time
import copy


class Generation:
    def __init__(self):
        self.genomes = [Genome() for i in range(12)]
        self.fittest = []
        self.browser = webdriver.Chrome()
        self.browser.get("chrome://dino")
        self.canvas = self.browser.find_element_by_id('t')
        self.others = []


    def survive(self):
        for i,genome in enumerate(self.genomes):
            self.canvas.send_keys(Keys.SPACE)
            while(1):
                try:
                    dist = (self.browser.execute_script('return Runner.instance_.horizon.obstacles[0].xPos')) - 24
                    speed = (self.browser.execute_script('return Runner.instance_.currentSpeed'))
                except:
                    dist=0
                    speed=0

                if dist < 0:
                    dist = 0
                output = genome.out(dist/1000,speed/10)
                if(output > 0.55):
                    self.canvas.send_keys(Keys.SPACE)

                if self.browser.execute_script('return Runner.instance_.crashed') == True:
                    genome.fitness = int(self.browser.execute_script('return Runner.instance_.distanceRan'))
                    print(genome.fitness)
                    self.browser.execute_script('Runner.instance_.restart()')
                    break

        self.genomes.sort(key=lambda x: x.fitness, reverse=True)
        for g in self.genomes:
            print("Fitness = ",g.fitness)
        self.fittest = self.genomes[:4]
        self.others = self.genomes[4:]
        self.genomes = self.fittest


    def breed_and_mutate(self):
        while len(self.genomes) < 8:
            g1 = np.random.choice(self.fittest)
            g2 = np.random.choice(self.fittest)
            print("Crossing ",g1.fitness,'and',g2.fitness)
            self.genomes.append(self.cross_over(self.mutate(g1), self.mutate(g2)))
        while len(self.genomes) < 12:
            g1 = np.random.choice(self.fittest)
            g2 = np.random.choice(self.others)
            self.genomes.append(self.cross_over(self.mutate(g1),self.mutate(g2)))

    def cross_over(self, g1, g2):
        new_genome = copy.deepcopy(g1)
        other_genome = copy.deepcopy(g2)
        for j in range(0,2):
            cut_loc = int(len(new_genome.w1[j])*np.random.uniform(0, 1))
            print("cutting at ",cut_loc)
            for i in range(cut_loc):
                new_genome.w1[j][i],g2.w1[j][i] = g2.w1[j][i], new_genome.w1[j][i]

        cut_loc = int(len(new_genome.w2)*np.random.uniform(0, 1))
        print("cutting at ",cut_loc)
        for i in range(cut_loc):
            new_genome.w2[i][0],g2.w2[i][0] = g2.w2[i][0], new_genome.w2[i][0]
        return new_genome

    def mutate_weights(self, weights):
        if np.random.uniform(0, 1) < 0.2:
            print("mutated")
            return weights * (np.random.uniform(0, 1) - 0.5) * 3 + (random.uniform(0, 1) - 0.5)
        else:
            return 0

    def mutate(self,g):
        new_genome = copy.deepcopy(g)
        new_genome.w1 += self.mutate_weights(new_genome.w1)
        new_genome.w2 += self.mutate_weights(new_genome.w2)
        return new_genome



