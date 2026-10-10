-- MySQL 8.0.16+; safe to rerun: existing records are retained.
CREATE DATABASE IF NOT EXISTS research_portal
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE research_portal;

CREATE TABLE IF NOT EXISTS opportunities (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    research_area VARCHAR(150) NOT NULL,
    faculty_name VARCHAR(150) NOT NULL,
    department VARCHAR(150) NOT NULL,
    required_skills TEXT NOT NULL,
    available_positions INT NOT NULL,
    application_deadline DATE NOT NULL,
    status ENUM('Open', 'Closed') NOT NULL DEFAULT 'Open',
    CONSTRAINT positions_non_negative CHECK (available_positions >= 0),
    CONSTRAINT title_not_blank CHECK (CHAR_LENGTH(TRIM(title)) > 0),
    CONSTRAINT description_not_blank CHECK (CHAR_LENGTH(TRIM(description)) > 0),
    CONSTRAINT area_not_blank CHECK (CHAR_LENGTH(TRIM(research_area)) > 0),
    CONSTRAINT faculty_not_blank CHECK (CHAR_LENGTH(TRIM(faculty_name)) > 0),
    CONSTRAINT department_not_blank CHECK (CHAR_LENGTH(TRIM(department)) > 0),
    CONSTRAINT skills_not_blank CHECK (CHAR_LENGTH(TRIM(required_skills)) > 0),
    CONSTRAINT status_valid CHECK (status IN ('Open', 'Closed'))
) ENGINE=InnoDB;
