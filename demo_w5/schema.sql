PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS BookBorrowRecord;
DROP TABLE IF EXISTS BorrowRecord;
DROP TABLE IF EXISTS BookAuthor;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS Reader;
DROP TABLE IF EXISTS Librarian;
DROP TABLE IF EXISTS Publisher;

-- Publisher
CREATE TABLE Publisher (
    PublisherID INTEGER PRIMARY KEY NOT NULL,
    PublisherName VARCHAR(100) NOT NULL,
    Address VARCHAR(200)
);

-- Book
CREATE TABLE Book (
    BookID INTEGER PRIMARY KEY NOT NULL,
    ISBN VARCHAR(13) NOT NULL,
    Description VARCHAR(200),
    Genres VARCHAR(50),
    Language VARCHAR(20),
    Number INTEGER,
    PublisherID INTEGER NOT NULL,
    FOREIGN KEY (PublisherID) REFERENCES Publisher(PublisherID)
);

-- Author
CREATE TABLE Author (
    AuthorID INTEGER PRIMARY KEY NOT NULL,
    Name VARCHAR(100) NOT NULL,
    DOB DATE,
    Nationality VARCHAR(20)
);

-- BookAuthor (many-to-many)
CREATE TABLE BookAuthor (
    BookID INTEGER NOT NULL,
    AuthorID INTEGER NOT NULL,
    PRIMARY KEY (BookID, AuthorID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID),
    FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID)
);

-- Reader
CREATE TABLE Reader (
    ReaderID INTEGER PRIMARY KEY NOT NULL,
    Name VARCHAR(50) NOT NULL,
    DOB DATE
);

-- Librarian
CREATE TABLE Librarian (
    EmployeeID INTEGER PRIMARY KEY NOT NULL,
    Name VARCHAR(50) NOT NULL,
    DOB DATE,
    Position VARCHAR(20)
);

-- BorrowRecord
CREATE TABLE BorrowRecord (
    RecordID INTEGER PRIMARY KEY NOT NULL,
    BookID INTEGER NOT NULL,
    ReaderID INTEGER NOT NULL,
    EmployeeID INTEGER NOT NULL,
    BorrowDate DATE,
    ReturnDate DATE,
    Status VARCHAR(20) NOT NULL,
    FOREIGN KEY (BookID) REFERENCES Book(BookID),
    FOREIGN KEY (ReaderID) REFERENCES Reader(ReaderID),
    FOREIGN KEY (EmployeeID) REFERENCES Librarian(EmployeeID)
);

-- BookBorrowRecord (bảng phụ)
CREATE TABLE BookBorrowRecord (
    RecordID INTEGER NOT NULL,
    BookID INTEGER NOT NULL,
    ReturnDate DATE,
    PRIMARY KEY (RecordID, BookID),
    FOREIGN KEY (RecordID) REFERENCES BorrowRecord(RecordID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID)
);