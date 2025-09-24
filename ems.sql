DROP DATABASE IF EXISTS EMS;
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

INSERT INTO Venues (VenueName, Capacity, Location, ContactPerson, ContactNumber) VALUES
('Sydney Convention Centre', 1500, 'Darling Harbour, Sydney NSW', 'Jessica Taylor', '+61 400 111 222'),
('Melbourne Exhibition Centre', 1200, 'South Wharf, Melbourne VIC', 'David Johnson', '+61 400 333 444'),
('Adelaide Showground', 800, 'Wayville, Adelaide SA', 'Emily Brown', '+61 400 555 666'),
('Brisbane City Hall', 600, 'King George Square, Brisbane QLD', 'Michael Lee', '+61 400 777 888'),
('Perth Convention Centre', 1000, 'Mounts Bay Road, Perth WA', 'Sophie Wilson', '+61 400 999 000');

INSERT INTO Organizers (OrganizerName, ContactPerson, ContactNumber, Email) VALUES
('Aussie Events Co.', 'Jessica Taylor', '+61 400 111 222', 'jessica@aussieevents.com'),
('Down Under Planners', 'David Johnson', '+61 400 333 444', 'david@duplanners.com'),
('Southern Cross Events', 'Emily Brown', '+61 400 555 666', 'emily@scevents.com'),
('Koala Creations', 'Michael Lee', '+61 400 777 888', 'michael@koalacreations.com'),
('Boomerang Events', 'Sophie Wilson', '+61 400 999 000', 'sophie@boomevents.com');

INSERT INTO Events (EventName, EventDate, StartTime, EndTime, Description, Status, Budget, VenueID, OrganizerID) VALUES
('Sydney Tech Expo', '2025-10-20', '09:00:00', '18:00:00', 'Technology showcase featuring Aussie startups and global leaders.', 'Active', 80000.00, 1, 1),
('Melbourne Food & Wine Festival', '2026-01-29', '11:00:00', '22:00:00', 'Celebrating the best of Victoria’s food and wine culture.', 'Active', 50000.00, 2, 2),
('Adelaide Arts Festival', '2025-12-01', '10:00:00', '20:00:00', 'Annual celebration of art, music, and theatre in Adelaide.', 'Active', 60000.00, 3, 3),
('Brisbane Startup Summit', '2025-05-04', '09:30:00', '17:00:00', 'Gathering of entrepreneurs, investors, and innovators.', 'Completed', 40000.00, 4, 4),
('Perth Sustainability Conference', '2025-07-25', '08:30:00', '16:30:00', 'Conference focusing on renewable energy and sustainability.', 'Completed', 45000.00, 5, 5);

INSERT INTO Attendees (FirstName, LastName, Email, ContactNumber) VALUES
('Liam', 'Anderson', 'liam.anderson@example.com', '+61 401 111 111'),
('Olivia', 'Williams', 'olivia.williams@example.com', '+61 402 222 222'),
('Noah', 'Thompson', 'noah.thompson@example.com', '+61 403 333 333'),
('Charlotte', 'Roberts', 'charlotte.roberts@example.com', '+61 404 444 444'),
('Ethan', 'Harris', 'ethan.harris@example.com', '+61 405 555 555');

INSERT INTO Registrations (EventID, AttendeeID, RegistrationDate) VALUES
(1, 1, '2025-01-10'),
(1, 2, '2025-01-12'),
(2, 3, '2025-02-05'),
(3, 4, '2025-03-01'),
(4, 5, '2025-03-28');

INSERT INTO Speakers (SpeakerName, Bio, ContactInformation) VALUES
('Prof. Andrew White', 'Expert in quantum computing from University of Queensland.', '+61 411 123 456'),
('Dr. Sarah Johnson', 'Food scientist and advocate for sustainable agriculture.', '+61 412 234 567'),
('Ms. Hannah Brown', 'Internationally acclaimed theatre director.', '+61 413 345 678'),
('Mr. Daniel Taylor', 'Founder of Brisbane-based startup accelerator.', '+61 414 456 789'),
('Dr. Chloe Martin', 'Researcher in renewable energy technologies.', '+61 415 567 890');

INSERT INTO Sponsors (SponsorName, ContactPerson, ContactNumber) VALUES
('Telstra', 'Mark Evans', '+61 420 111 111'),
('Qantas Airways', 'Laura Green', '+61 421 222 222'),
('Commonwealth Bank', 'James Carter', '+61 422 333 333'),
('Woolworths Group', 'Sophia Wright', '+61 423 444 444'),
('Rio Tinto', 'Benjamin Scott', '+61 424 555 555');

INSERT INTO Sessions (EventID, StartTime, EndTime, Title, SpeakerID) VALUES
(1, '09:30:00', '10:30:00', 'Keynote: Future of Aussie Tech', 1),
(2, '12:00:00', '13:30:00', 'Panel: The Evolution of Aussie Cuisine', 2),
(3, '14:00:00', '15:30:00', 'Play: Modern Australian Theatre', 3),
(4, '10:00:00', '11:30:00', 'Startup Pitches: Brisbane’s Brightest', 4),
(5, '13:00:00', '14:30:00', 'Workshop: Renewable Futures', 5);

INSERT INTO Feedback (EventID, AttendeeID, Rating, Comments) VALUES
(1, 1, 5, 'Amazing showcase of Australian innovation.'),
(1, 2, 4, 'Great event but could have more startups from regional areas.'),
(2, 3, 5, 'Best food festival I’ve ever attended.'),
(3, 4, 4, 'Loved the performances, very engaging.'),
(4, 5, 3, 'Good summit, but networking opportunities felt limited.');

INSERT INTO SocialMediaPromotion (EventID, Platform, Content, DatePosted) VALUES
(1, 'Twitter', 'Get ready for #SydneyTechExpo 2025! 🚀', '2025-01-05'),
(2, 'Facebook', 'Melbourne Food & Wine Festival is back this February! 🍷', '2025-02-01'),
(3, 'Instagram', 'Adelaide Arts Festival 🎭 Join the celebration of creativity!', '2025-03-01'),
(4, 'LinkedIn', 'Brisbane Startup Summit 2025 – connect with innovators!', '2025-03-25'),
(5, 'Twitter', 'Perth Sustainability Conference 🌏 Future starts here.', '2025-04-20');

Show tables;