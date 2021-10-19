A portal for SAC election

Frontend : ReactJS
Backend  : Python-Flask
Database : mysql-server

requirements.txt has the requirements for backend python code
DB/ contains the sqldump of the database	

Running backend

	$ cd Backend/
	$ python app.py
	
	Server will start on localhost:1234
	
	
Running frontend

	$ cd  Frontend/sac-election
	$ npm install
	$ npm start
	
	It will start on localhost:3000

	
Login as admin to add voters and candidates

	Admin credentials:

		username: admin
		password: admin123
		
candidates_sample.xlsx and voterlist_sample.xlsx are sample files to upload. The order of columns needs to be followed strictly.

After uploading voters a pwdFile.xlsx will be created inside Backend/ directory which contains passwords for all voters. 
[Note: Use passwords without ' in beginning. Password is a string of 8 numbers ]



