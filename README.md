# Hospital Management System
A python application using a MYSQL database to manage various aspects of a hospital.

## Technical Requirements
### Prerequisites
- Python 3.10 or higher
- MySQL 8.0 or higher
- pipenv (for dependency management)

### Dependencies
The project uses pipenv for dependency management. The required packages are:
- mysql-connector-python

## Installation
1. Clone the repository or download the source code

    `git clone https://github.com/AndrewLHellman/hospital-management.git`

2. Install dependencies using pipenv

    `pipenv install`

3. Set up the MySQL database

    - Create a database named `hospital_management`
    - Import the SQL schema file: `mysql -u username -p hospital_management < database/schema.sql`
    - Import the sample data: `mysql -u username -p hospital_management < database/sample_data.sql`

## Usage
1. Activate the virtual environment

    `pipenv shell`

2. Run the application

    `python hospital_management.py`

3. Input MySQL credentials

4. Navigate the menu to use the various functions

    - Patient Management (options 1-3)
    - Staff Management (options 4-5)
    - Resource Management (options 6-7)
    - Appointments (option 8)

## License
This project is licensed under the MIT License - see the LICENSE file for details.
