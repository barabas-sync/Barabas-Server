CREATE TABLE User (
	ID INTEGER AUTO_INCREMENT PRIMARY KEY,
	firstName VARCHAR(64),
	lastName VARCHAR(64),
	email VARCHAR(512) UNIQUE,
	lastLoginTime TIMESTAMP,
	registrationDate DATE
);

CREATE TABLE SyncedFile (
	ID INTEGER AUTO_INCREMENT PRIMARY KEY,
	fileName VARCHAR(512) NOT NULL,
	ownerID INTEGER REFERENCES User(ID),
	mimetype VARCHAR(64)
);

CREATE TABLE SyncedFileVersion (
	ID INTEGER AUTO_INCREMENT PRIMARY KEY,
	syncedFileID INTEGER NOT NULL,
	filePointer VARCHAR(512) NOT NULL,
	name VARCHAR(256),
	timeEdited TIMESTAMP NOT NULL,
	timeStored TIMESTAMP NOT NULL,
	FOREIGN KEY(syncedFileID) REFERENCES SyncedFile(ID)
);

CREATE TABLE FileTag (
	fileID INTEGER NOT NULL,
	tagName VARCHAR(128) NOT NULL,
	PRIMARY KEY(fileID, tagName),
	FOREIGN KEY(fileID) REFERENCES SyncedFile(ID)
);

CREATE TABLE PasswordAuthentication (
	ID INTEGER AUTO_INCREMENT PRIMARY KEY,
	userID INTEGER,
	username VARCHAR(64) UNIQUE,
	passwordHash VARCHAR(128),
	passwordSalt VARCHAR(32),
	resetHash VARCHAR(64),
	FOREIGN KEY (userID) REFERENCES User(ID)
);

CREATE TABLE HistoryLog (
	ID INTEGER AUTO_INCREMENT PRIMARY KEY,
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
	timeEdited TIMESTAMP,

	FOREIGN KEY (fileID) REFERENCES SyncedFile(ID),
	FOREIGN KEY (versionID) REFERENCES SyncedFileVersion(ID)
);
