import subprocess as sp
import pymysql
# import pymysql.cursor
# import pymysql.connector


# delete players with player id
def deletePlayer(cursor):
    id=input("Give the Player id: ")
    info = cursor.execute("delete from Players where Player_ID="+id)
    info = cursor.fetchall()
    print("deleted:",info)
    return info
    
# delete team with a team id
def deleteTeam(cursor):
    id=input("Give the Team id: ")
    info = cursor.execute("delete from Team where Team_ID="+id)
    info = cursor.fetchall()
    
    print("deleted:",info)
    return info

# select all players with victory>n
def selectPlayer(cursor):
    n=input("How many Victories: ")
    info=cursor.execute("Select * from (Players join Player_Stats on Players.Player_ID=Player_Stats.Player_ID) Where No_of_Matches_won_singles + No_of_Matches_won_doubles >"+n)
    info = cursor.fetchall()
    for ini in info:
        for ab in ini:
            print(ab,':',ini[ab])
        print()
    return info

# select all teams in a league
def selectTeam(cursor):
    n=input("League ID: ")
    info=cursor.execute("Select * from (Team join Plays_in on Team.Team_ID=Plays_in.Team_ID) Where League_ID ="+n)
    info = cursor.fetchall()
    for ini in info:
        for ab in ini:
            print(ab,':',ini[ab])
        print()
        
    return info

#select city location from stadium
def stadiumCity(cursor):
    info=cursor.execute("Select Name,City from Stadium")
    info = cursor.fetchall()
    for ini in info:
        for ab in ini:
            print(ab,':',ini[ab])
        print()
        
    # for ini in info:
    #     print(ini)
    return info
    
def insertTeam(cursor):
    # Team_id=int(input("Enter Team Id: "))
    Team_name =input("Enter Team Name: ")
    format=input("Enter format: ")
    no_of_Matches_Played='0'
    no_of_Players='0'
    head_coach=input("Enter the Headcoach's name: ")
    no_of_Wins='0'
    comm=f"INSERT INTO Team (Team_Name, Format, No_of_Matches_Played, No_of_Players, Head_Coach, No_of_Wins) VALUES ('{Team_name}', '{format}', '{no_of_Matches_Played}', '{no_of_Players}', '{head_coach}', '{no_of_Wins}');"
    cursor.execute(comm)
    cursor.fetchall()
    comm = "SELECT Team_ID FROM Team where Team_Name = %s and Format = %s and No_of_Matches_Played = %s and No_of_Players = %s and Head_Coach = %s and No_of_Wins = %s"
    values=(Team_name,format,no_of_Matches_Played,no_of_Players,head_coach,no_of_Wins)
    cursor.execute(comm,values)
    index= cursor.fetchall()
    Team_ID=index[0]['Team_ID']
    # print(Team_ID)
    print(f"Team Created with Team Id {Team_ID}")
    return cursor.fetchall()

def insertPlayer(cursor):
    # play_id=int(input("Enter Player Id"))
    play_f=input("First name: ")
    play_m=input("Middle name: ")
    play_l=input("Last name: ")
    dob=input("DOB: ")
    gender=input("Gender: ")
    country=input("Country: ")
    handed=input("Handed: ")
    # comm = f"INSERT INTO Players (Player_ID, First_Name, Middle_Name, Last_Name, DOB, Gender, Country, Handedness) VALUES ({play_id}, {play_f}, {play_m}, {play_l}, {dob}, {gender}, {country}, {handed})"
    comm = "INSERT INTO Players (First_Name, Middle_Name, Last_Name, DOB, Gender, Country, Handedness) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (play_f, play_m, play_l, dob, gender, country, handed)
    cursor.execute(comm, values)
    comm = "SELECT Player_ID FROM Players where First_Name = %s and Middle_Name = %s and Last_Name = %s and DOB = %s and Gender = %s and Country = %s and Handedness = %s"
    cursor.fetchall()
    cursor.execute(comm,values)
    index= cursor.fetchall()
    play_id=index[0]['Player_ID']
    # print(play_id)
    print(f"Player created with Player id {play_id}")
    return cursor.fetchall()

def nameTeam(cursor):
    id=input("Write Team id: ")
    info=cursor.execute("select Player_ID from Belongs_To where Team_ID="+id)
    info=cursor.fetchall()
    for ini in info:
        for ab in ini:
            print(ab,':',ini[ab])
        print()
    
