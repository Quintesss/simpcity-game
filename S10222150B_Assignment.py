#S10222150B - Wong Qi Yuan - P09

import random
import time

#function to give 2 random buildings
def rand_building():
    random_buildings = [random.randint(0,5),random.randint(0,5)]
    list_of_build = ["HSE","FAC","SHP","HWY","BCH","MON"]
    for building in range(len(random_buildings)):
        random_buildings[building] = list_of_build[random_buildings[building]]

    return random_buildings

#creates empty map layout in the form of a list
def empty_map():
    mapping = []
    for r in range(row):
        temp = []
        for c in range(column):
            temp.append("")
        mapping.append(temp)
    return mapping

#print map (each line is saved as an element in the strings <display_list> and <display_list2> then printed using a for loop)
def show_map(display):
    display_list=[]
    #print ABC...
    temp_display ="   "  #print("   ",end="")
    for x in range(len(display[0])):
        temp_display += "{:^5} ".format(chr(65+x)) #print("{:^5} ".format(chr(65+x)),end="")
    display_list.append(temp_display) #print()
    
    #prints non-hardcode +----+
    temp_display="  +" #print("  +",end="")
    for x in range(len(display[0])):
        temp_display+="{:-^5}+".format("") #print("{:-^5}".format(""),end="+")
    display_list.append(temp_display) #print()

    #prints the map
    count=1
    for x in display:
        temp_display=""
        temp_display+=" {}|".format(count) #print(" {}|".format(count),end = "")
        for n in x:
            temp_display+="{:^5}|".format(n) #print("{:^5}|".format(n), end="")
        display_list.append(temp_display) #print()
        count+=1
        #prints non-hardcode +----+
        temp_display="  +" #print("  +",end="")
        for x in range(len(display[0])):
            temp_display+="{:-^5}+".format("") #print("{:-^5}".format(""),end="+")
        display_list.append(temp_display) #print()
    #"prints" remaining buildings
    display_list2=[]
    display_list2.append("{}{:<11}{}".format("Building","","Remaining")) #print("{}{:<11}{}".format("Building","","Remaining"))
    display_list2.append("{:-^8}{:<11}{:-^9}".format("","","")) #print("{:-^8}{:<11}{:-^9}".format("","",""))
    for building in buildings_left:
        display_list2.append("{:<8}{:<11}{:<9}".format(building,"",buildings_left[building])) #print("{:<8}{:<11}{:<9}".format(building,"",buildings_left[building]))   
    if len(display_list2) > len(display_list):
        for x in range(len(display_list2)):
            try:
                print("{}     {}".format(display_list[x],display_list2[x]))
            except:
                print("{}     {}".format(" "*len(display_list[1]),display_list2[x]))        
    else:
        for x in range(len(display_list)):
            try:
                print("{}     {}".format(display_list[x],display_list2[x]))
            except:
                print(display_list[x])

#Save progress
def save():
    datafile = open("game_load_file.txt","w")
    datafile.write("{}\n{}".format(str(mapping),str(buildings_left)))
    datafile.close()
    print("Game saved!")

#determine which turn it is (esp. if from save file)
def check_turn(board):
    temp2=0
    for r in board:
        temp = r.count("")
        temp2+=temp
    return (row*column - temp2)

#update building quantity
def building_update(a_list,a_dict):
    for building in a_list:
        a_dict[building] = a_dict.get(building) - 1
    return a_dict

#print in-game menu
def print_menu():
    print("1. Build a {}".format(building_list[0]))
    print("2. Build a {}".format(building_list[1]))
    print("3. See current score")
    print()
    print("4. Save game")
    print("0. Exit to main menu")

#checks grid
def check_left(r,c):
    try:
        if c==0:
            return ""
        else:
            return mapping[r][c-1]
    except: #addresses if the grid is beside a "wall"
        return ""
def check_right(r,c):
    try:
        return mapping[r][c+1]
    except:
        return ""
