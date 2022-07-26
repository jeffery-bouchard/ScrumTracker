import sqlite3

class project:
    '''project class used to define new scrum project'''

    def __init__(self, name:str, sprint_duration:int=7) -> None:
        '''initialize object with project name and sprint duration'''
        self.conn = sqlite3.connect(f'{name}.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE scrum_team(
                                id              INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                first_name      TEXT NOT NULL,
                                last_name       TEXT NOT NULL,
                                role            TEXT);''')
        
        self.cursor.execute('''CREATE TABLE product_backlog(
                                id              INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                user_story      TEXT NOT NULL,
                                story_points    INTEGER,
                                priority        INTEGER,
                                sprint_id       INTEGER);''')
        self.conn.commit()
        self.sprintCnt = 0
        self.sprintLength = sprint_duration
    
    def addTeamMember(self, first_name:str, last_name:str, role:str=None) -> None:
        '''add scrum team member'''
        cmd = "INSERT INTO scrum_team(first_name, last_name, role) VALUES(?, ?, ?)"
        self.cursor.execute(cmd, (first_name, last_name, role))
        self.conn.commit()
    
    def addUserStory(self, user_story:str, story_points:int=None, priority:int=None, sprint_id:int=None) -> None:
        '''add user story to product backlog'''
        cmd = "INSERT INTO product_backlog(user_story, story_points, priority, sprint_id) VALUES(?, ?, ?, ?)"
        self.cursor.execute(cmd, (user_story, story_points, priority, sprint_id))
        self.conn.commit()

    def addSprint(self) -> None:
        '''add sprint to project'''
        self.sprintCnt += 1
        self.cursor.execute(f'CREATE TABLE sprint{self.sprintCnt}_backlog(                  \
                                id              INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                                task            STRING NOT NULL,                            \
                                story_id        INTEGER,                                    \
                                team_id         INTEGER,                                    \
                                status          STRING NOT NULL,                            \
                                hours_remaining INTEGER);')
        self.conn.commit()

    def addTask(self, name:str, story_id:int=None, team_id:int=None, status:str='NOT STARTED', hours_remaining:int=None) -> None:
        '''add task to current sprint'''
        if self.sprintCnt == 0:
            self.addSprint()
        cmd = f'INSERT INTO sprint{self.sprintCnt}_backlog(task, story_id, team_id, status, hours_remaining) VALUES(?, ?, ?, ?, ?)'
        self.cursor.execute(cmd, (name, story_id, team_id, status, hours_remaining))
        self.conn.commit()