def addTeam(cursor):
    player_id=int(input("Player id: "))
    team_id=int(input("Team id: "))
    entriescount=0
    info=cursor.execute(f"Insert into Belongs_To values ({player_id},{team_id});")
    info=cursor.fetchall()
    info=cursor.execute(f"Update Team SET No_of_Players=No_of_Players+1 where Team_ID={team_id};")
    info=cursor.fetchall()
    return info
    

def insertLeague(cursor):
    # League_id=int(input("Enter League Id: "))
    League_name =input("Enter League Name: ")
    Date_of_begin=input("Date of Beginning: ")
    Date_of_comp=input("Date of Completion: ")
    Scheduling_Format=input("Scheduling Format: ")
    Host_Country=input("Enter the Host Country: ")
    comm=f"INSERT INTO League (League_Name, Date_of_begin, Date_of_comp, Scheduling_Format, Host_Country) VALUES ('{League_name}', '{Date_of_begin}', '{Date_of_comp}', '{Scheduling_Format}', '{Host_Country}');"
    cursor.execute(comm)
    info = cursor.fetchall()
    # print(info)
    comm="SELECT League_ID FROM League where League_Name= %s and Date_of_begin = %s and Date_of_comp = %s and Scheduling_Format = %s and Host_Country = %s"
    values = (League_name,Date_of_begin,Date_of_comp,Scheduling_Format,Host_Country)
    cursor.execute(comm,values)
    index= cursor.fetchall()
    # print(index)
    League_id=index[0]['League_ID']
    print(f"Created League with ID = {League_id}")
    
    Format = input("Formats: ")
    Formats = (Format.strip()).split()
    for format in Formats:
        comm=f"INSERT INTO League_Format (League_ID, Format) VALUES ({League_id}, '{format}');"
        cursor.execute(comm)
    return cursor.fetchall()

