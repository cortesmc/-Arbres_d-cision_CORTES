import math

class Class_math:
    
    def __init__(self,data):
        self.data = data
        self.attributes = data[0]
        
    def get_data(self):
        return self.data
    
    def get_listAttributes(self):
        return self.attributes
        
    def getI(self,list_conc):
        '''
        Parameters
        ----------
        list_conc : List de lists
            Liste avec toutes les p et n de chaque attribute

        Returns
        -------
        DOUBLE
            Calcul d'Entropy de tout la columne.

        '''
        sommeTotal=0
        for i in list_conc :
           sommeTotal =sommeTotal+i
        I=0
        if sommeTotal!=0:
            for n in (list_conc):
                I = I -(n/sommeTotal)*math.log((n/sommeTotal),2)
            return I
        else:
            return 0

    def getNPdata(self,attribute,value,data = None):
        '''
        Parameters
        ----------
        attribute : String
            Nom d'attribute utilise
        value : String
            Nom de la valeur de l'attribute cherche
        data : Matrice
            jeu de données

        Returns
        -------
        list_donnes : TYPE
        Renvoie un list de list, chaque list possède l' information nécessaire 
        pour le calcul d' entropie de chaque children.
        '''
        if (data == None):
            data = self.get_data()  
            
        pos = self.getValeursPosibles(self.attributes[len(self.attributes)-1],self.get_data())
        list_donnes=[]
        list_1 = []
        list_2 = []
        for ind in range(len(data[0])):
            if data[0][ind]==attribute:
                for class_value in pos:
                    cpt = 0
                    for i,x in enumerate(data):
                        if (data[i][ind]==value or value==True) and data[i][len(data[i])-1]==class_value:
                            cpt+=1
                    if cpt!=0:
                        list_1.append(cpt)
                    else:
                        list_1.append(0.00001)
                    list_2.append(class_value)
        list_donnes.append(list_1)
        list_donnes.append(list_2)
        return list_donnes

    def getValeursPosibles(self,attribute,data = None):
        '''
        Parameters
        ----------
        attribute : String
            Nom d'attribute utilise
        data : Matrice
            jeu de données

        Returns
        -------
        valeurs : Liste String
            reenvoi list de lists avec chaque attribute et 
            chaque possible valeur 
        '''
        if (data == None):
            data = self.get_data()
        valeurs=[]
        for ind in range(len(data[0])):
            if data[0][ind]==attribute:
                for x in data:
                    valeurs.append(x[ind])
                valeurs.pop(0)
                valeurs = list(dict.fromkeys(valeurs))
        return valeurs  
    
    def getNewData(self,attribute,value,data = None):
        '''
        Parameters
        ----------
        attribute : String
            Nom d'attribute utilise
        value : String
            Nom de la valeur de l'attribute cherche
        data : Matrice
            jeu de données

        Returns
        -------
        data : Matrice
            Nouveau jeu de données filtre selon le value de l’attribute donné en paramètre
        '''
        if (data == None):
            data = self.get_data()
        newData = []
        newData.append(data[0])
        for ind1,att in enumerate(data[0]):
            if (att == attribute):
                for ind2 in range(len(data)):
                    if (data[ind2][ind1]!="?" and data[ind2][ind1]==value):
                        newData.append(data[ind2])
        return newData

    def calculItotal(self,data = None):
        '''
        Parameters
        ----------
        data : Matrice
            jeu de données

        Returns
        -------
        I : Double
            Calcul de l'entropie de la dernière colonne du jeu de données.

        '''
        if (data == None):
            data = self.get_data()
        donnes =self.getNPdata(self.attributes[len(self.attributes)-1],True,data)[0]
        I=self.getI(donnes)
        return I

    def getEAttribute(self,attribute,data = None):
        '''
        Parameters
        ----------
        attribute : String
            Nom d'attribute utilise
        data : Matrice
            jeu de données

        Returns
        -------
        E : Double 
            Entropie de l'attribut donnée en parametre.
        '''
        if (data == None):
            data = self.get_data()
        valeurs=self.getValeursPosibles(attribute,data)
        total = len(data)-1
        E=0
        for value in valeurs:
            np=self.getNPdata(attribute, value,data)
            t=0
            for i in np[0]:
                t+=i
            E+= ((t)/total)*self.getI(np[0])
        return E

    def getGainAttribute(self,attribute,data = None):
        '''
        Parameters
        ----------
        attribute : String
            Nom d'attribute utilise
        data : Matrice
            jeu de données

        Returns
        -------
        Gain Double 
            Calcul de du gain total de l'attribut donnée en paramètre.

        '''
        if (data == None):
            data = self.get_data()
        I = self.calculItotal(data)
        E = self.getEAttribute(attribute,data)
        return I - E

    def choixAttCible(self,data = None):
        '''
        Parameters
        ----------
        data : Matrice
            jeu de données

        Returns
        -------
        attributeCible String
            Re Envoi le attribute avec le gain plus grand si le jeu de données 
            est vide renvoi ‘null’.

        '''
        if (data == None):
            data = self.get_data()
        if len(data)==1:
            return 'null'
        attributeCible = self.get_listAttributes()[0]
        maxi = self.getGainAttribute(attributeCible,data)
        list_attributes = self.get_listAttributes().copy()
        list_attributes.pop(len(self.get_listAttributes())-1) #takes out "class" column
        for att in list_attributes:
            if maxi < self.getGainAttribute(att,data):
                maxi = self.getGainAttribute(att,data)
                attributeCible = att
        return attributeCible
    
    def is_leaf(self,data = None):
        '''
        Parameters
        ----------
        data : Matrice
            jeu de données

        Returns
        -------
        bool
            Re Envoi si dans le jeu de données donne en paramètre possède un seul 
            type de réponse possible. Dans le cas du dataset: golf.csv si dans la
            colonne “Play” il’y a que de “yes “ ou “non”
        '''
        if (data == None):
            data = self.get_data()
        if len(self.getValeursPosibles(self.attributes[len(self.attributes)-1],data))==1:
            return True
        else:
            return False
        
    def clean_data(self,data):
        '''

        Parameters
        ----------
        data : Matrice
            jeu de données

        Returns
        -------
        data : Matrice
            Nouveau jeu de données qui efface toutes les lignes qui possède un “?” .
        '''
        new_data = []
        for l in data:
            for c in l:
                if c=='?':
                    new_data.append(l)
                    break
        for val in new_data:
                data.remove(val)
        return data