def check_up(r,c):
    try:
        if r==0:
            return ""
        else:
            return mapping[r-1][c]
    except:
        return ""
def check_down(r,c):
    try:
        return mapping[r+1][c]
    except:
        return ""
def check_grid(r,c):
    return mapping[r][c] == ""

#calculate score (returns a list to be summed)
def cal_bch(): # checks for beach, then checks if it's on either column A or D
    bch_score=[]
    for r in mapping:
        for c in range(len(r)):
            x=0
            if r[c] == "BCH":
                x+=1
                if c==0 or c==(len(r)-1):
                    x+=2
                bch_score.append(x)
    if bch_score==[]:
        return [0]
    else:
        return bch_score

def cal_fac(): #gets number of factories, then checks quantity to give score
    fac_score=[]
    for r in mapping:
        for c in range(len(r)):
            if r[c] == "FAC":
                fac_score.append(1)
    if fac_score==[]:
        return [0]
    elif len(fac_score)>3: #doesn't matter if it's 3/4
        for x in range(4):
            fac_score[x] = 4
        return fac_score
    else:
        for x in range(len(fac_score)):
            fac_score[x]= len(fac_score)
        return fac_score

def cal_hse():
    hse_score=[]
    for r in range(len(mapping)):
        for c in range(len(mapping[r])):
            if mapping[r][c] == "HSE":
                surr_building = [check_up(r,c),check_down(r,c),check_left(r,c),check_right(r,c)] #saves surrounding buildings as a list
                if "FAC" in surr_building:
                    x=1
                else:
                    x=0
                    x+= surr_building.count("SHP")
                    x+= surr_building.count("HSE")
                    x+= (surr_building.count("BCH"))*2
                hse_score.append(x)
    if hse_score== []:
        return [0]
    else:
        return hse_score

def cal_shp():
    shp_score=[]
    for r in range(len(mapping)):
        for c in range(len(mapping[r])):
            if mapping[r][c] == "SHP":
                surr_building = set([check_up(r,c),check_down(r,c),check_left(r,c),check_right(r,c)]) #removes duplicates
                surr_building.discard("") #removes empty if any
                x = len(surr_building)
                shp_score.append(x)
    if shp_score== []:
        return [0]
    else:
        return shp_score

def cal_hwy():
    hwy_score=[] 
    for r in range(len(mapping)): 
        count = 0
        for c in range(len(mapping[r])): #keeps counting until either the right is not a hwy or it's the end of the row
            if mapping[r][c] == "HWY":
                count+=1
                if check_right(r,c) == "HWY": #check if the right is hwy
                    continue
                else:
                    for x in range(count):
                        hwy_score.append(1*count)
                    count = 0
    if 0 in hwy_score:
        for x in hwy_score:
            if x == 0:
                hwy_score.remove(x)
    if hwy_score==[]:
        return [0]
    else:
        return hwy_score

def cal_mon():
    mon_score=[]
    corner=0 #counting corner MONs
    if mapping[0][0] == "MON":
        corner += 1    
    if mapping[0][-1] == "MON":
        corner += 1    
    if mapping[-1][0] == "MON":
        corner += 1    
    if mapping[-1][-1] == "MON":
        corner += 1  
    if corner >2: #if 3 or more corner MONs, all MONs = 4
        for r in range(len(mapping)):
            for c in range(len(mapping[r])):
                if mapping[r][c] == "MON":
                    mon_score.append(4)
    else: #give corner MONs = 2 and other MONs =1
        for r in range(len(mapping)):
            for c in range(len(mapping[r])):
                if mapping[r][c] == "MON":
                    if (r == 0 or r == len(mapping)-1) and (c == 0 or c == len(mapping[r])-1):
                        mon_score.append(2)
                    else:
                        mon_score.append(1)
    if mon_score == []:
        return [0]
    else:
        return mon_score
        