def scoreline(cursor):
    match_id = int(input("Match ID: "))
    ref_id = int(input("Referee ID:"))
    score1 = input("Enter Score1: ")
    score2 = input("Enter Score2: ")
    # cursor.fetchall()
    team_id = cursor.execute(f"SELECT Team_1_ID from Matches where Match_ID = {match_id};")
    team_id = cursor.fetchall()
    # print(team_id)
    team1_id = team_id[0]['Team_1_ID']
    team_id = cursor.execute(f"SELECT Team_2_ID from Matches where Match_ID = {match_id};")
    team_id = cursor.fetchall()
    team2_id = team_id[0]['Team_2_ID']
    forming=cursor.execute(f"SELECT Format from Matches where Match_ID = {match_id};")
    forming=cursor.fetchall()
    form = forming[0]['Format']


    comm = f"UPDATE Matches SET Team_1_Score = {score1}, Team_2_Score = {score2} WHERE Matches.Match_ID = {match_id};"
    cursor.execute(comm)
    if score1 > score2 :
        winner = 1
        comm = f"UPDATE Team SET No_of_Wins = No_of_Wins + 1, No_of_Matches_Played = No_of_Matches_Played+1 WHERE Team.Team_ID = {team1_id};"
        cursor.execute(comm)
        comm = f"UPDATE Team SET No_of_Wins = No_of_Wins, No_of_Matches_Played = No_of_Matches_Played+1 WHERE Team.Team_ID = {team2_id};"

    elif score1 < score2 :
        winner = 2
        comm = f"UPDATE Team SET No_of_Wins = No_of_Wins + 1, No_of_Matches_Played = No_of_Matches_Played+1 WHERE Team.Team_ID = {team2_id};"
        # print("Waah")
        cursor.execute(comm)
        comm = f"UPDATE Team SET No_of_Wins = No_of_Wins, No_of_Matches_Played = No_of_Matches_Played+1 WHERE Team.Team_ID = {team1_id};"

    else :
        winner = 0
        comm = f"UPDATE Team SET No_of_Matches_Played = No_of_Matches_Played+1 WHERE Team.Team_ID = {team2_id} or Team.Team_ID = {team1_id};"
    
    # print("finally")
    cursor.execute(comm)
    comm = f"UPDATE Referees SET Experience = Experience + 1 WHERE Referee_ID = {ref_id};"
    cursor.execute(comm)
    comm = f"INSERT INTO Refs (Referee_ID,Match_ID) VALUES ({ref_id},{match_id});"
    cursor.execute(comm)
    cursor.fetchall()
    comm = f"SELECT Player_ID FROM Belongs_To WHERE Team_ID = {team1_id};"
    cursor.execute(comm)
    # val = f"SELECT * FROM Player_Stats;"
    play_id = 0
    info = cursor.fetchall()
    # print(info)
    
    for i in info :
        for x in i :
            play_id = i[x]
            # print(play_id)
            if form == "Singles" :
                var = f"UPDATE Player_Stats SET No_of_Matches_played_singles = No_of_Matches_played_singles + 1 WHERE Player_ID = {play_id};"
                cursor.execute(var)
                if winner == 1: 
                    var = f"UPDATE Player_Stats SET No_of_Matches_won_singles = No_of_Matches_won_singles + 1 WHERE Player_ID = {play_id};"
                    cursor.execute(var)
                
            else:
                var = f"UPDATE Player_Stats SET No_of_Matches_played_doubles = No_of_Matches_played_doubles + 1 WHERE Player_ID = {play_id};"
                cursor.execute(var)
                if winner == 1: 
                    var = f"UPDATE Player_Stats SET No_of_Matches_won_doubles = No_of_Matches_won_doubles + 1 WHERE Player_ID = {play_id};"
                    cursor.execute(var)
            cursor.fetchall()
            # break

    # cursor.fetchall()
    comm = f"SELECT Player_ID FROM Belongs_To WHERE Team_ID = {team2_id};"
    cursor.execute(comm)

    # val = f"SELECT * FROM Player_Stats;"
    play_id = 0
    info = cursor.fetchall()
    # print(info)
    # cursor.execute('ajhsjgdhabsd')
    for i in info :
        for x in i :
            play_id = i[x]
            # print(play_id,form,winner)
            if form == "Singles" :
                var = f"UPDATE Player_Stats SET No_of_Matches_played_singles = No_of_Matches_played_singles + 1 WHERE Player_ID = {play_id};"
                cursor.execute(var)
                if winner == 2: 
                    var = f"UPDATE Player_Stats SET No_of_Matches_won_singles = No_of_Matches_won_singles + 1 WHERE Player_ID = {play_id};"
                    cursor.execute(var)
                
            else:
                var = f"UPDATE Player_Stats SET No_of_Matches_played_doubles = No_of_Matches_played_doubles + 1 WHERE Player_ID = {play_id};"
                cursor.execute(var)
                if winner == 2: 
                    var = f"UPDATE Player_Stats SET No_of_Matches_won_doubles = No_of_Matches_won_doubles + 1 WHERE Player_ID = {play_id};"
                    cursor.execute(var)
            # break
    return cursor.fetchall()

def addMatches(cursor):
    team_id1=int(input("Team 1 id: "))
    team_id2=int(input("Team 2 id: "))
    league_id=int(input("Leauge_id: "))
    date=input("Date: ")
    format=input("Format: ")
    info=cursor.execute(f"Insert into Matches(Team_1_ID,Team_2_ID,Format,Date,League_ID,Team_1_Score,Team_2_Score) values ('{team_id1}','{team_id2}','{format}','{date}','{league_id}',0,0)")
    info=cursor.fetchall()
    return info

def delPlayerFromTeam(cursor):
    Player_ID=input("Enter Player id: ")
    Team_ID=input("Enter Team_ID: ")
    comm=f"DELETE FROM Belongs_To where Player_ID = {Player_ID} and Team_ID = {Team_ID};"
    cursor.execute(comm)
    return cursor.fetchall()

def delTeamFromLeague(cursor):
    Team_ID=input("Enter Team_ID: ")
    League_ID=input("Enter League_ID: ")
    comm=f"DELETE FROM Plays_in where Team_ID = {Team_ID} and League_ID = {League_ID};"
    cursor.execute(comm)
    return cursor.fetchall()

def addTeamToLeague(cursor):
    Team_ID=input("Enter Team ID: ")
    League_ID=input("Enter League ID: ")
    comm=f"INSERT INTO Plays_in (Team_ID,League_ID)VALUES ({Team_ID},{League_ID})"
    cursor.execute(comm)
    info = cursor.fetchall()
    # print(info)
    return info

def updateCapacity(cursor):
    Stadium_ID=input("Enter Venue ID: ")
    New_Capacity=input("Enter New capacity: ")
    comm=f"UPDATE Stadium SET Capacity={New_Capacity} where Venue_ID={Stadium_ID};"
    cursor.execute(comm)
    info=cursor.fetchall()
    return info
    
