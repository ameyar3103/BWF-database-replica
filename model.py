import mysql.connector

# Replace these values with your own
host = 'localhost'
user = 'example_user'
password = 'StrongPass123!'
database = 'BWF'

def executeQuery(cursor,comm):
    cursor.execute(comm)
    return cursor.fetchall()

# insert team 
# insert player



# delete players with player id
def deletePlayer(cursor):
    id=input("Give the Player id: ")
    info = cursor.execute("delete from Player where id="+id)
    info = cursor.fetchall()
    print("deleted:",info)
    
# delete team with a team id
def deleteTeam(cursor):
    id=input("Give the Team id: ")
    info = cursor.execute("delete from Team where id="+id)
    info = cursor.fetchall()
    
    print("deleted:",info)
    return info

# select all players with victory>n
def selectPlayer(cursor):
    n=input("How many Victories: ")
    info=cursor.execute("Select * from (Players join Player_Stats on Players.Player_ID=Player_Stats.Player_ID) Where No_of_Matches_won_singles + No_of_Matches_won_doubles >"+n)
    info = cursor.fetchall()
    
    print(info)
    return info

# select all teams in a league
def selectTeam(cursor):
    n=input("League ID: ")
    info=cursor.execute("Select * from (Team join Plays_in on Team.Team_ID=Plays_in.Team_ID) Where LeagueID ="+n)
    info = cursor.fetchall()
    
    print(info)
    return info

#select city location from stadium
def stadiumCity(cursor):
    info=cursor.execute("Select Name,City from Stadium")
    info = cursor.fetchall()
    print(info)




def main():
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            print(f"Connected to MySQL server (version {connection.get_server_info()})")

            # Perform a simple query
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_info = cursor.fetchall()
            print(f"Connected to database: {db_info}")
            cursor.execute("use BWF;")
            db_info = cursor.fetchall()
            print(f"Connected to database: {db_info}")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the connection
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")


if __name__ == '__main__':
    main()
