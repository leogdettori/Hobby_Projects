#!/usr/bin/env python
# coding: utf-8

#Created by Leonardo G. Dettori

# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#

#Defines functions to manage database/.poke files
#register, delete and edit

def register_pokemon(data_path,Species,Form,Image,Name,Type_1,Type_2,Ability_name,Ability_info,Item,Move_1,Move_type_1,Move_mode_1,Move_info_1,Move_method_1,Move_power_1,Move_accuracy_1,Move_PP_1,Move_Effect_1,Move_2,Move_type_2,Move_mode_2,Move_info_2,Move_method_2,Move_power_2,Move_accuracy_2,Move_PP_2,Move_Effect_2,Move_3,Move_type_3,Move_mode_3,Move_info_3,Move_method_3,Move_power_3,Move_accuracy_3,Move_PP_3,Move_Effect_3,Move_4,Move_type_4,Move_mode_4,Move_info_4,Move_method_4,Move_power_4,Move_accuracy_4,Move_PP_4,Move_Effect_4):
    
    #imports useful libraries
    import datetime
    import os
    
    #Useful variables        
    All_types = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']  #keeps track of all types
    current_outcome = ''  #keeps track of the outcome of the current type_match
    final_outcome = 0  #keeps track of the final outcome, after comparing to other moves(offense) or to pokemon's second type(defense)
                    #before adding it to a list (offense or defense) for data storage. Uses arbitrary low value '0' so it's not a string
                    #and ensures a pokemon with only Status moves will have 0 as the result of offensive type_match
    offense = []  #keeps track of the offensive type_match combining all types and all moves
    defense = []  #keeps track of the deffensive type_match combining all types
    
    
    #Checks if the file for that pokemon was created before
    if os.path.exists(str(data_path)+'/'+str(Name)+".poke"):
        #print("This pokemon entry already exists. Please try creating a different one or try deleting this entry first.")
        overwrite = 'yes'  #entry will be overwritten        
    else:  #file does not exist yet
        overwrite = 'no'  #entry will NOT be overwritten
        
        
    #Calculates Offensive type advantages:
    #For each type available as the Defensive type
    for types in All_types:

        #Resets helpful variable for the next iteration
        final_outcome = 0

        #Against Move_1 (if not a Status move)
        if Move_mode_1 != 'Status':
            final_outcome = type_match(Move_type_1,types)

        #Against Move_2 (if not a Status move)
        if Move_mode_2 != 'Status':
            current_outcome = type_match(Move_type_2,types)
            #If this outcome is better, it replaces the previous one (the user should use the best move available)
            if current_outcome > final_outcome:
                final_outcome = current_outcome

        #Against Move_3 (if not a Status move)
        if Move_mode_3 != 'Status':
            current_outcome = type_match(Move_type_3,types)
            #If this outcome is better, it replaces the previous one (the user should use the best move available)
            if current_outcome > final_outcome:
                final_outcome = current_outcome

        #Against Move_4 (if not a Status move)
        if Move_mode_4 != 'Status':
            current_outcome = type_match(Move_type_4,types)
            #If this outcome is better, it replaces the previous one (the user should use the best move available)
            if current_outcome > final_outcome:
                final_outcome = current_outcome

        #Adds current outcome to the offense list:
        offense.append(final_outcome)


    #Calculates Defensive type advantages:
    #For each type available as the Offensive type
    for types in All_types:

        #Against Type_1
        final_outcome = type_match(types,Type_1)

        #Against Type_2 (if there is a type 2)
        if Type_2 != '':
            current_outcome = type_match(types,Type_2)
            #Multiplies the two outcomes to generate the final type_match against both types
            final_outcome = final_outcome * current_outcome

        #Adds current outcome to the defense list
        defense.append(final_outcome)
        
    #Applies ability modifier
    (offense,defense) = ability_type_advantages_modifier(All_types,offense,defense,Ability_name,Move_mode_1,Move_mode_2,Move_mode_3,Move_mode_4)
    
    #Applies move modifier
    (offense,defense) =    move_type_advantages_modifier(All_types,offense,defense,Move_mode_1,Move_mode_2,Move_mode_3,Move_mode_4,Move_type_1,Move_type_2,Move_type_3,Move_type_4,Move_1,Move_2,Move_3,Move_4)

    #Creates .poke file to store that pokemon's information in the database
    f1 = open(str(data_path)+'/'+Name+".poke", "w")
    f1.write('Species:'+Species+'\n')
    f1.write('Form:'+Form+'\n')
    f1.write('Image:'+Image+'\n')
    f1.write('Name:'+Name+'\n')
    f1.write('Type1:'+Type_1+'\n')
    f1.write('Type2:'+Type_2+'\n')
    f1.write('Ability:'+Ability_name+':'+Ability_info+'\n')
    f1.write('Item:'+Item+'\n')
    f1.write('Move1:'+Move_1+':'+Move_type_1+':'+Move_mode_1+':'+Move_info_1+':'+Move_method_1+':'+Move_power_1+':'+Move_accuracy_1+':'+Move_PP_1+':'+Move_Effect_1+'\n')
    f1.write('Move2:'+Move_2+':'+Move_type_2+':'+Move_mode_2+':'+Move_info_2+':'+Move_method_2+':'+Move_power_2+':'+Move_accuracy_2+':'+Move_PP_2+':'+Move_Effect_2+'\n')
    f1.write('Move3:'+Move_3+':'+Move_type_3+':'+Move_mode_3+':'+Move_info_3+':'+Move_method_3+':'+Move_power_3+':'+Move_accuracy_3+':'+Move_PP_3+':'+Move_Effect_3+'\n')
    f1.write('Move4:'+Move_4+':'+Move_type_4+':'+Move_mode_4+':'+Move_info_4+':'+Move_method_4+':'+Move_power_4+':'+Move_accuracy_4+':'+Move_PP_4+':'+Move_Effect_4+'\n')
    f1.write('All_Types:'+str(All_types).strip('][').replace("'","").replace(", ",":")+'\n')
    f1.write('Offense:'+str(offense).strip('][').replace("'","").replace(", ",":")+'\n')
    f1.write('Defense:'+str(defense).strip('][').replace("'","").replace(", ",":")+'\n')
    f1.write('#============================================================# '+str(datetime.datetime.now())+'\n')
    f1.close()
    
    if overwrite == 'yes':
        print(str(Name)+' was successfully overwritten!')
    elif overwrite == 'no':
        print(str(Name)+' was successfully added!')    
    
# ========================================= #

def delete_pokemon(data_path,Name):
    
    #imports useful libraries
    import os
    
    #Checks if the file for that pokemon was indeed created before
    if os.path.exists(str(data_path)+'/'+str(Name)+".poke"):
        os.remove(str(data_path)+'/'+str(Name)+".poke")
        print(str(Name)+' was successfully deleted!')
    else:
        print("This Pokemon was not registered. Please try a different one.")
        
        
# ========================================= # 

