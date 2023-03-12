import math
import numpy as np 
import pandas as pd 
import graphviz
from src.Class_arbre import *
from src.Class_math import *
from src.Class_graph import *

class class_Prediction:
    
    def __init__(self,data):
        self.calc = Class_math(data) 
        self.labels = data[0]

        
    def confusionMatrix(self,list_arcs,data):
        '''
        Génère un matice de forme array avec toutes les données de la matrice de confusion. 

        Parameters
        ----------
        list_arcs : list des arcs
            chaque arc possède un node père, un node fil, le poid de l'arc et un id propre de
            chaque arc.
        data : Matrice
            jeu de données

        Returns
        -------
        matrix : array
        '''
        info = data
        pred_possibles = self.calc.getValeursPosibles(self.labels[len(self.labels)-1],data)
        info.pop(0)
        matrix = np.zeros((len(pred_possibles),len(pred_possibles)))
        
        for ligne in info:
            
            pred_arbre = self.prediction(list_arcs,ligne)
            pred_ligne = ligne[len(ligne)-1]
            self.update_matrix(matrix, pred_arbre, pred_ligne,pred_possibles)
        
        return matrix 
            
    def prediction(self, list_arcs,ligne_pred):
        '''
        

        Parameters
        ----------
        list_arcs : list des arcs
            chaque arc possède un node père, un node fil, le poid de l'arc et un id propre de
            chaque arc.
        ligne_pred : List 
            List avec toutes les données qu'on va alimente à notre arbre de décision

        Returns
        -------
        String
            String avec la décision prise par l’arbre de décision.
        '''
        id_arc = list_arcs[0].getFather().getID()
        ind_arc = 0
        for ind,arc in enumerate(list_arcs):
            if arc.getFather().getID() == id_arc : 
                for val in (ligne_pred):
                    if (arc.getWeight() == val):
                        id_arc = arc.getSon().getID()
                        ind_arc = ind
        return list_arcs[ind_arc].getSon().getValue()
           
    def update_matrix (self,matrix,pred_arbre,pred_test,possibilites):
        '''
        Permet d'augmenter la valeur d'un case dans une matrice de confusion en 1

        Parameters
        ----------
        matrix : List de list
            Matrice dont on va changer la valeur.
        pred_arbre : String 
            Prediction généré par l'arbre de décision
        pred_test : String
            Prediction réelle
        possibilites : Liste String
            Liste avec toutes les possibilités des reponses donnees par l'arbre de décision.

        Returns
        -------
        None.

        '''
        x = self.getIndice(pred_arbre,possibilites)
        y = self.getIndice(pred_test,possibilites)
        matrix[y][x] += 1

        
    def getIndice (self,value, possibilites):
        '''
        Donne la position dans une liste de string d'un valeur (String) donné en paramètre

        Parameters
        ----------
        value : String
            
        possibilites : String Liste
            

        Returns
        -------
        Int 
            position dans la liste

        '''
        for i,val in enumerate(possibilites):
            if val==value:
                return i-1

         
            
        