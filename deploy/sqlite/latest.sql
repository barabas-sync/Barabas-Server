CREATE TABLE User (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	firstName VARCHAR(64),
	lastName VARCHAR(64),
	email VARCHAR(512) UNIQUE,
	lastLoginTime TIMESTAMP DEFAULT NULL,
	registrationDate DATE
);

CREATE TABLE PasswordAuthentication (
	ID INTEGER,
	userID INTEGER,
	username VARCHAR(64) UNIQUE,
	passwordHash VARCHAR(128),
	passwordSalt VARCHAR(32),
	resetHash VARCHAR(64),
	FOREIGN KEY (userID) REFERENCES User(ID)
);

CREATE TABLE SyncedFile (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	fileName VARCHAR(512) NOT NULL,
	ownerID INTEGER REFERENCES User(ID),
	mimetype VARCHAR(64)
);

CREATE TABLE SyncedFileVersion (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	syncedFileID INTEGER NOT NULL,
	filePointer VARCHAR(512) NOT NULL,
	name VARCHAR(512),
	timeEdited VARCHAR(32) NOT NULL,
	timeStored TIMESTAMP NOT NULL,
	FOREIGN KEY(syncedFileID) REFERENCES SyncedFile(ID)
);

CREATE TABLE FileTag (
	fileID INTEGER NOT NULL,
	tagName VARCHAR(512) NOT NULL,
	PRIMARY KEY(fileID, tagName),
	FOREIGN KEY(fileID) REFERENCES SyncedFile(ID)
);

CREATE TABLE HistoryLog (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	fileID INTEGER NOT NULL,
	isNew BOOLEAN NOT NULL,
	
	-- New file parameters
	fileName VARCHAR(256),
	mimetype VARCHAR(64),
	
	-- Tag/Untag parameters
	tagName VARCHAR(128),
	
	-- New version parameters / Version rename
	versionID INTEGER,
	versionName VARCHAR(256),
	timeEdited VARCHAR(32)--,
	
	-- Disabled because it doesn't work
	-- FOREIGN KEY (fileID) REFERENCES SyncedFile(ID),
	-- FOREIGN KEY (versionID) REFERENCES SyncedFileVersion(ID)
);