def edit_pokemon(data_path,Species,Form,Image,Name,Type_1,Type_2,Ability_name,Ability_info,Item,Move_1,Move_type_1,Move_mode_1,Move_info_1,Move_method_1,Move_power_1,Move_accuracy_1,Move_PP_1,Move_Effect_1,Move_2,Move_type_2,Move_mode_2,Move_info_2,Move_method_2,Move_power_2,Move_accuracy_2,Move_PP_2,Move_Effect_2,Move_3,Move_type_3,Move_mode_3,Move_info_3,Move_method_3,Move_power_3,Move_accuracy_3,Move_PP_3,Move_Effect_3,Move_4,Move_type_4,Move_mode_4,Move_info_4,Move_method_4,Move_power_4,Move_accuracy_4,Move_PP_4,Move_Effect_4):
    
    #imports useful libraries
    import datetime
    import os
    
    #Useful variables        
    All_types = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']  #keeps track of all types
    current_outcome = ''  #keeps track of the outcome of the current type_match
    final_outcome = 0  #keeps track of the final outcome, after comparing to other moves(offense) or to pokemon's second type(defense)
                    #before adding it to a list (offense or defense) for data storage. Uses arbitrary low value '0' so it's not a string
                    #and ensures a pokemon with only Status moves will have 0 as the result of offensive type_match
    offense = []  #keeps track of the offensive type_match combining all types and all moves
    defense = []  #keeps track of the deffensive type_match combining all types
    
    #Checks if the file for that pokemon was created before
    if os.path.exists(str(data_path)+'/'+str(Name)+".poke"):
        
        #Calculates Offensive type advantages:
        #For each type available as the Defensive type
        for types in All_types:
            
            #Resets helpful variable for the next iteration
            final_outcome = 0
        
            #Against Move_1 (if not a Status move)
            if Move_mode_1 != 'Status':
                final_outcome = type_match(Move_type_1,types)
                
            #Against Move_2 (if not a Status move)
            if Move_mode_2 != 'Status':
                current_outcome = type_match(Move_type_2,types)
                #If this outcome is better, it replaces the previous one (the user should use the best move available)
                if current_outcome > final_outcome:
                    final_outcome = current_outcome
                    
            #Against Move_3 (if not a Status move)
            if Move_mode_3 != 'Status':
                current_outcome = type_match(Move_type_3,types)
                #If this outcome is better, it replaces the previous one (the user should use the best move available)
                if current_outcome > final_outcome:
                    final_outcome = current_outcome
                    
            #Against Move_4 (if not a Status move)
            if Move_mode_4 != 'Status':
                current_outcome = type_match(Move_type_4,types)
                #If this outcome is better, it replaces the previous one (the user should use the best move available)
                if current_outcome > final_outcome:
                    final_outcome = current_outcome
            
            #Adds current outcome to the offense list:
            offense.append(final_outcome)
        
        
        #Calculates Defensive type advantages:
        #For each type available as the Offensive type
        for types in All_types:
            
            #Against Type_1
            final_outcome = type_match(types,Type_1)
            
            #Against Type_2 (if there is a type 2)
            if Type_2 != '':
                current_outcome = type_match(types,Type_2)
                #Multiplies the two outcomes to generate the final type_match against both types
                final_outcome = final_outcome * current_outcome
                
            #Adds current outcome to the defense list
            defense.append(final_outcome)
            
        #Applies ability modifier
        (offense,defense) = ability_type_advantages_modifier(All_types,offense,defense,Ability_name,Move_mode_1,Move_mode_2,Move_mode_3,Move_mode_4)
        
        #Applies move modifier
        (offense,defense) =    move_type_advantages_modifier(All_types,offense,defense,Move_mode_1,Move_mode_2,Move_mode_3,Move_mode_4,Move_type_1,Move_type_2,Move_type_3,Move_type_4,Move_1,Move_2,Move_3,Move_4)
    
    
        #Overwrites the old .poke file with the new information
        f1 = open(str(data_path)+'/'+Name+".poke", "w")
        f1.write('Species:'+Species+'\n')
        f1.write('Form:'+Form+'\n')
        f1.write('Image:'+Image+'\n')
        f1.write('Name:'+Name+'\n')
        f1.write('Type1:'+Type_1+'\n')
        f1.write('Type2:'+Type_2+'\n')
        f1.write('Ability:'+Ability_name+':'+Ability_info+'\n')
        f1.write('Item:'+Item+'\n')
        f1.write('Move1:'+Move_1+':'+Move_type_1+':'+Move_mode_1+':'+Move_info_1+':'+Move_method_1+':'+Move_power_1+':'+Move_accuracy_1+':'+Move_PP_1+':'+Move_Effect_1+'\n')
        f1.write('Move2:'+Move_2+':'+Move_type_2+':'+Move_mode_2+':'+Move_info_2+':'+Move_method_2+':'+Move_power_2+':'+Move_accuracy_2+':'+Move_PP_2+':'+Move_Effect_2+'\n')
        f1.write('Move3:'+Move_3+':'+Move_type_3+':'+Move_mode_3+':'+Move_info_3+':'+Move_method_3+':'+Move_power_3+':'+Move_accuracy_3+':'+Move_PP_3+':'+Move_Effect_3+'\n')
        f1.write('Move4:'+Move_4+':'+Move_type_4+':'+Move_mode_4+':'+Move_info_4+':'+Move_method_4+':'+Move_power_4+':'+Move_accuracy_4+':'+Move_PP_4+':'+Move_Effect_4+'\n')
        f1.write('All_Types:'+str(All_types).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('Offense:'+str(offense).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('Defense:'+str(defense).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('#============================================================# '+str(datetime.datetime.now())+'\n')
        f1.close()

        print(str(Name)+' was successfully edited!')
    
    else:
        print("This Pokemon entry does not exist. Please try a different one.")
        
# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#        
        
#Defines functions to manage database/.team files
#register, delete and edit

def register_team(data_path,Team):
    
    #imports useful libraries
    import datetime
    import os
    import numpy as np
        
    #Checks if the file for that team was created before
    if os.path.exists(str(data_path)+'/'+str(Team['Team_Name'][0])+".team"):
        #print("This team entry already exists. Please try creating a different one or try deleting this entry first.")
        overwrite = 'yes'  #entry will be overwritten        
    else:  #file does not exist yet
        overwrite = 'no'  #entry will NOT be overwritten
        
    #Creates .team file to store that team's information in the database
    f1 = open(str(data_path)+'/'+str(Team['Team_Name'][0])+".team", "w")
    f1.write('Team_Name:'+str(Team['Team_Name'][0])+'\n')
    f1.write('Strengths:'+str(Team['Strengths'].tolist()).strip('][').replace("'","").replace(", ",":")+'\n')
    f1.write('Weaknesses:'+str(Team['Weaknesses'].tolist()).strip('][').replace("'","").replace(", ",":")+'\n')
    f1.write('Scores:'+str(Team['Scores'].tolist()).strip('][').replace("'","").replace(", ",":")+'\n')
    f1.write('Global_Score:'+str(Team['Global_Score']).strip('][').replace("'","")+'\n') 
    f1.write('Physical_Moves:'+str(Team['Stats']['Physical_Moves']).strip('][').replace("'","").replace(", ",":")+'\n')
    f1.write('Special_Moves:'+str(Team['Stats']['Special_Moves']).strip('][').replace("'","").replace(", ",":")+'\n')
    f1.write('Status_Moves:'+str(Team['Stats']['Status_Moves']).strip('][').replace("'","").replace(", ",":")+'\n')
    f1.write('Repeated_Items:'+str(Team['Stats']['Repeated_Items']).strip('][').replace("'","").replace(", ",":")+'\n')
    f1.write('#============================================================# '+str(Team['Date']).strip('][').replace("'","")+'\n')
    #For every pokemon in the team, the program writes their current information (at the time the team was created)
    for member in Team['Members']:
        f1.write('Species:'+str(Team['Members'][member]['Species'][0])+'\n')
        f1.write('Form:'+str(Team['Members'][member]['Form'][0])+'\n')
        f1.write('Image:'+str(Team['Members'][member]['Image'][0])+'\n')
        f1.write('Name:'+str(Team['Members'][member]['Name'][0])+'\n')
        f1.write('Type1:'+str(Team['Members'][member]['Types'][0])+'\n')
        f1.write('Type2:'+str(Team['Members'][member]['Types'][1])+'\n')
        f1.write('Ability:'+str(Team['Members'][member]['Ability']['Ability_Name'][0])+':'+str(Team['Members'][member]['Ability']['Ability_Info'][0])+'\n')
        f1.write('Item:'+str(Team['Members'][member]['Item'][0])+'\n')
        f1.write('Move1:'+str(Team['Members'][member]['Moves']['Move_Name'][0])+':'+str(Team['Members'][member]['Moves']['Move_Type'][0])+':'+str(Team['Members'][member]['Moves']['Move_Mode'][0])+':'+str(Team['Members'][member]['Moves']['Move_Info'][0])+':'+str(Team['Members'][member]['Moves']['Move_Method'][0])+':'+str(Team['Members'][member]['Moves']['Move_Power'][0])+':'+str(Team['Members'][member]['Moves']['Move_Accuracy'][0])+':'+str(Team['Members'][member]['Moves']['Move_PP'][0])+':'+str(Team['Members'][member]['Moves']['Move_Effect'][0])+'\n')
        f1.write('Move2:'+str(Team['Members'][member]['Moves']['Move_Name'][1])+':'+str(Team['Members'][member]['Moves']['Move_Type'][1])+':'+str(Team['Members'][member]['Moves']['Move_Mode'][1])+':'+str(Team['Members'][member]['Moves']['Move_Info'][1])+':'+str(Team['Members'][member]['Moves']['Move_Method'][1])+':'+str(Team['Members'][member]['Moves']['Move_Power'][1])+':'+str(Team['Members'][member]['Moves']['Move_Accuracy'][1])+':'+str(Team['Members'][member]['Moves']['Move_PP'][1])+':'+str(Team['Members'][member]['Moves']['Move_Effect'][1])+'\n')
        f1.write('Move3:'+str(Team['Members'][member]['Moves']['Move_Name'][2])+':'+str(Team['Members'][member]['Moves']['Move_Type'][2])+':'+str(Team['Members'][member]['Moves']['Move_Mode'][2])+':'+str(Team['Members'][member]['Moves']['Move_Info'][2])+':'+str(Team['Members'][member]['Moves']['Move_Method'][2])+':'+str(Team['Members'][member]['Moves']['Move_Power'][2])+':'+str(Team['Members'][member]['Moves']['Move_Accuracy'][2])+':'+str(Team['Members'][member]['Moves']['Move_PP'][2])+':'+str(Team['Members'][member]['Moves']['Move_Effect'][2])+'\n')
        f1.write('Move4:'+str(Team['Members'][member]['Moves']['Move_Name'][3])+':'+str(Team['Members'][member]['Moves']['Move_Type'][3])+':'+str(Team['Members'][member]['Moves']['Move_Mode'][3])+':'+str(Team['Members'][member]['Moves']['Move_Info'][3])+':'+str(Team['Members'][member]['Moves']['Move_Method'][3])+':'+str(Team['Members'][member]['Moves']['Move_Power'][3])+':'+str(Team['Members'][member]['Moves']['Move_Accuracy'][3])+':'+str(Team['Members'][member]['Moves']['Move_PP'][3])+':'+str(Team['Members'][member]['Moves']['Move_Effect'][3])+'\n')
        f1.write('All_Types:'+str(Team['Members'][member]['Type_Match']['All_Types']).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('Offense:'+str(Team['Members'][member]['Type_Match']['Offense']).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('Defense:'+str(Team['Members'][member]['Type_Match']['Defense']).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('#============================================================# '+str(str(Team['Members'][member]['Date'][0]))+'\n')
    f1.close()
    
    if overwrite == 'yes':
        print(str(Team['Team_Name'][0])+' was successfully overwritten!')
    elif overwrite == 'no':
        print(str(Team['Team_Name'][0])+' was successfully added!')
    
# ========================================= #

def delete_team(data_path,Name):
    
    #imports useful libraries
    import os
    
    #Checks if the file for that team was indeed created before
    if os.path.exists(str(data_path)+'/'+str(Name)+".team"):
        os.remove(str(data_path)+'/'+str(Name)+".team")
        print(str(Name)+' was successfully deleted!')
    else:
        print("This Team was not registered. Please try a different one.")
                
# ========================================= # 

def edit_team(data_path,Team):
    
    #imports useful libraries
    import datetime
    import os
    import numpy as np
        
    #Checks if the file for that team was created before
    if os.path.exists(str(data_path)+'/'+str(Team['Team_Name'][0])+".team"):
        #Overwrites the old .team file with the new information
        f1 = open(str(data_path)+'/'+str(Team['Team_Name'][0])+".team", "w")
        f1.write('Team_Name:'+str(Team['Team_Name'][0])+'\n')
        f1.write('Strengths:'+str(Team['Strengths'].tolist()).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('Weaknesses:'+str(Team['Weaknesses'].tolist()).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('Scores:'+str(Team['Scores'].tolist()).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('Global_Score:'+str(Team['Global_Score']).strip('][').replace("'","")+'\n') 
        f1.write('Physical_Moves:'+str(Team['Stats']['Physical_Moves']).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('Special_Moves:'+str(Team['Stats']['Special_Moves']).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('Status_Moves:'+str(Team['Stats']['Status_Moves']).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('Repeated_Items:'+str(Team['Stats']['Repeated_Items']).strip('][').replace("'","").replace(", ",":")+'\n')
        f1.write('#============================================================# '+str(Team['Date']).strip('][').replace("'","")+'\n')
        #For every pokemon in the team, the program writes their current information (at the time the team was created)
        for member in Team['Members']:
            f1.write('Species:'+str(Team['Members'][member]['Species'][0])+'\n')
            f1.write('Form:'+str(Team['Members'][member]['Form'][0])+'\n')
            f1.write('Image:'+str(Team['Members'][member]['Image'][0])+'\n')
            f1.write('Name:'+str(Team['Members'][member]['Name'][0])+'\n')
            f1.write('Type1:'+str(Team['Members'][member]['Types'][0])+'\n')
            f1.write('Type2:'+str(Team['Members'][member]['Types'][1])+'\n')
            f1.write('Ability:'+str(Team['Members'][member]['Ability']['Ability_Name'][0])+':'+str(Team['Members'][member]['Ability']['Ability_Info'][0])+'\n')
            f1.write('Item:'+str(Team['Members'][member]['Item'][0])+'\n')
            f1.write('Move1:'+str(Team['Members'][member]['Moves']['Move_Name'][0])+':'+str(Team['Members'][member]['Moves']['Move_Type'][0])+':'+str(Team['Members'][member]['Moves']['Move_Mode'][0])+':'+str(Team['Members'][member]['Moves']['Move_Info'][0])+':'+str(Team['Members'][member]['Moves']['Move_Method'][0])+':'+str(Team['Members'][member]['Moves']['Move_Power'][0])+':'+str(Team['Members'][member]['Moves']['Move_Accuracy'][0])+':'+str(Team['Members'][member]['Moves']['Move_PP'][0])+':'+str(Team['Members'][member]['Moves']['Move_Effect'][0])+'\n')
            f1.write('Move2:'+str(Team['Members'][member]['Moves']['Move_Name'][1])+':'+str(Team['Members'][member]['Moves']['Move_Type'][1])+':'+str(Team['Members'][member]['Moves']['Move_Mode'][1])+':'+str(Team['Members'][member]['Moves']['Move_Info'][1])+':'+str(Team['Members'][member]['Moves']['Move_Method'][1])+':'+str(Team['Members'][member]['Moves']['Move_Power'][1])+':'+str(Team['Members'][member]['Moves']['Move_Accuracy'][1])+':'+str(Team['Members'][member]['Moves']['Move_PP'][1])+':'+str(Team['Members'][member]['Moves']['Move_Effect'][1])+'\n')
            f1.write('Move3:'+str(Team['Members'][member]['Moves']['Move_Name'][2])+':'+str(Team['Members'][member]['Moves']['Move_Type'][2])+':'+str(Team['Members'][member]['Moves']['Move_Mode'][2])+':'+str(Team['Members'][member]['Moves']['Move_Info'][2])+':'+str(Team['Members'][member]['Moves']['Move_Method'][2])+':'+str(Team['Members'][member]['Moves']['Move_Power'][2])+':'+str(Team['Members'][member]['Moves']['Move_Accuracy'][2])+':'+str(Team['Members'][member]['Moves']['Move_PP'][2])+':'+str(Team['Members'][member]['Moves']['Move_Effect'][2])+'\n')
            f1.write('Move4:'+str(Team['Members'][member]['Moves']['Move_Name'][3])+':'+str(Team['Members'][member]['Moves']['Move_Type'][3])+':'+str(Team['Members'][member]['Moves']['Move_Mode'][3])+':'+str(Team['Members'][member]['Moves']['Move_Info'][3])+':'+str(Team['Members'][member]['Moves']['Move_Method'][3])+':'+str(Team['Members'][member]['Moves']['Move_Power'][3])+':'+str(Team['Members'][member]['Moves']['Move_Accuracy'][3])+':'+str(Team['Members'][member]['Moves']['Move_PP'][3])+':'+str(Team['Members'][member]['Moves']['Move_Effect'][3])+'\n')
            f1.write('All_Types:'+str(Team['Members'][member]['Type_Match']['All_Types']).strip('][').replace("'","").replace(", ",":")+'\n')
            f1.write('Offense:'+str(Team['Members'][member]['Type_Match']['Offense']).strip('][').replace("'","").replace(", ",":")+'\n')
            f1.write('Defense:'+str(Team['Members'][member]['Type_Match']['Defense']).strip('][').replace("'","").replace(", ",":")+'\n')
            f1.write('#============================================================# '+str(str(Team['Members'][member]['Date'][0]))+'\n')
        f1.close()

        print(str(Team['Team_Name'][0])+' was successfully edited!')
    
    else:
        print("This Team entry does not exist. Please try a different one.")

# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#

#Defines the read_Pokemon function which reads a single .poke file from the database and compiles the information into a dictionary
#the dictionary is returned so that the pokemon information can be utilized

def read_pokemon(data_path,Name):
    
    #imports useful libraries
    import os
    
    #checks if provided pokemon entry exists in the provided database
    if os.path.exists(str(data_path)+'/'+str(Name)+".poke") == False:
        print("This pokemon entry does not exists. Please try a different one.")
        print('Session was ended. Progressed was not saved.')
        return
        #sys.exit('Session was ended. Progressed was not saved.')
        

    #creates counters
    i = 1

    #Creates dictionary for current pokemon
    Pokemon = {'Species':[], 'Form':[], 'Image':[], 'Name':[], 'Types':[], 'Ability':{'Ability_Name':[], 'Ability_Info':[]}, 'Item':[], 'Moves':{'Move_Name':[], 'Move_Type':[], 'Move_Mode':[], 'Move_Info':[], 'Move_Method':[], 'Move_Power':[], 'Move_Accuracy':[], 'Move_PP':[], 'Move_Effect':[]}, 'Date':[], 'Type_Match':{'All_Types':[], 'Offense':[], 'Defense':[]}}
    

    #This is important for the program to know when to stop
    c = open(data_path+Name+'.poke')
    lines1 = c.readlines()
    total_lines = len(lines1)
    c.close()

    # Read the pokemon entry
    f = open(data_path+Name+'.poke')

    #Starts the loop trhough the file. Line by line.
    while i <= total_lines:
        this_line = f.readline()
        i = i + 1 
        
        #Finds the pokemon Species line
        if this_line.startswith('Species'):
            this_Species = this_line.split(':')[-1].strip('\n')
            #print(this_Species)
            #Adds pokemon Species to the dicitonary
            Pokemon['Species'].append(this_Species)
            
        #Finds the pokemon Form line
        if this_line.startswith('Form'):
            this_Form = this_line.split(':')[-1].strip('\n')
            #print(this_Form)
            #Adds pokemon Form to the dicitonary
            Pokemon['Form'].append(this_Form)
            
        #Finds the pokemon Image line
        if this_line.startswith('Image'):
            this_Image = this_line.split(':')[-1].strip('\n')
            #print(this_Image)
            #Adds pokemon Image to the dicitonary
            Pokemon['Image'].append(this_Image)

        #Finds the pokemon Name line
        if this_line.startswith('Name'):
            this_Name = this_line.split(':')[-1].strip('\n')
            #print(this_Name)
            #Adds pokemon name to the dicitonary
            Pokemon['Name'].append(this_Name)

        #Finds the pokemon Type 1 line
        if this_line.startswith('Type1'):
            Type_1 = this_line.split(':')[-1].strip('\n')
            #print(Type_1)
            #Adds pokemon Type 1 to the dicitonary
            Pokemon['Types'].append(Type_1)

        #Finds the pokemon Type 2 line
        if this_line.startswith('Type2'):
            Type_2 = this_line.split(':')[-1].strip('\n')
            #print(Type_2)
            #Adds pokemon Type 2 to the dicitonary
            Pokemon['Types'].append(Type_2)

        #Finds the pokemon Ability line
        if this_line.startswith('Ability'):
            Ability_name = this_line.split(':')[-2].strip('\n')
            #print(Ability_name)
            Ability_info = this_line.split(':')[-1].strip('\n')
            #print(Ability_info)
            #Adds pokemon Ability to the dicitonary
            Pokemon['Ability']['Ability_Name'].append(Ability_name)
            Pokemon['Ability']['Ability_Info'].append(Ability_info)

        #Finds the pokemon Item line
        if this_line.startswith('Item'):
            Item = this_line.split(':')[-1].strip('\n')
            #print(Item)
            #Adds pokemon Item to the dicitonary
            Pokemon['Item'].append(Item)

        #Finds the pokemon Move 1 line
        if this_line.startswith('Move1'):
            Move_1 = this_line.split(':')[-9].strip('\n')
            #print(Move_1)
            Move_type_1 = this_line.split(':')[-8].strip('\n')
            #print(Move_type_1)
            Move_mode_1 = this_line.split(':')[-7].strip('\n')
            #print(Move_mode_1)
            Move_info_1 = this_line.split(':')[-6].strip('\n')
            #print(Move_info_1)
            Move_method_1 = this_line.split(':')[-5].strip('\n')
            #print(Move_method_1)
            Move_power_1 = this_line.split(':')[-4].strip('\n')
            #print(Move_power_1)
            Move_accuracy_1 = this_line.split(':')[-3].strip('\n')
            #print(Move_accuracy_1)
            Move_PP_1 = this_line.split(':')[-2].strip('\n')
            #print(Move_PP_1)
            Move_Effect_1 = this_line.split(':')[-1].strip('\n')
            #print(Move_Effect_1)
            #Adds pokemon Move 1 to the dicitonary
            Pokemon['Moves']['Move_Name'].append(Move_1)
            Pokemon['Moves']['Move_Type'].append(Move_type_1)
            Pokemon['Moves']['Move_Mode'].append(Move_mode_1)
            Pokemon['Moves']['Move_Info'].append(Move_info_1)
            Pokemon['Moves']['Move_Method'].append(Move_method_1)
            Pokemon['Moves']['Move_Power'].append(Move_power_1)
            Pokemon['Moves']['Move_Accuracy'].append(Move_accuracy_1)
            Pokemon['Moves']['Move_PP'].append(Move_PP_1)
            Pokemon['Moves']['Move_Effect'].append(Move_Effect_1)

        #Finds the pokemon Move 2 line
        if this_line.startswith('Move2'):
            Move_2 = this_line.split(':')[-9].strip('\n')
            #print(Move_2)
            Move_type_2 = this_line.split(':')[-8].strip('\n')
            #print(Move_type_2)
            Move_mode_2 = this_line.split(':')[-7].strip('\n')
            #print(Move_mode_2)
            Move_info_2 = this_line.split(':')[-6].strip('\n')
            #print(Move_info_2)
            Move_method_2 = this_line.split(':')[-5].strip('\n')
            #print(Move_method_2)
            Move_power_2 = this_line.split(':')[-4].strip('\n')
            #print(Move_power_2)
            Move_accuracy_2 = this_line.split(':')[-3].strip('\n')
            #print(Move_accuracy_2)
            Move_PP_2 = this_line.split(':')[-2].strip('\n')
            #print(Move_PP_2)
            Move_Effect_2 = this_line.split(':')[-1].strip('\n')
            #print(Move_Effect_2)
            #Adds pokemon Move 2 to the dicitonary
            Pokemon['Moves']['Move_Name'].append(Move_2)
            Pokemon['Moves']['Move_Type'].append(Move_type_2)
            Pokemon['Moves']['Move_Mode'].append(Move_mode_2)
            Pokemon['Moves']['Move_Info'].append(Move_info_2)
            Pokemon['Moves']['Move_Method'].append(Move_method_2)
            Pokemon['Moves']['Move_Power'].append(Move_power_2)
            Pokemon['Moves']['Move_Accuracy'].append(Move_accuracy_2)
            Pokemon['Moves']['Move_PP'].append(Move_PP_2)
            Pokemon['Moves']['Move_Effect'].append(Move_Effect_2)

        #Finds the pokemon Move 3 line
        if this_line.startswith('Move3'):
            Move_3 = this_line.split(':')[-9].strip('\n')
            #print(Move_3)
            Move_type_3 = this_line.split(':')[-8].strip('\n')
            #print(Move_type_3)
            Move_mode_3 = this_line.split(':')[-7].strip('\n')
            #print(Move_mode_3)
            Move_info_3 = this_line.split(':')[-6].strip('\n')
            #print(Move_info_3)
            Move_method_3 = this_line.split(':')[-5].strip('\n')
            #print(Move_method_3)
            Move_power_3 = this_line.split(':')[-4].strip('\n')
            #print(Move_power_3)
            Move_accuracy_3 = this_line.split(':')[-3].strip('\n')
            #print(Move_accuracy_3)
            Move_PP_3 = this_line.split(':')[-2].strip('\n')
            #print(Move_PP_3)
            Move_Effect_3 = this_line.split(':')[-1].strip('\n')
            #print(Move_Effect_3)
            #Adds pokemon Move 3 to the dicitonary
            Pokemon['Moves']['Move_Name'].append(Move_3)
            Pokemon['Moves']['Move_Type'].append(Move_type_3)
            Pokemon['Moves']['Move_Mode'].append(Move_mode_3)
            Pokemon['Moves']['Move_Info'].append(Move_info_3)
            Pokemon['Moves']['Move_Method'].append(Move_method_3)
            Pokemon['Moves']['Move_Power'].append(Move_power_3)
            Pokemon['Moves']['Move_Accuracy'].append(Move_accuracy_3)
            Pokemon['Moves']['Move_PP'].append(Move_PP_3)
            Pokemon['Moves']['Move_Effect'].append(Move_Effect_3)

        #Finds the pokemon Move 4 line
        if this_line.startswith('Move4'):
            Move_4 = this_line.split(':')[-9].strip('\n')
            #print(Move_4)
            Move_type_4 = this_line.split(':')[-8].strip('\n')
            #print(Move_type_4)
            Move_mode_4 = this_line.split(':')[-7].strip('\n')
            #print(Move_mode_4)
            Move_info_4 = this_line.split(':')[-6].strip('\n')
            #print(Move_info_4)
            Move_method_4 = this_line.split(':')[-5].strip('\n')
            #print(Move_method_4)
            Move_power_4 = this_line.split(':')[-4].strip('\n')
            #print(Move_power_4)
            Move_accuracy_4 = this_line.split(':')[-3].strip('\n')
            #print(Move_accuracy_4)
            Move_PP_4 = this_line.split(':')[-2].strip('\n')
            #print(Move_PP_4)
            Move_Effect_4 = this_line.split(':')[-1].strip('\n')
            #print(Move_Effect_4)
            #Adds pokemon Move 4 to the dicitonary
            Pokemon['Moves']['Move_Name'].append(Move_4)
            Pokemon['Moves']['Move_Type'].append(Move_type_4)
            Pokemon['Moves']['Move_Mode'].append(Move_mode_4)
            Pokemon['Moves']['Move_Info'].append(Move_info_4)
            Pokemon['Moves']['Move_Method'].append(Move_method_4)
            Pokemon['Moves']['Move_Power'].append(Move_power_4)
            Pokemon['Moves']['Move_Accuracy'].append(Move_accuracy_4)
            Pokemon['Moves']['Move_PP'].append(Move_PP_4)
            Pokemon['Moves']['Move_Effect'].append(Move_Effect_4)
            
        #Updates dictionary with information of all types in the built-in sequence
        if this_line.startswith('All_Types'):
            this_All_Types = this_line.split(':')
            #print(this_All_Types)
            #Adds each type to the dictionary, one by one
            for k in this_All_Types:
                if k != 'All_Types': #ignores the word 'All_Types' and only adds the types to the dictionary
                    Pokemon['Type_Match']['All_Types'].append(k.strip('\n'))
            
        #Finds the offense line
        if this_line.startswith('Offense'):
            this_Offense = this_line.split(':')
            #print(this_Offense)
            #Adds each offensive type_match result to the dictionary, one by one
            for k in this_Offense:
                if k != 'Offense': #ignores the word 'Offense' and only adds the numbers to the dictionary
                    Pokemon['Type_Match']['Offense'].append(float(k.strip('\n')))
                    
        #Finds the defense line
        if this_line.startswith('Defense'):
            this_Defense = this_line.split(':')
            #print(this_Defense)
            #Adds each defensive type_match result to the dictionary, one by one
            for k in this_Defense:
                if k != 'Defense': #ignores the word 'Defense' and only adds the numbers to the dictionary
                    Pokemon['Type_Match']['Defense'].append(float(k.strip('\n')))
            
        #Finds the date when this pokemon entry was created/last edited
        if this_line.startswith('#============================================================#'):
            date = this_line.split('# ')[-1].strip('\n')
            #print(date)
            #Adds pokemon name to the dicitonary
            Pokemon['Date'].append(date)

    #Closes file after all the important information is extracted        
    f.close()

    #Returns the dictionary with the compiled information of the current pokemon
    return Pokemon

# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#

#Defines the read_team function which reads a single .team file from the database and compiles the information into a dictionary
#the dictionary is returned so that the team information can be utilized

def read_team(data_path,Name):
    
    #imports useful libraries
    import os
    import numpy as np
    
    #checks if provided team entry exists in the provided database
    if os.path.exists(str(data_path)+'/'+str(Name)+".team") == False:
        print("This team entry does not exists. Please try a different one.")
        print('Session was ended. Progressed was not saved.')
        return
        #sys.exit('Session was ended. Progressed was not saved.')
        

    #creates counters
    i = 1
    p = 0  #keeps track of how many pokemon are in the team
    
    #Creates dictionary for current team
    Team = {'Members':{}, 'Team_Name':[], 'Strengths':[], 'Weaknesses':[], 'Scores':[], 'Global_Score':[], 'Stats':{},'Date':[]}
    
    #Creates Team Stats Entries within the dictionary
    Team['Stats']['Physical_Moves'] = []  #creates Stats sub entry that keeps track of the name of pokemon with Physical moves in the team
    Team['Stats']['Special_Moves'] = []  #creates Stats sub entry that keeps track of the name of pokemon with Special moves in the team                
    Team['Stats']['Status_Moves'] = []  #creates Stats sub entry that keeps track of the name of pokemon with Status moves in the team
    Team['Stats']['Repeated_Items'] = []  #creates Stats sub entry that keeps track of the name of repeated items in the team

    
    #This is important for the program to know when to stop
    c = open(data_path+Name+'.team')
    lines1 = c.readlines()
    total_lines = len(lines1)
    c.close()

    # Read the team entry
    f = open(data_path+Name+'.team')

    #Starts the loop through the file. Line by line.
    while i <= total_lines:
        this_line = f.readline()
        i = i + 1
        
        # =============================== # For the general team information
        
        #Finds the Team_Name line
        if this_line.startswith('Team_Name'):
            this_Team_Name = this_line.split(':')[-1].strip('\n')
            #print(this_Team_Name)
            #Adds Team_Name to the dicitonary
            Team['Team_Name'].append(this_Team_Name)
            
        #Finds the Strengths line
        if this_line.startswith('Strengths'):
            this_Strengths = this_line.split(':')
            #print(this_Strengths)
            #Adds each Strengths result to the dictionary, one by one
            for k in this_Strengths:
                if k != 'Strengths': #ignores the word 'Strengths' and only adds the numbers to the dictionary
                    Team['Strengths'].append(float(k.strip('\n')))                    
            #Converts results into a numpy vector to facilitate future calculations
            Team['Strengths'] = np.array(Team['Strengths'])
                    
        #Finds the Weaknesses line
        if this_line.startswith('Weaknesses'):
            this_Weaknesses = this_line.split(':')
            #print(this_Weaknesses)
            #Adds each Weaknesses result to the dictionary, one by one
            for k in this_Weaknesses:
                if k != 'Weaknesses': #ignores the word 'Weaknesses' and only adds the numbers to the dictionary
                    Team['Weaknesses'].append(float(k.strip('\n')))
            #Converts results into a numpy vector to facilitate future calculations
            Team['Weaknesses'] = np.array(Team['Weaknesses'])
                    
        #Finds the Scores line
        if this_line.startswith('Scores'):
            this_Scores = this_line.split(':')
            #print(this_Scores)
            #Adds each Scores result to the dictionary, one by one
            for k in this_Scores:
                if k != 'Scores': #ignores the word 'Scores' and only adds the numbers to the dictionary
                    Team['Scores'].append(float(k.strip('\n')))
            #Converts results into a numpy vector to facilitate future calculations
            Team['Scores'] = np.array(Team['Scores'])
                    
        #Finds the Global_Score line
        if this_line.startswith('Global_Score'):
            this_Global_Score = this_line.split(':')[-1].strip('\n')
            #print(this_Global_Score)
            #Adds Global_Score to the dicitonary
            Team['Global_Score'].append(float(this_Global_Score.strip('\n')))
            
        #Finds the Physical_Moves line
        if this_line.startswith('Physical_Moves'):
            this_Physical_Moves = this_line.split(':')
            #print(this_Physical_Moves)
            #Adds each Physical_Moves result to the dictionary, one by one
            for k in this_Physical_Moves:
                if k != 'Physical_Moves': #ignores the word 'Physical_Moves' and only adds the names to the dictionary
                    Team['Stats']['Physical_Moves'].append(k.strip('\n'))
        
        #Finds the Special_Moves line
        if this_line.startswith('Special_Moves'):
            this_Special_Moves = this_line.split(':')
            #print(this_Special_Moves)
            #Adds each Special_Moves result to the dictionary, one by one
            for k in this_Special_Moves:
                if k != 'Special_Moves': #ignores the word 'Special_Moves' and only adds the names to the dictionary
                    Team['Stats']['Special_Moves'].append(k.strip('\n'))
                    
        #Finds the Status_Moves line
        if this_line.startswith('Status_Moves'):
            this_Status_Moves = this_line.split(':')
            #print(this_Status_Moves)
            #Adds each Status_Moves result to the dictionary, one by one
            for k in this_Status_Moves:
                if k != 'Status_Moves': #ignores the word 'Status_Moves' and only adds the names to the dictionary
                    Team['Stats']['Status_Moves'].append(k.strip('\n'))
                    
        #Finds the Repeated_Items line
        if this_line.startswith('Repeated_Items'):
            this_Repeated_Items = this_line.split(':')
            #print(this_Repeated_Items)
            #Adds each Repeated_Items result to the dictionary, one by one
            for k in this_Repeated_Items:
                if k != 'Repeated_Items': #ignores the word 'Repeated_Items' and only adds the names to the dictionary
                    Team['Stats']['Repeated_Items'].append(k.strip('\n'))
                    
        #Finds the date when this team entry was created/last edited (and avoids pokemon date by using p == 0)
        if this_line.startswith('#============================================================#') and p == 0:
            date = this_line.split('# ')[-1].strip('\n')
            #print(date)
            #Adds date to the dicitonary
            Team['Date'].append(date)
        
        # =============================== # For each pokemon, one by one
        
        #Finds the pokemon Species line
        if this_line.startswith('Species'):
            Species = this_line.split(':')[-1].strip('\n')
            #print(Species)
            #This means a new pokemon was found, thus a new entry will be added to the dictionary
            p = p + 1 #a new pokemon was found in the team
            Team['Members']['Pokemon_'+str(p)] = {'Species':[], 'Form':[], 'Image':[], 'Name':[], 'Types':[], 'Ability':{'Ability_Name':[], 'Ability_Info':[]}, 'Item':[], 'Moves':{'Move_Name':[], 'Move_Type':[], 'Move_Mode':[], 'Move_Info':[], 'Move_Method':[], 'Move_Power':[], 'Move_Accuracy':[], 'Move_PP':[], 'Move_Effect':[]}, 'Date':[], 'Type_Match':{'All_Types':[], 'Offense':[], 'Defense':[]}}
            #Adds pokemon Species to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Species'].append(Species)

        #Finds the pokemon Name line
        if this_line.startswith('Name'):
            this_Name = this_line.split(':')[-1].strip('\n')
            #print(this_Name)
            #Adds pokemon name to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Name'].append(this_Name)
            
        #Finds the pokemon Form line
        if this_line.startswith('Form'):
            Form = this_line.split(':')[-1].strip('\n')
            #print(Form)
            #Adds pokemon Form to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Form'].append(Form)
            
        #Finds the pokemon Image line
        if this_line.startswith('Image'):
            Image = this_line.split(':')[-1].strip('\n')
            #print(Image)
            #Adds pokemon Species to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Image'].append(Image)
        
        #Finds the pokemon Type 1 line
        if this_line.startswith('Type1'):
            Type_1 = this_line.split(':')[-1].strip('\n')
            #print(Type_1)
            #Adds pokemon Type 1 to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Types'].append(Type_1)

        #Finds the pokemon Type 2 line
        if this_line.startswith('Type2'):
            Type_2 = this_line.split(':')[-1].strip('\n')
            #print(Type_2)
            #Adds pokemon Type 2 to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Types'].append(Type_2)

        #Finds the pokemon Ability line
        if this_line.startswith('Ability'):
            Ability_name = this_line.split(':')[-2].strip('\n')
            #print(Ability_name)
            Ability_info = this_line.split(':')[-1].strip('\n')
            #print(Ability_info)
            #Adds pokemon Ability to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Ability']['Ability_Name'].append(Ability_name)
            Team['Members']['Pokemon_'+str(p)]['Ability']['Ability_Info'].append(Ability_info)

        #Finds the pokemon Item line
        if this_line.startswith('Item'):
            Item = this_line.split(':')[-1].strip('\n')
            #print(Item)
            #Adds pokemon Item to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Item'].append(Item)

        #Finds the pokemon Move 1 line
        if this_line.startswith('Move1'):
            Move_1 = this_line.split(':')[-9].strip('\n')
            #print(Move_1)
            Move_type_1 = this_line.split(':')[-8].strip('\n')
            #print(Move_type_1)
            Move_mode_1 = this_line.split(':')[-7].strip('\n')
            #print(Move_mode_1)
            Move_info_1 = this_line.split(':')[-6].strip('\n')
            #print(Move_info_1)
            Move_method_1 = this_line.split(':')[-5].strip('\n')
            #print(Move_method_1)
            Move_power_1 = this_line.split(':')[-4].strip('\n')
            #print(Move_power_1)
            Move_accuracy_1 = this_line.split(':')[-3].strip('\n')
            #print(Move_accuracy_1)
            Move_PP_1 = this_line.split(':')[-2].strip('\n')
            #print(Move_PP_1)
            Move_Effect_1 = this_line.split(':')[-1].strip('\n')
            #print(Move_Effect_1)
            #Adds pokemon Move 1 to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Name'].append(Move_1)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Type'].append(Move_type_1)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Mode'].append(Move_mode_1)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Info'].append(Move_info_1)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Method'].append(Move_method_1)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Power'].append(Move_power_1)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Accuracy'].append(Move_accuracy_1)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_PP'].append(Move_PP_1)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Effect'].append(Move_Effect_1)

        #Finds the pokemon Move 2 line
        if this_line.startswith('Move2'):
            Move_2 = this_line.split(':')[-9].strip('\n')
            #print(Move_2)
            Move_type_2 = this_line.split(':')[-8].strip('\n')
            #print(Move_type_2)
            Move_mode_2 = this_line.split(':')[-7].strip('\n')
            #print(Move_mode_2)
            Move_info_2 = this_line.split(':')[-6].strip('\n')
            #print(Move_info_2)
            Move_method_2 = this_line.split(':')[-5].strip('\n')
            #print(Move_method_2)
            Move_power_2 = this_line.split(':')[-4].strip('\n')
            #print(Move_power_2)
            Move_accuracy_2 = this_line.split(':')[-3].strip('\n')
            #print(Move_accuracy_2)
            Move_PP_2 = this_line.split(':')[-2].strip('\n')
            #print(Move_PP_2)
            Move_Effect_2 = this_line.split(':')[-1].strip('\n')
            #print(Move_Effect_2)
            #Adds pokemon Move 2 to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Name'].append(Move_2)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Type'].append(Move_type_2)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Mode'].append(Move_mode_2)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Info'].append(Move_info_2)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Method'].append(Move_method_2)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Power'].append(Move_power_2)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Accuracy'].append(Move_accuracy_2)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_PP'].append(Move_PP_2)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Effect'].append(Move_Effect_2)


        #Finds the pokemon Move 3 line
        if this_line.startswith('Move3'):
            Move_3 = this_line.split(':')[-9].strip('\n')
            #print(Move_3)
            Move_type_3 = this_line.split(':')[-8].strip('\n')
            #print(Move_type_3)
            Move_mode_3 = this_line.split(':')[-7].strip('\n')
            #print(Move_mode_3)
            Move_info_3 = this_line.split(':')[-6].strip('\n')
            #print(Move_info_3)
            Move_method_3 = this_line.split(':')[-5].strip('\n')
            #print(Move_method_3)
            Move_power_3 = this_line.split(':')[-4].strip('\n')
            #print(Move_power_3)
            Move_accuracy_3 = this_line.split(':')[-3].strip('\n')
            #print(Move_accuracy_3)
            Move_PP_3 = this_line.split(':')[-2].strip('\n')
            #print(Move_PP_3)
            Move_Effect_3 = this_line.split(':')[-1].strip('\n')
            #print(Move_Effect_3)
            #Adds pokemon Move 3 to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Name'].append(Move_3)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Type'].append(Move_type_3)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Mode'].append(Move_mode_3)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Info'].append(Move_info_3)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Method'].append(Move_method_3)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Power'].append(Move_power_3)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Accuracy'].append(Move_accuracy_3)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_PP'].append(Move_PP_3)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Effect'].append(Move_Effect_3)


        #Finds the pokemon Move 4 line
        if this_line.startswith('Move4'):
            Move_4 = this_line.split(':')[-9].strip('\n')
            #print(Move_4)
            Move_type_4 = this_line.split(':')[-8].strip('\n')
            #print(Move_type_4)
            Move_mode_4 = this_line.split(':')[-7].strip('\n')
            #print(Move_mode_4)
            Move_info_4 = this_line.split(':')[-6].strip('\n')
            #print(Move_info_4)
            Move_method_4 = this_line.split(':')[-5].strip('\n')
            #print(Move_method_4)
            Move_power_4 = this_line.split(':')[-4].strip('\n')
            #print(Move_power_4)
            Move_accuracy_4 = this_line.split(':')[-3].strip('\n')
            #print(Move_accuracy_4)
            Move_PP_4 = this_line.split(':')[-2].strip('\n')
            #print(Move_PP_4)
            Move_Effect_4 = this_line.split(':')[-1].strip('\n')
            #print(Move_Effect_4)
            #Adds pokemon Move 4 to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Name'].append(Move_4)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Type'].append(Move_type_4)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Mode'].append(Move_mode_4)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Info'].append(Move_info_4)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Method'].append(Move_method_4)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Power'].append(Move_power_4)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Accuracy'].append(Move_accuracy_4)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_PP'].append(Move_PP_4)
            Team['Members']['Pokemon_'+str(p)]['Moves']['Move_Effect'].append(Move_Effect_4)

            
        #Updates dictionary with information of all types in the built-in sequence
        if this_line.startswith('All_Types'):
            this_All_Types = this_line.split(':')
            #print(this_All_Types)
            #Adds each type to the dictionary, one by one
            for k in this_All_Types:
                if k != 'All_Types': #ignores the word 'All_Types' and only adds the types to the dictionary
                    Team['Members']['Pokemon_'+str(p)]['Type_Match']['All_Types'].append(k.strip('\n'))
            
        #Finds the offense line
        if this_line.startswith('Offense'):
            this_Offense = this_line.split(':')
            #print(this_Offense)
            #Adds each offensive type_match result to the dictionary, one by one
            for k in this_Offense:
                if k != 'Offense': #ignores the word 'Offense' and only adds the numbers to the dictionary
                    Team['Members']['Pokemon_'+str(p)]['Type_Match']['Offense'].append(float(k.strip('\n')))
                    
        #Finds the defense line
        if this_line.startswith('Defense'):
            this_Defense = this_line.split(':')
            #print(this_Defense)
            #Adds each defensive type_match result to the dictionary, one by one
            for k in this_Defense:
                if k != 'Defense': #ignores the word 'Defense' and only adds the numbers to the dictionary
                    Team['Members']['Pokemon_'+str(p)]['Type_Match']['Defense'].append(float(k.strip('\n')))
            
        #Finds the date when this pokemon entry was created/last edited (makes sure it avoids the team date using p != 0)
        if this_line.startswith('#============================================================#') and p != 0:
            date = this_line.split('# ')[-1].strip('\n')
            #print(date)
            #Adds pokemon date to the dicitonary
            Team['Members']['Pokemon_'+str(p)]['Date'].append(date)

    #Closes file after all the important information is extracted        
    f.close()

    #Returns the dictionary with the compiled information of the current team
    return Team

# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#

#Defines function to do the calculation for the pokemon and export a dictionary, but without creating a .poke file
#this function was designed to be used in the GUI version of the program and allow for previewing a pokemon entry before saving it

def preview_pokemon(Species,Form,Image,Name,Type_1,Type_2,Ability_name,Ability_info,Item,Move_1,Move_type_1,Move_mode_1,Move_info_1,Move_method_1,Move_power_1,Move_accuracy_1,Move_PP_1,Move_Effect_1,Move_2,Move_type_2,Move_mode_2,Move_info_2,Move_method_2,Move_power_2,Move_accuracy_2,Move_PP_2,Move_Effect_2,Move_3,Move_type_3,Move_mode_3,Move_info_3,Move_method_3,Move_power_3,Move_accuracy_3,Move_PP_3,Move_Effect_3,Move_4,Move_type_4,Move_mode_4,Move_info_4,Move_method_4,Move_power_4,Move_accuracy_4,Move_PP_4,Move_Effect_4):
    
    #imports useful libraries
    import datetime
    import os
    
    #Useful variables        
    All_types = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']  #keeps track of all types
    current_outcome = ''  #keeps track of the outcome of the current type_match
    final_outcome = 0  #keeps track of the final outcome, after comparing to other moves(offense) or to pokemon's second type(defense)
                    #before adding it to a list (offense or defense) for data storage. Uses arbitrary low value '0' so it's not a string
                    #and ensures a pokemon with only Status moves will have 0 as the result of offensive type_match
    offense = []  #keeps track of the offensive type_match combining all types and all moves
    defense = []  #keeps track of the deffensive type_match combining all types
    
    #Creates dictionary for current pokemon
    Pokemon = {'Species':[], 'Form':[], 'Image':[], 'Name':[], 'Types':[], 'Ability':{'Ability_Name':[], 'Ability_Info':[]}, 'Item':[], 'Moves':{'Move_Name':[], 'Move_Type':[], 'Move_Mode':[], 'Move_Info':[], 'Move_Method':[], 'Move_Power':[], 'Move_Accuracy':[], 'Move_PP':[], 'Move_Effect':[]}, 'Date':[], 'Type_Match':{'All_Types':[], 'Offense':[], 'Defense':[]}}
    
        
    #Calculates Offensive type advantages:
    #For each type available as the Defensive type
    for types in All_types:

        #Resets helpful variable for the next iteration
        final_outcome = 0

        #Against Move_1 (if not a Status move)
        if Move_mode_1 != 'Status':
            final_outcome = type_match(Move_type_1,types)

        #Against Move_2 (if not a Status move)
        if Move_mode_2 != 'Status':
            current_outcome = type_match(Move_type_2,types)
            #If this outcome is better, it replaces the previous one (the user should use the best move available)
            if current_outcome > final_outcome:
                final_outcome = current_outcome

        #Against Move_3 (if not a Status move)
        if Move_mode_3 != 'Status':
            current_outcome = type_match(Move_type_3,types)
            #If this outcome is better, it replaces the previous one (the user should use the best move available)
            if current_outcome > final_outcome:
                final_outcome = current_outcome

        #Against Move_4 (if not a Status move)
        if Move_mode_4 != 'Status':
            current_outcome = type_match(Move_type_4,types)
            #If this outcome is better, it replaces the previous one (the user should use the best move available)
            if current_outcome > final_outcome:
                final_outcome = current_outcome

        #Adds current outcome to the offense list:
        offense.append(final_outcome)


    #Calculates Defensive type advantages:
    #For each type available as the Offensive type
    for types in All_types:

        #Against Type_1
        final_outcome = type_match(types,Type_1)

        #Against Type_2 (if there is a type 2)
        if Type_2 != '':
            current_outcome = type_match(types,Type_2)
            #Multiplies the two outcomes to generate the final type_match against both types
            final_outcome = final_outcome * current_outcome

        #Adds current outcome to the defense list
        defense.append(final_outcome)
        
    #Applies ability modifier
    (offense,defense) = ability_type_advantages_modifier(All_types,offense,defense,Ability_name,Move_mode_1,Move_mode_2,Move_mode_3,Move_mode_4)
    
    #Applies move modifier
    (offense,defense) =    move_type_advantages_modifier(All_types,offense,defense,Move_mode_1,Move_mode_2,Move_mode_3,Move_mode_4,Move_type_1,Move_type_2,Move_type_3,Move_type_4,Move_1,Move_2,Move_3,Move_4)
        

    #Starts to fill in the pokemon dictionary
    #Adds pokemon Species to the dicitonary
    Pokemon['Species'].append(Species)
    #Adds pokemon Form to the dicitonary
    Pokemon['Form'].append(Form)
    #Adds pokemon Image to the dicitonary
    Pokemon['Image'].append(Image)
    #Adds pokemon name to the dicitonary
    Pokemon['Name'].append(Name)
    #Adds pokemon Type 1 to the dicitonary
    Pokemon['Types'].append(Type_1)
    #Adds pokemon Type 2 to the dicitonary
    Pokemon['Types'].append(Type_2)
    #Adds pokemon Ability Name and Info to the dicitonary
    Pokemon['Ability']['Ability_Name'].append(Ability_name)
    Pokemon['Ability']['Ability_Info'].append(Ability_info)
    #Adds pokemon Item to the dicitonary
    Pokemon['Item'].append(Item)

    #Adds pokemon Move 1 to the dicitonary
    Pokemon['Moves']['Move_Name'].append(Move_1)
    Pokemon['Moves']['Move_Type'].append(Move_type_1)
    Pokemon['Moves']['Move_Mode'].append(Move_mode_1)
    Pokemon['Moves']['Move_Info'].append(Move_info_1)
    Pokemon['Moves']['Move_Method'].append(Move_method_1)
    Pokemon['Moves']['Move_Power'].append(Move_power_1)
    Pokemon['Moves']['Move_Accuracy'].append(Move_accuracy_1)
    Pokemon['Moves']['Move_PP'].append(Move_PP_1)
    Pokemon['Moves']['Move_Effect'].append(Move_Effect_1)

    #Adds pokemon Move 2 to the dicitonary
    Pokemon['Moves']['Move_Name'].append(Move_2)
    Pokemon['Moves']['Move_Type'].append(Move_type_2)
    Pokemon['Moves']['Move_Mode'].append(Move_mode_2)
    Pokemon['Moves']['Move_Info'].append(Move_info_2)
    Pokemon['Moves']['Move_Method'].append(Move_method_2)
    Pokemon['Moves']['Move_Power'].append(Move_power_2)
    Pokemon['Moves']['Move_Accuracy'].append(Move_accuracy_2)
    Pokemon['Moves']['Move_PP'].append(Move_PP_2)
    Pokemon['Moves']['Move_Effect'].append(Move_Effect_2)

    #Adds pokemon Move 3 to the dicitonary
    Pokemon['Moves']['Move_Name'].append(Move_3)
    Pokemon['Moves']['Move_Type'].append(Move_type_3)
    Pokemon['Moves']['Move_Mode'].append(Move_mode_3)
    Pokemon['Moves']['Move_Info'].append(Move_info_3)
    Pokemon['Moves']['Move_Method'].append(Move_method_3)
    Pokemon['Moves']['Move_Power'].append(Move_power_3)
    Pokemon['Moves']['Move_Accuracy'].append(Move_accuracy_3)
    Pokemon['Moves']['Move_PP'].append(Move_PP_3)
    Pokemon['Moves']['Move_Effect'].append(Move_Effect_3)

    #Adds pokemon Move 4 to the dicitonary
    Pokemon['Moves']['Move_Name'].append(Move_4)
    Pokemon['Moves']['Move_Type'].append(Move_type_4)
    Pokemon['Moves']['Move_Mode'].append(Move_mode_4)
    Pokemon['Moves']['Move_Info'].append(Move_info_4)
    Pokemon['Moves']['Move_Method'].append(Move_method_4)
    Pokemon['Moves']['Move_Power'].append(Move_power_4)
    Pokemon['Moves']['Move_Accuracy'].append(Move_accuracy_4)
    Pokemon['Moves']['Move_PP'].append(Move_PP_4)
    Pokemon['Moves']['Move_Effect'].append(Move_Effect_4)
    
    
    #Adds all types to dictionary
    Pokemon['Type_Match']['All_Types'] = All_types
    
    #Adds offensive type_match result to the dictionary
    Pokemon['Type_Match']['Offense'] = offense
    
    #Adds defensive type_match result to the dictionary
    Pokemon['Type_Match']['Defense'] = defense


    #Adds date to the dicitonary
    Pokemon['Date'].append(str(datetime.datetime.now()))


    #Returns the dictionary with the compiled information of the current pokemon
    return Pokemon 
    

# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#

#Defines a function that uses the data base path and a list of pokemon names from the database 
#to assemble, and return, the Team python dictionary and calculate its "statisticcs"

def assemble_team(data_path,Team_name,selected_pokemon):
    
    #imports useful libraries
    import os
    import datetime
    import numpy as np

    #Defines handy counter
    team_counter = 0
    
    #Defines Python Dictionary Team to organize team's information
    Team = {'Members':{'Pokemon_1':{},'Pokemon_2':{},'Pokemon_3':{},'Pokemon_4':{},'Pokemon_5':{},'Pokemon_6':{},}, 'Team_Name':[], 'Strengths':[], 'Weaknesses':[], 'Scores':[], 'Global_Score':[], 'Stats':{},'Date':[]}  
      #Python dictionary to organize the information of all pokemon in the team. 
      #The dictionary is built from the database entries with the aid of the function read_pokemon(data_path,Name)    
    
    
    # ================================================================================= #  Loads data from each pokemon into the Team Python dictionary

    #Reads pokemon information from the database entries one by one and compiles a Python dictionary named Team
    for j in selected_pokemon:
        #Moves handy team counter to the next iteration
        team_counter = team_counter + 1                
        #Reads current pokemon entry
        Pokemon = read_pokemon(data_path,j)
        #Creates dictionary entry within 'Members' for current pokemon
        Team['Members']['Pokemon_'+str(team_counter)] = {}
        #Adds current pokemon entry to the Team Python dictionary
        Team['Members']['Pokemon_'+str(team_counter)].update(Pokemon)
    #Updates Team Name
    Team['Team_Name'].append(Team_name)                

    # ================================================================================= #  Calculates Strengths and Weaknesses, Score and Global Score for the Team

    #Sets up the Strengths and Weaknesses vectors for the Team
    Team['Strengths'] = np.array([0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ])  #sets up Strengths as a numpy vector for ease of calculation
    Team['Weaknesses'] = np.array([0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ]) #sets up Weaknesses as a numpy vector for ease of calculation

    #Adds strengths and weaknesses of each pokemon in the team, one by one
    for pokemon in Team['Members']:  
        Team['Strengths'] = Team['Strengths'] + Team['Members'][pokemon]['Type_Match']['Offense']
        Team['Weaknesses'] = Team['Weaknesses'] + Team['Members'][pokemon]['Type_Match']['Defense']
        
    #Divides strengths and weaknesses by the number of pokemon in the team and rounds to get average value for the team
    Team['Strengths'] = np.round(Team['Strengths']/len(selected_pokemon),3)
    Team['Weaknesses'] = np.round(Team['Weaknesses']/len(selected_pokemon),3)

    #Calculates the Scores for the Team (Strengths/len(selected_pokemon) - Weaknesses/len(selected_pokemon)) for each type
    #Team['Scores'] = np.round(np.round(Team['Strengths']/len(selected_pokemon),3) - np.round(Team['Weaknesses']/len(selected_pokemon),3),3)
    Team['Scores'] = np.round(Team['Strengths'] - Team['Weaknesses'],3)

    #Calculates Global Score for the Team (sum of all individual scores)
    Team['Global_Score'] = sum(Team['Scores'])

    # ================================================================================= #  Checks the team for repeated items 

    #Checks for repeated item in the team (repeated item is normally not allowed in comepetitive gameplay)
    #Resets Repetaed_Item and Items
    Team['Stats']['Repeated_Items'] = []  #resets Stats sub entry that keeps track of the name of repeated items in the team
    Items = []  #keeps track of all items in the team

    #Starts a loop to compile a list with all items in the team
    for poke in Team['Members']:
        Items.append(Team['Members'][poke]['Item'][0])

    #Checks if there is a repeated element in the list
    for element in Items:
        #if an item appears more than once, its name will be added to the Repeated_Item sub entry
        if Items.count(element) > 1:  
            #Only adds item name to the sub entry for the first time, avoiding adding the same item name twice
            if element not in Team['Stats']['Repeated_Items']:
                Team['Stats']['Repeated_Items'].append(element)

    # ================================================================================= #  Checks the team for various conditions and stats 

    #Checks for Physical Attackers, Special Attackers and Pokemon with Status Moves
    #Resets Team Stats Entries
    Team['Stats']['Physical_Moves'] = []  #resets Stats sub entry that keeps track of the name of pokemon with Physical moves in the team
    Team['Stats']['Special_Moves'] = []  #resets Stats sub entry that keeps track of the name of pokemon with Special moves in the team                
    Team['Stats']['Status_Moves'] = []  #resets Stats sub entry that keeps track of the name of pokemon with Status moves in the team

    #Starts to loop through the team to analyze the Pokemons' moves and add them to the appropriate lists
    for poke in Team['Members']:
        #Checks if current pokemon has a physical move
        if 'Physical' in Team['Members'][poke]['Moves']['Move_Mode']:
            #If so, adds pokemon name to the list
            Team['Stats']['Physical_Moves'].append(Team['Members'][poke]['Name'][0])
        #Checks if current pokemon has a special move
        if 'Special' in Team['Members'][poke]['Moves']['Move_Mode']:
            #If so, adds pokemon name to the list
            Team['Stats']['Special_Moves'].append(Team['Members'][poke]['Name'][0])
        #Checks if current pokemon has a status move
        if 'Status' in Team['Members'][poke]['Moves']['Move_Mode']:
            #If so, adds pokemon name to the list
            Team['Stats']['Status_Moves'].append(Team['Members'][poke]['Name'][0])
            
    
    #Gets the date and time of the creation of the new/edited team entry
    Team['Date'] = datetime.datetime.now()
        
    #When done, returns the assembled Team dictionary
    return Team

# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#

#Defines interactive function that helps the use to manage the selected databse (add, edit or delte .poke files)
#Requires the path to the folder relative to the databse to be managed

def manage_data(data_path):
    
    #imports useful libraries
    import datetime
    import os
    import sys

    #Defines useful variables
    goal = ''  #keeps track of the user's goal (add, edit or delete)

    new_goal = ''  #new goal is used when the original goal cannot be executed for some reason (e.g. tried to add an entry that already exists)
    #new_goal is useful to redirect the user to another goal without having to restart the program
    
    pokemon_list = []  #Keeps track of all pokemon entries in the database
    
    change = ''  #helps the user select what to change about the pokemon when editing a pokemon entry

    check = ''  #helps the user check if provided information is correct and ready to be saved

    Name = ''  #pokemon name

    Type_1 = ''  #pokemon type 1

    Type_2 = ''  #pokemon type 2

    Ability = ''  #pokemon ability

    Item = ''  #pokemon item

    Move_1 = ''  #move 1 name
    Move_type_1 = ''  #move 1 type
    Move_mode_1 = ''  #move 1 mode (Physical,Special or Status)

    Move_2 = ''  #move 2 name
    Move_type_2 = ''  #move 2 type
    Move_mode_2 = ''  #move 2 mode (Physical,Special or Status)

    Move_3 = ''  #move 3 name
    Move_type_3 = ''  #move 3 type
    Move_mode_3 = ''  #move 3 mode (Physical,Special or Status)

    Move_4 = ''  #move 4 name
    Move_type_4 = ''  #move 4 type
    Move_mode_4 = ''  #move 4 mode (Physical,Special or Status)

    #keeps track of all types
    All_types = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']

    #keeps track of all types excpet selected pokemon type 1 when selecting pokemon type 2
    All_types_2 = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']

    #keeps track of all possible move modes
    All_Move_modes = ['Physical', 'Special', 'Status']
    
    # ============================================ #  Makes preparations to start program
    
    #Compiles list of files within the input directory
    files = next(os.walk(data_path))[2]
    #print(files)
        
    #Compiles a list of available pokemon within the database
    for f in files:
        if f.endswith('.poke'):
            pokemon_list.append(f.replace('.poke',''))            
            
    # ============================================ #  Gives the user options 
    

    #Asks the user if they would like to add, edit or delete an entry
    goal = input("Would like to add, edit or delete a pokemon entry?"+'\n'+"Write exit to end session."+'\n')

    #Ensures the user will only proceed in case they used one of the four valid options
    while goal != 'add' and goal != 'Add' and goal != 'edit' and goal != 'Edit' and goal != 'delete' and goal != 'Delete' and goal != 'exit' and goal != 'Exit':
        print(str(goal)+' is not a valid option. Please try again.')
        goal = input("Would like to add, edit or delete a pokemon entry?"+'\n'+"Write exit to end session."+'\n')


    # ============================================ #  Add Entry

    #In case the user wants to add a pokemon entry
    if goal == 'add' or goal == 'Add':

        #Asks the user the information for the pokemon and passes it to the register_pokemon function

        #Fisrt, it asks the pokemon name
        Name = input('What is the pokemon name?'+'\n')  #pokemon name

        #Checks if the file for that pokemon was created before
        if os.path.exists(str(data_path)+'/'+str(Name)+".poke"):
            print("This pokemon entry already exists.")

            #Asks the user what to do then
            new_goal = input("Would you like to overwrite that entry instead? Or would you like to end session instead? (Write exit to end session)"+'\n'+"If overwriting entry, previous entry will be forever deleted."+'\n')

            #ensures the user will only proceed in case they used one of the two valid options
            while new_goal != 'overwrite' and new_goal != 'Overwrite' and new_goal != 'yes' and new_goal != 'Yes' and new_goal != 'exit' and new_goal != 'Exit':
                print(str(new_goal)+" is not a valid option. Please try again.")
                new_goal = input("Would you like to overwrite that entry instead? Or would to like to end session instead? (Write exit to end session)"+'\n'+"If overwriting entry, previous entry will be forever deleted."+'\n')

        #Ends session in case the user decided to do so
        if new_goal == 'exit' or new_goal =='Exit': 
            print('Session was ended. Progressed was not saved.')
            return
            #sys.exit('Session was ended. Progressed was not saved.')

        #If the user decided to either add a new entry or overwrite an old entry, the program proceeds normally under the 'add' option
        if new_goal == '' or new_goal == 'overwrite' or new_goal == 'Overwrite' or new_goal == 'yes' or new_goal == 'Yes':

            #Asks pokemon type 1
            Type_1 = input('What is '+ str(Name) + "'s first type?"+'\n')  #pokemon type 1

            #If a non-existing type was inserted or if a type was misspelled, it makes sure the user will have a chance to correct it
            if Type_1 not in All_types:
                print(str(Type_1)+" is not a valid type. Please try inserting one of the following:")
                print(str(All_types).strip('][').replace("'",""))
                print('Or write exit to end session.')

                #Makes sure the user only selects one of the valid options
                while Type_1 != 'exit' and Type_1 != 'Exit' and Type_1 not in All_types:
                    print(str(Type_1)+" is not a valid type. Please try inserting one of the following:")
                    print(str(All_types).strip('][').replace("'",""))
                    print('Or write exit to end session.')
                    Type_1 = input('What is '+ str(Name) + "'s first type?"+'\n')  #pokemon type 1

            #Ends session in case the user decided to do so
            if Type_1 == 'exit' or Type_1 =='Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')

            #Asks pokemon type 2 in case the user decided not to end session
            Type_2 = input('What is '+ str(Name) + "'s second type? Please leave this field empty if there is no second type."+'\n')  #pokemon type 2

            #Removes selected pokemon type 1 from possible options for type 2
            All_types_2.remove(Type_1)

            #If a non-existing type was inserted or if a type was misspelled, it makes sure the user will have a chance to correct it
            if Type_2 != '' and Type_2 not in All_types_2 and Type_2 != Type_1:
                print(str(Type_2)+" is not a valid type. Please leave this field empty if there is no second type or try inserting one of the following:")
                print(str(All_types_2).strip('][').replace("'",""))
                print('Or write exit to end session.')

                #Makes sure the user only selects one of the valid options
                while Type_2 != 'exit' and Type_2 != 'Exit' and Type_2 != '' and Type_2 not in All_types_2:
                    print(str(Type_2)+" is not a valid type. Please leave this field empty if there is no second type or try inserting one of the following:")
                    print(str(All_types_2).strip('][').replace("'",""))
                    print('Or write exit to end session.')
                    Type_2 = input('What is '+ str(Name) + "'s second type? Please leave this field empty if there is no second type."+'\n')  #pokemon type 2

            #If pokemon type 1 was selected again, it makes sure the user will have a chance to correct it
            if Type_2 == Type_1:
                print(str(Type_1)+" was already selected as the first type. Please leave this field empty if there is no second type.")
                print("Or try inserting one of the following:")
                print(str(All_types_2).strip('][').replace("'",""))
                print('Or write exit to end session.')

                #Makes sure the user only selects one of the valid options
                while Type_2 != 'exit' and Type_2 != 'Exit' and Type_2 != '' and Type_2 not in All_types_2:
                    print(str(Type_2)+" is not a valid type. Please leave this field empty if there is no second type or try inserting one of the following:")
                    print(str(All_types_2).strip('][').replace("'",""))
                    print('Or write exit to end session.')
                    Type_2 = input('What is '+ str(Name) + "'s second type? Please leave this field empty if there is no second type."+'\n')  #pokemon type 2

            #Ends session in case the user decided to do so
            if Type_2 == 'exit' or Type_2 =='Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')


            #Asks pokemon ability in case the user decided not to end session
            Ability = input('What is '+ str(Name) + "'s Ability? (Write exit to end session)"+'\n')  #pokemon ability

            #Ends session in case the user decided to do so
            if Ability == 'exit' or Ability == 'Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')

            #Asks pokemon item in case the user decided not to end session
            Item = input('What is '+ str(Name) + "'s Held Item? (Write exit to end session)"+'\n')  #pokemon item

            #Ends session in case the user decided to do so
            if Item == 'exit' or Item ==  'Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')

        # ======= # Move 1

            #Asks pokemon move 1 in case the user decided not to end session
            Move_1 = input('What is '+ str(Name) + "'s Move 1? (Write exit to end session)"+'\n')  #pokemon move 1

            #Ends session in case the user decided to do so
            if Move_1 == 'exit' or Move_1 ==  'Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')          

            #Asks pokemon Move type 1
            Move_type_1 = input('What is '+ str(Name) + "'s move 1 type?"+'\n')  #pokemon move type 1

            #If a non-existing type was inserted or if a type was misspelled, it makes sure the user will have a chance to correct it
            if Move_type_1 not in All_types:

                #Makes sure the user only selects one of the valid options
                while Move_type_1 != 'exit' and Move_type_1 != 'Exit' and Move_type_1 not in All_types:
                    print(str(Move_type_1)+" is not a valid type. Please try inserting one of the following:")
                    print(str(All_types).strip('][').replace("'",""))
                    print('Or write exit to end session.')
                    Move_type_1 = input('What is '+ str(Name) + "'s move 1 type?"+'\n')  #pokemon move type 1

            #Ends session in case the user decided to do so
            if Move_type_1 == 'exit' or Move_type_1 =='Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')

            #Asks pokemon Move mode 1
            Move_mode_1 = input('What is '+ str(Name) + "'s move 1 mode?"+'\n')  #pokemon move mode 1

            #If a non-existing mode was inserted or if a mode was misspelled, it makes sure the user will have a chance to correct it
            if Move_mode_1 not in All_Move_modes:

                #Makes sure the user only selects one of the valid options
                while Move_mode_1 != 'exit' and Move_mode_1 != 'Exit' and Move_mode_1 not in All_Move_modes:
                    print(str(Move_mode_1)+" is not a valid mode. Please try inserting one of the following:")
                    print(str(All_Move_modes ).strip('][').replace("'",""))
                    print('Or write exit to end session.')
                    Move_mode_1 = input('What is '+ str(Name) + "'s move 1 mode?"+'\n')  #pokemon move mode 1

            #Ends session in case the user decided to do so
            if Move_mode_1 == 'exit' or Move_mode_1 =='Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')

        # ======= # Move 2

            #Asks pokemon move 2 in case the user decided not to end session
            Move_2 = input('What is '+ str(Name) + "'s Move 2? (Write exit to end session)"+'\n')  #pokemon move 2

            #Ends session in case the user decided to do so
            if Move_2 == 'exit' or Move_2 ==  'Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')          

            #Asks pokemon Move type 2
            Move_type_2 = input('What is '+ str(Name) + "'s move 2 type?"+'\n')  #pokemon move type 2

            #If a non-existing type was inserted or if a type was misspelled, it makes sure the user will have a chance to correct it
            if Move_type_2 not in All_types:

                #Makes sure the user only selects one of the valid options
                while Move_type_2 != 'exit' and Move_type_2 != 'Exit' and Move_type_2 not in All_types:
                    print(str(Move_type_2)+" is not a valid type. Please try inserting one of the following:")
                    print(str(All_types).strip('][').replace("'",""))
                    print('Or write exit to end session.')
                    Move_type_2 = input('What is '+ str(Name) + "'s move 2 type?"+'\n')  #pokemon move type 2

            #Ends session in case the user decided to do so
            if Move_type_2 == 'exit' or Move_type_2 =='Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')

            #Asks pokemon Move mode 2
            Move_mode_2 = input('What is '+ str(Name) + "'s move 2 mode?"+'\n')  #pokemon move mode 2

            #If a non-existing mode was inserted or if a mode was misspelled, it makes sure the user will have a chance to correct it
            if Move_mode_2 not in All_Move_modes:

                #Makes sure the user only selects one of the valid options
                while Move_mode_2 != 'exit' and Move_mode_2 != 'Exit' and Move_mode_2 not in All_Move_modes:
                    print(str(Move_mode_2)+" is not a valid mode. Please try inserting one of the following:")
                    print(str(All_Move_modes ).strip('][').replace("'",""))
                    print('Or write exit to end session.')
                    Move_mode_2 = input('What is '+ str(Name) + "'s move 2 mode?"+'\n')  #pokemon move mode 2

            #Ends session in case the user decided to do so
            if Move_mode_2 == 'exit' or Move_mode_2 =='Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')

        # ======= # Move 3

            #Asks pokemon move 3 in case the user decided not to end session
            Move_3 = input('What is '+ str(Name) + "'s Move 3? (Write exit to end session)"+'\n')  #pokemon move 3

            #Ends session in case the user decided to do so
            if Move_3 == 'exit' or Move_3 ==  'Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')        

            #Asks pokemon Move type 3
            Move_type_3 = input('What is '+ str(Name) + "'s move 3 type?"+'\n')  #pokemon move type 3

            #If a non-existing type was inserted or if a type was misspelled, it makes sure the user will have a chance to correct it
            if Move_type_3 not in All_types:

                #Makes sure the user only selects one of the valid options
                while Move_type_3 != 'exit' and Move_type_3 != 'Exit' and Move_type_3 not in All_types:
                    print(str(Move_type_3)+" is not a valid type. Please try inserting one of the following:")
                    print(str(All_types).strip('][').replace("'",""))
                    print('Or write exit to end session.')
                    Move_type_3 = input('What is '+ str(Name) + "'s move 3 type?"+'\n')  #pokemon move type 3

            #Ends session in case the user decided to do so
            if Move_type_3 == 'exit' or Move_type_3 =='Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')

            #Asks pokemon Move mode 3
            Move_mode_3 = input('What is '+ str(Name) + "'s move 3 mode?"+'\n')  #pokemon move mode 3

            #If a non-existing mode was inserted or if a mode was misspelled, it makes sure the user will have a chance to correct it
            if Move_mode_3 not in All_Move_modes:

                #Makes sure the user only selects one of the valid options
                while Move_mode_3 != 'exit' and Move_mode_3 != 'Exit' and Move_mode_3 not in All_Move_modes:
                    print(str(Move_mode_3)+" is not a valid mode. Please try inserting one of the following:")
                    print(str(All_Move_modes ).strip('][').replace("'",""))
                    print('Or write exit to end session.')
                    Move_mode_3 = input('What is '+ str(Name) + "'s move 3 mode?"+'\n')  #pokemon move mode 3

            #Ends session in case the user decided to do so
            if Move_mode_3 == 'exit' or Move_mode_3 =='Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')

        # ======= # Move 4

            #Asks pokemon move 4 in case the user decided not to end session
            Move_4 = input('What is '+ str(Name) + "'s Move 4? (Write exit to end session)"+'\n')  #pokemon move 4


            #Ends session in case the user decided to do so
            if Move_4 == 'exit' or Move_4 ==  'Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')           

            #Asks pokemon Move type 4
            Move_type_4 = input('What is '+ str(Name) + "'s move 4 type?"+'\n')  #pokemon move type 4

            #If a non-existing type was inserted or if a type was misspelled, it makes sure the user will have a chance to correct it
            if Move_type_4 not in All_types:

                #Makes sure the user only selects one of the valid options
                while Move_type_4 != 'exit' and Move_type_4 != 'Exit' and Move_type_4 not in All_types:
                    print(str(Move_type_4)+" is not a valid type. Please try inserting one of the following:")
                    print(str(All_types).strip('][').replace("'",""))
                    print('Or write exit to end session.')
                    Move_type_4 = input('What is '+ str(Name) + "'s move 4 type?"+'\n')  #pokemon move type 4

            #Ends session in case the user decided to do so
            if Move_type_4 == 'exit' or Move_type_4 =='Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')

            #Asks pokemon Move mode 4
            Move_mode_4 = input('What is '+ str(Name) + "'s move 4 mode?"+'\n')  #pokemon move mode 4

            #If a non-existing mode was inserted or if a mode was misspelled, it makes sure the user will have a chance to correct it
            if Move_mode_4 not in All_Move_modes:

                #Makes sure the user only selects one of the valid options
                while Move_mode_4 != 'exit' and Move_mode_4 != 'Exit' and Move_mode_4 not in All_Move_modes:
                    print(str(Move_mode_4)+" is not a valid mode. Please try inserting one of the following:")
                    print(str(All_Move_modes ).strip('][').replace("'",""))
                    print('Or write exit to end session.')
                    Move_mode_4 = input('What is '+ str(Name) + "'s move 4 mode?"+'\n')  #pokemon move mode 4

            #Ends session in case the user decided to do so
            if Move_mode_4 == 'exit' or Move_mode_4 =='Exit': 
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')


            #Displays all the provided information to the user for a final check
            print("#============================================================#"+'\n')
            print('Name: '+Name+'\n')
            print('Type1: '+Type_1+'\n')
            print('Type2: '+Type_2+'\n')
            print('Ability: '+Ability+'\n')
            print('Item: '+Item+'\n')
            print('Move1: '+Move_1+' : '+Move_type_1+' : '+Move_mode_1+'\n')
            print('Move2: '+Move_2+' : '+Move_type_2+' : '+Move_mode_2+'\n')
            print('Move3: '+Move_3+' : '+Move_type_3+' : '+Move_mode_3+'\n')
            print('Move4: '+Move_4+' : '+Move_type_4+' : '+Move_mode_4+'\n')
            print("#============================================================#")

            #Final check
            check = input('Is the information above correct? Write yes to save data or no to end program.'+'\n')

            #Makes sure the user selects a valid option
            while check != 'yes' and check != 'Yes' and check != 'no' and check != 'No' and check != 'exit' and check != 'Exit':
                print(str(check)+' is not a valid option. Please try again.')
                check = input('Is the information above correct? Write yes to save data or no to end program. (Write exit to end session)'+'\n')

            if check == 'yes' or check == 'Yes':
                register_pokemon(data_path,Name,Type_1,Type_2,Ability,Item,Move_1,Move_type_1,Move_mode_1,Move_2,Move_type_2,Move_mode_2,Move_3,Move_type_3,Move_mode_3,Move_4,Move_type_4,Move_mode_4)
                #print('Data was successfully saved for '+str(Name)+'!')

            if check == 'no' or check == 'No' or check == 'exit' or check == 'Exit':
                print('Session was ended. Progressed was not saved.')
                return
                #sys.exit('Session was ended. Progressed was not saved.')


    # ============================================ #  Delete Entry


    #In case the user wants to delete a pokemon entry
    if goal == 'delete' or goal == 'Delete':
        
        #Shows the user all pokemon entries in the database
        print('Available Pokemon: ' + str(pokemon_list).strip('][').replace("'",""))

        #Asks the user the information for the pokemon and passes it to the delete_pokemon function

        #Fisrt, it asks the pokemon name
        Name = input('What is the pokemon name?'+'\n')  #pokemon name

        #Checks if the file for that pokemon was created before and gives the user the chance to try another file
        while os.path.exists(str(data_path)+'/'+str(Name)+".poke") == False and Name != 'exit' and Name != 'Exit':
            print("This pokemon entry does not exist in the specified database folder. Please try again. (Write exit to end session)")
            Name = input('What is the pokemon name?'+'\n')  #pokemon name

        #Ends session in case the user decided to do so
        if Name == 'exit' or Name =='Exit': 
            print('Session was ended. Pokemon entry was not deleted.')
            return
            #sys.exit('Session was ended. Pokemon entry was not deleted.')

        #Asks the user if they really want to delete the entry
        new_goal = input("Are you sure you want to permanently delete this pokemon entry? Or would to like to end session instead? (Write exit to end session)"+'\n')

        #ensures the user will only proceed in case they used one of the valid options
        while new_goal != 'yes' and new_goal != 'Yes' and new_goal != 'exit' and new_goal != 'Exit' and new_goal != 'no' and new_goal != 'No':
            print(str(new_goal)+" is not a valid option. Please try again.")
            new_goal = input("Are you sure you want to permanently delete this pokemon entry? Or would to like to end session instead? (Write exit to end session)"+'\n')

        #Ends session in case the user decided to do so
        if new_goal == 'exit' or new_goal =='Exit' or new_goal == 'no' or new_goal =='No': 
            print('Session was ended. Pokemon entry was not deleted.')
            return
            #sys.exit('Session was ended. Pokemon entry was not deleted.')


        #Proceeds if the user decide to delete the entry, the information is passed to the delete_pokemon function
        if new_goal == 'Yes' or new_goal == 'yes':
            delete_pokemon(data_path,Name)


    # ============================================ #  Edit Entry


    #In case the user wants to edit a pokemon entry
    if goal == 'edit' or goal == 'Edit':
        
        #Shows the user all pokemon entries in the database
        print('Available Pokemon: ' + str(pokemon_list).strip('][').replace("'",""))
        
        #Asks the name of the Pokemon
        Name = input('What is the pokemon name?'+'\n')  #pokemon name

        #Checks if the file for that pokemon was created before and gives the user the chance to try another file
        while os.path.exists(str(data_path)+'/'+str(Name)+".poke") == False and Name != 'exit' and Name != 'Exit':
            print("This pokemon entry does not exist in the specified database folder. Please try again. (Write exit to end session)")
            Name = input('What is the pokemon name?'+'\n')  #pokemon name

        #Ends session in case the user decided to do so
        if Name == 'exit' or Name =='Exit': 
            print('Session was ended. Progressed was not saved.')
            return
            #sys.exit('Session was ended. Progressed was not saved.')
            
        #Reads pokemon information from the file
        Pokemon = read_pokemon(data_path,Name)
        
        #Displays current pokemon information
        print(str(Name)+"'s entry currently is:")
        print('#============================================================#'+'\n')
        print('Name: '+str(Pokemon['Name'][0])+'\n')
        print('Type1: '+str(Pokemon['Types'][0])+'\n')
        print('Type2: '+str(Pokemon['Types'][1])+'\n')
        print('Ability: '+str(Pokemon['Ability'][0])+'\n')
        print('Item: '+str(Pokemon['Item'][0])+'\n')
        print('Move1: '+str(Pokemon['Moves']['Move_Name'][0])+' : '+str(Pokemon['Moves']['Move_Type'][0])+' : '+str(Pokemon['Moves']['Move_Mode'][0])+'\n')
        print('Move2: '+str(Pokemon['Moves']['Move_Name'][1])+' : '+str(Pokemon['Moves']['Move_Type'][1])+' : '+str(Pokemon['Moves']['Move_Mode'][1])+'\n')
        print('Move3: '+str(Pokemon['Moves']['Move_Name'][2])+' : '+str(Pokemon['Moves']['Move_Type'][2])+' : '+str(Pokemon['Moves']['Move_Mode'][2])+'\n')
        print('Move4: '+str(Pokemon['Moves']['Move_Name'][3])+' : '+str(Pokemon['Moves']['Move_Type'][3])+' : '+str(Pokemon['Moves']['Move_Mode'][3])+'\n')
        print('#============================================================# '+str(Pokemon['Date'][0]))
        
        
        #Asks the user what they would like to change
        while change != 'Done' and change != 'done':
            change = input("What would you like to change? Write Done when finished or Exit to quit.")
            
            #When changing type 1
            if change == 'Type_1' or change == 'type_1' or change == 'Type1' or change == 'type1' or change == 'Type 1' or change == 'type 1':
                
                #resets all types available as type 1
                All_types = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']
                
                #removes current type 2 from options available for type 1
                All_types.remove(Pokemon['Types'][1])
                
                #Asks user the new type_1
                Pokemon['Types'][0] = input('What is '+ str(Name) + "'s first type?"+'\n')  #pokemon type 1

                #If a non-existing type was inserted or if a type was misspelled, it makes sure the user will have a chance to correct it
                if Pokemon['Types'][0] != 'exit' and Pokemon['Types'][0] != 'Exit' and Pokemon['Types'][0] not in All_types:

                    #Makes sure the user only selects one of the valid options
                    while Pokemon['Types'][0] != 'exit' and Pokemon['Types'][0] != 'Exit' and Pokemon['Types'][0] not in All_types:
                        
                        if Pokemon['Types'][0] == Pokemon['Types'][1]:  #when type_2 was selected again
                            print(str(Pokemon['Types'][1])+" was already selected as the second type.")
                            print("Please try inserting one of the following:")
                            print(str(All_types).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            Pokemon['Types'][0] = input('What is '+ str(Name) + "'s firt type?"+'\n')  #pokemon type 1
                        
                        else: #when type_2 wasn't selected again
                            print(str(Pokemon['Types'][0])+" is not a valid type. Please try inserting one of the following:")
                            print(str(All_types).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            Pokemon['Types'][0] = input('What is '+ str(Name) + "'s first type?"+'\n')  #pokemon type 1   

                #Ends session in case the user decided to do so
                if Pokemon['Types'][0] == 'exit' or Pokemon['Types'][0] =='Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')
            
            #When changing type 2
            elif change == 'Type_2' or change == 'type_2' or change == 'Type2' or change == 'type2' or change == 'Type 2' or change == 'type 2':
                #Resets possibilities for pokemon type 2
                All_types_2 = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']
                
                #Removes selected pokemon type 1 from possible options for type 2
                All_types_2.remove(Pokemon['Types'][0])
                
                #Asks user the new type_2
                Pokemon['Types'][1] = input('What is '+ str(Name) + "'s second type? Please leave this field empty if there is no second type."+'\n')  #pokemon type 2

                #If a non-existing type was inserted or if a type was misspelled, it makes sure the user will have a chance to correct it
                if Pokemon['Types'][1] != 'exit' and Pokemon['Types'][1] != 'Exit' and Pokemon['Types'][1] != '' and Pokemon['Types'][1] not in All_types_2:
                    #Makes sure the user only selects one of the valid options
                    while Pokemon['Types'][1] != 'exit' and Pokemon['Types'][1] != 'Exit' and Pokemon['Types'][1] != '' and Pokemon['Types'][1] not in All_types_2:
                        
                        if Pokemon['Types'][1] == Pokemon['Types'][0]:  #when type_1 was selected again
                            print(str(Pokemon['Types'][0])+" was already selected as the first type. Please leave this field empty if there is no second type.")
                            print("Or try inserting one of the following:")
                            print(str(All_types_2).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            Pokemon['Types'][1] = input('What is '+ str(Name) + "'s second type? Please leave this field empty if there is no second type."+'\n')  #pokemon type 2
                        
                        else: #when type_1 wasn't selected again
                            print(str(Pokemon['Types'][1])+" is not a valid type. Please try inserting one of the following:")
                            print(str(All_types_2).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            Pokemon['Types'][1] = input('What is '+ str(Name) + "'s second type? Please leave this field empty if there is no second type."+'\n')  #pokemon type 2                 

                #Ends session in case the user decided to do so
                if Pokemon['Types'][1] == 'exit' or Pokemon['Types'][1] =='Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')
                    
                    
            #When changing ability
            elif change == 'Ability' or change == 'ability':
                
                #Asks pokemon ability in case the user decided to do so
                Pokemon['Ability'][0] = input('What is '+ str(Name) + "'s Ability? (Write exit to end session)"+'\n')  #pokemon ability

                #Ends session in case the user decided to do so
                if Pokemon['Ability'][0] == 'exit' or Pokemon['Ability'][0] == 'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')
                    
                    
            #When changing pokemon item
            elif change == 'Item' or change == 'item':                    
                    
                #Asks pokemon item in case the user decided not to end session
                Pokemon['Item'][0] = input('What is '+ str(Name) + "'s Held Item? (Write exit to end session)"+'\n')  #pokemon item

                #Ends session in case the user decided to do so
                if Pokemon['Item'][0] == 'exit' or Pokemon['Item'][0] ==  'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')        


        # ======= # Move 1
        
            #If the user decided to change pokemon move 1
            elif change == 'Move_1' or change == 'move_1' or change == 'Move1' or change == 'move1' or change == 'Move 1' or change == 'move 1':

                #Asks pokemon move 1 in case the user decided to change it
                Pokemon['Moves']['Move_Name'][0] = input('What is '+ str(Name) + "'s Move 1? (Write exit to end session)"+'\n') #pokemon move 1

                #Ends session in case the user decided to do so
                if Pokemon['Moves']['Move_Name'][0] == 'exit' or Pokemon['Moves']['Move_Name'][0] ==  'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')

                #Asks if the user would like to change pokemon move type 1
                change_move_type_1 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 1 type?"+'\n')

                #Makes sure the user chooses a valid option
                while change_move_type_1 != "Yes" and change_move_type_1 != "yes" and change_move_type_1 != "No" and change_move_type_1 != "no" and change_move_type_1 != "Exit" and change_move_type_1 != "exit":
                    print(str(change_move_type_1)+" is not a valid option. Please try again. (Write exit to end session)")
                    change_move_type_1 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 1 type?"+'\n')

                #Ends session in case the user decided to do so
                if change_move_type_1 == 'exit' or change_move_type_1 == 'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')

                #If the user decided to change pokemon move 1 type
                if change_move_type_1 == 'yes' or change_move_type_1 == 'Yes':

                    #Asks pokemon Move type 1
                    Pokemon['Moves']['Move_Type'][0] = input('What is '+ str(Name) + "'s Move 1 type?"+'\n')  #pokemon move type 1

                    #If a non-existing type was inserted or if a type was misspelled, it makes sure the user will have a chance to correct it
                    if Pokemon['Moves']['Move_Type'][0] not in All_types:

                        #Makes sure the user only selects one of the valid options
                        while Pokemon['Moves']['Move_Type'][0] != 'exit' and Pokemon['Moves']['Move_Type'][0] != 'Exit' and Pokemon['Moves']['Move_Type'][0] not in All_types:
                            print(str(Pokemon['Moves']['Move_Type'][0])+" is not a valid type. Please try inserting one of the following:")
                            print(str(All_types).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            Pokemon['Moves']['Move_Type'][0] = input('What is '+ str(Name) + "'s Move 1 type?"+'\n')  #pokemon move type 1

                    #Ends session in case the user decided to do so
                    if Pokemon['Moves']['Move_Type'][0] == 'exit' or Pokemon['Moves']['Move_Type'][0] =='Exit': 
                        print('Session was ended. Progressed was not saved.')
                        return
                        #sys.exit('Session was ended. Progressed was not saved.')

                #Asks if the user would like to change pokemon move mode 1
                change_move_mode_1 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 1 mode?"+'\n')

                #Makes sure the user chooses a valid option
                while change_move_mode_1 != "Yes" and change_move_mode_1 != "yes" and change_move_mode_1 != "No" and change_move_mode_1 != "no" and change_move_mode_1 != "Exit" and change_move_mode_1 != "exit":
                    print(str(change_move_mode_1)+" is not a valid option. Please try again. (Write exit to end session)")
                    change_move_mode_1 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 1 mode?"+'\n')

                #Ends session in case the user decided to do so
                if change_move_mode_1 == 'exit' or change_move_mode_1 == 'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')

                #If the user decided to change pokemon move 1 mode
                if change_move_mode_1 == 'yes' or change_move_mode_1 == 'Yes':

                    #Asks pokemon Move mode 1
                    Pokemon['Moves']['Move_Mode'][0] = input('What is '+ str(Name) + "'s move 1 Mode?"+'\n')  #pokemon move mode 1

                    #If a non-existing mode was inserted or if a mode was misspelled, it makes sure the user will have a chance to correct it
                    if Pokemon['Moves']['Move_Mode'][0] not in All_Move_modes:

                        #Makes sure the user only selects one of the valid options
                        while Pokemon['Moves']['Move_Mode'][0] != 'exit' and Pokemon['Moves']['Move_Mode'][0] != 'Exit' and Pokemon['Moves']['Move_Mode'][0] not in All_Move_modes:
                            print(str(Pokemon['Moves']['Move_Mode'][0])+" is not a valid mode. Please try inserting one of the following:")
                            print(str(All_Move_modes ).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            Pokemon['Moves']['Move_Mode'][0] = input('What is '+ str(Name) + "'s move 1 Mode?"+'\n')  #pokemon move mode 1

                    #Ends session in case the user decided to do so
                    if Pokemon['Moves']['Move_Mode'][0] == 'exit' or Pokemon['Moves']['Move_Mode'][0] =='Exit': 
                        print('Session was ended. Progressed was not saved.')
                        return
                        #sys.exit('Session was ended. Progressed was not saved.')

        # ======= # Move 2

            #If the user decided to change pokemon move 2
            elif change == 'Move_2' or change == 'move_2' or change == 'Move2' or change == 'move2' or change == 'Move 2' or change == 'move 2':

                #Asks pokemon move 2 in case the user decided not to end session
                Pokemon['Moves']['Move_Name'][1] = input('What is '+ str(Name) + "'s Move 2? (Write exit to end session)"+'\n')  #pokemon move 2

                #Ends session in case the user decided to do so
                if Pokemon['Moves']['Move_Name'][1] == 'exit' or Pokemon['Moves']['Move_Name'][1] ==  'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')

                #Asks if the user would like to change pokemon move type 2
                change_move_type_2 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 2 type?"+'\n')

                #Makes sure the user chooses a valid option
                while change_move_type_2 != "Yes" and change_move_type_2 != "yes" and change_move_type_2 != "No" and change_move_type_2 != "no" and change_move_type_2 != "Exit" and change_move_type_2 != "exit":
                    print(str(change_move_type_2)+" is not a valid option. Please try again. (Write exit to end session)")
                    change_move_type_2 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 2 type?"+'\n')

                #Ends session in case the user decided to do so
                if change_move_type_2 == 'exit' or change_move_type_2 == 'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')

                #If the user decided to change pokemon move 2 type
                if change_move_type_2 == 'yes' or change_move_type_2 == 'Yes':

                    #Asks pokemon Move type 2
                    Pokemon['Moves']['Move_Type'][1] = input('What is '+ str(Name) + "'s Move 2 type?"+'\n')  #pokemon move type 2

                    #If a non-existing type was inserted or if a type was misspelled, it makes sure the user will have a chance to correct it
                    if Pokemon['Moves']['Move_Type'][1] not in All_types:

                        #Makes sure the user only selects one of the valid options
                        while Pokemon['Moves']['Move_Type'][1] != 'exit' and Pokemon['Moves']['Move_Type'][1] != 'Exit' and Pokemon['Moves']['Move_Type'][1] not in All_types:
                            print(str(Pokemon['Moves']['Move_Type'][1])+" is not a valid type. Please try inserting one of the following:")
                            print(str(All_types).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            Pokemon['Moves']['Move_Type'][1] = input('What is '+ str(Name) + "'s Move 2 type?"+'\n')  #pokemon move type 2

                    #Ends session in case the user decided to do so
                    if Pokemon['Moves']['Move_Type'][1] == 'exit' or Pokemon['Moves']['Move_Type'][1] =='Exit': 
                        print('Session was ended. Progressed was not saved.')
                        return
                        #sys.exit('Session was ended. Progressed was not saved.')

                #Asks if the user would like to change pokemon move mode 2
                change_move_mode_2 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 2 mode?"+'\n')

                #Makes sure the user chooses a valid option
                while change_move_mode_2 != "Yes" and change_move_mode_2 != "yes" and change_move_mode_2 != "No" and change_move_mode_2 != "no" and change_move_mode_2 != "Exit" and change_move_mode_2 != "exit":
                    print(str(change_move_mode_2)+" is not a valid option. Please try again. (Write exit to end session)")
                    change_move_mode_2 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 2 mode?"+'\n')

                #Ends session in case the user decided to do so
                if change_move_mode_2 == 'exit' or change_move_mode_2 == 'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')

                #If the user decided to change pokemon move 2 mode
                if change_move_mode_2 == 'yes' or change_move_mode_2 == 'Yes':

                    #Asks pokemon Move mode 2
                    Pokemon['Moves']['Move_Mode'][1] = input('What is '+ str(Name) + "'s move 2 Mode?"+'\n')  #pokemon move mode 2

                    #If a non-existing mode was inserted or if a mode was misspelled, it makes sure the user will have a chance to correct it
                    if Pokemon['Moves']['Move_Mode'][1] not in All_Move_modes:

                        #Makes sure the user only selects one of the valid options
                        while Pokemon['Moves']['Move_Mode'][1] != 'exit' and Pokemon['Moves']['Move_Mode'][1] != 'Exit' and Pokemon['Moves']['Move_Mode'][1] not in All_Move_modes:
                            print(str(Pokemon['Moves']['Move_Mode'][1])+" is not a valid mode. Please try inserting one of the following:")
                            print(str(All_Move_modes ).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            Pokemon['Moves']['Move_Mode'][1] = input('What is '+ str(Name) + "'s move 2 Mode?"+'\n')  #pokemon move mode 2

                    #Ends session in case the user decided to do so
                    if Pokemon['Moves']['Move_Mode'][1] == 'exit' or Pokemon['Moves']['Move_Mode'][1] =='Exit': 
                        print('Session was ended. Progressed was not saved.')
                        return
                        #sys.exit('Session was ended. Progressed was not saved.')

        # ======= # Move 3
            
            #If the user decided to change pokemon move 3
            elif change == 'Move_3' or change == 'move_3' or change == 'Move3' or change == 'move3' or change == 'Move 3' or change == 'move 3':

                #Asks pokemon move 3 in case the user decided not to end session
                Pokemon['Moves']['Move_Name'][2] = input('What is '+ str(Name) + "'s Move 3? (Write exit to end session)"+'\n')  #pokemon move 3

                #Ends session in case the user decided to do so
                if Pokemon['Moves']['Move_Name'][2] == 'exit' or Pokemon['Moves']['Move_Name'][2] ==  'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')

                #Asks if the user would like to change pokemon move type 3
                change_move_type_3 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 3 type?"+'\n')

                #Makes sure the user chooses a valid option
                while change_move_type_3 != "Yes" and change_move_type_3 != "yes" and change_move_type_3 != "No" and change_move_type_3 != "no" and change_move_type_3 != "Exit" and change_move_type_3 != "exit":
                    print(str(change_move_type_3)+" is not a valid option. Please try again. (Write exit to end session)")
                    change_move_type_3 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 3 type?"+'\n')

                #Ends session in case the user decided to do so
                if change_move_type_3 == 'exit' or change_move_type_3 == 'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')

                #If the user decided to change pokemon move 3 type
                if change_move_type_3 == 'yes' or change_move_type_3 == 'Yes':

                    #Asks pokemon Move type 3
                    Pokemon['Moves']['Move_Type'][2] = input('What is '+ str(Name) + "'s Move 3 type?"+'\n')  #pokemon move type 3

                    #If a non-existing type was inserted or if a type was misspelled, it makes sure the user will have a chance to correct it
                    if Pokemon['Moves']['Move_Type'][2] not in All_types:

                        #Makes sure the user only selects one of the valid options
                        while Pokemon['Moves']['Move_Type'][2] != 'exit' and Pokemon['Moves']['Move_Type'][2] != 'Exit' and Pokemon['Moves']['Move_Type'][2] not in All_types:
                            print(str(Pokemon['Moves']['Move_Type'][2])+" is not a valid type. Please try inserting one of the following:")
                            print(str(All_types).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            Pokemon['Moves']['Move_Type'][2] = input('What is '+ str(Name) + "'s Move 3 type?"+'\n')  #pokemon move type 3

                    #Ends session in case the user decided to do so
                    if Pokemon['Moves']['Move_Type'][2] == 'exit' or Pokemon['Moves']['Move_Type'][2] =='Exit': 
                        print('Session was ended. Progressed was not saved.')
                        return
                        #sys.exit('Session was ended. Progressed was not saved.')

                #Asks if the user would like to change pokemon move mode 3
                change_move_mode_3 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 3 mode?"+'\n')

                #Makes sure the user chooses a valid option
                while change_move_mode_3 != "Yes" and change_move_mode_3 != "yes" and change_move_mode_3 != "No" and change_move_mode_3 != "no" and change_move_mode_3 != "Exit" and change_move_mode_3 != "exit":
                    print(str(change_move_mode_3)+" is not a valid option. Please try again. (Write exit to end session)")
                    change_move_mode_3 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 3 mode?"+'\n')

                #Ends session in case the user decided to do so
                if change_move_mode_3 == 'exit' or change_move_mode_3 == 'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')

                #If the user decided to change pokemon move 3 mode
                if change_move_mode_3 == 'yes' or change_move_mode_3 == 'Yes':

                    #Asks pokemon Move mode 3
                    Pokemon['Moves']['Move_Mode'][2] = input('What is '+ str(Name) + "'s move 3 Mode?"+'\n')  #pokemon move mode 3

                    #If a non-existing mode was inserted or if a mode was misspelled, it makes sure the user will have a chance to correct it
                    if Pokemon['Moves']['Move_Mode'][2] not in All_Move_modes:

                        #Makes sure the user only selects one of the valid options
                        while Pokemon['Moves']['Move_Mode'][2] != 'exit' and Pokemon['Moves']['Move_Mode'][2] != 'Exit' and Pokemon['Moves']['Move_Mode'][2] not in All_Move_modes:
                            print(str(Pokemon['Moves']['Move_Mode'][2])+" is not a valid mode. Please try inserting one of the following:")
                            print(str(All_Move_modes ).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            Pokemon['Moves']['Move_Mode'][2] = input('What is '+ str(Name) + "'s move 3 Mode?"+'\n')  #pokemon move mode 3

                    #Ends session in case the user decided to do so
                    if Pokemon['Moves']['Move_Mode'][2] == 'exit' or Pokemon['Moves']['Move_Mode'][2] =='Exit': 
                        print('Session was ended. Progressed was not saved.')
                        return
                        #sys.exit('Session was ended. Progressed was not saved.')

        # ======= # Move 4

            #If the user decided to change pokemon move 4
            elif change == 'Move_4' or change == 'move_4' or change == 'Move4' or change == 'move4' or change == 'Move 4' or change == 'move 4':

                #Asks pokemon move 4 in case the user decided not to end session
                Pokemon['Moves']['Move_Name'][3] = input('What is '+ str(Name) + "'s Move 4? (Write exit to end session)"+'\n')  #pokemon move 4

                #Ends session in case the user decided to do so
                if Pokemon['Moves']['Move_Name'][3] == 'exit' or Pokemon['Moves']['Move_Name'][3] ==  'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')

                #Asks if the user would like to change pokemon move type 4
                change_move_type_4 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 4 type?"+'\n')

                #Makes sure the user chooses a valid option
                while change_move_type_4 != "Yes" and change_move_type_4 != "yes" and change_move_type_4 != "No" and change_move_type_4 != "no" and change_move_type_4 != "Exit" and change_move_type_4 != "exit":
                    print(str(change_move_type_4)+" is not a valid option. Please try again. (Write exit to end session)")
                    change_move_type_4 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 4 type?"+'\n')

                #Ends session in case the user decided to do so
                if change_move_type_4 == 'exit' or change_move_type_4 == 'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')

                #If the user decided to change pokemon move 4 type
                if change_move_type_4 == 'yes' or change_move_type_4 == 'Yes':

                    #Asks pokemon Move type 4
                    Pokemon['Moves']['Move_Type'][3] = input('What is '+ str(Name) + "'s Move 4 type?"+'\n')  #pokemon move type 4

                    #If a non-existing type was inserted or if a type was misspelled, it makes sure the user will have a chance to correct it
                    if Pokemon['Moves']['Move_Type'][3] not in All_types:

                        #Makes sure the user only selects one of the valid options
                        while Pokemon['Moves']['Move_Type'][3] != 'exit' and Pokemon['Moves']['Move_Type'][3] != 'Exit' and Pokemon['Moves']['Move_Type'][3] not in All_types:
                            print(str(Pokemon['Moves']['Move_Type'][3])+" is not a valid type. Please try inserting one of the following:")
                            print(str(All_types).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            Pokemon['Moves']['Move_Type'][3] = input('What is '+ str(Name) + "'s Move 4 type?"+'\n')  #pokemon move type 4

                    #Ends session in case the user decided to do so
                    if Pokemon['Moves']['Move_Type'][3] == 'exit' or Pokemon['Moves']['Move_Type'][3] =='Exit': 
                        print('Session was ended. Progressed was not saved.')
                        return
                        #sys.exit('Session was ended. Progressed was not saved.')

                #Asks if the user would like to change pokemon move mode 4
                change_move_mode_4 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 4 mode?"+'\n')

                #Makes sure the user chooses a valid option
                while change_move_mode_4 != "Yes" and change_move_mode_4 != "yes" and change_move_mode_4 != "No" and change_move_mode_4 != "no" and change_move_mode_4 != "Exit" and change_move_mode_4 != "exit":
                    print(str(change_move_mode_4)+" is not a valid option. Please try again. (Write exit to end session)")
                    change_move_mode_4 = input("Would you like to change "+str(Pokemon['Name'][0])+"'s Move 4 mode?"+'\n')

                #Ends session in case the user decided to do so
                if change_move_mode_4 == 'exit' or change_move_mode_4 == 'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')

                #If the user decided to change pokemon move 4 mode
                if change_move_mode_4 == 'yes' or change_move_mode_4 == 'Yes':

                    #Asks pokemon Move mode 4
                    Pokemon['Moves']['Move_Mode'][3] = input('What is '+ str(Name) + "'s move 4 Mode?"+'\n')  #pokemon move mode 4

                    #If a non-existing mode was inserted or if a mode was misspelled, it makes sure the user will have a chance to correct it
                    if Pokemon['Moves']['Move_Mode'][3] not in All_Move_modes:

                        #Makes sure the user only selects one of the valid options
                        while Pokemon['Moves']['Move_Mode'][3] != 'exit' and Pokemon['Moves']['Move_Mode'][3] != 'Exit' and Pokemon['Moves']['Move_Mode'][3] not in All_Move_modes:
                            print(str(Pokemon['Moves']['Move_Mode'][3])+" is not a valid mode. Please try inserting one of the following:")
                            print(str(All_Move_modes ).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            Pokemon['Moves']['Move_Mode'][3] = input('What is '+ str(Name) + "'s move 4 Mode?"+'\n')  #pokemon move mode 4

                    #Ends session in case the user decided to do so
                    if Pokemon['Moves']['Move_Mode'][3] == 'exit' or Pokemon['Moves']['Move_Mode'][3] =='Exit': 
                        print('Session was ended. Progressed was not saved.')
                        return
                        #sys.exit('Session was ended. Progressed was not saved.')

            #If the user chooses an invalid option
            else:
                print(str(change)+" is not a valid option. Please choose one of the following options:")
                print("Type_1, Type_2, Item, Ability, Move_1, Move_2, Move_3 or Move_4")      
            
                        
        #Displays all the provided information to the user for a final check
        print('#============================================================#'+'\n')
        print('Name: '+str(Pokemon['Name'][0])+'\n')
        print('Type1: '+str(Pokemon['Types'][0])+'\n')
        print('Type2: '+str(Pokemon['Types'][1])+'\n')
        print('Ability: '+str(Pokemon['Ability'][0])+'\n')
        print('Item: '+str(Pokemon['Item'][0])+'\n')
        print('Move1: '+str(Pokemon['Moves']['Move_Name'][0])+' : '+str(Pokemon['Moves']['Move_Type'][0])+' : '+str(Pokemon['Moves']['Move_Mode'][0])+'\n')
        print('Move2: '+str(Pokemon['Moves']['Move_Name'][1])+' : '+str(Pokemon['Moves']['Move_Type'][1])+' : '+str(Pokemon['Moves']['Move_Mode'][1])+'\n')
        print('Move3: '+str(Pokemon['Moves']['Move_Name'][2])+' : '+str(Pokemon['Moves']['Move_Type'][2])+' : '+str(Pokemon['Moves']['Move_Mode'][2])+'\n')
        print('Move4: '+str(Pokemon['Moves']['Move_Name'][3])+' : '+str(Pokemon['Moves']['Move_Type'][3])+' : '+str(Pokemon['Moves']['Move_Mode'][3])+'\n')
        print('#============================================================# ')

        #Final check
        check = input('Is the information above correct? Write yes to save data or no to end program.'+'\n')

        #Makes sure the user selects a valid option
        while check != 'yes' and check != 'Yes' and check != 'no' and check != 'No' and check != 'exit' and check != 'Exit':
            print(str(check)+' is not a valid option. Please try again.')
            check = input('Is the information above correct? Write yes to save data or no to end program. (Write exit to end session)'+'\n')

        if check == 'yes' or check == 'Yes':
            edit_pokemon(data_path,Pokemon['Name'][0],Pokemon['Types'][0],Pokemon['Types'][1],Pokemon['Ability'][0],Pokemon['Item'][0],Pokemon['Moves']['Move_Name'][0],Pokemon['Moves']['Move_Type'][0],Pokemon['Moves']['Move_Mode'][0],Pokemon['Moves']['Move_Name'][1],Pokemon['Moves']['Move_Type'][1],Pokemon['Moves']['Move_Mode'][1],Pokemon['Moves']['Move_Name'][2],Pokemon['Moves']['Move_Type'][2],Pokemon['Moves']['Move_Mode'][2],Pokemon['Moves']['Move_Name'][3],Pokemon['Moves']['Move_Type'][3],Pokemon['Moves']['Move_Mode'][3])
            #print('Data was successfully edited for '+str(Name)+'!')

        if check == 'no' or check == 'No' or check == 'exit' or check == 'Exit':
            print('Session was ended. Progressed was not saved.')
            return
            #sys.exit('Session was ended. Progressed was not saved.')


# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#

#Defines Team Manager Module
#This module allows the user to manage their teams (e.g. build, edit, delete) of six pokemon from the provided database
#and calculate the type advanatage analysis and other statistics/information about the team

def manage_team(data_path):
    
    #imports useful libraries
    import os
    import datetime
    import numpy as np

    #Defines useful variables

    goal = ''   #keeps track of the user's goal (add, visualize, edit or delete)

    new_goal = ''  #new goal is used when the original goal cannot be executed for some reason (e.g. tried to add an entry that already exists)
        #new_goal is useful to redirect the user to another goal without having to restart the program

    pokemon_list = []  #Keeps track of all pokemon available for the current team
    
    team_list = []  #Keeps track of all teams in the database

    selected_pokemon = []  #Keeps track of pokemon that were already selected for the current team

    Team_name = ''  #Keeps track of team name

    current_pokemon = ''   #current pokemon name
    
    reselect = ''  #allows the user to reselect the 6 pokemon for the team
    
    change = ''  #helps the user change pokemon in the team when editing a team
    
    final_reselect = '' #allows the user to reselect the 6 pokemon for the team after all the statistics are calculated and displayed
    
    Database = {'All_Pokemon':{}}  #Python dictionary to load and organize the entire database allowing for nice display of all pokemon
    
    Team = {'Members':{'Pokemon_1':{},'Pokemon_2':{},'Pokemon_3':{},'Pokemon_4':{},'Pokemon_5':{},'Pokemon_6':{},}, 'Team_Name':[], 'Strengths':[], 'Weaknesses':[], 'Scores':[], 'Global_Score':[], 'Stats':{},'Date':[]}  
              #Python dictionary to organize the information of all pokemon in the team. 
              #The dictionary is built from the database entries with the aid of the function read_pokemon(data_path,Name)
    
    Pokemon = {}  #Dictionary that keeps information of current pokemon and helps with editing a team
    
    #Useful counters
    
    poke_counter = 0  #keeps track of how many pokemon were added to the list
    database_counter = 0  #keeps track of pokemon number being added to the Database Python dictionary
    team_counter = 0  #keeps track of pokemon number being added to the Team Python dictionary

    # ============================================ # Makes preparations to start program

    #Compiles list of files within the input directory
    files = next(os.walk(data_path))[2]
    #print(files)

    #Compiles a list of available pokemon within the database
    for f in files:
        if f.endswith('.poke'):
            pokemon_list.append(f.replace('.poke',''))
        elif f.endswith('.team'):
            team_list.append(f.replace('.team',''))
            
    #Loads database into Database Python dictionary, entry by entry
    for i in pokemon_list:
        #Moves handy database counter to the next iteration
        database_counter = database_counter + 1                
        #Reads current pokemon entry
        Pokemon = read_pokemon(data_path,i)
        #Adds current pokemon entry to the Databse Python dictionary under a newly created sub-dictionary
        Database['All_Pokemon']['Pokemon_'+str(database_counter)] = Pokemon            
            
    # ============================================ # Gives the user options        
            
    #Asks the user if they would like to add, edit or delete an entry
    goal = input("Would like to add, edit or delete a team entry?"+'\n'+"Write exit to end session."+'\n')

    #Ensures the user will only proceed in case they used one of the four valid options
    while goal != 'add' and goal != 'Add' and goal != 'edit' and goal != 'Edit' and goal != 'delete' and goal != 'Delete' and goal != 'exit' and goal != 'Exit':
        print(str(goal)+' is not a valid option. Please try again.')
        goal = input("Would like to add, edit or delete a team entry?"+'\n'+"Write exit to end session."+'\n')

    # ============================================ #
    # ============================================ # When the user decides to add a team

    #In case the user wants to add a team entry
    if goal == 'add' or goal == 'Add':

        #Asks the user the information for the team and passes it to the register_team function

        #Fisrt, it asks the team name
        Team_name = input('What is the team name?'+'\n')  #team name

        #Checks if a file with that team name was created before
        if os.path.exists(str(data_path)+'/'+str(Team_name)+".team"):
            print("This team entry already exists.")

            #Asks the user what to do then
            new_goal = input("Would you like to overwrite that entry instead? Or would you like to end session instead? (Write exit to end session)"+'\n'+"If overwriting entry, previous entry will be forever deleted."+'\n')

            #ensures the user will only proceed in case they used one of the two valid options
            while new_goal != 'overwrite' and new_goal != 'Overwrite' and new_goal != 'yes' and new_goal != 'Yes' and new_goal != 'exit' and new_goal != 'Exit':
                print(str(new_goal)+" is not a valid option. Please try again.")
                new_goal = input("Would you like to overwrite that entry instead? Or would to like to end session instead? (Write exit to end session)"+'\n'+"If overwriting entry, previous entry will be forever deleted."+'\n')

        #Ends session in case the user decided to do so
        if new_goal == 'exit' or new_goal =='Exit': 
            print('Session was ended. Progressed was not saved.')
            return
            #sys.exit('Session was ended. Progressed was not saved.')

        #If the user decided to either add a new entry or overwrite an old entry, the program proceeds normally under the 'add' option
        if new_goal == '' or new_goal == 'overwrite' or new_goal == 'Overwrite' or new_goal == 'yes' or new_goal == 'Yes':
            
            #Displays all available pokemon from the current database in an organized fashion
            print('\n'+"#=======#  Avalaible Pokemon in: "+str(data_path)+"  #=======#"+'\n')
            for pokemon in Database['All_Pokemon']:
                if Database['All_Pokemon'][pokemon]['Types'][1] == '':  #When the pokemon has only one type
                    print('Name: '+str(Database['All_Pokemon'][pokemon]['Name']).strip('][').replace("'","")+' ['+str(Database['All_Pokemon'][pokemon]['Types']).strip('][').replace("'","").replace(", ","")+']\n')
                else:  #When the pokemon has two types
                    print('Name: '+str(Database['All_Pokemon'][pokemon]['Name']).strip('][').replace("'","")+' ['+str(Database['All_Pokemon'][pokemon]['Types']).strip('][').replace("'","").replace(", ","] [")+']\n')
                print('Ability: '+str(Database['All_Pokemon'][pokemon]['Ability']).strip('][').replace("'",""))
                print('Item: '+str(Database['All_Pokemon'][pokemon]['Item']).strip('][').replace("'","")+'\n')
                print('Move1: '+str(Database['All_Pokemon'][pokemon]['Moves']['Move_Name'][0]).strip('][').replace("'","")+'\n       '+str(Database['All_Pokemon'][pokemon]['Moves']['Move_Mode'][0]).strip('][').replace("'","")+' ['+str(Database['All_Pokemon'][pokemon]['Moves']['Move_Type'][0]).strip('][').replace("'","")+']')
                print('Move2: '+str(Database['All_Pokemon'][pokemon]['Moves']['Move_Name'][1]).strip('][').replace("'","")+'\n       '+str(Database['All_Pokemon'][pokemon]['Moves']['Move_Mode'][1]).strip('][').replace("'","")+' ['+str(Database['All_Pokemon'][pokemon]['Moves']['Move_Type'][1]).strip('][').replace("'","")+']')
                print('Move3: '+str(Database['All_Pokemon'][pokemon]['Moves']['Move_Name'][2]).strip('][').replace("'","")+'\n       '+str(Database['All_Pokemon'][pokemon]['Moves']['Move_Mode'][2]).strip('][').replace("'","")+' ['+str(Database['All_Pokemon'][pokemon]['Moves']['Move_Type'][2]).strip('][').replace("'","")+']')
                print('Move4: '+str(Database['All_Pokemon'][pokemon]['Moves']['Move_Name'][3]).strip('][').replace("'","")+'\n       '+str(Database['All_Pokemon'][pokemon]['Moves']['Move_Mode'][3]).strip('][').replace("'","")+' ['+str(Database['All_Pokemon'][pokemon]['Moves']['Move_Type'][3]).strip('][').replace("'","")+']\n')
                print("#============================================================#"+'\n')

    # ================================================================================= # Selecting 6 pokemon for the team
    
            #This line establishes a final check in case the user is not happy with the team after the team statistics are calculated and displayed
            while final_reselect != 'yes' and final_reselect != 'Yes':               

                #Sets up the loop to add 6 pokemon to the team, allowing the user to reselect if they wish to before they're done
                while reselect != 'yes' and reselect != 'Yes':
                    poke_counter = poke_counter + 1

                    #Asks the user the name of the pokemon to be added to team
                    current_pokemon = input('What is pokemon #'+str(poke_counter)+' name?'+'\n')  #pokemon name

                    #If a pokemon not available in the databse was inserted or if the name was misspelled, it makes sure the user will have a chance to correct it
                    if current_pokemon not in pokemon_list:

                        #Makes sure the user only selects one of the valid options
                        while current_pokemon != 'exit' and current_pokemon != 'Exit' and current_pokemon not in pokemon_list:
                            print(str(current_pokemon)+" is not a valid option. Please try inserting one of the following:")
                            print(str(pokemon_list).strip('][').replace("'",""))
                            print('Or write exit to end session.')
                            current_pokemon = input('What is pokemon #'+str(poke_counter)+' name?'+'\n')  #pokemon name

                    #Ends session in case the user decided to do so
                    if current_pokemon == 'exit' or current_pokemon =='Exit': 
                        print('Session was ended. Progress was not saved.')
                        return
                        #sys.exit('Session was ended. Progressed was not saved.')

                    #Adds selected pokemon to the selected pokemon list and removes it from the pokemon_list:
                    selected_pokemon.append(current_pokemon)
                    print('Selected Pokemon: ' + str(selected_pokemon).strip('][').replace("'",""))                
                    pokemon_list.remove(current_pokemon)
                    print('Available Pokemon: ' + str(pokemon_list).strip('][').replace("'",""))

                    #Resets current pokemon name variable
                    current_pokemon = ''

                    #When 6 pokemon were selected
                    if poke_counter == 6:
                        #Checks if the user is satisfied with the selection or if they want to reselect all 6 pokemon
                        print('All 6 pokemon were selected:')
                        print(str(selected_pokemon).strip('][').replace("'",""))
                        reselect = input('Is this selection correct? If not, write no to reselect the 6 pokemon.'+'\n')

                        #makes sure the user selects one of the valid options
                        while reselect != 'yes' and reselect != 'Yes' and reselect != 'no' and reselect != 'No' and reselect != 'exit' and reselect != 'Exit':
                            print(str(reselect)+' is not a valid option. Please try again.')
                            print('Or write exit to end session.')
                            reselect = input('Is the selection correct? If not, write no to reselect the 6 pokemon.'+'\n')

                            #If the user decided to reselect the 6 pokemon
                            if reselect == 'no' or reselect == 'No':
                                #Resets pokemon counter
                                poke_counter = 0
                                #Resets lists
                                pokemon_list = pokemon_list + selected_pokemon
                                selected_pokemon = []                           
                                print('Please reselect team members.'+'\n')

                            #Ends session in case the user decided to do so
                            if reselect == 'exit' or reselect =='Exit': 
                                print('Session was ended. Progress was not saved.')
                                return
                                #sys.exit('Session was ended. Progressed was not saved.')
                
                #Feeds Team_name and the selected_pokemon list into a function to assemble a python dictionary for the team
                #This function also calculates various infomation and statistics for the team
                Team = assemble_team(data_path,Team_name,selected_pokemon)
              
    # ================================================================================= # Displays all team info and gives the suer a final chance to reselect
                
                #Displays the summary of the team:                 
                print('\n'+"#==========================# "+str(Team['Team_Name'])+":  #=======#"+'\n')
                
                #Attacks Stats
                print('Phsycal Attackers: ' + str(Team['Stats']['Physical_Moves']).strip('][').replace("'",""))
                print('Special Attackers: ' + str(Team['Stats']['Special_Moves']).strip('][').replace("'",""))
                print('Status Attackers:  ' + str(Team['Stats']['Status_Moves']).strip('][').replace("'","")+'\n')
                
                #Repeated Items        
                if len(Team['Stats']['Repeated_Items']) > 0:  #If Repeated_Item sub entry had at least 1 item, it shows the Repeated_Items
                    print('Repeated items in the team: ' + str(Team['Stats']['Repeated_Items']).strip('][').replace("'","")+'\n')
                #If no repeated items
                else:
                    print('No repeated items in the team.'+'\n')
                
                print("#============================================================#"+'\n')
                #Displays information of the team pokemon
                for pokemon in Team['Members']:
                    if Team['Members'][pokemon]['Types'][1] == '':  #When the pokemon has only one type
                        print('Name: '+str(Team['Members'][pokemon]['Name']).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Types']).strip('][').replace("'","").replace(", ","")+']\n')
                    else:  #When the pokemon has two types
                        print('Name: '+str(Team['Members'][pokemon]['Name']).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Types']).strip('][').replace("'","").replace(", ","] [")+']\n')
                    print('Ability: '+str(Team['Members'][pokemon]['Ability']).strip('][').replace("'",""))
                    print('Item: '+str(Team['Members'][pokemon]['Item']).strip('][').replace("'","")+'\n')
                    print('Move1: '+str(Team['Members'][pokemon]['Moves']['Move_Name'][0]).strip('][').replace("'","")+'\n       '+str(Team['Members'][pokemon]['Moves']['Move_Mode'][0]).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Moves']['Move_Type'][0]).strip('][').replace("'","")+']')
                    print('Move2: '+str(Team['Members'][pokemon]['Moves']['Move_Name'][1]).strip('][').replace("'","")+'\n       '+str(Team['Members'][pokemon]['Moves']['Move_Mode'][1]).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Moves']['Move_Type'][1]).strip('][').replace("'","")+']')
                    print('Move3: '+str(Team['Members'][pokemon]['Moves']['Move_Name'][2]).strip('][').replace("'","")+'\n       '+str(Team['Members'][pokemon]['Moves']['Move_Mode'][2]).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Moves']['Move_Type'][2]).strip('][').replace("'","")+']')
                    print('Move4: '+str(Team['Members'][pokemon]['Moves']['Move_Name'][3]).strip('][').replace("'","")+'\n       '+str(Team['Members'][pokemon]['Moves']['Move_Mode'][3]).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Moves']['Move_Type'][3]).strip('][').replace("'","")+']\n')
                    print("#============================================================#"+'\n')           
                   
                
                #Checks one last time if the user is satisfied with the selection or if they want to reselect all 6 pokemon
                #print('All 6 pokemon were selected:')
                #print(str(selected_pokemon).strip('][').replace("'",""))
                final_reselect = input('Do you want to save this data? If not, write no to reselect the 6 pokemon or exit to quit.'+'\n')

                #makes sure the user selects one of the valid options
                while final_reselect != 'yes' and final_reselect != 'Yes' and final_reselect != 'no' and final_reselect != 'No' and final_reselect != 'exit' and final_reselect != 'Exit':
                    print(str(final_reselect)+' is not a valid option. Please try again.')
                    print('Or write exit to end session.')
                    final_reselect = input('Is the selection correct? If not, write no to reselect the 6 pokemon.'+'\n')

                #If the user decided to reselect the 6 pokemon
                if final_reselect == 'no' or final_reselect == 'No':
                    #Resets pokemon counter Things to reset
                    #Resets reselect, poke_counter,team_counter and Team Dictionary:
                    reselect = ''
                    poke_counter = 0
                    team_counter = 0
                    Team.clear()
                    Team = {'Members':{'Pokemon_1':{},'Pokemon_2':{},'Pokemon_3':{},'Pokemon_4':{},'Pokemon_5':{},'Pokemon_6':{},}, 'Team_Name':[], 'Strengths':[], 'Weaknesses':[], 'Scores':[], 'Global_Score':[], 'Stats':{},'Date':[]}  
                    #Resets lists
                    pokemon_list = pokemon_list + selected_pokemon
                    selected_pokemon = []                           
                    print('Please reselect team members.'+'\n')
                    print('Available Pokemon: ' + str(pokemon_list).strip('][').replace("'",""))

                #Ends session in case the user decided to do so
                if final_reselect == 'exit' or final_reselect =='Exit': 
                    print('Session was ended. Progress was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')
                
    # ================================================================================= #  Wraps up and creates the new team entry         
          
        #Saves the team data into a .team file
        register_team(data_path,Team)
        
        return Team        
        
    # ============================================ #
    # ============================================ # When the user decides to delete a team 

    #In case the user wants to delete a team entry
    if goal == 'delete' or goal == 'Delete':
        
        #Shows the user the available teams
        print('Available Teams: ' + str(team_list).strip('][').replace("'",""))

        #Asks the user the information for the team and passes it to the delete_team function

        #Fisrt, it asks the team name
        Name = input('What is the team name?'+'\n')  #team name

        #Checks if the file for that team was created before and gives the user the chance to try another file
        while os.path.exists(str(data_path)+'/'+str(Name)+".team") == False and Name != 'exit' and Name != 'Exit':
            print("This team entry does not exist in the specified database folder. Please try again. (Write exit to end session)")
            Name = input('What is the team name?'+'\n')  #team name

        #Ends session in case the user decided to do so
        if Name == 'exit' or Name =='Exit': 
            print('Session was ended. Team entry was not deleted.')
            return
            #sys.exit('Session was ended. Team entry was not deleted.')

        #Asks the user if they really want to delete the entry
        new_goal = input("Are you sure you want to permanently delete this team entry? Or would to like to end session instead? (Write exit to end session)"+'\n')

        #ensures the user will only proceed in case they used one of the valid options
        while new_goal != 'yes' and new_goal != 'Yes' and new_goal != 'exit' and new_goal != 'Exit' and new_goal != 'no' and new_goal != 'No':
            print(str(new_goal)+" is not a valid option. Please try again.")
            new_goal = input("Are you sure you want to permanently delete this team entry? Or would to like to end session instead? (Write exit to end session)"+'\n')

        #Ends session in case the user decided to do so
        if new_goal == 'exit' or new_goal =='Exit' or new_goal == 'no' or new_goal =='No': 
            print('Session was ended. Team entry was not deleted.')
            return
            #sys.exit('Session was ended. Team entry was not deleted.')

        #Proceeds if the user decide to delete the entry, the information is passed to the delete_team function
        if new_goal == 'Yes' or new_goal == 'yes':
            delete_team(data_path,Name)
            
    # ============================================ #
    # ============================================ # When the user decides to edit a team     
    
    #In case the user wants to edit a team entry
    if goal == 'edit' or goal == 'Edit':
        
        #Shows the user all team entries in the database
        print('Available Teams: ' + str(team_list).strip('][').replace("'",""))
        
        #Asks the name of the Team
        Name = input('What is the Team name?'+'\n')  #team name

        #Checks if the file for that team was created before and gives the user the chance to try another file
        while os.path.exists(str(data_path)+'/'+str(Name)+".team") == False and Name != 'exit' and Name != 'Exit':
            print("This team entry does not exist in the specified database folder. Please try again. (Write exit to end session)")
            Name = input('What is the Team name?'+'\n')  #team name

        #Ends session in case the user decided to do so
        if Name == 'exit' or Name =='Exit': 
            print('Session was ended. Progressed was not saved.')
            return
            #sys.exit('Session was ended. Progressed was not saved.')
            
        # ================================================================================= # Reads provide team's info and prepares helpfuls lists
        
        #Reads team information from the file
        Team = read_team(data_path,Name)
        
        #Compiles a list of team members: selected_pokemon
        for member in Team['Members']:
            selected_pokemon.append(Team['Members'][member]['Name'][0])
            
        #Removes selected pokemon from the available pokemon list: pokemon_list
        for pokemon in selected_pokemon:
            #print(pokemon)
            #print(pokemon_list)
            pokemon_list.remove(pokemon)
  
        # ================================================================================= #  Displays provided Team's info  
        
        #Displays the summary of the team:                 
        print('\n'+"#==========================# "+str(Team['Team_Name']).strip('][').replace("'","")+":  #=======#"+'\n')

        #Attacks Stats
        print('Phsycal Attackers: ' + str(Team['Stats']['Physical_Moves']).strip('][').replace("'",""))
        print('Special Attackers: ' + str(Team['Stats']['Special_Moves']).strip('][').replace("'",""))
        print('Status Attackers:  ' + str(Team['Stats']['Status_Moves']).strip('][').replace("'","")+'\n')

        #Repeated Items        
        if len(Team['Stats']['Repeated_Items']) > 0:  #If Repeated_Item sub entry had at least 1 item, it shows the Repeated_Items
            print('Repeated items in the team: ' + str(Team['Stats']['Repeated_Items']).strip('][').replace("'","")+'\n')
        #If no repeated items
        else:
            print('No repeated items in the team.'+'\n')

        #Displays information of the team pokemon
        for pokemon in Team['Members']:
            print("#==========================# "+str(pokemon)+":  #=======#"+'\n')
            if Team['Members'][pokemon]['Types'][1] == '':  #When the pokemon has only one type
                print('Name: '+str(Team['Members'][pokemon]['Name']).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Types']).strip('][').replace("'","").replace(", ","")+']\n')
            else:  #When the pokemon has two types
                print('Name: '+str(Team['Members'][pokemon]['Name']).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Types']).strip('][').replace("'","").replace(", ","] [")+']\n')
            print('Ability: '+str(Team['Members'][pokemon]['Ability']).strip('][').replace("'",""))
            print('Item: '+str(Team['Members'][pokemon]['Item']).strip('][').replace("'","")+'\n')
            print('Move1: '+str(Team['Members'][pokemon]['Moves']['Move_Name'][0]).strip('][').replace("'","")+'\n       '+str(Team['Members'][pokemon]['Moves']['Move_Mode'][0]).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Moves']['Move_Type'][0]).strip('][').replace("'","")+']')
            print('Move2: '+str(Team['Members'][pokemon]['Moves']['Move_Name'][1]).strip('][').replace("'","")+'\n       '+str(Team['Members'][pokemon]['Moves']['Move_Mode'][1]).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Moves']['Move_Type'][1]).strip('][').replace("'","")+']')
            print('Move3: '+str(Team['Members'][pokemon]['Moves']['Move_Name'][2]).strip('][').replace("'","")+'\n       '+str(Team['Members'][pokemon]['Moves']['Move_Mode'][2]).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Moves']['Move_Type'][2]).strip('][').replace("'","")+']')
            print('Move4: '+str(Team['Members'][pokemon]['Moves']['Move_Name'][3]).strip('][').replace("'","")+'\n       '+str(Team['Members'][pokemon]['Moves']['Move_Mode'][3]).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Moves']['Move_Type'][3]).strip('][').replace("'","")+']\n')
        print("#============================================================#"+'\n')    
        
        # ================================================================================= #   Gives the user options
                
        #Asks the user what pokemon they would like to replace
        while change != 'Done' and change != 'done':
            change = input("What pokemon would you like to replace? Write Done when finished or Exit to quit.")  #replaced pokemon
            
            #When a viable pokemon is selected
            if change in selected_pokemon:
                
                #Creates/resets helpful variable confirm_change
                confirm_change = ''
                
                #Resets current pokemon name variable
                current_pokemon = ''
                
                #Resets current Pokemon dictionary
                Pokemon.clear()
                
                #Shows available pokemon (database - selected pokemon)
                print('Available Pokemon: ' + str(pokemon_list).strip('][').replace("'",""))
                
                #Asks what pokemon will replace it 
                current_pokemon = input('What pokemon will replace '+ str(change) + "? (Write exit to end session)"+'\n')  #replacing pokemon

                #If an invalid option was inserted, it makes sure the user will have a chance to correct it
                if current_pokemon != 'exit' and current_pokemon != 'Exit' and current_pokemon not in pokemon_list:
                    #Makes sure the user only selects one of the valid options
                    while current_pokemon != 'exit' and current_pokemon != 'Exit' and current_pokemon not in pokemon_list:
                        print(str(current_pokemon)+" is not a valid type. Please try inserting one of the following:")
                        print(str(pokemon_list).strip('][').replace("'",""))
                        print('Or write exit to end session.')
                        current_pokemon = input('What pokemon will replace '+ str(change) + "? (Write exit to end session)"+'\n')  #replacing pokemon                 
                
                #Ends session in case the user decided to do so
                if current_pokemon == 'exit' or current_pokemon == 'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')
                    
                #Reads selected replacing pokemon entry
                Pokemon = read_pokemon(data_path,current_pokemon)
                
                #Displays current pokemon info for the user
                print('\n'+"#============================================================#"+'\n')
                if Pokemon['Types'][1] == '':  #When the pokemon has only one type
                    print('Name: '+str(Pokemon['Name']).strip('][').replace("'","")+' ['+str(Pokemon['Types']).strip('][').replace("'","").replace(", ","")+']\n')
                else:  #When the pokemon has two types
                    print('Name: '+str(Pokemon['Name']).strip('][').replace("'","")+' ['+str(Pokemon['Types']).strip('][').replace("'","").replace(", ","] [")+']\n')
                print('Ability: '+str(Pokemon['Ability']).strip('][').replace("'",""))
                print('Item: '+str(Pokemon['Item']).strip('][').replace("'","")+'\n')
                print('Move1: '+str(Pokemon['Moves']['Move_Name'][0]).strip('][').replace("'","")+'\n       '+str(Pokemon['Moves']['Move_Mode'][0]).strip('][').replace("'","")+' ['+str(Pokemon['Moves']['Move_Type'][0]).strip('][').replace("'","")+']')
                print('Move2: '+str(Pokemon['Moves']['Move_Name'][1]).strip('][').replace("'","")+'\n       '+str(Pokemon['Moves']['Move_Mode'][1]).strip('][').replace("'","")+' ['+str(Pokemon['Moves']['Move_Type'][1]).strip('][').replace("'","")+']')
                print('Move3: '+str(Pokemon['Moves']['Move_Name'][2]).strip('][').replace("'","")+'\n       '+str(Pokemon['Moves']['Move_Mode'][2]).strip('][').replace("'","")+' ['+str(Pokemon['Moves']['Move_Type'][2]).strip('][').replace("'","")+']')
                print('Move4: '+str(Pokemon['Moves']['Move_Name'][3]).strip('][').replace("'","")+'\n       '+str(Pokemon['Moves']['Move_Mode'][3]).strip('][').replace("'","")+' ['+str(Pokemon['Moves']['Move_Type'][3]).strip('][').replace("'","")+']\n')
                print("#============================================================#"+'\n')
                
                #Asks the user if they want to confirm the replacement
                confirm_change = input('Do you really want to replace ' + str(change) + ' with ' + str(current_pokemon) + '?')
                
                #If an invalid option was inserted, it makes sure the user will have a chance to correct it
                if confirm_change != 'exit' and confirm_change != 'Exit' and confirm_change != 'yes' and confirm_change != 'Yes' and confirm_change != 'no' and confirm_change != 'No':
                    #Makes sure the user only selects one of the valid options
                    while confirm_change != 'exit' and confirm_change != 'Exit' and confirm_change != 'yes' and confirm_change != 'Yes' and confirm_change != 'no' and confirm_change != 'No':
                        print(str(confirm_change)+" is not a valid option. Please choose yes, no or write exit to end session.")
                        confirm_change = input('Do you really want to replace ' + str(change) + ' with ' + str(current_pokemon) + '?')                 
                
                #Ends session in case the user decided to do so
                if confirm_change == 'exit' or confirm_change == 'Exit': 
                    print('Session was ended. Progressed was not saved.')
                    return
                    #sys.exit('Session was ended. Progressed was not saved.')
                    
                #If the user decided to confirm replacement
                if confirm_change == 'yes' or confirm_change == 'Yes':
                    #Removes replaced pokemon (change) from the selected_pokemon list:
                    selected_pokemon.remove(change)
                    #Adds replacing pokemon (current_pokemon) to the selected_pokemon list:
                    selected_pokemon.append(current_pokemon)
                    #Adds replaced pokemon (change) to the available pokemon list (pokemon_list):
                    pokemon_list.append(change)
                    #Removes replacing pokemon (current_pokemon) from the available pokemon list (pokemon_list):
                    pokemon_list.remove(current_pokemon)           
            
            #If the user chooses an invalid option
            else:
                print(str(change)+" is not a valid option. Please choose one of the following options:")
                print("Team's Pokemon: " + str(selected_pokemon).strip('][').replace("'",""))   
                
                
        # ================================================================================= #   Assembles the edited team and asks if the user wans to save changes
        
        #When the user is done replacing pokemon, the program assembles the new team
        
        #Resets the old Team and Pokemon dictionaries and resets the handy team_counter (just in case)
        Team.clear()
        Team = {'Members':{'Pokemon_1':{},'Pokemon_2':{},'Pokemon_3':{},'Pokemon_4':{},'Pokemon_5':{},'Pokemon_6':{},}, 'Team_Name':[], 'Strengths':[], 'Weaknesses':[], 'Scores':[], 'Global_Score':[], 'Stats':{},'Date':[]}  
        Pokemon.clear()
        team_counter = 0
              
        #Feeds Team_name and the selected_pokemon list into a function to assemble a python dictionary for the edited team
        #This function also calculates various infomation and statistics for the edited team
        Team = assemble_team(data_path,Name,selected_pokemon)
        
        #Displays the summary of the edited team:                 
        print('\n'+"#==========================# "+str(Team['Team_Name']).strip('][').replace("'","")+":  #=======#"+'\n')

        #Attacks Stats
        print('Phsycal Attackers: ' + str(Team['Stats']['Physical_Moves']).strip('][').replace("'",""))
        print('Special Attackers: ' + str(Team['Stats']['Special_Moves']).strip('][').replace("'",""))
        print('Status Attackers:  ' + str(Team['Stats']['Status_Moves']).strip('][').replace("'","")+'\n')

        #Repeated Items        
        if len(Team['Stats']['Repeated_Items']) > 0:  #If Repeated_Item sub entry had at least 1 item, it shows the Repeated_Items
            print('Repeated items in the team: ' + str(Team['Stats']['Repeated_Items']).strip('][').replace("'","")+'\n')
        #If no repeated items
        else:
            print('No repeated items in the team.'+'\n')
            
        #Displays information of the team pokemon
        for pokemon in Team['Members']:
            print("#==========================# "+str(pokemon)+":  #=======#"+'\n')
            if Team['Members'][pokemon]['Types'][1] == '':  #When the pokemon has only one type
                print('Name: '+str(Team['Members'][pokemon]['Name']).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Types']).strip('][').replace("'","").replace(", ","")+']\n')
            else:  #When the pokemon has two types
                print('Name: '+str(Team['Members'][pokemon]['Name']).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Types']).strip('][').replace("'","").replace(", ","] [")+']\n')
            print('Ability: '+str(Team['Members'][pokemon]['Ability']).strip('][').replace("'",""))
            print('Item: '+str(Team['Members'][pokemon]['Item']).strip('][').replace("'","")+'\n')
            print('Move1: '+str(Team['Members'][pokemon]['Moves']['Move_Name'][0]).strip('][').replace("'","")+'\n       '+str(Team['Members'][pokemon]['Moves']['Move_Mode'][0]).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Moves']['Move_Type'][0]).strip('][').replace("'","")+']')
            print('Move2: '+str(Team['Members'][pokemon]['Moves']['Move_Name'][1]).strip('][').replace("'","")+'\n       '+str(Team['Members'][pokemon]['Moves']['Move_Mode'][1]).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Moves']['Move_Type'][1]).strip('][').replace("'","")+']')
            print('Move3: '+str(Team['Members'][pokemon]['Moves']['Move_Name'][2]).strip('][').replace("'","")+'\n       '+str(Team['Members'][pokemon]['Moves']['Move_Mode'][2]).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Moves']['Move_Type'][2]).strip('][').replace("'","")+']')
            print('Move4: '+str(Team['Members'][pokemon]['Moves']['Move_Name'][3]).strip('][').replace("'","")+'\n       '+str(Team['Members'][pokemon]['Moves']['Move_Mode'][3]).strip('][').replace("'","")+' ['+str(Team['Members'][pokemon]['Moves']['Move_Type'][3]).strip('][').replace("'","")+']\n')
        print("#============================================================#"+'\n')    
        
        
        #If the user likes the edited team, the data will be saved. Otherwise, the program will end without saving progress
        check = input('Would you like to save the changes to the Team? Write yes to save data or no to end program.'+'\n')

        #Makes sure the user selects a valid option
        while check != 'yes' and check != 'Yes' and check != 'no' and check != 'No' and check != 'exit' and check != 'Exit':
            print(str(check)+' is not a valid option. Please try again.')
            check = input('Would you like to save the changes to the Team? Write yes to save data or no to end program. (Write exit to end session)'+'\n')

        #If the user decided to save changes
        if check == 'yes' or check == 'Yes':
            edit_team(data_path,Team)

        #If the user decided NOT to save changes
        if check == 'no' or check == 'No' or check == 'exit' or check == 'Exit':
            print('Session was ended. Progressed was not saved.')
            return
            #sys.exit('Session was ended. Progressed was not saved.')
            

# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#
        

#Defines essential type_match function to find the outcome of two types, an offensive/attack type (o_type) vs.a defensive type (d_type)
#Returns results as 1 (normal damage), 2 (super effective / double damage), 0.5 (not effective / half damage), 0 (doesn't affect / no damage)

def type_match(o_type,d_type):
    
    #imports required libraries
    import sys
    
    #defines the result variable to be the output of the function
    result = ''

    # ================================================= # 1

    if o_type == 'Normal': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 1

        if d_type == 'Flying':
            result = 1

        if d_type == 'Poison':
            result = 1

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 0.5

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 0

        if d_type == 'Steel':
            result = 0.5

        if d_type == 'Fire':
            result = 1

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 1

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 1

        if d_type == 'Dark':
            result = 1

        if d_type == 'Fairy':
            result = 1

    # ================================================= # 2

    elif o_type == 'Fighting': 

        if d_type == 'Normal':
            result = 2

        if d_type == 'Fighting':
            result = 1

        if d_type == 'Flying':
            result = 0.5

        if d_type == 'Poison':
            result = 0.5

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 2

        if d_type == 'Bug':
            result = 0.5

        if d_type == 'Ghost':
            result = 0

        if d_type == 'Steel':
            result = 2

        if d_type == 'Fire':
            result = 1

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 1

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 0.5

        if d_type == 'Ice':
            result = 2

        if d_type == 'Dragon':
            result = 1

        if d_type == 'Dark':
            result = 2

        if d_type == 'Fairy':
            result = 0.5

    # ================================================= # 3

    elif o_type == 'Flying': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 2

        if d_type == 'Flying':
            result = 1

        if d_type == 'Poison':
            result = 1

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 0.5

        if d_type == 'Bug':
            result = 2

        if d_type == 'Ghost':
            result = 1

        if d_type == 'Steel':
            result = 0.5

        if d_type == 'Fire':
            result = 1

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 2

        if d_type == 'Electric':
            result = 0.5

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 1

        if d_type == 'Dark':
            result = 1

        if d_type == 'Fairy':
            result = 1

    # ================================================= # 4

    elif o_type == 'Poison': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 1

        if d_type == 'Flying':
            result = 1

        if d_type == 'Poison':
            result = 0.5

        if d_type == 'Ground':
            result = 0.5

        if d_type == 'Rock':
            result = 0.5

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 0.5

        if d_type == 'Steel':
            result = 0

        if d_type == 'Fire':
            result = 1

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 2

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 1

        if d_type == 'Dark':
            result = 1

        if d_type == 'Fairy':
            result = 2

    # ================================================= # 5

    elif o_type == 'Ground': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 1

        if d_type == 'Flying':
            result = 0

        if d_type == 'Poison':
            result = 2

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 2

        if d_type == 'Bug':
            result = 0

        if d_type == 'Ghost':
            result = 1

        if d_type == 'Steel':
            result = 2

        if d_type == 'Fire':
            result = 2

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 0.5

        if d_type == 'Electric':
            result = 2

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 1

        if d_type == 'Dark':
            result = 1

        if d_type == 'Fairy':
            result = 1

    # ================================================= # 6

    elif o_type == 'Rock': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 0.5

        if d_type == 'Flying':
            result = 2

        if d_type == 'Poison':
            result = 1

        if d_type == 'Ground':
            result = 0.5

        if d_type == 'Rock':
            result = 1

        if d_type == 'Bug':
            result = 2

        if d_type == 'Ghost':
            result = 1

        if d_type == 'Steel':
            result = 0.5

        if d_type == 'Fire':
            result = 2

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 1

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 2

        if d_type == 'Dragon':
            result = 1

        if d_type == 'Dark':
            result = 1

        if d_type == 'Fairy':
            result = 1

    # ================================================= # 7

    elif o_type == 'Bug': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 0.5

        if d_type == 'Flying':
            result = 0.5

        if d_type == 'Poison':
            result = 0.5

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 1

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 0.5

        if d_type == 'Steel':
            result = 0.5

        if d_type == 'Fire':
            result = 0.5

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 2

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 2

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 1

        if d_type == 'Dark':
            result = 2

        if d_type == 'Fairy':
            result = 0.5

    # ================================================= # 8

    elif o_type == 'Ghost': 

        if d_type == 'Normal':
            result = 0

        if d_type == 'Fighting':
            result = 1

        if d_type == 'Flying':
            result = 1

        if d_type == 'Poison':
            result = 1

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 1

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 2

        if d_type == 'Steel':
            result = 1

        if d_type == 'Fire':
            result = 1

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 1

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 2

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 1

        if d_type == 'Dark':
            result = 0.5

        if d_type == 'Fairy':
            result = 1

    # ================================================= # 9

    elif o_type == 'Steel': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 1

        if d_type == 'Flying':
            result = 1

        if d_type == 'Poison':
            result = 1

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 2

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 1

        if d_type == 'Steel':
            result = 0.5

        if d_type == 'Fire':
            result = 0.5

        if d_type == 'Water':
            result = 0.5

        if d_type == 'Grass':
            result = 1

        if d_type == 'Electric':
            result = 0.5

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 2

        if d_type == 'Dragon':
            result = 1

        if d_type == 'Dark':
            result = 1

        if d_type == 'Fairy':
            result = 2

    # ================================================= # 10

    elif o_type == 'Fire': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 1

        if d_type == 'Flying':
            result = 1

        if d_type == 'Poison':
            result = 1

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 0.5

        if d_type == 'Bug':
            result = 2

        if d_type == 'Ghost':
            result = 1

        if d_type == 'Steel':
            result = 2

        if d_type == 'Fire':
            result = 0.5

        if d_type == 'Water':
            result = 0.5

        if d_type == 'Grass':
            result = 2

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 2

        if d_type == 'Dragon':
            result = 0.5

        if d_type == 'Dark':
            result = 1

        if d_type == 'Fairy':
            result = 1

    # ================================================= # 11

    elif o_type == 'Water': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 1

        if d_type == 'Flying':
            result = 1

        if d_type == 'Poison':
            result = 1

        if d_type == 'Ground':
            result = 2

        if d_type == 'Rock':
            result = 2

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 1

        if d_type == 'Steel':
            result = 1

        if d_type == 'Fire':
            result = 2

        if d_type == 'Water':
            result = 0.5

        if d_type == 'Grass':
            result = 0.5

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 0.5

        if d_type == 'Dark':
            result = 1

        if d_type == 'Fairy':
            result = 1

    # ================================================= # 12

    elif o_type == 'Grass': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 1

        if d_type == 'Flying':
            result = 0.5

        if d_type == 'Poison':
            result = 0.5

        if d_type == 'Ground':
            result = 2

        if d_type == 'Rock':
            result = 2

        if d_type == 'Bug':
            result = 0.5

        if d_type == 'Ghost':
            result = 1

        if d_type == 'Steel':
            result = 0.5

        if d_type == 'Fire':
            result = 0.5

        if d_type == 'Water':
            result = 2

        if d_type == 'Grass':
            result = 0.5

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 0.5

        if d_type == 'Dark':
            result = 1

        if d_type == 'Fairy':
            result = 1

    # ================================================= # 13

    elif o_type == 'Electric': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 1

        if d_type == 'Flying':
            result = 2

        if d_type == 'Poison':
            result = 1

        if d_type == 'Ground':
            result = 0

        if d_type == 'Rock':
            result = 1

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 1

        if d_type == 'Steel':
            result = 1

        if d_type == 'Fire':
            result = 1

        if d_type == 'Water':
            result = 2

        if d_type == 'Grass':
            result = 0.5

        if d_type == 'Electric':
            result = 0.5

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 0.5

        if d_type == 'Dark':
            result = 1

        if d_type == 'Fairy':
            result = 1

    # ================================================= # 14

    elif o_type == 'Psychic': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 2

        if d_type == 'Flying':
            result = 1

        if d_type == 'Poison':
            result = 2

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 1

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 1

        if d_type == 'Steel':
            result = 0.5

        if d_type == 'Fire':
            result = 1

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 1

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 0.5

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 1

        if d_type == 'Dark':
            result = 0

        if d_type == 'Fairy':
            result = 1
            
    # ================================================= # 15

    elif o_type == 'Ice': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 1

        if d_type == 'Flying':
            result = 2

        if d_type == 'Poison':
            result = 1

        if d_type == 'Ground':
            result = 2

        if d_type == 'Rock':
            result = 1

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 1

        if d_type == 'Steel':
            result = 0.5

        if d_type == 'Fire':
            result = 0.5

        if d_type == 'Water':
            result = 0.5

        if d_type == 'Grass':
            result = 2

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 0.5

        if d_type == 'Dragon':
            result = 2

        if d_type == 'Dark':
            result = 1

        if d_type == 'Fairy':
            result = 1

    # ================================================= # 16

    elif o_type == 'Dragon': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 1

        if d_type == 'Flying':
            result = 1

        if d_type == 'Poison':
            result = 1

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 1

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 1

        if d_type == 'Steel':
            result = 0.5

        if d_type == 'Fire':
            result = 1

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 1

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 2

        if d_type == 'Dark':
            result = 1

        if d_type == 'Fairy':
            result = 0

    # ================================================= # 17

    elif o_type == 'Dark': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 0.5

        if d_type == 'Flying':
            result = 1

        if d_type == 'Poison':
            result = 1

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 1

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 2

        if d_type == 'Steel':
            result = 1

        if d_type == 'Fire':
            result = 1

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 1

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 2

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 1

        if d_type == 'Dark':
            result = 0.5

        if d_type == 'Fairy':
            result = 0.5

    # ================================================= # 18

    elif o_type == 'Fairy': 

        if d_type == 'Normal':
            result = 1

        if d_type == 'Fighting':
            result = 2

        if d_type == 'Flying':
            result = 1

        if d_type == 'Poison':
            result = 0.5

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 1

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 1

        if d_type == 'Steel':
            result = 0.5

        if d_type == 'Fire':
            result = 0.5

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 1

        if d_type == 'Electric':
            result = 1

        if d_type == 'Psychic':
            result = 1

        if d_type == 'Ice':
            result = 1

        if d_type == 'Dragon':
            result = 2

        if d_type == 'Dark':
            result = 2

        if d_type == 'Fairy':
            result = 1
            
    # ================================================= # 19 Flying Press move exception (Fighting and Flying type move)

    elif o_type == 'Flying Press': 

        if d_type == 'Normal':
            result = 2

        if d_type == 'Fighting':
            result = 2

        if d_type == 'Flying':
            result = 0.5

        if d_type == 'Poison':
            result = 0.5

        if d_type == 'Ground':
            result = 1

        if d_type == 'Rock':
            result = 1

        if d_type == 'Bug':
            result = 1

        if d_type == 'Ghost':
            result = 0

        if d_type == 'Steel':
            result = 1

        if d_type == 'Fire':
            result = 1

        if d_type == 'Water':
            result = 1

        if d_type == 'Grass':
            result = 2

        if d_type == 'Electric':
            result = 0.5

        if d_type == 'Psychic':
            result = 0.5

        if d_type == 'Ice':
            result = 2

        if d_type == 'Dragon':
            result = 1

        if d_type == 'Dark':
            result = 2

        if d_type == 'Fairy':
            result = 0.5
            
    # ================================================= #
    
    else:  #in case o_type is misspeled
        sys.exit('Error!! Move type: ' + o_type + ' is likely misspelled.' +'\n' + 'Please correct it and try again.')
        
    if result == '':  #in case d_type is misspeled
        sys.exit('Error!! Pokemon type: ' + d_type + ' is likely misspelled.' +'\n' + 'Please correct it and try again.')      
        
    if result != '':  #in case there was no error and the result was indeed calculated
        return result

    
# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#


#Defines function to handle exceptions to type advanatges created by ablities

def ability_type_advantages_modifier(All_types,offense,defense,ability,Move_mode_1,Move_mode_2,Move_mode_3,Move_mode_4):
    
    if ability == 'Motor Drive':
        defense[All_types.index('Electric')] = 0
        
    if ability == 'Sap Sipper':
        defense[All_types.index('Grass')] = 0
        
    if ability == 'Flash Fire':
        defense[All_types.index('Fire')] = 0
        
    if ability == 'Storm Drain':
        defense[All_types.index('Water')] = 0
        
    if ability == 'Water Absorb':
        defense[All_types.index('Water')] = 0
        
    if ability == 'Dry Skin':
        defense[All_types.index('Water')] = 0
        defense[All_types.index('Fire')] = defense[All_types.index('Fire')] * 1.25
        
    if ability == 'Lightning Rod':
        defense[All_types.index('Electric')] = 0
        
    if ability == 'Volt Absorb':
        defense[All_types.index('Electric')] = 0
        
    if ability == 'Levitate':
        defense[All_types.index('Ground')] = 0
        
    if ability == 'Wonder Guard':
        #Loops through all types
        for this_type in All_types:
            #Checks if not super effective (damage < 2)
            if defense[All_types.index(this_type)] < 2:
                #if not, pokemon takes no damage from that type
                defense[All_types.index(this_type)] = 0
        
    if ability == 'Thick Fat':
        defense[All_types.index('Fire')] = defense[All_types.index('Fire')] * 0.5
        defense[All_types.index('Ice')] = defense[All_types.index('Ice')] * 0.5
        
    if ability == 'Fluffy':
        defense[All_types.index('Fire')] = defense[All_types.index('Fire')] * 2
        
    if ability == 'Heatproof':
        defense[All_types.index('Fire')] = defense[All_types.index('Fire')] * 0.5
    
    if ability == 'Tinted Lens':
        #Loops through all types
        for this_type in All_types:
            #Checks if not very effective (damage = 0.5)
            if offense[All_types.index(this_type)] == 0.5:
                #if so, doubles the inflicted damage
                offense[All_types.index(this_type)] = offense[All_types.index(this_type)] * 2
        
    
    #if ability is Scrappy and the pokemon knows at least one non-Status move 
    if ability == 'Scrappy' and (Move_mode_1 != 'Status' or Move_mode_2 != 'Status' or Move_mode_3 != 'Status' or Move_mode_4 != 'Status'):
        #if pokemon is unable to hit ghost types
        if offense[All_types.index('Ghost')] == 0:
            #Now it causes regular damage to ghost types
            offense[All_types.index('Ghost')] = 1
        
        
    return (offense,defense)


# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#


#Defines function to handle exceptions to type advanatges created by moves

def move_type_advantages_modifier(All_types,offense,defense,Move_mode_1,Move_mode_2,Move_mode_3,Move_mode_4,Move_type_1,Move_type_2,Move_type_3,Move_type_4,Move_name_1,Move_name_2,Move_name_3,Move_name_4):
    
    #if the pokemon knows Freeze-Dry, this ice type move is also good against water
    if Move_name_1 == 'Freeze-Dry' or Move_name_2 == 'Freeze-Dry' or Move_name_3 == 'Freeze-Dry' or Move_name_4 == 'Freeze-Dry':
        #Checks if not super effective (damage < 2) to water
        if offense[All_types.index('Water')] < 2:
            offense[All_types.index('Water')] = 2
            
    #if the pokemon knows Flying Press, this move is both flying and fighting type
    if Move_name_1 == 'Flying Press' or Move_name_2 == 'Flying Press' or Move_name_3 == 'Flying Press' or Move_name_4 == 'Flying Press':
        #Erases offense list
        offense = []            
            
        #Calculates Offensive type advantages again:
        #For each type available as the Defensive type
        for types in All_types:

            #Resets helpful variable for the next iteration
            final_outcome = 0

            #Against Move_1 (if not a Status move nor Flying Press)
            if Move_mode_1 != 'Status' and Move_name_1 !='Flying Press':
                final_outcome = type_match(Move_type_1,types)
            #if Flying Press
            if Move_name_1 =='Flying Press':
                final_outcome = type_match(Move_name_1,types)

            #Against Move_2 (if not a Status move nor Flying Press)
            if Move_mode_2 != 'Status' and Move_name_2 !='Flying Press':
                current_outcome = type_match(Move_type_2,types)
                #If this outcome is better, it replaces the previous one (the user should use the best move available)
                if current_outcome > final_outcome:
                    final_outcome = current_outcome
            #if Flying Press
            if Move_name_2 =='Flying Press':
                current_outcome = type_match(Move_name_2,types)
                #If this outcome is better, it replaces the previous one (the user should use the best move available)
                if current_outcome > final_outcome:
                    final_outcome = current_outcome            

            #Against Move_3 (if not a Status move nor Flying Press)
            if Move_mode_3 != 'Status' and Move_name_3 !='Flying Press':
                current_outcome = type_match(Move_type_3,types)
                #If this outcome is better, it replaces the previous one (the user should use the best move available)
                if current_outcome > final_outcome:
                    final_outcome = current_outcome
            #if Flying Press
            if Move_name_3 =='Flying Press':
                current_outcome = type_match(Move_name_3,types)
                #If this outcome is better, it replaces the previous one (the user should use the best move available)
                if current_outcome > final_outcome:
                    final_outcome = current_outcome 

            #Against Move_4 (if not a Status move nor Flying Press)
            if Move_mode_4 != 'Status' and Move_name_4 !='Flying Press':
                current_outcome = type_match(Move_type_4,types)
                #If this outcome is better, it replaces the previous one (the user should use the best move available)
                if current_outcome > final_outcome:
                    final_outcome = current_outcome
            #if Flying Press
            if Move_name_4 =='Flying Press':
                current_outcome = type_match(Move_name_4,types)
                #If this outcome is better, it replaces the previous one (the user should use the best move available)
                if current_outcome > final_outcome:
                    final_outcome = current_outcome 

            #Adds current outcome to the offense list:
            offense.append(final_outcome)
            
    return (offense,defense)
        


# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#


#Defines function to color background of TextCtrl box according to type (to be used in the GUI version of the program)

def background_type(text_box, TYPE):
    
    if TYPE == '':
        #Changes background color
        text_box.SetBackgroundColour((255,255,255))
        #Changes text color to white
        text_box.SetForegroundColour((0,0,0))
    
    if TYPE == 'Normal':
        #Changes background color
        text_box.SetBackgroundColour((168,168,120))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Fighting':
        text_box.SetBackgroundColour((192,48,40))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Flying':
        text_box.SetBackgroundColour((168,144,240))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Poison':
        text_box.SetBackgroundColour((160,64,160))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Ground':
        text_box.SetBackgroundColour((224,192,104))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Rock':
        text_box.SetBackgroundColour((184,160,56))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Bug':
        text_box.SetBackgroundColour((168,184,32))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Ghost':
        text_box.SetBackgroundColour((112,88,152))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Steel':
        text_box.SetBackgroundColour((184,184,208))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Fire':
        text_box.SetBackgroundColour((240,128,48))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Water':
        text_box.SetBackgroundColour((104,144,240))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Grass':
        text_box.SetBackgroundColour((120,200,80))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Electric':
        text_box.SetBackgroundColour((248,208,48))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Psychic':
        text_box.SetBackgroundColour((248,88,136))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Ice':
        text_box.SetBackgroundColour((152,216,216))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Dragon':
        text_box.SetBackgroundColour((112,56,248))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Dark':
        text_box.SetBackgroundColour((112,88,72))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))

    if TYPE == 'Fairy':
        text_box.SetBackgroundColour((222,165,222))
        #Changes text color to white
        text_box.SetForegroundColour((255,255,255))
        

# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#

#Defines function to sort Pokemon ListCtrl box according to specified argument (to be used in the GUI version of the program)

def pokemon_list_ctrl_dictionary_sorting(Database,sorting_parameter):    
    
    #Creates a list of all pokemon names to ensure there are no duplicates when sorting
    name_list =[]
    #Filling up list
    for pokemon in Database:
        name_list.append(Database[pokemon]['Name'][0])

    #Creating an empty list where the values will be sorted
    sorting_list = []
    #Creating sorted dictionary
    sorted_dictionary = {}
    #Creates sorting counter
    sorting_counter = 1

    if sorting_parameter == 'Name':
        #Filling up list
        for pokemon in Database:
            sorting_list.append(Database[pokemon]['Name'][0])
        #Sorting list    
        sorting_list.sort()
        #Looping through item list to reassemble dictionary
        for item in sorting_list:
            #Looping through pokemon sub-dictionaries until the matching item is found
            for pokemon in Database:
                #When there is a match and the pokemon was not added yet
                if Database[pokemon]['Name'][0] == item and Database[pokemon]['Name'][0] in name_list:
                    #Adds pokemon sub-dictionary to new sorted dictionary
                    sorted_dictionary['Pokemon_'+str(sorting_counter)] = Database[pokemon]
                    #Removes pokemon from name list to avoid duplicates
                    name_list.remove(Database[pokemon]['Name'][0])
                    #Moves counter to next iteration
                    sorting_counter = sorting_counter + 1
                    #print('hey')

    if sorting_parameter == 'Type 1':
        #Filling up list
        for pokemon in Database:
            sorting_list.append(Database[pokemon]['Types'][0])
        #Sorting list    
        sorting_list.sort()
        #Looping through item list to reassemble dictionary
        for item in sorting_list:
            #Looping through pokemon sub-dictionaries until the matching item is found
            for pokemon in Database:
                #When there is a match and the pokemon was not added yet
                if Database[pokemon]['Types'][0] == item and Database[pokemon]['Name'][0] in name_list:
                    #Adds pokemon sub-dictionary to new sorted dictionary
                    sorted_dictionary['Pokemon_'+str(sorting_counter)] = Database[pokemon]
                    #Removes pokemon from name list to avoid duplicates
                    name_list.remove(Database[pokemon]['Name'][0])
                    #Moves counter to next iteration
                    sorting_counter = sorting_counter + 1
                    #print('hey')

    if sorting_parameter == 'Type 2':
        #Filling up list
        for pokemon in Database:
            sorting_list.append(Database[pokemon]['Types'][1])
        #Sorting list    
        sorting_list.sort()
        #Looping through item list to reassemble dictionary
        for item in sorting_list:
            #Looping through pokemon sub-dictionaries until the matching item is found
            for pokemon in Database:
                #When there is a match and the pokemon was not added yet
                if Database[pokemon]['Types'][1] == item and Database[pokemon]['Name'][0] in name_list:
                    #Adds pokemon sub-dictionary to new sorted dictionary
                    sorted_dictionary['Pokemon_'+str(sorting_counter)] = Database[pokemon]
                    #Removes pokemon from name list to avoid duplicates
                    name_list.remove(Database[pokemon]['Name'][0])
                    #Moves counter to next iteration
                    sorting_counter = sorting_counter + 1
                    #print('hey')

    if sorting_parameter == 'Ability':
        #Filling up list
        for pokemon in Database:
            sorting_list.append(Database[pokemon]['Ability']['Ability_Name'][0])
        #Sorting list    
        sorting_list.sort()
        #Looping through item list to reassemble dictionary
        for item in sorting_list:
            #Looping through pokemon sub-dictionaries until the matching item is found
            for pokemon in Database:
                #When there is a match and the pokemon was not added yet
                if Database[pokemon]['Ability']['Ability_Name'][0] == item and Database[pokemon]['Name'][0] in name_list:
                    #Adds pokemon sub-dictionary to new sorted dictionary
                    sorted_dictionary['Pokemon_'+str(sorting_counter)] = Database[pokemon]
                    #Removes pokemon from name list to avoid duplicates
                    name_list.remove(Database[pokemon]['Name'][0])
                    #Moves counter to next iteration
                    sorting_counter = sorting_counter + 1
                    #print('hey')

    if sorting_parameter == 'Item':
        #Filling up list
        for pokemon in Database:
            sorting_list.append(Database[pokemon]['Item'][0])
        #Sorting list    
        sorting_list.sort()
        #Looping through item list to reassemble dictionary
        for item in sorting_list:
            #Looping through pokemon sub-dictionaries until the matching item is found
            for pokemon in Database:
                #When there is a match and the pokemon was not added yet
                if Database[pokemon]['Item'][0] == item and Database[pokemon]['Name'][0] in name_list:
                    #Adds pokemon sub-dictionary to new sorted dictionary
                    sorted_dictionary['Pokemon_'+str(sorting_counter)] = Database[pokemon]
                    #Removes pokemon from name list to avoid duplicates
                    name_list.remove(Database[pokemon]['Name'][0])
                    #Moves counter to next iteration
                    sorting_counter = sorting_counter + 1
                    #print('hey')

    if sorting_parameter == 'Move 1':
        #Filling up list
        for pokemon in Database:
            sorting_list.append(Database[pokemon]['Moves']['Move_Name'][0])
        #Sorting list    
        sorting_list.sort()
        #Looping through item list to reassemble dictionary
        for item in sorting_list:
            #Looping through pokemon sub-dictionaries until the matching item is found
            for pokemon in Database:
                #When there is a match and the pokemon was not added yet
                if Database[pokemon]['Moves']['Move_Name'][0] == item and Database[pokemon]['Name'][0] in name_list:
                    #Adds pokemon sub-dictionary to new sorted dictionary
                    sorted_dictionary['Pokemon_'+str(sorting_counter)] = Database[pokemon]
                    #Removes pokemon from name list to avoid duplicates
                    name_list.remove(Database[pokemon]['Name'][0])
                    #Moves counter to next iteration
                    sorting_counter = sorting_counter + 1
                    #print('hey')

    if sorting_parameter == 'Move 2':
        #Filling up list
        for pokemon in Database:
            sorting_list.append(Database[pokemon]['Moves']['Move_Name'][1])
        #Sorting list    
        sorting_list.sort()
        #Looping through item list to reassemble dictionary
        for item in sorting_list:
            #Looping through pokemon sub-dictionaries until the matching item is found
            for pokemon in Database:
                #When there is a match and the pokemon was not added yet
                if Database[pokemon]['Moves']['Move_Name'][1] == item and Database[pokemon]['Name'][0] in name_list:
                    #Adds pokemon sub-dictionary to new sorted dictionary
                    sorted_dictionary['Pokemon_'+str(sorting_counter)] = Database[pokemon]
                    #Removes pokemon from name list to avoid duplicates
                    name_list.remove(Database[pokemon]['Name'][0])
                    #Moves counter to next iteration
                    sorting_counter = sorting_counter + 1
                    #print('hey')

    if sorting_parameter == 'Move 3':
        #Filling up list
        for pokemon in Database:
            sorting_list.append(Database[pokemon]['Moves']['Move_Name'][2])
        #Sorting list    
        sorting_list.sort()
        #Looping through item list to reassemble dictionary
        for item in sorting_list:
            #Looping through pokemon sub-dictionaries until the matching item is found
            for pokemon in Database:
                #When there is a match and the pokemon was not added yet
                if Database[pokemon]['Moves']['Move_Name'][2] == item and Database[pokemon]['Name'][0] in name_list:
                    #Adds pokemon sub-dictionary to new sorted dictionary
                    sorted_dictionary['Pokemon_'+str(sorting_counter)] = Database[pokemon]
                    #Removes pokemon from name list to avoid duplicates
                    name_list.remove(Database[pokemon]['Name'][0])
                    #Moves counter to next iteration
                    sorting_counter = sorting_counter + 1
                    #print('hey')

    if sorting_parameter == 'Move 4':
        #Filling up list
        for pokemon in Database:
            sorting_list.append(Database[pokemon]['Moves']['Move_Name'][3])
        #Sorting list    
        sorting_list.sort()
        #Looping through item list to reassemble dictionary
        for item in sorting_list:
            #Looping through pokemon sub-dictionaries until the matching item is found
            for pokemon in Database:
                #When there is a match and the pokemon was not added yet
                if Database[pokemon]['Moves']['Move_Name'][3] == item and Database[pokemon]['Name'][0] in name_list:
                    #Adds pokemon sub-dictionary to new sorted dictionary
                    sorted_dictionary['Pokemon_'+str(sorting_counter)] = Database[pokemon]
                    #Removes pokemon from name list to avoid duplicates
                    name_list.remove(Database[pokemon]['Name'][0])
                    #Moves counter to next iteration
                    sorting_counter = sorting_counter + 1
                    #print('hey')

    return sorted_dictionary

#Defines function to sort Team ListCtrl box according to specified argument (to be used in the GUI version of the program)

#def team_list_ctrl_dictionary_sorting(Database,sorting_parameter): 

    #return sorted_dictionary

# ======================================================================================================================#
# ======================================================================================================================#
# ======================================================================================================================#

#Defines function to parse Pokemon entry file from downloaded Serebii txt and organize pokemon info into a neat dictionary
#The input is the path to the downlaoded Serebii txt file and the output is a dictionary organizing the pokemon info

def load_dex_entry(dex_entry_path):
    
    #Prepares a first loop through the file to identify if the pokemon has Alternate Forms

    #Creates a temporary list to store the form names
    forms = []

    # Reads the data
    g = open(dex_entry_path)

    #Starts the loop through the file. Line by line.
    for line in g:
        #Finds the pokemon Form lines (only exists in case pokemon has Alternate Forms)
        if line.startswith('			<tr><td class="pkmn"><b>'):

            #Splits line per form using reference string
            all_forms = line.split('loading="lazy" alt="')
            #Finds the total number of forms
            forms_number = len(all_forms) - 1

            #Creates helpful counter to loop through different forms
            i = 1

            #Starts the loop to extract all form names and add to temporary list forms
            while i <= forms_number:
                this_form = all_forms[i].split('"')[0]
                #Adds form name to list
                forms.append(this_form)
                #print(this_form)
                #Moves to next iteration    
                i = i + 1
                
        #Finds the pokemon Form lines for Articuno, Moltres and Zapdos (they don't have the usual form line for their multiple forms)
        if ('Articuno' in dex_entry_path or 'Moltres' in dex_entry_path or 'Zapdos' in dex_entry_path) and line.startswith('<div class="navheader">Picture</div><br'):
            #Adds Standard and Galarian Forms to temporary list forms
            forms.append('Standard Form')
            forms.append('Galarian Form')
            #print(forms)

    #If there aren't Alternate Forms
    if forms == []:
        forms.append('Only Form')

    #print(forms)

    g.close()


    #This is important for the program to know when to stop
    c = open(dex_entry_path)
    lines1 = c.readlines()
    total_lines = len(lines1)
    c.close()

    #creates dictionary to store pokemon information
    dex_pokemon = {'Species':[], 'Dex':[], 'Forms':{}}

    #Sets helpful level_up_moves_final_check variable to 0
    #This makes sure the analysis of whether ALL FORMS have assigned Level Up Moves is only conducted once
    level_up_moves_final_check = 0 

    #Starts second loop to collect all necessary information and store into dictionary

    # Reads the data
    f = open(dex_entry_path)

    #Starts helpful loop counter
    loop_counter = 1

    #Starts the loop through the file. Line by line.
    while loop_counter <= total_lines:
        line = f.readline()
        loop_counter = loop_counter + 1    

        #Finds the pokemon Species and National Dex Number line
        if line.startswith('<title>'):
            this_Species = line.split('>')[1].split(' - #')[0]
            this_Dex = line.split('>')[1].split(' - #')[1].split(' -')[0]
            #print(this_Species)
            #print(this_Dex)

            #Handling Exceptions (not taking care of names containing space or : here)
            #Dealing with the nidoran problem
            if 'Nidoran' in this_Species:       
                #For female nidoran
                if '29' in this_Dex:
                    this_Species = 'Nidoran F'
                #For male nidoran
                if '32' in this_Dex:
                    this_Species = 'Nidoran M'

            #Dealing with the pikachu alternate forms problem
            if 'Pikachu' in this_Species:
                #Only considers a single form (ignores the different cap forms)
                forms = []
                forms.append('Only Form')
                #print(forms)
                
            #Dealing with the Meowstic Male and Female form differences problem
            if 'Meowstic' in this_Species:
            #dex_pokemon['Species'][0] == 'Meowstic'
                forms = []
                forms.append('Male')
                forms.append('Female')
                #print(forms)
                
            #Dealing with the Indeedee Male and Female form differences problem
            if 'Indeedee' in this_Species:
            #dex_pokemon['Species'][0] == 'Indeedee'
                forms = []
                forms.append('Male')
                forms.append('Female')
                #print(forms)


            #Adds Species Name to the dicitonary
            dex_pokemon['Species'].append(this_Species)
            #print(dex_pokemon['Species'][0])
            #Adds National Dex Number to the dicitonary
            dex_pokemon['Dex'].append(this_Dex)
            #print(dex_pokemon['Dex'][0])


            #Takes care of the different forms
            #Defines/resets helpful counter for forms and 
            forms_counter = 1
            move_counter = {}

            #Sets up the forms into the dictionary
            for current_form in forms:
                #Creates dictionary entries for current form
                dex_pokemon['Forms']['Form'+str(forms_counter)] = {'Name':[], 'Types':[], 'Ability':{}, 'Moves':[]}
                #Adds form name to dictionary
                dex_pokemon['Forms']['Form'+str(forms_counter)]['Name'] = current_form
                #Crestes sub-entries for Ability
                dex_pokemon['Forms']['Form'+str(forms_counter)]['Ability'] = {'Name':[], 'Info':[]}
                #Crestes sub-entries for Moves
                dex_pokemon['Forms']['Form'+str(forms_counter)]['Moves'] = {}

                #Creates move_counter dictionary entry for curent form:
                move_counter['Form'+str(forms_counter)] = 1

                #Moves counter to next iteration
                forms_counter = forms_counter + 1        


        #Finds the pokemon Types lines
        #For single form pokemon or pokemon that all forms share the same types
        #Finding line (this line only exists in files that fit these conditions)
        if line.startswith('			<td class="cen"><a href="') and dex_pokemon['Forms']['Form1']['Types'] == []:
            #Splits line for the first time to identify how many types the pokemon has
            all_types = line.split('/type/')
            #When there is only one type
            if len(all_types) == 2:
                #for type 1
                type_1 = all_types[1].split('.gif"')[0].capitalize()
                #for type 2
                type_2 = ''              
            #When there are two types
            if len(all_types) > 2:
                #for type 1
                type_1 = all_types[1].split('.gif"')[0].capitalize()
                #for type 2
                type_2 = all_types[2].split('.gif"')[0].capitalize()

            #Adding type to dictionary inside each form sub-dictionary
            #Defines/resets helpful counter for forms
            forms_counter = 1

            #Loops through the different form sub-dictionaries
            for current_form in forms:
                #Adds Type 1 to current form
                dex_pokemon['Forms']['Form'+str(forms_counter)]['Types'].append(type_1)
                #Adds Type 2 to current form
                dex_pokemon['Forms']['Form'+str(forms_counter)]['Types'].append(type_2)
                #Moves counter to next iteration
                forms_counter = forms_counter + 1  


        #For multiple form pokemon
        #Finding line (this line only exists in files that fit these conditions)
        if line.startswith('			<td class="cen"><table') and dex_pokemon['Forms']['Form1']['Types'] == []:

            #The order of the form names from before doesn't always agree with the order of form names for the types
            #so we need a temporary form_types dictionary to help us organize the information before passing to final dicitonary
            temp_forms_types = {}

            #print(forms)        

            #In the lines below, we're searaching for the TYPES for EACH FORM and the FORM NAME

            #Sometimes the types inforamtion of multiple forms is scattered throughout multiple lines,
            #so we need to use the strategy below to search through multiple lines, combine them into 1 big line
            #and later split the big line into a line for each form

            #Creates/resets helpful variables big_line, line_count, line_end
            big_line = ""
            line_count = 0
            line_end = 5

            #Looks for first form's name or '"50%">Normal', which they normally use to refer to first form
            if current_form in line or '"50%">Normal' in line:
                #print('here!!!!!')
                #print("line 0 (searchable line):")
                #print(line)
                #Adds line to big_line:
                big_line = big_line + line
                #Moves to next iteration
                line_count = line_count + 1

                #Gets the following x lines (specified by the helpful variable line_end) and combines them into 1 big line
                #(sometimes the inforamtion of multiple forms is scattered throughout multiple lines)
                while line_count <= line_end:
                    #Moves to next line
                    line = f.readline()
                    #print("line "+str(line_count)+":")
                    #print(line)
                    #Adds line to big_line:
                    big_line = big_line + line
                    #Moves to next iteration
                    line_count = line_count + 1

                #print(big_line)

                #Splits big_line using </td><td to extract information for FORM NAME
                line_form_name = big_line.split('</td><td')
                #Deletes last element since it has no FORM NAME information
                del line_form_name[-1]
                #Creates/resets helpful counter for form names
                counter_form_names = 1            
                #Goes through each part to extract form name
                for part in line_form_name:
                    #Creates entry on temporary form_types dictionary for current form
                    temp_forms_types['Form'+str(counter_form_names)] = {'Name':[],'Types':[]}
                    #Splits again using ="50%"> and adds the form name from the last part to the temporary dictionary
                    temp_forms_types['Form'+str(counter_form_names)]['Name'].append(part.split('="50%">')[-1])
                    #Moves counter tok next iteration
                    counter_form_names = counter_form_names + 1


                #Splits big_line according to the number of forms using </td><td , which appears after every form name
                #The TYPES normally follow the form name, so part 0 doesn't have any types information

                #Creates/resets helpful counter form_number
                form_number = 0

                while form_number < len(forms):                

                    #Splits big_line using </td><td to extract information for current form's TYPES
                    #which is in part i+1, since part 0 doesn't have any types information
                    line = big_line.split('</td><td')[form_number+1]
                    #print(line)

                    #Here we further split big_line_split to look for the types information:
                    #Splits line for the first time to identify how many types the pokemon has
                    all_types = line.split('/type/')
                    #When there is only one type
                    if len(all_types) == 2:
                        #for type 1
                        type_1 = all_types[1].split('.gif"')[0].capitalize()
                        #for type 2
                        type_2 = ''              
                    #When there are two types
                    if len(all_types) > 2:
                        #for type 1
                        type_1 = all_types[1].split('.gif"')[0].capitalize()
                        #for type 2
                        type_2 = all_types[2].split('.gif"')[0].capitalize()

                    #Adds current form's types to temporary dictionary
                    temp_forms_types['Form'+str(form_number+1)]['Types'].append(type_1)
                    temp_forms_types['Form'+str(form_number+1)]['Types'].append(type_2)

                    #print(forms[form_number])
                    #print(type_1)
                    #print(type_2)                    

                    #Moves to next iteration
                    form_number = form_number + 1

                    #print(big_line_split)                
                #print(temp_forms_types)


            #Approach 1: When FORM NAMES are written the same, but the order is different
            #Compares temporary dictionary to actual dictionary to finally add FORM TYPES
            #Starts to loop through temporary dictionary
            for item in temp_forms_types:
                #print(' ')
                #print(temp_forms_types[item]['Name'][0])
                #Starts to loop through actual dictionary  dex_pokemon['Forms'] to check for a form name match
                for item_final in dex_pokemon['Forms']:
                    #print(dex_pokemon['Forms'][item_final]['Name'])
                    #Looking for the TYPE NAME match
                    if temp_forms_types[item]['Name'][0] == dex_pokemon['Forms'][item_final]['Name']:
                        #Adds types to actual dictionary dex_pokemon['Forms']
                        dex_pokemon['Forms'][item_final]['Types'].append(temp_forms_types[item]['Types'][0])
                        dex_pokemon['Forms'][item_final]['Types'].append(temp_forms_types[item]['Types'][1])


            #Approach 2: When FORM NAMES are NOT written the same, we have to assume the order is the same
            #Compares actual dictionary to temporary dictionary to finally add FORM TYPES
            #Starts to loop through actual dictionary dex_pokemon['Forms']
            for item_final in dex_pokemon['Forms']:
                #Checks if TYPES is empty so we need to switch to Approach 2 (equal order)
                if dex_pokemon['Forms'][item_final]['Types'] == []:
                    #Adds types to actual dictionary dex_pokemon['Forms']
                    dex_pokemon['Forms'][item_final]['Types'].append(temp_forms_types[item_final]['Types'][0])
                    dex_pokemon['Forms'][item_final]['Types'].append(temp_forms_types[item_final]['Types'][1])



        #Starts looking for abilities for both SINGLE FORM and MULTIPLE FORM pokemon    

        #For SINGLE FORM Pokemon:
        if len(dex_pokemon['Forms']) == 1:
            #For Regular Abilities
            if line.startswith('<a href="/abilitydex/'):
                this_Ability = line.split('><b>')[1].split('</b>')[0]
                this_Ability_Info = line.split('></a>: ')[1].split(' <')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                #Adds Ability Name and Info to the dicitonary
                dex_pokemon['Forms']['Form1']['Ability']['Name'].append(this_Ability)
                dex_pokemon['Forms']['Form1']['Ability']['Info'].append(this_Ability_Info)
                #print(dex_pokemon['Forms']['Form1']['Ability'])
            #For Hidden Abilities
            if line.startswith('<b>Hidden Ability</b><!-- <i>(Available)'):        
                #Checks if this is a Hidden Ability
                this_Ability = line.split('><b>')[1].split('</b>')[0] + ' (Hidden Ability)'
                this_Ability_Info = line.split('></a>: ')[1].split(' <')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                #Adds Ability Name and Info to the dicitonary
                dex_pokemon['Forms']['Form1']['Ability']['Name'].append(this_Ability)
                dex_pokemon['Forms']['Form1']['Ability']['Info'].append(this_Ability_Info)
                #print(dex_pokemon['Forms']['Form1']['Ability'])


        #For MULTIPLE FORM Pokemon:
        #Creates/resets helpful form counter
        counter_forms_abilities = 1

        if len(dex_pokemon['Forms']) > 1:
            #Finding first ability line:
            if line.startswith('<a href="/abilitydex/'):
                
                #For most pokemon
                if '></a>: ' in line:
                    #Finds first ability for first form
                    this_Ability = line.split('><b>')[1].split('</b>')[0]                    
                    this_Ability_Info = line.split('></a>: ')[1].split(' <')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'").replace('&#8220;','"').replace('&#8221','"')  #fixes bug with the text
                    #Adds Ability Name and Info to first form
                    dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Name'].append(this_Ability)
                    dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Info'].append(this_Ability_Info)
                #print(dex_pokemon['Forms']['Form1']['Ability'])
                #For few exceptions, namely basculin
                if '</i>: ' in line:
                    #Splits the line according to number of abilities in line
                    split_ability_line = line.split('><b>')
                    #Removes fraction without abilities
                    split_ability_line.pop(0)
                    #Starts a loop for each ability
                    for splits in split_ability_line:
                        #Finds first ability
                        this_Ability = splits.split('</b>')[0] 
                        #Finds form name
                        this_ability_form = splits.split('<i>(')[1].split(')</i>')[0].replace(' Form','').replace(' ','-')
                        #Finds ability info                               
                        this_Ability_Info = splits.split('</i>: ')[1].split(' <')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                        #Adds Ability Name and Info to matching form
                        for forms in dex_pokemon['Forms']:
                            #If there is a match
                            if this_ability_form in dex_pokemon['Forms'][forms]['Name']:
                                #print(this_ability_form)
                                #Adds Ability Name and Info to first form
                                dex_pokemon['Forms'][forms]['Ability']['Name'].append(this_Ability)
                                dex_pokemon['Forms'][forms]['Ability']['Info'].append(this_Ability_Info)

                #Starts a sub-loop to go through ability lines
                while line.startswith('		</tr>') == False:
                    #Moves to next line
                    line = f.readline()
                    #print(line)

                    #Checks if next line is a regular ability line
                    if line.startswith('<a href="/abilitydex/'):
                        #For most pokemon
                        if '></a>: ' in line:                        
                            #Finds ability for current form
                            this_Ability = line.split('><b>')[1].split('</b>')[0]
                            this_Ability_Info = line.split('></a>: ')[1].split(' <')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                            #Adds Ability Name and Info to current form
                            dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Name'].append(this_Ability)
                            dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Info'].append(this_Ability_Info)
                        #For few exceptions, namely basculin
                        if '</i>: ' in line:
                            #Finds ability
                            this_Ability = line.split('><b>')[1].split('</b>')[0] 
                            #Finds form name
                            this_ability_form = line.split('<i>(')[1].split(')</i>')[0]#.replace(' Form','').replace(' ','-')
                            #Finds ability info                               
                            this_Ability_Info = line.split('</i>: ')[1].split(' <')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                            #When the ability is shared by All Forms, which is the case for basculin
                            if 'All Forms' in this_ability_form:
                                for forms in dex_pokemon['Forms']:
                                    #Adds Ability Name and Info to form
                                    dex_pokemon['Forms'][forms]['Ability']['Name'].append(this_Ability)
                                    dex_pokemon['Forms'][forms]['Ability']['Info'].append(this_Ability_Info)

                    #Checks if next line is a hidden ability line
                    if line.startswith('<b>Hidden'):
                        #For most pokemon
                        if '></a>: ' in line and dex_pokemon['Species'][0] != 'Meowstic':
                            #Checks if this is a Hidden Ability
                            this_Ability = line.split('><b>')[1].split('</b>')[0] + ' (Hidden Ability)'
                            this_Ability_Info = line.split('></a>: ')[1].split(' <')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                            #Adds Ability Name and Info to current form
                            dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Name'].append(this_Ability)
                            dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Info'].append(this_Ability_Info)
                        #If the pokemon is Meowstic, we find different hidden abilities for the different genders
                        if '</a>: ' in line and dex_pokemon['Species'][0] == 'Meowstic':
                            #Copies first two regular abilities (name + info) into Female Form dictionary, since both forms can have them
                            dex_pokemon['Forms']['Form'+str(2)]['Ability']['Name'].append(dex_pokemon['Forms']['Form'+str(1)]['Ability']['Name'][0])
                            dex_pokemon['Forms']['Form'+str(2)]['Ability']['Name'].append(dex_pokemon['Forms']['Form'+str(1)]['Ability']['Name'][1])
                            dex_pokemon['Forms']['Form'+str(2)]['Ability']['Info'].append(dex_pokemon['Forms']['Form'+str(1)]['Ability']['Info'][0])
                            dex_pokemon['Forms']['Form'+str(2)]['Ability']['Info'].append(dex_pokemon['Forms']['Form'+str(1)]['Ability']['Info'][1]) 
                            #Finds first Hidden ability (Male only)
                            this_Ability = line.split('><b>')[1].split('</b>')[0] + ' (Hidden Ability)'
                            this_Ability_Info = line.split('</a>: ')[1].split(' <')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                            #Adds Ability Name and Info to current form
                            dex_pokemon['Forms']['Form'+str(1)]['Ability']['Name'].append(this_Ability)
                            dex_pokemon['Forms']['Form'+str(1)]['Ability']['Info'].append(this_Ability_Info)
                            #Finds second Hidden ability (Female only)
                            this_Ability = line.split('><b>')[2].split('</b>')[0] + ' (Hidden Ability)'
                            this_Ability_Info = line.split('</a>: ')[2].split(' <')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                            #Adds Ability Name and Info to current form
                            dex_pokemon['Forms']['Form'+str(2)]['Ability']['Name'].append(this_Ability)
                            dex_pokemon['Forms']['Form'+str(2)]['Ability']['Info'].append(this_Ability_Info)
                                                    
                        #For few exceptions, namely basculin
                        if '</i>: ' in line:
                            #Finds ability
                            this_Ability = line.split('><b>')[1].split('</b>')[0] + ' (Hidden Ability)'
                            #Finds form name
                            this_ability_form = line.split('<i>(')[1].split(')</i>')[0]#.replace(' Form','').replace(' ','-')
                            #Finds ability info                               
                            this_Ability_Info = line.split('</i>: ')[1].split(' <')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                            #When the ability is shared by All Forms, which is the case for basculin
                            if 'All Forms' in this_ability_form:
                                for forms in dex_pokemon['Forms']:
                                    #Adds Ability Name and Info to form
                                    dex_pokemon['Forms'][forms]['Ability']['Name'].append(this_Ability)
                                    dex_pokemon['Forms'][forms]['Ability']['Info'].append(this_Ability_Info)
                                                                
                    #Checks if next line is a NEW FORM line 
                    #since both NEW FORM lines and hidden ability lines start very similarly, we have to be more selective
                    if line.startswith('<b>') == True and line.startswith('<b>Hidden') == False and line.startswith('<b>Other Ability</b>') == False:
                        #Extracts form name
                        form_name = line.split(' Abilit')[0].strip('<b>')
                        #form_name = line.split(' Abilities</b>')[0].strip('<b>') #Had to change line due to plural/singular discrepancy
                        #print(form_name)

                        #Moves to the form with the MATCHING FORM NAME
                        #Sometimes more than one form share the same abilities and the abilities are only displayed once
                        #So we assume that the abilites are the same for the previous forms until we find a MATCH
                        #Moves to NEXT FORM
                        counter_forms_abilities = counter_forms_abilities + 1  
                        #If there is no MATCH, we assume that the abilites are the same for the previous forms until we find a MATCH
                        while form_name not in dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Name']:
                            #Copies Ability Name and Info to current form from previous form
                            dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Name'] = dex_pokemon['Forms']['Form'+str(counter_forms_abilities-1)]['Ability']['Name']
                            dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Info'] = dex_pokemon['Forms']['Form'+str(counter_forms_abilities-1)]['Ability']['Info']

                            #Moves to NEXT FORM
                            counter_forms_abilities = counter_forms_abilities + 1 

                        #If there is a MATCH
                        #Adds ability to current form
                        this_Ability = line.split('><b>')[1].split('</b>')[0]
                        this_Ability_Info = line.split('></a>: ')[1].split(' <')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'").replace('Pok&#233;mon','Pokemon')  #fixes bug with the text
                        #Adds Ability Name and Info to current form
                        dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Name'].append(this_Ability)
                        dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Info'].append(this_Ability_Info)

                    #Checks if next line is a Other Ability line, namely for Zygarde
                    #since both NEW FORM lines and hidden ability lines start very similarly, we have to be more selective
                    if line.startswith('<b>') == True and line.startswith('<b>Hidden') == False and line.startswith('<b>Other Ability</b>') == True:
                        #Finds ability name and info
                        this_Ability = line.split('><b>')[1].split('</b>')[0]
                        this_Ability_Info = line.split('></a>: ')[1].split(' <')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'") + ' (Some 10%/50%/Complete Forme)'  #fixes bug with the text
                        #Adds ability to all forms, one by one
                        for forms in dex_pokemon['Forms']:
                            dex_pokemon['Forms'][forms]['Ability']['Name'].append(this_Ability)
                            dex_pokemon['Forms'][forms]['Ability']['Info'].append(this_Ability_Info)
                            
                            
        ############### For SINGLE FORM POKEMON - Moves
        if len(dex_pokemon['Forms']) == 1:

            #Finding Level Up Moves Title Line
            if 'Level Up</h3>' in line and '"legendsattacks"' not in line:
                #Creates/Updates current_method and number_info variable to Level Up
                current_method = 'Level up'
                number_info = 'Level '

                #Moves to next line
                line = f.readline()

                #Starts a sub-loop through the lines until the end of the Level up block
                while line.startswith('	<td class="foox"') == False and '<td rowspan="2" class="fooinfo"><a' not in line and line.startswith('				<tr><td class="fooinfo"') == False:


                    #Extracts move information using a loop of 9 lines for each move

                    #Sets up sub dictionary entry for a new move
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])] = {'Name':[], 'Number':[], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}

                    #0)Adds Method to this set of moves:
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Method'].append(current_method)

                    #1)For the number:
                    #Extracts number
                    this_number = line.split('>')[1].split('<')[0]
                    #When there is no level 
                    if this_number == '&#8212;':
                        this_number = '-'
                    #print(number_info+this_number)
                    #When learns move upon evolving
                    if this_number == 'Evolve' or this_number == '-':
                        #Adds to current form
                        dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Number'].append(this_number)
                    else:
                        #Adds to current form
                        dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Number'].append(number_info+this_number)

                    #2)For the Move Name:
                    #Moves to next line
                    #print(line)
                    line = f.readline()
                    #Extracts Name
                    #print(line)
                    this_name = line.split('.shtml">')[1].split('<')[0]
                    #print(this_name)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Name'].append(this_name)

                    #3)For the Move Type:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Type
                    this_type = line.split('/type/')[1].split('.gif')[0].capitalize()
                    #print(this_type)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Type'].append(this_type)

                    #4)For the Move Mode:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Mode
                    this_mode = line.split('/type/')[1].split('.png')[0].capitalize()
                    #When it's a Status Move 
                    if this_mode == 'other' or this_mode == 'Other':
                        this_mode = 'Status'
                    #print(this_mode)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Mode'].append(this_mode)

                    #5)For the Power:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Power
                    this_power = line.split('>')[1].split('<')[0]
                    #print(this_power)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Power'].append(this_power)

                    #6)For the Accuracy:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Accuracy
                    this_accuracy = line.split('>')[1].split('<')[0]
                    #print(this_accuracy)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Accuracy'].append(this_accuracy)

                    #7)For the PP:
                    #Moves to next line
                    line = f.readline()
                    #Extracts PP
                    this_pp = line.split('>')[1].split('<')[0]
                    #print(this_pp)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['PP'].append(this_pp)

                    #8)For the Effect %:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Effect %
                    this_effect = line.split('>')[1].split('<')[0]
                    #print(this_effect)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Effect'].append(this_effect)

                    #9)For the Info:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Info
                    this_info = line.split('colspan="6">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                    #print(this_info)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Info'].append(this_info)

                    #Moves to next line only if
                    if '.</td></tr><tr>' in line:
                        line = f.readline()
                    #Moves move_counter to next iteration
                    move_counter['Form1'] = move_counter['Form1'] + 1


            #Finding Sword & Shield Technical Machine Attacks Title Line
            if 'Sword & Shield Technical Machine Attacks' in line or '>Technical Machine Attacks<' in line:
                #Creates/Updates current_method and number_info variable to TMs
                current_method = 'Sword & Shield TMs'
                #number_info = 'TM' 

                #Starts a sub-loop through the lines until the end of the Sword & Shield TMs block
                while 'Technical Record Attacks' not in line and '</a><h3>Egg Moves</h3>' not in line and 'Usable Max Moves' not in line:

                    #Extracts move information using a loop of 9 lines for each move

                    #Sets up sub dictionary entry for a new move
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])] = {'Name':[], 'Number':[], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}

                    #0)Adds Method to this set of moves:
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Method'].append(current_method)

                    #1)For the number:
                    #Extracts number
                    this_number = line.split('.shtml">')[1].split('<')[0]
                    #print(this_number)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Number'].append(this_number)

                    #2)For the Move Name:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Name
                    this_name = line.split('.shtml">')[1].split('<')[0]
                    #print(this_name)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Name'].append(this_name)

                    #3)For the Move Type:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Type
                    this_type = line.split('/type/')[1].split('.gif')[0].capitalize()
                    #print(this_type)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Type'].append(this_type)

                    #4)For the Move Mode:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Mode
                    this_mode = line.split('/type/')[1].split('.png')[0].capitalize()
                    #When it's a Status Move 
                    if this_mode == 'other' or this_mode == 'Other':
                        this_mode = 'Status'
                    #print(this_mode)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Mode'].append(this_mode)

                    #5)For the Power:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Power
                    this_power = line.split('>')[1].split('<')[0]
                    #print(this_power)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Power'].append(this_power)

                    #6)For the Accuracy:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Accuracy
                    this_accuracy = line.split('>')[1].split('<')[0]
                    #print(this_accuracy)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Accuracy'].append(this_accuracy)

                    #7)For the PP:
                    #Moves to next line
                    line = f.readline()
                    #Extracts PP
                    this_pp = line.split('>')[1].split('<')[0]
                    #print(this_pp)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['PP'].append(this_pp)

                    #8)For the Effect %:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Effect %
                    this_effect = line.split('>')[1].split('<')[0]
                    #print(this_effect)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Effect'].append(this_effect)

                    #9)For the Info:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Info
                    this_info = line.split('colspan="6">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                    #print(this_info)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Info'].append(this_info)

                    #Moves move_counter to next iteration
                    move_counter['Form1'] = move_counter['Form1'] + 1


            #Finding Technical Record Attacks Title Line
            if 'Technical Record Attacks' in line:
                #Creates/Updates current_method and number_info variable to TRs
                current_method = 'TRs'
                number_info = 'TR' 

                #Starts a sub-loop through the lines until the end of the TRs block
                while 'BDSP Technical Machine Attacks' not in line and '</a><h3>Egg Moves</h3>' not in line and 'Move Tutor Attacks<' not in line and 'Usable Max Moves' not in line:

                    #Extracts move information using a loop of 9 lines for each move

                    #Sets up sub dictionary entry for a new move
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])] = {'Name':[], 'Number':[], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}

                    #0)Adds Method to this set of moves:
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Method'].append(current_method)

                    #1)For the number:
                    #Extracts number
                    this_number = line.split('.shtml">')[1].split('<')[0]
                    #print(this_number)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Number'].append(this_number)

                    #2)For the Move Name:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Name
                    this_name = line.split('.shtml">')[1].split('<')[0]
                    #print(this_name)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Name'].append(this_name)

                    #3)For the Move Type:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Type
                    this_type = line.split('/type/')[1].split('.gif')[0].capitalize()
                    #print(this_type)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Type'].append(this_type)

                    #4)For the Move Mode:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Mode
                    this_mode = line.split('/type/')[1].split('.png')[0].capitalize()
                    #When it's a Status Move 
                    if this_mode == 'other' or this_mode == 'Other':
                        this_mode = 'Status'
                    #print(this_mode)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Mode'].append(this_mode)

                    #5)For the Power:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Power
                    this_power = line.split('>')[1].split('<')[0]
                    #print(this_power)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Power'].append(this_power)

                    #6)For the Accuracy:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Accuracy
                    this_accuracy = line.split('>')[1].split('<')[0]
                    #print(this_accuracy)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Accuracy'].append(this_accuracy)

                    #7)For the PP:
                    #Moves to next line
                    line = f.readline()
                    #Extracts PP
                    this_pp = line.split('>')[1].split('<')[0]
                    #print(this_pp)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['PP'].append(this_pp)

                    #8)For the Effect %:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Effect %
                    this_effect = line.split('>')[1].split('<')[0]
                    #print(this_effect)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Effect'].append(this_effect)

                    #9)For the Info:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Info
                    this_info = line.split('colspan="6">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                    #print(this_info)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Info'].append(this_info)

                    #Moves move_counter to next iteration
                    move_counter['Form1'] = move_counter['Form1'] + 1


            #Finding BDSP Technical Machine Attacks Title Line
            if 'BDSP Technical Machine Attacks' in line:
                #Creates/Updates current_method and number_info variable to TMs
                current_method = 'BDSP TMs'
                number_info = 'TM' 

                #Starts a sub-loop through the lines until the end of the TRs block
                while '</a><h3>Egg Moves</h3>' not in line and 'Move Tutor Attacks<' not in line and '"transfer"' not in line and 'Usable Max Moves' not in line:

                    #Extracts move information using a loop of 9 lines for each move

                    #Sets up sub dictionary entry for a new move
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])] = {'Name':[], 'Number':[], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}

                    #0)Adds Method to this set of moves:
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Method'].append(current_method)

                    #1)For the number:
                    #Extracts number
                    this_number = line.split('.shtml">')[1].split('<')[0]
                    #print(this_number)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Number'].append(this_number)

                    #2)For the Move Name:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Name
                    this_name = line.split('.shtml">')[1].split('<')[0]
                    #print(this_name)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Name'].append(this_name)

                    #3)For the Move Type:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Type
                    this_type = line.split('/type/')[1].split('.gif')[0].capitalize()
                    #print(this_type)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Type'].append(this_type)

                    #4)For the Move Mode:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Mode
                    this_mode = line.split('/type/')[1].split('.png')[0].capitalize()
                    #When it's a Status Move 
                    if this_mode == 'other' or this_mode == 'Other':
                        this_mode = 'Status'
                    #print(this_mode)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Mode'].append(this_mode)

                    #5)For the Power:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Power
                    this_power = line.split('>')[1].split('<')[0]
                    #print(this_power)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Power'].append(this_power)

                    #6)For the Accuracy:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Accuracy
                    this_accuracy = line.split('>')[1].split('<')[0]
                    #print(this_accuracy)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Accuracy'].append(this_accuracy)

                    #7)For the PP:
                    #Moves to next line
                    line = f.readline()
                    #Extracts PP
                    this_pp = line.split('>')[1].split('<')[0]
                    #print(this_pp)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['PP'].append(this_pp)

                    #8)For the Effect %:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Effect %
                    this_effect = line.split('>')[1].split('<')[0]
                    #print(this_effect)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Effect'].append(this_effect)

                    #9)For the Info:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Info
                    this_info = line.split('colspan="6">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                    #print(this_info)    
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Info'].append(this_info)

                    #Moves move_counter to next iteration
                    move_counter['Form1'] = move_counter['Form1'] + 1

            #Finding Egg Moves Title Line
            if '</a><h3>Egg Moves</h3>' in line:
                #Creates/Updates current_method and number_info variable to TMs
                current_method = 'Egg Moves' 

                #Starts a sub-loop through the lines until the end of the TRs block
                while 'Move Tutor Attacks<' not in line and 'Usable Max Moves' not in line and 'name="transfer"' not in line:

                    #Extracts move information using a loop of 8 lines for each move

                    #Sets up sub dictionary entry for a new move
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])] = {'Name':[], 'Number':['--'], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}

                    #0)Adds Method to this set of moves:
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Method'].append(current_method)

                    #1)For the Move Name:
                    #Extracts Name
                    #For this first Egg Move
                    if 'egg.shtml">' in line:
                        this_name = line.split('egg.shtml">')[1].split('.shtml">')[1].split('<')[0]
                    #For following Egg Moves
                    if 'egg.shtml">' not in line:
          ####              ###print(line)
                        this_name = line.split('.shtml">')[1].split('<')[0]
                    #print(this_name)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Name'].append(this_name)

                    #2)For the Move Type:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Type
                    this_type = line.split('/type/')[1].split('.gif')[0].capitalize()
                    #print(this_type)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Type'].append(this_type)

                    #3)For the Move Mode:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Mode
                    this_mode = line.split('/type/')[1].split('.png')[0].capitalize()
                    #When it's a Status Move 
                    if this_mode == 'other' or this_mode == 'Other':
                        this_mode = 'Status'
                    #print(this_mode)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Mode'].append(this_mode)

                    #4)For the Power:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Power
                    this_power = line.split('>')[1].split('<')[0]
                    #print(this_power)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Power'].append(this_power)      

                    #5)For the Accuracy:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Accuracy
                    this_accuracy = line.split('>')[1].split('<')[0]
                    #print(this_accuracy)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Accuracy'].append(this_accuracy)

                    #6)For the PP:
                    #Moves to next line
                    line = f.readline()
                    #Extracts PP
                    this_pp = line.split('>')[1].split('<')[0]
                    #print(this_pp)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['PP'].append(this_pp)

                    #7)For the Effect %:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Effect %
                    this_effect = line.split('>')[1].split('<')[0]
                    #print(this_effect)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Effect'].append(this_effect)

                    #8)For the Info:
                    #Moves to next line (skipping the 'Details' line)
                    line = f.readline()
                    #Moves to next line (skipping the blank line)
                    line = f.readline()
                    #Moves to next line
                    line = f.readline()
                    #Extracts Info
                    if 'colspan="6">' in line:
                        this_info = line.split('colspan="6">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                    else: #when there is additional information besides move info (e.g. special requirement to learn egg move -> Pikachu)
                        this_info = line.split('">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")+' '+line.split('">')[2].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text                   
                    #print(this_info)   
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Info'].append(this_info)

                    #Moves move_counter to next iteration
                    move_counter['Form1'] = move_counter['Form1'] + 1


            #Finding Move Tutor Attacks Title Line
            if 'Move Tutor Attacks<' in line:
                #Creates/Updates current_method and number_info variable to TMs
                current_method = 'Move Tutor'

                #print(line)

                #Splits the line right in front of move name to separate line by moves
                split_line = line.split('.shtml">')
                #Deletes first element from the list
                split_line.pop(0)

                #Creates a loop to use all elements of split_line, except for element 0
                for element in split_line:

                    #Extracts move information using line splitting

                    #Sets up sub dictionary entry for a new move
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])] = {'Name':[], 'Number':['--'], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}

                    #0)Adds Method to this set of moves:
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Method'].append(current_method)

                    #1)For the Move Name:
                    #Extracts Name
                    this_name = element.split('</a></')[0]
                    #print(this_name)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Name'].append(this_name)

                    #2)For the Move Type:
                    #Extracts Type
                    this_type = element.split('/type/')[1].split('.gif')[0].capitalize()
                    #print(this_type)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Type'].append(this_type)

                    #3)For the Move Mode:
                    #Extracts Mode
                    this_mode = element.split('/type/')[2].split('.png')[0].capitalize()
                    #When it's a Status Move 
                    if this_mode == 'other' or this_mode == 'Other':
                        this_mode = 'Status'
                    #print(this_mode)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Mode'].append(this_mode)

                    #4)For the Power:
                    #Extracts Power
                    this_power = element.split('"fooinfo">')[3].split('<')[0]
                    #print(this_power)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Power'].append(this_power)

                    #5)For the Accuracy:
                    #Extracts Accuracy
                    this_accuracy = element.split('"fooinfo">')[4].split('<')[0]
                    #print(this_accuracy)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Accuracy'].append(this_accuracy)

                    #6)For the PP:
                    #Extracts PP
                    this_pp = element.split('"fooinfo">')[5].split('<')[0]
                    #print(this_pp)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['PP'].append(this_pp)

                    #7)For the Effect %:
                    #Extracts Effect %
                    this_effect = element.split('"fooinfo">')[6].split('<')[0]
                    #print(this_effect)
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Effect'].append(this_effect)

                    #8)For the Info:
                    #Extracts Info
                    this_info = element.split('"fooinfo">')[7].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                    #print(this_info)   
                    #Adds to current form
                    dex_pokemon['Forms']['Form1']['Moves']['Move'+str(move_counter['Form1'])]['Info'].append(this_info)

                    #Moves move_counter to next iteration
                    move_counter['Form1'] = move_counter['Form1'] + 1


        ############### For MULTI FORM POKEMON - Moves
        if len(dex_pokemon['Forms']) > 1:

            #Finding Level Up Moves Title Lines (for all the forms)
            while ('Level Up</h3>' in line or 'Level Up - ' in line) and '"legendsattacks"' not in line and ' White-Striped Form' not in line: #This last condition is to avoid Basculin's Legend Arceus info
                
                #For most pokemon
                if 'Level Up</h3>' in line: 
                    #Identifying the form
                    current_form = line.split('level"></a>')[1].split(' Level')[0].strip(' Form')
                    #Creates/Updates current_method and number_info variable to Level Up
                    current_method = 'Level up'
                    number_info = 'Level '
                    
                ### Dealing with the Level Up - XXX Form Title Line Discrepancy
                #Identifying the form
                #When Sword and Shield/Diamond and Pearl have NO Level up differences
                if '>Level Up - ' in line:                
                    current_form = line.split('Level Up - ')[1].split('<')[0].replace(' Forme','').replace(' Form','')
                    #Specifies method as Level up
                    current_method = 'Level up'
                    number_info = 'Level '
                #When Sword and Shield/Diamond and Pearl have Level up differences
                if ' Level Up - ' in line:
                    current_form = line.split(' Level Up -')[0].split('level"></a>')[1].strip(' Forme').strip(' Form')
                    #Specifies method as Level up + Game title
                    current_method = 'Level up' + line.split(' Level Up -')[1].split('<')[0]
                    number_info = 'Level '
                #print(current_form)
                          
                #Fixes the Alolan/Alola Form discrepancy
                if current_form == 'Alolan':
                    current_form = 'Alola' #the shorter form will always work when using the in statement
                #print(current_form)

                #Finding the corresponding form within the dictionary
                #Creating/resetting helpful loop counter:
                form_counter = 1

                #When dealing with the Standard form  (assumes standard form to be Form1)
                if current_form == 'Standard':
                    form_counter = 1
                    #print('yes')
                    #print(form_counter)

                #When not dealing with standard form
                if current_form != 'Standard':
                    #Starting loop
                    while current_form not in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                        #When not a match, moves counter to next iteration
                        form_counter = form_counter + 1
                        #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                    #When a match, does nothing (this is only used for debugging)
                    #if current_form in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                        #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                        #print('yes')
                        #print(form_counter)

                #Moves to next line
                line = f.readline()

                #Starts a sub-loop through the lines until the end of the Level up block
                while line.startswith('	<td class="foox"') == False and '<td rowspan="2" class="fooinfo"><a' not in line and line.startswith('				<tr><td class="fooinfo"') == False:

                    #Extracts move information using a loop of 9 lines for each move

                    #Sets up sub dictionary entry for a new move
                    dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])] = {'Name':[], 'Number':[], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}

                    #0)Adds Method to this set of moves:
                    dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Method'].append(current_method)

                    #1)For the number:
                    #Extracts number
                    this_number = line.split('>')[1].split('<')[0]
                    #When there is no level 
                    if this_number == '&#8212;':
                        this_number = '-'
                    #print(number_info+this_number)
                    #When learns move upon evolving
                    if this_number == 'Evolve' or this_number == '-':
                        #Adds to current form
                        dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Number'].append(this_number)
                    else:
                        #Adds to current form
                        dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Number'].append(number_info+this_number)

                    #2)For the Move Name:
                    #Moves to next line
                    #print(line)
                    line = f.readline()
                    #Extracts Name
                    #print(line)
                    this_name = line.split('.shtml">')[1].split('<')[0]
                    #print(this_name)
                    #Adds to current form
                    dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Name'].append(this_name)
                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Name'])

                    #3)For the Move Type:
                    #Moves to next line
                    line = f.readline()
                    #print(line)
                    #Extracts Type
                    this_type = line.split('/type/')[1].split('.gif')[0].capitalize()
                    #print(this_type)
                    #Adds to current form
                    dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Type'].append(this_type)

                    #4)For the Move Mode:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Mode
                    this_mode = line.split('/type/')[1].split('.png')[0].capitalize()
                    #When it's a Status Move 
                    if this_mode == 'other' or this_mode == 'Other':
                        this_mode = 'Status'
                    #print(this_mode)
                    #Adds to current form
                    dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Mode'].append(this_mode)

                    #5)For the Power:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Power
                    this_power = line.split('>')[1].split('<')[0]
                    #print(this_power)
                    #Adds to current form
                    dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Power'].append(this_power)

                    #6)For the Accuracy:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Accuracy
                    this_accuracy = line.split('>')[1].split('<')[0]
                    #print(this_accuracy)
                    #Adds to current form
                    dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Accuracy'].append(this_accuracy)

                    #7)For the PP:
                    #Moves to next line
                    line = f.readline()
                    #Extracts PP
                    this_pp = line.split('>')[1].split('<')[0]
                    #print(this_pp)
                    #Adds to current form
                    dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['PP'].append(this_pp)

                    #8)For the Effect %:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Effect %
                    this_effect = line.split('>')[1].split('<')[0]
                    #print(this_effect)
                    #Adds to current form
                    dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Effect'].append(this_effect)

                    #9)For the Info:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Info
                    this_info = line.split('colspan="6">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                    #print(this_info)
                    #Adds to current form
                    dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Info'].append(this_info)

                    #Moves to next line only if
                    if '.</td></tr><tr>' in line:
                        line = f.readline()
                    #Moves move_counter to next iteration
                    move_counter['Form'+str(form_counter)] = move_counter['Form'+str(form_counter)] + 1
       
    

    #########Final check to make sure ALL FORMS have assigned Level Up Moves  (May not be the fastest way to do this...)
            #This is strategically positioned so only Level up Moves were loaded at this point
            #This is very important for when MULTIPLE FORMS share the same Level Up Moves and the Level Up Moves are only stated once (e.g. Darmanitan and Rotom)
            #This analysis is conducted only once and AFTER THE LEVEL UP MOVES WERE ADDED
            if level_up_moves_final_check == 0 and len(dex_pokemon['Forms']['Form1']['Moves']) > 1:
                #Makes sure this analysis is only conducted only once by setting variable to 1
                level_up_moves_final_check = 1  

                #Creates/resets helpful form counter
                counter_forms_level_up_moves = 1
                #Starts to loop through dictionary
                while counter_forms_level_up_moves <= len(dex_pokemon['Forms']):

                    #Sets/Resets useful variable to 0 (meaning there are NO Level up Moves for current form)
                    level_up_moves = 0
                    #Loops through moves within form
                    for moves in dex_pokemon['Forms']['Form'+str(counter_forms_level_up_moves)]['Moves']:
                        #If current form has at least one Level up Move
                        if 'Level up' in dex_pokemon['Forms']['Form'+str(counter_forms_level_up_moves)]['Moves'][moves]['Method'][0]:
                            level_up_moves = 1

                    #If there were No Level up moves
                    if level_up_moves == 0:
                        #print('No')  
                        #Copies information from the previous FORM (Assumes Level Up Moves to be the same between the two FORMS)
                        #When working with Darmamitan, we want to forever link Zen mode and Normal mode's moves for each regional variant so we don't have to worry about copying TMs/TRs/Move tutor/Egg moves
                        if dex_pokemon['Species'][0] == 'Darmanitan':  
                            dex_pokemon['Forms']['Form'+str(counter_forms_level_up_moves)]['Moves'] = dex_pokemon['Forms']['Form'+str(counter_forms_level_up_moves-1)]['Moves']  
                            #This ^ forever links the two dictionaries = when one changes, the other automatically changes
                        #When not working with Darmanitan, we don't want to forever link forms' moves because they may vary later on (e.g. move tutor, special moves)
                        if dex_pokemon['Species'][0] != 'Darmanitan':
                            dex_pokemon['Forms']['Form'+str(counter_forms_level_up_moves)]['Moves'] = dict(dex_pokemon['Forms']['Form'+str(counter_forms_level_up_moves-1)]['Moves'])  
                            #This ^ copies the info from one dict to the other without linking them forever
                        #Updates move_counter to appropriate number, so more moves can be added without replacing previous ones
                        move_counter['Form'+str(counter_forms_level_up_moves)] = move_counter['Form'+str(counter_forms_level_up_moves-1)]
                        #This ^ works here because we're refering directly to the value, in this case an int
                    #Moves to next iteration
                    counter_forms_level_up_moves = counter_forms_level_up_moves + 1        


            #Finding Sword & Shield Technical Machine Attacks Title Line
            if 'Sword & Shield Technical Machine Attacks' in line or '>Technical Machine Attacks<' in line:
                #Creates/Updates current_method and number_info variable to TMs
                current_method = 'Sword & Shield TMs'
                #number_info = 'TM' 

                #Checks if TMs are separated by FORMS (e.g. differennt forms learn different moves)
                if '>Form<' in line or dex_pokemon['Species'][0] == 'Calyrex':  #Calyrex has TMs/TRs separated by forms without using the word forms in the title:
                    #Sets/resets individual_form_TM_TR to 1:
                    individual_form_TM_TR = 1
                else:
                    #Sets/resets individual_form_TM_TR to 0:
                    individual_form_TM_TR = 0

                #Starts a sub-loop through the lines until the end of the Sword & Shield TMs block
                while 'Technical Record Attacks' not in line and '</a><h3>Egg Moves</h3>' not in line and 'Usable Max Moves' not in line:          

                    #Extracts move information using a loop of 10 lines for each move

                    #1)For the number:
                    #Extracts number
                    this_number = line.split('.shtml">')[1].split('<')[0]
                    #print(this_number)

                    #2)For the Move Name:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Name
                    this_name = line.split('.shtml">')[1].split('<')[0]
                    #print(this_name)

                    #3)For the Move Type:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Type
                    this_type = line.split('/type/')[1].split('.gif')[0].capitalize()
                    #print(this_type)

                    #4)For the Move Mode:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Mode
                    this_mode = line.split('/type/')[1].split('.png')[0].capitalize()
                    #When it's a Status Move 
                    if this_mode == 'other' or this_mode == 'Other':
                        this_mode = 'Status'
                    #print(this_mode)

                    #5)For the Power:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Power
                    this_power = line.split('>')[1].split('<')[0]
                    #print(this_power)

                    #6)For the Accuracy:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Accuracy
                    this_accuracy = line.split('>')[1].split('<')[0]
                    #print(this_accuracy)

                    #7)For the PP:
                    #Moves to next line
                    line = f.readline()
                    #Extracts PP
                    this_pp = line.split('>')[1].split('<')[0]
                    #print(this_pp)

                    #8)For the Effect %:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Effect %
                    this_effect = line.split('>')[1].split('<')[0]
                    #print(this_effect)

                    #8.5)For individual form information
                    if individual_form_TM_TR == 1:
                        #Moves to next line
                        line = f.readline()
                        #Extracts FORM info
                        #Makes first split before the names of the forms
                        this_form_info = line.split('alt="')
                        #Removes initial text
                        this_form_info.pop(0)
                        #Creates/resets this_form_list
                        this_form_list = []
                        #Makes the second split to isolate form names and adds them to this_form_list
                        for form in this_form_info:
                            #Prepares form
                            form = form.split('"')[0].strip(' Form')
                            #Fixes the Alolan/Alola Form discrepancy
                            if form == 'Alolan':
                                form = 'Alola' #the shorter form will always work when using the in statement
                            #Adds form to list
                            this_form_list.append(form)
                        #print(this_form_list)

                    #9)For the Info:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Info
                    this_info = line.split('colspan="6">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                    #print(this_info)

                    #Starts a loop to add move information to the dictitionary for the corresponding FORMS
                    #For individual form information
                    if individual_form_TM_TR == 1:
                        #Starts loop through the forms in this_form_list
                        for current_form in this_form_list:                    
                            #Finding the corresponding form within the dictionary
                            #Creating/resetting helpful loop counter:
                            form_counter = 1

                            #When dealing with the Standard form  (assumes standard form to be Form1)
                            if current_form == 'Standard' or current_form == 'Normal':
                                form_counter = 1
                                #print('yes')
                                #print(form_counter)

                            #When not dealing with standard form
                            if current_form != 'Standard' and current_form != 'Normal':
                                #Starting loop
                                while current_form not in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                                    #When not a match, moves counter to next iteration
                                    form_counter = form_counter + 1
                                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                                #When a match, does nothing (this is only used for debugging)
                                #if current_form in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                                    #print('yes')
                                    #print(form_counter)                                    

                            #Adds move information to dictionary for current_form
                            #Sets up sub dictionary entry for a new move
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])] = {'Name':[], 'Number':[], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}                
                            #0)Adds Method to this set of moves:
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Method'].append(current_method)                
                            #1)Adds Number to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Number'].append(this_number)                
                            #2)Adds Move Name to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Name'].append(this_name)                
                            #3)Adds Move Type to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Type'].append(this_type)                
                            #4)Adds Move Mode to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Mode'].append(this_mode)                
                            #5)Adds Move Power to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Power'].append(this_power)                
                            #6)Adds Move Accuracy to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Accuracy'].append(this_accuracy)                
                            #7)Adds Move PP to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['PP'].append(this_pp)                        
                            #8)Adds Move Effect % to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Effect'].append(this_effect)                
                            #9)Adds Move Info to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Info'].append(this_info)                

                            #Moves move_counter to next iteration for current form
                            move_counter['Form'+str(form_counter)] = move_counter['Form'+str(form_counter)] + 1

                    #When there is no individual form information, we assume all forms can learn these moves
                    if individual_form_TM_TR == 0:
                        #Loops through all the forms, one by one
                        for current_form in dex_pokemon['Forms']:
                            #Adds move information to dictionary for current_form
                            #Sets up sub dictionary entry for a new move
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])] = {'Name':[], 'Number':[], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}                
                            #0)Adds Method to this set of moves:
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Method'].append(current_method)                
                            #1)Adds Number to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Number'].append(this_number)                
                            #2)Adds Move Name to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Name'].append(this_name)                
                            #3)Adds Move Type to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Type'].append(this_type)                
                            #4)Adds Move Mode to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Mode'].append(this_mode)                
                            #5)Adds Move Power to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Power'].append(this_power)                
                            #6)Adds Move Accuracy to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Accuracy'].append(this_accuracy)                
                            #7)Adds Move PP to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['PP'].append(this_pp)                        
                            #8)Adds Move Effect % to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Effect'].append(this_effect)                
                            #9)Adds Move Info to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Info'].append(this_info)                

                            #Moves move_counter to next iteration for current form
                            move_counter[current_form] = move_counter[current_form] + 1


            #Finding Technical Record Attacks Title Line
            if 'Technical Record Attacks' in line:
                #Creates/Updates current_method and number_info variable to TRs
                current_method = 'TRs'
                number_info = 'TR' 

                #Checks if TRs are separated by FORMS (e.g. differennt forms learn different moves)
                if '>Form<' in line or dex_pokemon['Species'][0] == 'Calyrex':  #Calyrex has TMs/TRs separated by forms without using the word forms in the title
                    #Sets/resets individual_form_TM_TR to 1:
                    individual_form_TM_TR = 1
                else:
                    #Sets/resets individual_form_TM_TR to 0:
                    individual_form_TM_TR = 0

                #Starts a sub-loop through the lines until the end of the TRs block
                while 'BDSP Technical Machine Attacks' not in line and '</a><h3>Egg Moves</h3>' not in line and 'Move Tutor Attacks<' not in line and 'Usable Max Moves' not in line:

                    #Extracts move information using a loop of 10 lines for each move

                    #1)For the number:
                    #Extracts number
                    this_number = line.split('.shtml">')[1].split('<')[0]
                    #print(this_number)

                    #2)For the Move Name:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Name
                    this_name = line.split('.shtml">')[1].split('<')[0]
                    #print(this_name)

                    #3)For the Move Type:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Type
                    this_type = line.split('/type/')[1].split('.gif')[0].capitalize()
                    #print(this_type)

                    #4)For the Move Mode:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Mode
                    this_mode = line.split('/type/')[1].split('.png')[0].capitalize()
                    #When it's a Status Move 
                    if this_mode == 'other' or this_mode == 'Other':
                        this_mode = 'Status'
                    #print(this_mode)

                    #5)For the Power:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Power
                    this_power = line.split('>')[1].split('<')[0]
                    #print(this_power)

                    #6)For the Accuracy:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Accuracy
                    this_accuracy = line.split('>')[1].split('<')[0]
                    #print(this_accuracy)

                    #7)For the PP:
                    #Moves to next line
                    line = f.readline()
                    #Extracts PP
                    this_pp = line.split('>')[1].split('<')[0]
                    #print(this_pp)

                    #8)For the Effect %:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Effect %
                    this_effect = line.split('>')[1].split('<')[0]
                    #print(this_effect)

                    #8.5)For individual form information
                    if individual_form_TM_TR == 1:
                        #Moves to next line
                        line = f.readline()
                        #Extracts FORM info
                        #Makes first split before the names of the forms
                        this_form_info = line.split('alt="')
                        #Removes initial text
                        this_form_info.pop(0)
                        #Creates/resets this_form_list
                        this_form_list = []
                        #Makes the second split to isolate form names and adds them to this_form_list
                        for form in this_form_info:
                            #Prepares form
                            form = form.split('"')[0].strip(' Form')
                            #Fixes the Alolan/Alola Form discrepancy
                            if form == 'Alolan':
                                form = 'Alola' #the shorter form will always work when using the in statement
                            #Adds form to list
                            this_form_list.append(form)
                        #print(this_form_list)

                    #9)For the Info:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Info
                    this_info = line.split('colspan="6">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                    #print(this_info)


                    #Starts a loop to add move information to the dictitionary for the corresponding FORMS
                    #For individual form information
                    if individual_form_TM_TR == 1:
                        #Starts loop through the forms in this_form_list
                        for current_form in this_form_list:                    
                            #Finding the corresponding form within the dictionary
                            #Creating/resetting helpful loop counter:
                            form_counter = 1

                            #When dealing with the Standard form  (assumes standard form to be Form1)
                            if current_form == 'Standard' or current_form == 'Normal':
                                form_counter = 1
                                #print('yes')
                                #print(form_counter)

                            #When not dealing with standard form
                            if current_form != 'Standard' and current_form != 'Normal':
                                #Starting loop
                                while current_form not in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                                    #When not a match, moves counter to next iteration
                                    form_counter = form_counter + 1
                                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                                #When a match, does nothing (this is only used for debugging)
                                #if current_form in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                                    #print('yes')
                                    #print(form_counter)                                    

                            #Adds move information to dictionary for current_form
                            #Sets up sub dictionary entry for a new move
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])] = {'Name':[], 'Number':[], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}                
                            #0)Adds Method to this set of moves:
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Method'].append(current_method)                
                            #1)Adds Number to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Number'].append(this_number)                
                            #2)Adds Move Name to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Name'].append(this_name)                
                            #3)Adds Move Type to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Type'].append(this_type)                
                            #4)Adds Move Mode to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Mode'].append(this_mode)                
                            #5)Adds Move Power to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Power'].append(this_power)                
                            #6)Adds Move Accuracy to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Accuracy'].append(this_accuracy)                
                            #7)Adds Move PP to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['PP'].append(this_pp)                        
                            #8)Adds Move Effect % to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Effect'].append(this_effect)                
                            #9)Adds Move Info to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Info'].append(this_info)                

                            #Moves move_counter to next iteration for current form
                            move_counter['Form'+str(form_counter)] = move_counter['Form'+str(form_counter)] + 1

                    #When there is no individual form information, we assume all forms can learn these moves
                    if individual_form_TM_TR == 0:
                        #Loops through all the forms, one by one
                        for current_form in dex_pokemon['Forms']:
                            #Adds move information to dictionary for current_form
                            #Sets up sub dictionary entry for a new move
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])] = {'Name':[], 'Number':[], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}                
                            #0)Adds Method to this set of moves:
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Method'].append(current_method)                
                            #1)Adds Number to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Number'].append(this_number)                
                            #2)Adds Move Name to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Name'].append(this_name)                
                            #3)Adds Move Type to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Type'].append(this_type)                
                            #4)Adds Move Mode to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Mode'].append(this_mode)                
                            #5)Adds Move Power to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Power'].append(this_power)                
                            #6)Adds Move Accuracy to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Accuracy'].append(this_accuracy)                
                            #7)Adds Move PP to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['PP'].append(this_pp)                        
                            #8)Adds Move Effect % to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Effect'].append(this_effect)                
                            #9)Adds Move Info to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Info'].append(this_info)                

                            #Moves move_counter to next iteration for current form
                            move_counter[current_form] = move_counter[current_form] + 1


            #Finding BDSP Technical Machine Attacks Title Line - NO REGIONAL VARIANTS APPEAR IN BDSP
            if 'BDSP Technical Machine Attacks' in line:
                #Creates/Updates current_method and number_info variable to TMs
                current_method = 'BDSP TMs'
                number_info = 'TM' 

                #Checks if TMs are separated by FORMS (e.g. differennt forms learn different moves)
                if '>Form<' in line:
                    #Sets/resets individual_form_TM_TR to 1:
                    individual_form_TM_TR = 1
                else:
                    #Sets/resets individual_form_TM_TR to 0:
                    individual_form_TM_TR = 0

                #Starts a sub-loop through the lines until the end of the TRs block
                while '</a><h3>Egg Moves</h3>' not in line and 'Move Tutor Attacks<' not in line and '"transfer"' not in line:

                    #Extracts move information using a loop of 9 lines for each move

                    #1)For the number:
                    #Extracts number
                    this_number = line.split('.shtml">')[1].split('<')[0]
                    #print(this_number)

                    #2)For the Move Name:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Name
                    this_name = line.split('.shtml">')[1].split('<')[0]
                    #print(this_name)

                    #3)For the Move Type:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Type
                    this_type = line.split('/type/')[1].split('.gif')[0].capitalize()
                    #print(this_type)

                    #4)For the Move Mode:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Mode
                    this_mode = line.split('/type/')[1].split('.png')[0].capitalize()
                    #When it's a Status Move 
                    if this_mode == 'other' or this_mode == 'Other':
                        this_mode = 'Status'
                    #print(this_mode)

                    #5)For the Power:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Power
                    this_power = line.split('>')[1].split('<')[0]
                    #print(this_power)

                    #6)For the Accuracy:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Accuracy
                    this_accuracy = line.split('>')[1].split('<')[0]
                    #print(this_accuracy)

                    #7)For the PP:
                    #Moves to next line
                    line = f.readline()
                    #Extracts PP
                    this_pp = line.split('>')[1].split('<')[0]
                    #print(this_pp)

                    #8)For the Effect %:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Effect %
                    this_effect = line.split('>')[1].split('<')[0]
                    #print(this_effect)

                    #8.5)For individual form information
                    if individual_form_TM_TR == 1:
                        #Moves to next line
                        line = f.readline()
                        #Extracts FORM info
                        #Makes first split before the names of the forms
                        this_form_info = line.split('alt="')
                        #Removes initial text
                        this_form_info.pop(0)
                        #Creates/resets this_form_list
                        this_form_list = []
                        #Makes the second split to isolate form names and adds them to this_form_list
                        for form in this_form_info:
                            #Prepares form
                            form = form.split('"')[0].strip(' Form')
                            #Fixes the Alolan/Alola Form discrepancy
                            if form == 'Alolan':
                                form = 'Alola' #the shorter form will always work when using the in statement
                            #Adds form to list
                            this_form_list.append(form)
                        #print(this_form_list)

                    #9)For the Info:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Info
                    this_info = line.split('colspan="6">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                    #print(this_info)    

                    #Starts a loop to add move information to the dictitionary for the corresponding FORMS
                    #For individual form information
                    if individual_form_TM_TR == 1:
                        #Starts loop through the forms in this_form_list
                        for current_form in this_form_list:                    
                            #Finding the corresponding form within the dictionary
                            #Creating/resetting helpful loop counter:
                            form_counter = 1

                            #When dealing with the Standard form  (assumes standard form to be Form1)
                            if current_form == 'Standard' or current_form == 'Normal':
                                form_counter = 1
                                #print('yes')
                                #print(form_counter)

                            #When not dealing with standard form
                            if current_form != 'Standard' and current_form != 'Normal':
                                #Starting loop
                                while current_form not in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                                    #When not a match, moves counter to next iteration
                                    form_counter = form_counter + 1
                                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                                #When a match, does nothing (this is only used for debugging)
                                #if current_form in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                                    #print('yes')
                                    #print(form_counter)                                    

                            #Adds move information to dictionary for current_form
                            #Sets up sub dictionary entry for a new move
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])] = {'Name':[], 'Number':[], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}                
                            #0)Adds Method to this set of moves:
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Method'].append(current_method)                
                            #1)Adds Number to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Number'].append(this_number)                
                            #2)Adds Move Name to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Name'].append(this_name)                
                            #3)Adds Move Type to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Type'].append(this_type)                
                            #4)Adds Move Mode to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Mode'].append(this_mode)                
                            #5)Adds Move Power to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Power'].append(this_power)                
                            #6)Adds Move Accuracy to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Accuracy'].append(this_accuracy)                
                            #7)Adds Move PP to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['PP'].append(this_pp)                        
                            #8)Adds Move Effect % to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Effect'].append(this_effect)                
                            #9)Adds Move Info to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Info'].append(this_info)                

                            #Moves move_counter to next iteration for current form
                            move_counter['Form'+str(form_counter)] = move_counter['Form'+str(form_counter)] + 1

                    #When there is no individual form information, we assume all forms can learn these moves
                    if individual_form_TM_TR == 0:
                        #Loops through all the forms, one by one
                        for current_form in dex_pokemon['Forms']:
                            #Adds move information to dictionary for current_form
                            #Sets up sub dictionary entry for a new move
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])] = {'Name':[], 'Number':[], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}                
                            #0)Adds Method to this set of moves:
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Method'].append(current_method)                
                            #1)Adds Number to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Number'].append(this_number)                
                            #2)Adds Move Name to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Name'].append(this_name)                
                            #3)Adds Move Type to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Type'].append(this_type)                
                            #4)Adds Move Mode to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Mode'].append(this_mode)                
                            #5)Adds Move Power to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Power'].append(this_power)                
                            #6)Adds Move Accuracy to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Accuracy'].append(this_accuracy)                
                            #7)Adds Move PP to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['PP'].append(this_pp)                        
                            #8)Adds Move Effect % to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Effect'].append(this_effect)                
                            #9)Adds Move Info to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Info'].append(this_info)                

                            #Moves move_counter to next iteration for current form
                            move_counter[current_form] = move_counter[current_form] + 1


            #Finding Egg Moves Title Line
            if '</a><h3>Egg Moves</h3>' in line:
                #Creates/Updates current_method and number_info variable to TMs
                current_method = 'Egg Moves' 

                #Starts a sub-loop through the lines until the end of the TRs block
                while 'Move Tutor Attacks<' not in line and 'Usable Max Moves' not in line and 'name="transfer"' not in line:

                    #Sets/resets individual_form_egg_move to 0:
                    #This variable is specially useful when different forms learn different egg moves
                    individual_form_egg_move = 0                

                    #Extracts move information using a loop of 8 lines for each move

                    #1)For the Move Name:
                    #Extracts Name
                    #For this first Egg Move
                    if 'egg.shtml">' in line:
                        this_name = line.split('egg.shtml">')[1].split('.shtml">')[1].split('<')[0]
                    #For following Egg Moves
                    if 'egg.shtml">' not in line:
          ####              ###print(line)
                        this_name = line.split('.shtml">')[1].split('<')[0]
                    #print(this_name)

                    #2)For the Move Type:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Type
                    this_type = line.split('/type/')[1].split('.gif')[0].capitalize()
                    #print(this_type)

                    #3)For the Move Mode:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Mode
                    this_mode = line.split('/type/')[1].split('.png')[0].capitalize()
                    #When it's a Status Move 
                    if this_mode == 'other' or this_mode == 'Other':
                        this_mode = 'Status'
                    #print(this_mode)

                    #4)For the Power:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Power
                    this_power = line.split('>')[1].split('<')[0]
                    #print(this_power)      

                    #5)For the Accuracy:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Accuracy
                    this_accuracy = line.split('>')[1].split('<')[0]
                    #print(this_accuracy)

                    #6)For the PP:
                    #Moves to next line
                    line = f.readline()
                    #Extracts PP
                    this_pp = line.split('>')[1].split('<')[0]
                    #print(this_pp)

                    #7)For the Effect %:
                    #Moves to next line
                    line = f.readline()
                    #Extracts Effect %
                    this_effect = line.split('>')[1].split('<')[0]
                    #print(this_effect)

                    #7.5)For individual FORM information
                    #Moves to next line (the 'Details' line)
                    line = f.readline()
                    #Checking if there is a .png for a FORM here, if so FORMS learn individual egg moves
                    if '.png"' in line:
                        #Sets individual_form_egg_move to 1
                        individual_form_egg_move = 1
                        #Extracts FORM info for current egg move
                        #Makes first split before the names of the forms
                        this_form_info = line.split('alt="')
                        #Removes initial text
                        this_form_info.pop(0)
                        #Creates/resets this_form_list
                        this_form_list = []
                        #Makes the second split to isolate form names and adds them to this_form_list
                        for form in this_form_info:
                            #Prepares form
                            form = form.split('"')[0].strip(' Form')
                            #Fixes the Alolan/Alola Form discrepancy
                            if form == 'Alolan':
                                form = 'Alola' #the shorter form will always work when using the in statement
                            #Adds form to list
                            this_form_list.append(form)
                        #print(this_form_list)         

                    #8)For the Info:
                    #Moves to next line (skipping the blank line)
                    line = f.readline()
                    #Moves to next line
                    line = f.readline()
                    #Extracts Info
                    if 'colspan="6">' in line:
                        this_info = line.split('colspan="6">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                    else: #when there is additional information besides move info (e.g. special requirement to learn egg move -> Pikachu)
                        this_info = line.split('">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")+' '+line.split('">')[2].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text   
                    #print(this_info)   

                    #Starts a loop to add move information to the dictitionary for the corresponding FORMS
                    #For individual form information
                    if individual_form_egg_move == 1:
                        #Starts loop through the forms in this_form_list
                        for current_form in this_form_list:                    
                            #Finding the corresponding form within the dictionary
                            #Creating/resetting helpful loop counter:
                            form_counter = 1

                            #When dealing with the Standard form  (assumes standard form to be Form1)
                            if current_form == 'Standard' or current_form == 'Normal':
                                form_counter = 1
                                #print('yes')
                                #print(form_counter)

                            #When not dealing with standard form
                            if current_form != 'Standard' and current_form != 'Normal':
                                #Starting loop
                                while current_form not in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                                    #When not a match, moves counter to next iteration
                                    form_counter = form_counter + 1
                                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                                #When a match, does nothing (this is only used for debugging)
                                #if current_form in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                                    #print('yes')
                                    #print(form_counter)                                    

                            #Adds move information to dictionary for current_form
                            #Sets up sub dictionary entry for a new move
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])] = {'Name':[], 'Number':['--'], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}                
                            #0)Adds Method to this set of moves:
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Method'].append(current_method)                
                            #1)Adds Move Name to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Name'].append(this_name)                
                            #2)Adds Move Type to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Type'].append(this_type)                
                            #3)Adds Move Mode to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Mode'].append(this_mode)                
                            #4)Adds Move Power to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Power'].append(this_power)                
                            #5)Adds Move Accuracy to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Accuracy'].append(this_accuracy)                
                            #6)Adds Move PP to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['PP'].append(this_pp)                        
                            #7)Adds Move Effect % to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Effect'].append(this_effect)                
                            #8)Adds Move Info to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Info'].append(this_info)                

                            #Moves move_counter to next iteration for current form
                            move_counter['Form'+str(form_counter)] = move_counter['Form'+str(form_counter)] + 1

                    #When there is no individual form information, we assume ALL FORMS can learn these moves
                    if individual_form_egg_move == 0:
                        #Loops through all the forms, one by one
                        for current_form in dex_pokemon['Forms']:
                            #Adds move information to dictionary for current_form
                            #Sets up sub dictionary entry for a new move
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])] = {'Name':[], 'Number':['--'], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}                
                            #0)Adds Method to this set of moves:
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Method'].append(current_method)                
                            #1)Adds Move Name to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Name'].append(this_name)                
                            #2)Adds Move Type to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Type'].append(this_type)                
                            #3)Adds Move Mode to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Mode'].append(this_mode)                
                            #4)Adds Move Power to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Power'].append(this_power)                
                            #5)Adds Move Accuracy to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Accuracy'].append(this_accuracy)                
                            #6)Adds Move PP to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['PP'].append(this_pp)                        
                            #7)Adds Move Effect % to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Effect'].append(this_effect)                
                            #8)Adds Move Info to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Info'].append(this_info)                

                            #Moves move_counter to next iteration for current form
                            move_counter[current_form] = move_counter[current_form] + 1


            #Finding Move Tutor Attacks Title Line
            if 'Move Tutor Attacks<' in line:
                #Creates/Updates current_method and number_info variable to TMs
                current_method = 'Move Tutor'

                #Checks if moves are separated by FORMS (e.g. differennt forms learn different moves)
                if 'attheader">Form' in line:
                    #Sets/resets individual_form_move_tutor to 1:
                    individual_form_move_tutor = 1
                else:
                    #Sets/resets individual_form_move_tutor to 0:
                    individual_form_move_tutor = 0

                #When moves are separated by FORMS, the information no longer comes in a single line
                if individual_form_move_tutor == 1:

                    #Starts a sub-loop through the lines until the end of the move tutor block
                    while 'Usable Max Moves' not in line and 'name="transfer"' not in line and '>Special Moves<' not in line:

                        #Extracts move information                    

                        #Splits the line right in front of move name
                        element = line.split('.shtml">')[1]

                        #1)For the Move Name:
                        #Extracts Name
                        this_name = element.split('</a></')[0]
                        #print(this_name)

                        #2)For the Move Type:
                        #Extracts Type
                        this_type = element.split('/type/')[1].split('.gif')[0].capitalize()
                        #print(this_type)

                        #3)For the Move Mode:
                        #Extracts Mode
                        this_mode = element.split('/type/')[2].split('.png')[0].capitalize()
                        #When it's a Status Move 
                        if this_mode == 'other' or this_mode == 'Other':
                            this_mode = 'Status'
                        #print(this_mode)

                        #4)For the Power:
                        #Extracts Power
                        this_power = element.split('"fooinfo">')[3].split('<')[0]
                        #print(this_power)

                        #5)For the Accuracy:
                        #Extracts Accuracy
                        this_accuracy = element.split('"fooinfo">')[4].split('<')[0]
                        #print(this_accuracy)

                        #6)For the PP:
                        #Extracts PP
                        this_pp = element.split('"fooinfo">')[5].split('<')[0]
                        #print(this_pp)

                        #7)For the Effect %:
                        #Extracts Effect %
                        this_effect = element.split('"fooinfo">')[6].split('<')[0]
                        #print(this_effect)

                        #7.5)For the FORM info
                        #Moves to next line
                        line = f.readline()
                        #print(line)
                        #Gets the FORM info part of the line
                        form_info_line = line.split('></table></')[0]
                        #Extracts FORM info
                        #Makes first split before the names of the forms
                        this_form_info = form_info_line.split('alt="')
                        #Removes initial text
                        this_form_info.pop(0)
                        #Creates/resets this_form_list
                        this_form_list = []
                        #Makes the second split to isolate form names and adds them to this_form_list
                        for form in this_form_info:
                            #Prepares form
                            form = form.split('"')[0].strip(' Form').replace(' Necrozma','')
                            #print(form)
                            #Fixes the Alolan/Alola Form discrepancy
                            if form == 'Alolan':
                                form = 'Alola' #the shorter form will always work when using the in statement
                            #Fixes the Standard replaced by Pokemon Name discrepancy
                            if form in dex_pokemon['Species'][0]:
                                form = 'Standard' #replacing the pokemon name with Standard makes the code more universal                        
                            #Adds form to list
                            this_form_list.append(form)
                        #print(this_form_list)                    

                        #8)For the Info:
                        #When the pokemon learns from 2 different move tutors, the line breaks into 2 after forms info
                        if '"fooinfo">' not in line:
                            #Moves to next line
                            line = f.readline()                        
                        #Extracts Info
                        this_info = line.split('"fooinfo">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                        #print(this_info)   

                        #Starts a loop to add move information to the dictitionary for the corresponding FORMS for individual form information
                        #Starts loop through the forms in this_form_list
                        for current_form in this_form_list:                    
                            #Finding the corresponding form within the dictionary
                            #Creating/resetting helpful loop counter:
                            form_counter = 1

                            #When dealing with the Standard form  (assumes standard form to be Form1)
                            if current_form == 'Standard' or current_form == 'Normal':
                                form_counter = 1
                                #print('yes')
                                #print(form_counter)

                            #When not dealing with standard form
                            if current_form != 'Standard' and current_form != 'Normal':
                                #Starting loop
                                while current_form not in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                                    #print(current_form)
                                    #When not a match, moves counter to next iteration
                                    form_counter = form_counter + 1
                                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                                #When a match, does nothing (this is only used for debugging)
                                #if current_form in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                                    #print('yes')
                                    #print(form_counter)                                    

                            #Adds move information to dictionary for current_form
                            #Sets up sub dictionary entry for a new move
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])] = {'Name':[], 'Number':['--'], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}                
                            #0)Adds Method to this set of moves:
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Method'].append(current_method)                
                            #1)Adds Move Name to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Name'].append(this_name)                
                            #2)Adds Move Type to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Type'].append(this_type)                
                            #3)Adds Move Mode to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Mode'].append(this_mode)                
                            #4)Adds Move Power to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Power'].append(this_power)                
                            #5)Adds Move Accuracy to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Accuracy'].append(this_accuracy)                
                            #6)Adds Move PP to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['PP'].append(this_pp)                        
                            #7)Adds Move Effect % to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Effect'].append(this_effect)                
                            #8)Adds Move Info to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Info'].append(this_info)                

                            #Moves move_counter to next iteration for current form
                            move_counter['Form'+str(form_counter)] = move_counter['Form'+str(form_counter)] + 1


                #When moves are not separated by FORMS, we assume ALL FORMS can leaarn the moves
                if individual_form_move_tutor == 0:

                    #Splits the line, first close to the Move Tutor title to avoid information from the following session (e.g. Max Moves, Special Moves for Rotom)
                    #second, right in front of move name to separate line by moves
                    split_line = line.split('">Attack Name</')[1].split('.shtml">')
                    #Deletes first element from the list
                    split_line.pop(0)

                    #Creates a loop to use all elements of split_line, except for element 0
                    for element in split_line:

                        #Extracts move information using line splitting

                        #1)For the Move Name:
                        #Extracts Name
                        this_name = element.split('</a></')[0]
                        #print(this_name)

                        #2)For the Move Type:
                        #Extracts Type
                        this_type = element.split('/type/')[1].split('.gif')[0].capitalize()
                        #print(this_type)

                        #3)For the Move Mode:
                        #Extracts Mode
                        this_mode = element.split('/type/')[2].split('.png')[0].capitalize()
                        #When it's a Status Move 
                        if this_mode == 'other' or this_mode == 'Other':
                            this_mode = 'Status'
                        #print(this_mode)

                        #4)For the Power:
                        #Extracts Power
                        this_power = element.split('"fooinfo">')[3].split('<')[0]
                        #print(this_power)

                        #5)For the Accuracy:
                        #Extracts Accuracy
                        this_accuracy = element.split('"fooinfo">')[4].split('<')[0]
                        #print(this_accuracy)

                        #6)For the PP:
                        #Extracts PP
                        this_pp = element.split('"fooinfo">')[5].split('<')[0]
                        #print(this_pp)

                        #7)For the Effect %:
                        #Extracts Effect %
                        this_effect = element.split('"fooinfo">')[6].split('<')[0]
                        #print(this_effect)

                        #8)For the Info:
                        #Extracts Info
                        this_info = element.split('"fooinfo">')[7].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                        #print(this_info)   

                        #Loops through all the forms, one by one
                        for current_form in dex_pokemon['Forms']:
                            #Adds move information to dictionary for current_form
                            #Sets up sub dictionary entry for a new move
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])] = {'Name':[], 'Number':['--'], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}                
                            #0)Adds Method to this set of moves:
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Method'].append(current_method)                
                            #1)Adds Move Name to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Name'].append(this_name)                
                            #2)Adds Move Type to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Type'].append(this_type)                
                            #3)Adds Move Mode to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Mode'].append(this_mode)                
                            #4)Adds Move Power to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Power'].append(this_power)                
                            #5)Adds Move Accuracy to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Accuracy'].append(this_accuracy)                
                            #6)Adds Move PP to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['PP'].append(this_pp)                        
                            #7)Adds Move Effect % to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Effect'].append(this_effect)                
                            #8)Adds Move Info to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Info'].append(this_info)                

                            #Moves move_counter to next iteration for current form
                            move_counter[current_form] = move_counter[current_form] + 1

        ##################### STOPPED HERE!!! #Special Moves for Rotom is done!!!

            #Finding Special Moves Title Line
            if '="fooevo">Special Moves<' in line and '"legendsattacks"' not in line and '>Move Shop Attacks<' not in line:
                #Creates/Updates current_method and number_info variable to TMs
                current_method = 'Special Moves'

                #Checks if moves are separated by FORMS (e.g. differennt forms learn different moves)
                if '90">Form<' in line:
                    #Sets/resets individual_form_special_moves to 1:
                    individual_form_special_moves = 1
                else:
                    #Sets/resets individual_form_special_moves to 0:
                    individual_form_special_moves = 0

                #When moves are separated by FORMS, the information no longer comes in a single line
                if individual_form_special_moves == 1:

                    #Splits the line, first right at the Special Moves title to avoid information from the session before 
                    line = line.split('="fooevo">Special Moves<')[1]

                    #Starts a sub-loop through the lines until the end of the move tutor block
                    while 'Usable Max Moves' not in line and 'name="transfer"' not in line and 'name="stats"' not in line:

                        #Extracts move information                  

                        #Splits the line, right in front of move name to start from the move name
                        #print(line)
                        element = line.split('.shtml">')[1]
                        #print(element)

                        #1)For the Move Name:
                        #Extracts Name
                        this_name = element.split('</a></')[0]
                        #print(this_name)

                        #2)For the Move Type:
                        #Extracts Type
                        this_type = element.split('/type/')[1].split('.gif')[0].capitalize()
                        #print(this_type)

                        #3)For the Move Mode:
                        #Extracts Mode
                        this_mode = element.split('/type/')[2].split('.png')[0].capitalize()
                        #When it's a Status Move 
                        if this_mode == 'other' or this_mode == 'Other':
                            this_mode = 'Status'
                        #print(this_mode)

                        #4)For the Power:
                        #Extracts Power
                        this_power = element.split('"fooinfo">')[3].split('<')[0]
                        #print(this_power)

                        #5)For the Accuracy:
                        #Extracts Accuracy
                        this_accuracy = element.split('"fooinfo">')[4].split('<')[0]
                        #print(this_accuracy)

                        #6)For the PP:
                        #Extracts PP
                        this_pp = element.split('"fooinfo">')[5].split('<')[0]
                        #print(this_pp)

                        #7)For the Effect %:
                        #Extracts Effect %
                        this_effect = element.split('"fooinfo">')[6].split('<')[0]
                        #print(this_effect)

                        #7.5)For the FORM info
                        #Moves to next line
                        line = f.readline()
                        #print(line)
                        #Gets the FORM info part of the line
                        form_info_line = line.split('.</td><td')[0]
                        #Extracts FORM info
                        #Makes first split before the names of the forms
                        this_form_info = form_info_line.split('alt="')
                        #Removes initial text
                        this_form_info.pop(0)
                        #Creates/resets this_form_list
                        this_form_list = []
                        #Makes the second split to isolate form names and adds them to this_form_list
                        for form in this_form_info:
                            #Prepares form
                            form = form.split('"')[0]
                            #If the word Form is in the form name text (e.g. Rotom is not using the word Form after the form names)
                            if 'Form' in form:
                                form = form.strip(' Form')
                            #Removes the word Rotom from Rotom Form names to facilitate for the program
                            if 'Rotom' in form:
                                form = form.replace(' Rotom','')
                            #Fixes the Alolan/Alola Form discrepancy
                            if form == 'Alolan':
                                form = 'Alola' #the shorter form will always work when using the in statement
                            #Fixes the Standard replaced by Pokemon Name discrepancy
                            if form == dex_pokemon['Species'][0]:
                                form = 'Standard' #replacing the pokemon name with Standard makes the code more universal                        
                            #Adds form to list
                            this_form_list.append(form)
                        #print(this_form_list)                    

                        #8)For the Info:
                        #When the pokemon learns from 2 different move tutors, the line breaks into 2 after forms info
                        if '"fooinfo">' not in line:
                            #Moves to next line
                            line = f.readline()                        
                        #Extracts Info
                        this_info = line.split('"fooinfo">')[1].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                        #print(this_info)

                        #Starts a loop to add move information to the dictitionary for the corresponding FORMS for individual form information
                        #Starts loop through the forms in this_form_list
                        for current_form in this_form_list:  
                            #print(current_form)
                            #Finding the corresponding form within the dictionary
                            #Creating/resetting helpful loop counter:
                            form_counter = 1
                            
                            #Fixing Zamazentas Form name glitch 
                            #(using the word Crowned only is a simple solution, since it's part of the correct form name)
                            if 'Crowned' in current_form:
                                current_form = 'Crowned'

                            #When dealing with the Standard form  (assumes standard form to be Form1)
                            if current_form == 'Standard' or current_form == 'Normal':
                                form_counter = 1
                                #print('yes')
                                #print(form_counter)

                            #When not dealing with standard form
                            if current_form != 'Standard' and current_form != 'Normal':
                                #Starting loop
                                while current_form not in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                                    #When not a match, moves counter to next iteration
                                    form_counter = form_counter + 1
                                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                                #When a match, does nothing (this is only used for debugging)
                                #if current_form in dex_pokemon['Forms']['Form'+str(form_counter)]['Name']:
                                    #print(dex_pokemon['Forms']['Form'+str(form_counter)]['Name'])
                                    #print('yes')
                                    #print(form_counter)
                                    #print(move_counter['Form'+str(form_counter)])


                            #Adds move information to dictionary for current_form
                            #Sets up sub dictionary entry for a new move
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])] = {'Name':[], 'Number':['--'], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}                
                            #0)Adds Method to this set of moves:
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Method'].append(current_method)                
                            #1)Adds Move Name to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Name'].append(this_name)                
                            #2)Adds Move Type to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Type'].append(this_type)                
                            #3)Adds Move Mode to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Mode'].append(this_mode)                
                            #4)Adds Move Power to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Power'].append(this_power)                
                            #5)Adds Move Accuracy to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Accuracy'].append(this_accuracy)                
                            #6)Adds Move PP to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['PP'].append(this_pp)                        
                            #7)Adds Move Effect % to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Effect'].append(this_effect)                
                            #8)Adds Move Info to current form
                            dex_pokemon['Forms']['Form'+str(form_counter)]['Moves']['Move'+str(move_counter['Form'+str(form_counter)])]['Info'].append(this_info)                

                            #Moves move_counter to next iteration for current form
                            move_counter['Form'+str(form_counter)] = move_counter['Form'+str(form_counter)] + 1



                #When moves are not separated by FORMS, we assume ALL FORMS can leaarn the moves
                if individual_form_special_moves == 0:

                    #Splits the line, first close to the Move Tutor title to avoid information from the following session (e.g. Max Moves, Special Moves for Rotom)
                    #second, right in front of move name to separate line by moves
                    split_line = line.split('">Attack Name</')[1].split('.shtml">')
                    #Deletes first element from the list
                    split_line.pop(0)

                    #Creates a loop to use all elements of split_line, except for element 0
                    for element in split_line:

                        #Extracts move information using line splitting

                        #1)For the Move Name:
                        #Extracts Name
                        this_name = element.split('</a></')[0]
                        #print(this_name)

                        #2)For the Move Type:
                        #Extracts Type
                        this_type = element.split('/type/')[1].split('.gif')[0].capitalize()
                        #print(this_type)

                        #3)For the Move Mode:
                        #Extracts Mode
                        this_mode = element.split('/type/')[2].split('.png')[0].capitalize()
                        #When it's a Status Move 
                        if this_mode == 'other' or this_mode == 'Other':
                            this_mode = 'Status'
                        #print(this_mode)

                        #4)For the Power:
                        #Extracts Power
                        this_power = element.split('"fooinfo">')[3].split('<')[0]
                        #print(this_power)

                        #5)For the Accuracy:
                        #Extracts Accuracy
                        this_accuracy = element.split('"fooinfo">')[4].split('<')[0]
                        #print(this_accuracy)

                        #6)For the PP:
                        #Extracts PP
                        this_pp = element.split('"fooinfo">')[5].split('<')[0]
                        #print(this_pp)

                        #7)For the Effect %:
                        #Extracts Effect %
                        this_effect = element.split('"fooinfo">')[6].split('<')[0]
                        #print(this_effect)

                        #8)For the Info:
                        #Extracts Info
                        this_info = element.split('"fooinfo">')[7].split('<')[0].replace('Pok&eacute;mon','Pokemon').replace('&#x2019;',"'")  #fixes bug with the text
                        #print(this_info)   

                        #Loops through all the forms, one by one
                        for current_form in dex_pokemon['Forms']:
                            #Adds move information to dictionary for current_form
                            #Sets up sub dictionary entry for a new move
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])] = {'Name':[], 'Number':['--'], 'Type':[], 'Mode':[], 'Power':[], 'Accuracy':[], 'Effect':[], 'PP':[], 'Method':[], 'Info':[]}                
                            #0)Adds Method to this set of moves:
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Method'].append(current_method)                
                            #1)Adds Move Name to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Name'].append(this_name)                
                            #2)Adds Move Type to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Type'].append(this_type)                
                            #3)Adds Move Mode to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Mode'].append(this_mode)                
                            #4)Adds Move Power to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Power'].append(this_power)                
                            #5)Adds Move Accuracy to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Accuracy'].append(this_accuracy)                
                            #6)Adds Move PP to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['PP'].append(this_pp)                        
                            #7)Adds Move Effect % to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Effect'].append(this_effect)                
                            #8)Adds Move Info to current form
                            dex_pokemon['Forms'][current_form]['Moves']['Move'+str(move_counter[current_form])]['Info'].append(this_info)                

                            #Moves move_counter to next iteration for current form
                            move_counter[current_form] = move_counter[current_form] + 1




        #####################


    #Final check to make sure ALL FORMS have assigned abilities
    #This is very important for when MULTIPLE FORMS share the same abilities and the abilities are only stated once (e.g. Darmanitan and Rotom)
    #Creates/resets helpful form counter
    counter_forms_abilities = 1
    #Starts to loop through dictionary
    while counter_forms_abilities <= len(dex_pokemon['Forms']):
        #Checks if ability name entry is empty
        if dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Name'] == []:
            #If the entry is empty for current FORM, copies information from the previous FORM (assumes abilities to be the same between the two FORMS)
            dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Name'] = dex_pokemon['Forms']['Form'+str(counter_forms_abilities-1)]['Ability']['Name']
            dex_pokemon['Forms']['Form'+str(counter_forms_abilities)]['Ability']['Info'] = dex_pokemon['Forms']['Form'+str(counter_forms_abilities-1)]['Ability']['Info']

        #Moves to next iteration
        counter_forms_abilities = counter_forms_abilities + 1    

    #Closes dex entry txt file
    f.close()
    #Returns dictionary
    return dex_pokemon