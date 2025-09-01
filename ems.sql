DROP DATABASE EMS;
CREATE SCHEMA EMS;
USE EMS;

CREATE TABLE Venues (
    VenueID INT PRIMARY KEY AUTO_INCREMENT,
    VenueName VARCHAR(255) NOT NULL,
    Capacity INT,
    Location VARCHAR(255),
    ContactPerson VARCHAR(100),
    ContactNumber VARCHAR(20)
);

CREATE TABLE Organizers (
    OrganizerID INT PRIMARY KEY AUTO_INCREMENT,
    OrganizerName VARCHAR(255) NOT NULL,
    ContactPerson VARCHAR(100),
    ContactNumber VARCHAR(20),
    Email VARCHAR(255)
);

CREATE TABLE Events (
    EventID INT PRIMARY KEY AUTO_INCREMENT,
    EventName VARCHAR(255) NOT NULL,
    EventDate DATE,
    StartTime TIME,
    EndTime TIME,
    Description TEXT,
    Status VARCHAR(50),
    Budget DECIMAL(10, 2),
    VenueID INT,
    OrganizerID INT,
    FOREIGN KEY (VenueID) REFERENCES Venues(VenueID),
    FOREIGN KEY (OrganizerID) REFERENCES Organizers(OrganizerID)
);