def print_score(score_list): #formatting to print <1+2+1+...>
    printable=""
    for x in score_list:
        printable += " {} +".format(str(x))
    printable = printable.rstrip("+")
    print("{} = {}".format(printable,sum(score_list)))

def show_fullscore(): #full display of score
    print("HSE: ",end="")
    print_score(cal_hse())
    print("FAC: ",end="")
    print_score(cal_fac())
    print("SHP: ",end="")
    print_score(cal_shp())
    print("HWY: ",end="")
    print_score(cal_hwy())
    print("BCH: ",end="")
    print_score(cal_bch())
    print("MON: ",end="")
    print_score(cal_mon())                
    print("Total score: {}".format(str(sum(cal_hse())+sum(cal_fac())+sum(cal_shp())+sum(cal_hwy())+sum(cal_bch())+sum(cal_mon()))))                                                               
    print()    

def show_leaderboard(leaderboards): #take a list to display leaderboard
    if leaderboards == []:
        print("No High Score found.")    
    else:
        print("{:-^31}".format(" HIGH SCORES "))
        print("{:>3} {:<22}{:>5}".format("Pos","Player","Score"))
        print("{:-^3} {:-^6}{:>15}{:-^5}".format("","","",""))
        for player_num in range(len(leaderboards)):
            print("{:>2}.{:<22}{:>5}".format(str(player_num+1),(leaderboards[player_num][0]),str(leaderboards[player_num][1])))
        print("{:-^31}".format(""))
    print()
    time.sleep(1)

def get_leaderboards(): #determine which file to get leaderboards from
    score_file_name = "{}x{}leaderboards.txt".format(row,column)
    try:
        score_file= open(score_file_name,"r")
        leaderboard = eval(score_file.readline()) #file will contain a list in string form. This converts it to a list.
        score_file.close()
        return leaderboard
    except: #if file doesn't exist
        return []

def save_leaderboards(leaderboards):
    score_file_name = "{}x{}leaderboards.txt".format(row,column)
    score_file= open(score_file_name,"w")
    score_file.write(str(leaderboards)) #saves the list as a string
    score_file.close()


