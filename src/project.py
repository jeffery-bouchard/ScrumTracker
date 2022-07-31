import sqlite3
import os
import pandas as pd

class project:
    '''project class used to define new scrum project'''

    def __init__(self, name:str, sprint_duration:int=5) -> None:
        '''initialize project object with project name and sprint duration (days)'''

        #create database
        dir = os.getcwd()
        self.conn = sqlite3.connect(f'{dir}/projects/{name}.sqlite')
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
                                priority_id     INTEGER,
                                status_id       INTEGER);''')

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


    def addUserStory(self, user_story:str, story_points:int=None, priority_id:int=2, status_id:int=1) -> int:
        '''add user story to product backlog, return product backlog ID (user story ID)'''

        cmd = "INSERT OR IGNORE INTO product_backlog(user_story, story_points, priority_id, status_id) VALUES(?, ?, ?, ?)"
        self.cursor.execute(cmd, (user_story, story_points, priority_id, status_id))
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

    def updateTask(self, task_id:int, status_id:int, hours_remaining:int) -> None:
        '''update task in current sprint backlog'''

        cmd = f'UPDATE sprint{self.sprintCnt}_backlog SET status_id = ?, hours_remaining = ? WHERE id = ?'
        self.cursor.execute(cmd, (status_id, hours_remaining, task_id))
        self.conn.commit()


    def getSprintBacklog(self) -> pd.DataFrame:
        '''retrieve current sprint backlog dataframe'''

        self.cursor.execute(f'SELECT sprint{self.sprintCnt}_backlog.task, team.name, status.name, sprint{self.sprintCnt}_backlog.hours_remaining \
                              FROM sprint{self.sprintCnt}_backlog JOIN team JOIN status \
                              ON sprint{self.sprintCnt}_backlog.team_id = team.id AND sprint{self.sprintCnt}_backlog.status_id = status.id')

        rows = self.cursor.fetchall()
        data = {'Task': [], 'Owner': [], 'Status': [], 'Hours Remaining': []}
        for row in rows:
            data['Task'].append(row[0])
            data['Owner'].append(row[1])
            data['Status'].append(row[2])
            data['Hours Remaining'].append(row[3])

        return pd.DataFrame(data=data)

    def getProductBacklog(self) -> pd.DataFrame:
        '''retrieve product backlog dataframe'''

        self.cursor.execute(f'SELECT product_backlog.user_story, status.name, priority.name, product_backlog.story_points \
                              FROM product_backlog JOIN status JOIN priority \
                              ON product_backlog.status_id = status.id AND product_backlog.priority_id = priority.id')

        rows = self.cursor.fetchall()
        data = {'User Story': [], 'Status': [], 'Priority': [], 'Story Points': []}
        for row in rows:
            data['User Story'].append(row[0])
            data['Status'].append(row[1])
            data['Priority'].append(row[2])
            data['Story Points'].append(row[3])

        return pd.DataFrame(data=data)