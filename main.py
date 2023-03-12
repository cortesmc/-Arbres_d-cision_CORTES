
"""
PROJ631 - Projet Algorithmique
Arbres de décision - ID3
"""

import csv
import math
import graphviz
from sklearn.metrics import confusion_matrix
from src.Class_arbre import *
from src.Class_math import *
from src.class_Prediction import *
from src.Class_graph import *

if __name__ == "__main__":
    '''
    Extaction des données des fichiers .csv
    '''
    
    data_app = []
    data_pred = []
    with open("./soybean-app.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            data_app.append(row)
            
    with open("./soybean-pred.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            data_pred.append(row)
         
    data_apprentisage = data_app #Ici on peut sélectionner le nom du jeu de données générer l’arbre de décision.
    data_prediction = data_pred #Ici on peut sélectionner le nom du jeu de données pour trouver et afficher la matrice de confusion.

    calc = Class_math(data_apprentisage)  
    '''
    Nettoyage des données par l'élimination des toutes les lignes qu’ont des données 
    manquantes (== ?)
    '''
    data_apprentisage = calc.clean_data(data_apprentisage)
    
    root = Node(calc.choixAttCible(),0) #Définition de la racine de l’arbre
    
    values_arc = calc.getValeursPosibles(root.getValue())
    
    list_arc = [] #Liste dans laquelle on va stocker tous les arcs qui vont former l’arbre de décision.

    
    for value in values_arc:
        arc = Arc(value, root)
        list_arc.append(arc)
    
    '''
    En préparant l’information et variables nécessaires pour générer l’arbre.    
    '''
    list_arc_copy = list_arc.copy()
    cpt = 0
    fatherNode = list_arc_copy[0].getFather()
    dataSet = data_apprentisage
    fatherNodeValue = list_arc_copy[0].getFather().getValue()
    arc_weight = list_arc_copy[0].getWeight()
    
    '''
    Boucle de création de l’arbre on utilise un copie de la list des arc qu’on utilise en 
    itération de type FIFO pour générer l’arbre:
        1. Définir les jeux des données dans lesquels on va prendre les mesures de gain.
        
        2. Vérification des jeux de données est vide ou si le choix d'attribuer cible 
        trouve à partir du jeu de données est une feuille de l’arbre et on l'ajoute à 
        l’arc comme node fils.
        
        3. Si la deuxième condition n’est pas vérifiée, on crée une nouveau node, on 
        extrait leurs valeurs possibles qui sont présents dans cet attribute de la 
        liste et on les ajoutes comme des nouveau arcs qu’on ajoute à notre list des 
        arcs (copie et réelle) avec le node qu’on vient de créer comme le node père 
        et node fille qu’on ajoutera dans une deuxième instance.

    '''
    while (list_arc_copy != []):
        first_arc = list_arc_copy[0]
        if (fatherNodeValue != first_arc.getFather().getValue()):
            for a in list_arc:
                if a.getSon()==first_arc.getFather():
                    dataSet = a.getData() 
                    fatherNodeValue = a.getFather().getValue()
                    arc_weight = a.getWeight()
                    dataSet = calc.getNewData(fatherNodeValue,arc_weight,dataSet)
                    
        newData = calc.getNewData(first_arc.getFather().getValue(),first_arc.getWeight(),dataSet)
        
        if calc.is_leaf(newData):
            value_leaf = newData[1][len(newData[0])-1]
            node_leaf = Node(value_leaf,cpt+1)
            list_arc[cpt].setSon(node_leaf)
        else:
            newValue = calc.choixAttCible(newData)
            new_Node= Node(newValue,cpt+1)
            list_arc[cpt].setSon(new_Node)
            values_arc = calc.getValeursPosibles(newValue)
            
            for value in values_arc:
                arc = Arc(value, new_Node)
                arc.setData(newData)
                list_arc.append(arc)
                list_arc_copy.append(arc)
                
        cpt += 1
        list_arc_copy.pop(0)

    '''
    On génère le graph de l’arbre de decision à partir de la liste des arcs.
    '''
    graph = graph(list_arc)
    graph.plot_arbre()
    
    '''
    On  génère une matrice de confusion en donnant un jeu de données et en utilisant 
    la liste des arcs pour prédire une réponse.
    On utilise la matrice génère pour les afficher comme une image

    '''
    
    pred = class_Prediction(data_prediction)
    
    data_prediction = calc.clean_data(data_prediction)
    
    matrix = pred.confusionMatrix(list_arc,data_prediction)
    graph.plot_matrice(matrix,data_prediction)