def hireAnEmployee():
    """
    This is a sample function implemented for the refrence.
    This example is related to the Employee Database.
    In addition to taking input, you are required to handle domain errors as well
    For example: the SSN should be only 9 characters long
    Sex should be only M or F
    If you choose to take Super_SSN, you need to make sure the foreign key constraint is satisfied
    HINT: Instead of handling all these errors yourself, you can make use of except clause to print the error returned to you by pymysql
    """
    try:
        # Takes emplyee details as input
        row = {}
        print("Enter new employee's details: ")
        name = (input("Name (Fname Minit Lname): ")).split(' ')
        row["Fname"] = name[0]
        row["Minit"] = name[1]
        row["Lname"] = name[2]
        row["Ssn"] = input("SSN: ")
        row["Bdate"] = input("Birth Date (YYYY-MM-DD): ")
        row["Address"] = input("Address: ")
        row["Sex"] = input("Sex: ")
        row["Salary"] = float(input("Salary: "))
        row["Dno"] = int(input("Dno: "))

        query = "INSERT INTO EMPLOYEE(Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Dno) VALUES('%s', '%c', '%s', '%s', '%s', '%s', '%c', %f, %d)" % (
            row["Fname"], row["Minit"], row["Lname"], row["Ssn"], row["Bdate"], row["Address"], row["Sex"], row["Salary"], row["Dno"])

        print(query)
        cur.execute(query)
        con.commit()

        print("Inserted Into Database")

    except Exception as e:
        con.rollback()
        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)

    return




def dispatch(ch,cursor):
    """
    Function that maps helper functions to option entered
    """
    
    try:
        if(ch == 2):
            selectPlayer(cursor)
        elif(ch == 1):
            selectTeam(cursor)
        elif(ch == 3):
            deleteTeam(cursor)
        elif(ch == 4):
            deletePlayer(cursor)
        elif (ch == 5):
            stadiumCity(cursor)
        elif (ch == 6):
            insertTeam(cursor)
        elif (ch == 7):
            insertPlayer(cursor)
        elif (ch == 8):
            nameTeam(cursor)
        elif (ch == 9):
            addTeam(cursor)
        elif (ch == 10):
            insertLeague(cursor)
        elif (ch == 11):
            addMatches(cursor)
        elif (ch == 12):
            scoreline(cursor)
        elif (ch == 13):
            delPlayerFromTeam(cursor)
        elif (ch == 14):
            delTeamFromLeague(cursor)
        elif (ch==15):
            addTeamToLeague(cursor)
        elif (ch==16):
            updateCapacity(cursor)
        else:
            print("Error: Invalid Option")
        
        con.commit()    
    except Exception as e:
        con.rollback()
        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)


# Global
while(1):
    tmp = sp.call('clear', shell=True)
    
    # Can be skipped if you want to hardcode username and password
    # username = input("Username: ")
    # password = input("Password: ")

    try:
        # Set db name accordingly which have been create by you
        # Set host to the server's address if you don't want to use local SQL server 
        con = pymysql.connect(host='localhost',
                              unix_socket="/var/run/mysqld/mysqld.sock",
                              user="example_user",
                              password="StrongPass123!",
                              db='BWF',
                              cursorclass=pymysql.cursors.DictCursor)
        tmp = sp.call('clear', shell=True)

        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            while(1):
                tmp = sp.call('clear', shell=True)
                # Here taking example of Employee Mini-world
                print("1. Show all teams in a league")  # Hire an Employee
                print("2. Show Player with victory greater than n")  # Fire an Employee
                print("3. Delete Team")  # Promote Employee
                print("4. Delete Player")  # Employee Statistics
                print("5. Show all stadiums and their City")
                print("6. Insert Team")
                print("7. Insert Player")
                print("8. Get id of Players in a Team")
                print("9. Add Player in a Team")
                print("10. Insert League")
                print("11. Add Match")
                print("12. Update Match Score")
                print("13. Delete a Player from a Team")
                print("14. Delete a Team from a League")    
                print("15. Add Team in a League")   
                print("16. Update Stadium Capacity")         
                print("20. Logout")
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if ch == 20:
                    exit()
                else:
                    dispatch(ch,cur)
                    tmp = input("Enter any key to CONTINUE>")

    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