CREATE TABLE Tickets (
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    EventID INT NOT NULL,
    AttendeeName VARCHAR(255) NOT NULL,
    PurchaseTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Attendees (
    AttendeeID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Email VARCHAR(255),
    ContactNumber VARCHAR(20)
);

CREATE TABLE Registrations (
    RegistrationID INT PRIMARY KEY AUTO_INCREMENT,
    EventID INT,
    AttendeeID INT,
    RegistrationDate DATE,
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (AttendeeID) REFERENCES Attendees(AttendeeID)
);

CREATE TABLE Speakers (
    SpeakerID INT PRIMARY KEY AUTO_INCREMENT,
    SpeakerName VARCHAR(255) NOT NULL,
    Bio TEXT,
    ContactInformation VARCHAR(255)
);

CREATE TABLE Sponsors (
    SponsorID INT PRIMARY KEY AUTO_INCREMENT,
    SponsorName VARCHAR(255) NOT NULL,
    ContactPerson VARCHAR(100),
    ContactNumber VARCHAR(20)
);

CREATE TABLE Sessions (
    SessionID INT PRIMARY KEY AUTO_INCREMENT,
    EventID INT,
    StartTime TIME,
    EndTime TIME,
    Title VARCHAR(255),
    SpeakerID INT,
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (SpeakerID) REFERENCES Speakers(SpeakerID)
);

CREATE TABLE Feedback (
    FeedbackID INT PRIMARY KEY AUTO_INCREMENT,
    EventID INT,
    AttendeeID INT,
    Rating INT,
    Comments TEXT,
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (AttendeeID) REFERENCES Attendees(AttendeeID)
);

CREATE TABLE SocialMediaPromotion (
    PromotionID INT PRIMARY KEY AUTO_INCREMENT,
    EventID INT,
    Platform VARCHAR(50),
    Content TEXT,
    DatePosted DATE,
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY AUTO_INCREMENT,
    AttendeeID INT,
    Amount DECIMAL(10,2),
    PaymentDate DATE,
    Status VARCHAR(50),
    FOREIGN KEY (AttendeeID) REFERENCES Attendees(AttendeeID)
);

CREATE TABLE EventPayments (
    EventID INT,
    PaymentID INT,
    PRIMARY KEY(EventID, PaymentID),
    FOREIGN KEY(EventID) REFERENCES Events(EventID),
    FOREIGN KEY(PaymentID) REFERENCES Payments(PaymentID)
);

INSERT INTO Venues (VenueID, VenueName, Capacity, Location, ContactPerson, ContactNumber)
VALUES
    (1, 'Lahore Convention Center', 1000, 'Johar Town, Lahore', 'Ali Khan', '+92 300 1234567'),
    (2, 'Pearl Continental Hotel', 500, 'Mall Road, Lahore', 'Sara Ahmed', '+92 321 9876543'),
    (3, 'Royal Palm Golf & Country Club', 300, 'Canal Bank Road, Lahore', 'Ahmed Raza', '+92 333 5558888'),
    (4, 'Alhamra Arts Council', 200, 'Mall Road, Lahore', 'Nida Fatima', '+92 345 6789123'),
    (5, 'Liberty Castle', 150, 'Liberty Market, Lahore', 'Bilal Khan', '+92 302 1112233');
    
INSERT INTO Organizers (OrganizerID, OrganizerName, ContactPerson, ContactNumber, Email)
VALUES
    (1, 'EventPro Solutions', 'Ali Khan', '+92 300 1234567', 'ali@example.com'),
    (2, 'Grand Events', 'Sara Ahmed', '+92 321 9876543', 'sara@example.com'),
    (3, 'Royal Events', 'Ahmed Raza', '+92 333 5558888', 'ahmed@example.com'),
    (4, 'Star Planners', 'Nida Fatima', '+92 345 6789123', 'nida@example.com'),
    (5, 'Elite Organizers', 'Bilal Khan', '+92 302 1112233', 'bilal@example.com');

INSERT INTO Events (EventID, EventName, EventDate, StartTime, EndTime, Description, Status, Budget, VenueID, OrganizerID)
VALUES
    (1, 'Tech Expo', '2024-01-15', '09:00:00', '18:00:00', 'Technology exhibition showcasing latest innovations.', 'Active', 50000.00, 1, 1),
    (2, 'Finance Seminar', '2024-02-01', '10:00:00', '16:00:00', 'Seminar on financial strategies and market trends.', 'Active', 30000.00, 2, 2),
    (3, 'GreenTech Workshop', '2024-02-10', '14:00:00', '17:00:00', 'Workshop promoting sustainable and green technologies.', 'Active', 20000.00, 3, 3),
    (4, 'Digital Marketing Showcase', '2024-02-20', '11:00:00', '15:00:00', 'Showcasing the latest trends in digital marketing.', 'Active', 25000.00, 4, 4),
    (5, 'AI Innovation Event', '2024-03-01', '13:00:00', '19:00:00', 'Event focusing on artificial intelligence and its applications.', 'Active', 35000.00, 5, 5);

INSERT INTO Attendees (AttendeeID, FirstName, LastName, Email, ContactNumber)
VALUES
    (1, 'John', 'Doe', 'john@example.com', '+92 300 1112233'),
    (2, 'Emma', 'Smith', 'emma@example.com', '+92 321 4445566'),
    (3, 'James', 'Johnson', 'james@example.com', '+92 333 7778899'),
    (4, 'Sophia', 'Brown', 'sophia@example.com', '+92 345 9991122'),
    (5, 'Michael', 'Davis', 'michael@example.com', '+92 302 1113344');

INSERT INTO Registrations (RegistrationID, EventID, AttendeeID, RegistrationDate)
VALUES
    (1, 1, 1, '2024-01-01'),
    (2, 1, 2, '2024-01-02'),
    (3, 2, 3, '2024-01-03'),
    (4, 3, 4, '2024-01-04'),
    (5, 4, 5, '2024-01-05');

INSERT INTO Speakers (SpeakerID, SpeakerName, Bio, ContactInformation)
VALUES
    (1, 'Dr. Ayesha Khan', 'Renowned researcher in technology', '+92 300 1112222'),
    (2, 'Mr. Fahad Ahmed', 'Expert in business strategy', '+92 321 3334444'),
    (3, 'Prof. Sarah Malik', 'Academician and author', '+92 333 5556666'),
    (4, 'Ms. Aliya Khan', 'Digital marketing specialist', '+92 345 7778888'),
    (5, 'Mr. Ahmed Shah', 'Innovator in artificial intelligence', '+92 302 9990000');

INSERT INTO Sponsors (SponsorID, SponsorName, ContactPerson, ContactNumber)
VALUES
    (1, 'Tech Solutions', 'Ali Khan', '+92 300 1110000'),
    (2, 'Finance Innovations', 'Sara Ahmed', '+92 321 2221111'),
    (3, 'Green Energy Ltd.', 'Ahmed Raza', '+92 333 3334444'),
    (4, 'Digital Marketing Experts', 'Nida Fatima', '+92 345 5556666'),
    (5, 'AI Innovations', 'Bilal Khan', '+92 302 7778888');

INSERT INTO Sessions (SessionID, EventID, StartTime, EndTime, Title, SpeakerID)
VALUES
    (1, 1, '09:00:00', '10:30:00', 'Keynote Address', 1),
    (2, 1, '11:00:00', '12:30:00', 'Panel Discussion on Future Trends', 2),
    (3, 2, '10:00:00', '11:30:00', 'Workshop: Digital Marketing Strategies', 4),
    (4, 3, '14:00:00', '15:30:00', 'Seminar: Sustainable Business Practices', 3),
    (5, 4, '13:00:00', '14:30:00', 'Innovation Showcase', 5);

INSERT INTO Feedback (FeedbackID, EventID, AttendeeID, Rating, Comments)
VALUES
    (1, 1, 1, 4, 'Great event, informative sessions'),
    (2, 1, 2, 5, 'Excellent organization and speakers'),
    (3, 2, 3, 3, 'Good workshop but room for improvement'),
    (4, 3, 4, 4, 'Loved the seminar, insightful content'),
    (5, 4, 5, 5, 'Innovation showcase was amazing');

INSERT INTO SocialMediaPromotion (PromotionID, EventID, Platform, Content, DatePosted)
VALUES
    (1, 1, 'Twitter', 'Exciting tech conference coming up in Lahore! #TechExpo', '2024-01-05'),
    (2, 2, 'Facebook', 'Join us at the Finance Seminar in Karachi. Register now!', '2024-02-01'),
    (3, 3, 'Instagram', "GreenTech Workshop in Faisalabad. Don't miss out!", '2024-02-10'),
    (4, 4, 'LinkedIn', 'Digital Marketing Showcase in Quetta. Connect with experts!', '2024-02-20'),
    (5, 5, 'Twitter', 'AI Innovation event in Multan. Explore the future!', '2024-03-01');

INSERT INTO EventPayments (EventID, PaymentID)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);

Show tables;