#start menu
while True:
    print("Welcome, mayor of Simp City!")
    print("{:-^28}".format(""))
    print("1. Start new game\n2. Load saved game\n3. Show high scores\n\n0. Exit")
    try:
        option = int(input("Your choice? "))
    except:
        print()
        print("Invalid Input!")
        continue
    print()
    if option not in range(4):
        print("Invalid Input!")
        continue
    if option == 0:
        break
    elif option == 1:
        while True:
            try:
                print("Map layout\n\n1. Default (Saveable)\n2. Custom")
                choose_map = int(input("Your choice? ")) #lets user to choose grid size
                if choose_map == 1:
                    row = 4
                    column = 4
                    break
                elif choose_map == 2:
                    row_check = int(input("Please enter number of rows: "))
                    colum_check = int(input("Please enter number of column: "))
                    if row_check < 1 or row_check > 26 or colum_check < 1 or colum_check > 26:
                        print("Map size unavailable")
                        continue
                    else:
                        row = row_check
                        column = colum_check
                        break
            except:
                print("Invalid Input!")
                continue
        mapping = empty_map()
        if (row*column) % 2 !=0: #check odd (impt for 1x1 grids)
            building_start_quantity = int(row * column /2) + 1
        else:
            building_start_quantity = int(row * column /2)
        buildings_left = {"HSE":building_start_quantity,"FAC":building_start_quantity,"SHP":building_start_quantity,"HWY":building_start_quantity,"BCH":building_start_quantity,"MON":building_start_quantity} #dictionary for building quantity
    elif option == 2:
        row =4
        column=4
        datafile  = open("game_load_file.txt","r")
        mapping = eval(datafile.readline()) #reads the file as a string, then converts it into a list using eval()
        buildings_left = eval(datafile.readline())
        datafile.close()
        print("Game Loaded!")
    elif option == 3:
        while True:
            try:
                row_check = int(input("Please enter number of rows: "))
                colum_check = int(input("Please enter number of column: "))
                if row_check > 26 or colum_check > 26:
                    print("Map size unavailable")
                    continue
                else:
                    row = row_check
                    column = colum_check
                    break   
            except:
                print("Invalid Input!")
                continue                    
        leaderboard = get_leaderboards()
        show_leaderboard(leaderboard)
        continue
        
    turn = check_turn(mapping)
    #game starts
    while turn < row*column:
        turn+=1

        while True:
            building_list = rand_building()
            if buildings_left[building_list[0]] > 0 and buildings_left[building_list[1]] > 0:
                break

        while True:
            print("Turn {}".format(turn))
            show_map(mapping)            
            print_menu()
            try:
                option = int(input("Your choice? "))
            except:
                print("Invalid Input!")
                continue    
            print()
            if option not in range(5):
                print("Invalid Input!")
                continue

            if option== 3:
                show_fullscore()
                time.sleep(1)

            elif option==4:
                if row == 4 and column == 4:
                    save()
                else:
                    print("Save unavailable")
            else:
                break

        if option ==0:
            break    
        elif option == 1 or 2:
            while True:
                placement = input("Build where? ")
                placement = [x for x in placement]
                try:
                    placement[0] = ord(placement[0].lower()) -97
                    placement[1] = int(placement[1])-1
                    if (turn == 1) or (check_grid(placement[1],placement[0]) and (check_up(placement[1],placement[0]) != "" or check_down(placement[1],placement[0])!= "" or check_left(placement[1],placement[0])!= "" or check_right(placement[1],placement[0])!= "")): #check if placement is a valid move
                        buildings_left = building_update(building_list,buildings_left)                
                        mapping[placement[1]][placement[0]] = building_list[option-1]
                        break
                    else:
                        print("Illegal placement, pick another grid!")
                except:
                    print("Illegal placement, pick another grid!")
        if turn == row*column:
            print()
            print("Final layout of Simp City:")
            show_map(mapping)
            show_fullscore()
            leaderboard = get_leaderboards()
            final_score=sum(cal_hse())+sum(cal_fac())+sum(cal_shp())+sum(cal_hwy())+sum(cal_bch())+sum(cal_mon())
            if leaderboard == []: #if leaderboard is empty
                print("Congratulations! You made the high score board at position 1!")
                while True:
                    name= input("Please enter your name (max 20 chars): ")
                    print()
                    if len(name) <= 20:
                        break
                leaderboard.insert(1,[name,final_score])
                show_leaderboard(leaderboard)
                save_leaderboards(leaderboard)    
            elif final_score>leaderboard[-1][1]: #if score is in the middle of other scores
                for player_num in range(len(leaderboard)):
                    if final_score>leaderboard[player_num][1]:
                        print("Congratulations! You made the high score board at position {}!".format(str(player_num+1)))
                        while True:
                            name= input("Please enter your name (max 20 chars): ")
                            print()
                            if len(name) <= 20:
                                break                            
                        leaderboard.insert(player_num,[name,final_score])
                        if len(leaderboard)>10: #deletes the last score if leaderboard is full
                            leaderboard.pop()
                        show_leaderboard(leaderboard)
                        save_leaderboards(leaderboard)
                        break
            elif len(leaderboard) < 10: #if score is last but leaderboard still have positions to fill
                print("Congratulations! You made the high score board at position {}!".format(str(len(leaderboard)+1)))
                while True:
                    name= input("Please enter your name (max 20 chars): ")
                    print()
                    if len(name) <= 20:
                        break
                leaderboard.insert(len(leaderboard)+1,[name,final_score]) #updates leaderboards
                show_leaderboard(leaderboard)
                save_leaderboards(leaderboard)                

