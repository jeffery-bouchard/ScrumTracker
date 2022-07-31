from src.project import project
import pytest
import sqlite3
import os

class TestProject:
    '''test project class used for unit test'''

    def setup_class(self):
        '''creates new project instance and sets up database for unit tests'''

        name = 'test'
        dir = os.getcwd()
        self.db = f'{dir}/projects/{name}.sqlite'
        self.newProj = project(name)
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.tables = self.cursor.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()

    def test_init_databaseExists(self):
        '''tests if project database was created'''

        assert os.path.exists(self.db), f'database not present: {self.db}'

    def test_init_teamTableExists(self):
        '''tests if team table was created'''

        assert 'team' in self.tables[0], 'could not find team table'

    def test_init_prodBacklogTableExists(self):
        '''tests if product backlog table was created'''

        assert 'product_backlog' in self.tables[2], 'could not find product backlog table'

    def test_init_statusTableExists(self):
        '''tests if status table was created'''

        assert 'status' in self.tables[3], 'could not find status table'

    def test_init_priorityTableExists(self):
        '''tests if priority table was created'''

        assert 'priority' in self.tables[4], 'could not find priority table'

    def test_addTeamMember_teamMemberExists(self):
        '''tests if new team member is successfully added to team table'''

        name = 'Luke Skywalker'
        self.newProj.addTeamMember(name)
        members = [x[0] for x in self.cursor.execute("SELECT name FROM team").fetchall()]
        assert name in members, 'could not find team member in team table'

    def test_addUserStory_userStoryExists(self):
        '''tests if new user story is successfully added to product backlog table'''

        name = 'user story'
        self.newProj.addUserStory(name)
        members = [x[0] for x in self.cursor.execute("SELECT user_story FROM product_backlog").fetchall()]
        assert name in members, 'could not find user story in product backlog table'

    def test_addSprint_sprintTableExists(self):
        '''tests if sprint table was created'''

        self.newProj.addSprint()
        self.tables = self.cursor.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()
        assert 'sprint1_backlog' in self.tables[5], 'could not find sprint table'

    def test_addTask_taskExists(self):
        '''tests if new task is successfully added to sprint backlog table'''

        name = 'task'
        self.newProj.addTask(name)
        members = [x[0] for x in self.cursor.execute("SELECT task FROM sprint1_backlog").fetchall()]
        assert name in members, 'could not find task in sprint backlog table'