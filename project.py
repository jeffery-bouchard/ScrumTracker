import sqlite3

class project:
    '''project class used to define new scrum project'''

    def __init__(self, name:str, sprint_duration:int=5) -> None:
        '''initialize project object with project name and sprint duration (days)'''

        #create database
        self.conn = sqlite3.connect(f'{name}.sqlite')
        self.cursor = self.conn.cursor()

        #create scrum team table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS team(
                                id              INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                name            TEXT NOT NULL UNIQUE,
                                role            TEXT);''')
        
        #create product backlog table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS product_backlog(
                                id              INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                user_story      TEXT NOT NULL UNIQUE,
                                story_points    INTEGER,
                                priority        INTEGER,
                                sprint_id       INTEGER);''')

        #create status table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS status(
                                id              INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                name            TEXT NOT NULL UNIQUE);''')
        statusNames = [('Not Started',),
                       ('In Progress',),
                       ('Complete',)]
        self.cursor.executemany("INSERT OR IGNORE INTO status(name) VALUES (?)", statusNames)

        #create priority table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS priority(
                                id              INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                name            TEXT NOT NULL UNIQUE);''')
        priorityNames = [('Low',),
                         ('Med',),
                         ('High',)]
        self.cursor.executemany("INSERT OR IGNORE INTO priority(name) VALUES (?)", priorityNames)

        #commit database and initialize variables
        self.conn.commit()
        self.sprintCnt = 0
        self.sprintLength = sprint_duration
    

    def addTeamMember(self, name:str, role:str=None) -> int:
        '''add scrum team member, return team ID'''
        cmd = "INSERT OR IGNORE INTO team(name, role) VALUES(?, ?)"
        self.cursor.execute(cmd, (name, role))
        self.conn.commit()
        return self.cursor.lastrowid


    def addUserStory(self, user_story:str, story_points:int=None, priority:int=None, sprint_id:int=None) -> int:
        '''add user story to product backlog, return product backlog ID (user story ID)'''
        cmd = "INSERT OR IGNORE INTO product_backlog(user_story, story_points, priority, sprint_id) VALUES(?, ?, ?, ?)"
        self.cursor.execute(cmd, (user_story, story_points, priority, sprint_id))
        self.conn.commit()
        return self.cursor.lastrowid


    def addSprint(self) -> None:
        '''add sprint to project'''
        self.sprintCnt += 1
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS sprint{self.sprintCnt}_backlog(               \
                                id                  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, \
                                task                STRING NOT NULL UNIQUE,                            \
                                product_backlog_id  INTEGER,                                           \
                                team_id             INTEGER,                                           \
                                status_id           INTEGER NOT NULL,                                  \
                                hours_remaining     INTEGER);')
        self.conn.commit()


    def addTask(self, name:str, product_backlog_id:int=None, team_id:int=None, status_id:int=1, hours_remaining:int=None) -> int:
        '''add task to current sprint, return task ID'''
        if self.sprintCnt == 0:
            self.addSprint()
        cmd = f'INSERT OR IGNORE INTO sprint{self.sprintCnt}_backlog(task, product_backlog_id, team_id, status_id, hours_remaining) VALUES(?, ?, ?, ?, ?)'
        self.cursor.execute(cmd, (name, product_backlog_id, team_id, status_id, hours_remaining))
        self.conn.commit()
        return self.cursor.lastrowid

