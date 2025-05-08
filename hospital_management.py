import mysql.connector
from mysql.connector import Error
import datetime
import sys
from typing import Optional, List, Dict, Any, Tuple

class HospitalManagementSystem:
    def __init__(self, host: str, user: str, password: str, database: str):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("MySQL connection established successfully!")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            sys.exit(1)

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed.")

    def calculate_age(self, date_of_birth: str) -> int:
        if not date_of_birth:
            return 0

        try:
            dob = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            today = datetime.date.today()

            age = today.year - dob.year

            if (today.month, today.day) < (dob.month, dob.day):
                age -= 1

            return age
        except ValueError:
            print(f"Invalid date format: {date_of_birth}")
            return 0

    def is_valid_patient(self, patient_id: str) -> bool:
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(*) FROM PATIENT WHERE patientID = %s"
            cursor.execute(query, (patient_id,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0
        except Error as e:
            print(f"Error checking patient: {e}")
            return False

    def is_valid_doctor(self, doctor_id: str) -> bool:
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(*) FROM DOCTOR WHERE doctorID = %s"
            cursor.execute(query, (doctor_id,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0
        except Error as e:
            print(f"Error checking doctor: {e}")
            return False

    def is_valid_department(self, department_id: str) -> bool:
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(*) FROM DEPARTMENT WHERE deptID = %s"
            cursor.execute(query, (department_id,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0
        except Error as e:
            print(f"Error checking department: {e}")
            return False

    def is_doctor_available(self, doctor_id: str, date_time: str, duration: int) -> bool:
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT COUNT(*) FROM APPOINTMENT
                WHERE doctorID = %s AND status = 'Scheduled' AND
                ((dateTime <= %s AND DATE_ADD(dateTime, INTERVAL duration MINUTE) > %s) OR
                (dateTime < DATE_ADD(%s, INTERVAL %s MINUTE) AND dateTime >= %s))
            """
            cursor.execute(query, (doctor_id, date_time, date_time, date_time, duration, date_time))
            result = cursor.fetchone()
            cursor.close()
            return result[0] == 0
        except Error as e:
            print(f"Error checking doctor availability: {e}")
            return False

    def find_available_room(self, preferred_room: str, date_time: str, duration: int, doctor_id: str) -> Optional[str]:
        try:
            cursor = self.connection.cursor()

            dept_query = "SELECT departmentID FROM DOCTOR WHERE doctorID = %s"
            cursor.execute(dept_query, (doctor_id,))
            dept_result = cursor.fetchone()

            if not dept_result:
                cursor.close()
                return None

            department_id = dept_result[0]

            if preferred_room:
                preferred_query = """
                    SELECT r.roomNumber FROM ROOM r
                    LEFT JOIN APPOINTMENT a ON r.roomNumber = a.roomNumber AND
                    a.status = 'Scheduled' AND
                    ((a.dateTime <= %s AND DATE_ADD(a.dateTime, INTERVAL a.duration MINUTE) > %s) OR
                    (a.dateTime < DATE_ADD(%s, INTERVAL %s MINUTE) AND a.dateTime >= %s))
                    WHERE r.roomNumber = %s AND r.status = 'Available' AND r.departmentID = %s
                    GROUP BY r.roomNumber
                    HAVING COUNT(a.appointmentID) = 0
                """
                cursor.execute(preferred_query, (date_time, date_time, date_time, duration, date_time, preferred_room, department_id))
                preferred_result = cursor.fetchone()

                if preferred_result:
                    room_number = preferred_result[0]
                    cursor.close()
                    return room_number

            any_room_query = """
                SELECT r.roomNumber FROM ROOM r
                LEFT JOIN APPOINTMENT a ON r.roomNumber = a.roomNumber AND
                a.status = 'Scheduled' AND
                ((a.dateTime <= %s AND DATE_ADD(a.dateTime, INTERVAL a.duration MINUTE) > %s) OR
                (a.dateTime < DATE_ADD(%s, INTERVAL %s MINUTE) AND a.dateTime >= %s))
                WHERE r.status = 'Available' AND r.departmentID = %s
                GROUP BY r.roomNumber
                HAVING COUNT(a.appointmentID) = 0
                LIMIT 1
            """
            cursor.execute(any_room_query, (date_time, date_time, date_time, duration, date_time, department_id))
            any_room_result = cursor.fetchone()

            cursor.close()
            return any_room_result[0] if any_room_result else None

        except Error as e:
            print(f"Error finding available room: {e}")
            return None

    def generate_unique_id(self, table: str, id_field: str, prefix: str) -> str:
        try:
            cursor = self.connection.cursor()
            query = f"SELECT MAX(CAST(SUBSTRING({id_field}, {len(prefix) + 1}) AS UNSIGNED)) FROM {table}"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()

            max_id = 0
            if result[0] is not None:
                max_id = result[0]

            return f"{prefix}{max_id + 1:03d}"
        except Error as e:
            print(f"Error generating unique ID: {e}")
            return f"{prefix}001"

    def schedule_patient_appointment(self) -> None:
        try:
            patient_id = input("Enter Patient ID: ")
            doctor_id = input("Enter Doctor ID: ")
            date_str = input("Enter Appointment Date (YYYY-MM-DD): ")
            time_str = input("Enter Appointment Time (HH:MM): ")
            duration = int(input("Enter Duration (minutes): "))
            appointment_type = input("Enter Appointment Type: ")
            preferred_room = input("Enter Preferred Room Number (or leave blank): ")

            if not self.is_valid_patient(patient_id):
                print("Invalid patient ID. Please check and try again.")
                return

            if not self.is_valid_doctor(doctor_id):
                print("Invalid doctor ID. Please check and try again.")
                return

            date_time = f"{date_str} {time_str}:00"

            if not self.is_doctor_available(doctor_id, date_time, duration):
                print("Doctor is not available at the requested time.")
                return

            room_number = self.find_available_room(preferred_room, date_time, duration, doctor_id)
            if not room_number:
                print("No suitable room available at the requested time.")
                return

            appointment_id = self.generate_unique_id("APPOINTMENT", "appointmentID", "APP")

            cursor = self.connection.cursor()
            status = "Scheduled"
            notes = ""

            insert_query = """
                INSERT INTO APPOINTMENT (appointmentID, dateTime, duration, status, type, notes, patientID, doctorID, roomNumber)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (appointment_id, date_time, duration, status, appointment_type, notes, patient_id, doctor_id, room_number))
            self.connection.commit()

            print("\nAppointment scheduled successfully!")
            print(f"Appointment ID: {appointment_id}")
            print(f"Room Number: {room_number}")
            print(f"Date/Time: {date_time}")

            cursor.close()

        except Error as e:
            print(f"Error scheduling appointment: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def generate_patient_medical_history(self) -> None:
        try:
            patient_id = input("Enter Patient ID: ")
            start_date = input("Enter Start Date (YYYY-MM-DD) or leave blank for all: ")
            end_date = input("Enter End Date (YYYY-MM-DD) or leave blank for all: ")

            if not self.is_valid_patient(patient_id):
                print("Invalid patient ID. Please check and try again.")
                return

            cursor = self.connection.cursor(dictionary=True)

            patient_query = "SELECT * FROM PATIENT WHERE patientID = %s"
            cursor.execute(patient_query, (patient_id,))
            patient_info = cursor.fetchone()

            print("\n===== PATIENT INFORMATION =====")
            print(f"Patient ID: {patient_info['patientID']}")
            print(f"Name: {patient_info['name']}")
            print(f"Date of Birth: {patient_info['dateOfBirth']}")

            age = self.calculate_age(str(patient_info['dateOfBirth']))
            print(f"Age: {age}")

            address_parts = []
            if patient_info['street_number']:
                address_parts.append(patient_info['street_number'])
            if patient_info['street_name']:
                address_parts.append(patient_info['street_name'])
            if patient_info['apt_number']:
                address_parts.append(f"Apt {patient_info['apt_number']}")
            if patient_info['city']:
                address_parts.append(patient_info['city'])
            if patient_info['state']:
                address_parts.append(patient_info['state'])
            if patient_info['zip_code']:
                address_parts.append(patient_info['zip_code'])
            if patient_info['country']:
                address_parts.append(patient_info['country'])

            address = ", ".join(address_parts)
            print(f"Address: {address}")
            print(f"Insurance: {patient_info['insuranceInfo']}")

            phone_query = "SELECT patientPhoneNumber FROM PATIENT_PHONE_NUMBERS WHERE patientID = %s"
            cursor.execute(phone_query, (patient_id,))
            phone_numbers = cursor.fetchall()

            print("\n===== PATIENT PHONE NUMBERS =====")
            for phone in phone_numbers:
                print(f"Phone: {phone['patientPhoneNumber']}")

            record_query = "SELECT * FROM MEDICAL_RECORD WHERE patientID = %s"
            params = [patient_id]

            if start_date and end_date:
                record_query += " AND date BETWEEN %s AND %s"
                params.extend([start_date, end_date])
            elif start_date:
                record_query += " AND date >= %s"
                params.append(start_date)
            elif end_date:
                record_query += " AND date <= %s"
                params.append(end_date)

            record_query += " ORDER BY date DESC"
            cursor.execute(record_query, params)
            medical_records = cursor.fetchall()

            print("\n===== MEDICAL RECORDS =====")

            for record in medical_records:
                record_id = record['recordID']
                print(f"\nRecord ID: {record_id}")
                print(f"Date: {record['date']}")
                print(f"Diagnosis: {record['diagnosis']}")
                print(f"Treatment: {record['treatment']}")
                print(f"Notes: {record['note']}")

                prescription_query = """
                    SELECT p.prescriptionNumber, p.dosage, p.frequency, p.startDate, p.endDate,
                           m.medicationID, m.name, m.type, m.unit
                    FROM PRESCRIPTION p
                    JOIN MEDICATION m ON p.medicationID = m.medicationID
                    WHERE p.recordID = %s
                """
                cursor.execute(prescription_query, (record_id,))
                prescriptions = cursor.fetchall()

                print("  --- Prescriptions ---")
                for prescription in prescriptions:
                    print(f"  Prescription #: {prescription['prescriptionNumber']}")
                    print(f"  Medication: {prescription['name']} ({prescription['type']})")
                    print(f"  Dosage: {prescription['dosage']} {prescription['unit']}")
                    print(f"  Frequency: {prescription['frequency']}")
                    print(f"  Duration: {prescription['startDate']} to {prescription['endDate']}")
                    print()

            cursor.close()

        except Error as e:
            print(f"Error generating patient medical history: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def manage_department_staff_assignment(self) -> None:
        try:
            department_id = input("Enter Department ID: ")
            doctor_id = input("Enter Doctor ID: ")

            if not self.is_valid_department(department_id):
                print("Invalid department ID. Please check and try again.")
                return

            if not self.is_valid_doctor(doctor_id):
                print("Invalid doctor ID. Please check and try again.")
                return

            cursor = self.connection.cursor(dictionary=True)

            head_check_query = "SELECT headDoctor FROM DEPARTMENT WHERE deptID = %s"
            cursor.execute(head_check_query, (department_id,))
            head_check_result = cursor.fetchone()

            if head_check_result and doctor_id == head_check_result['headDoctor']:
                print("Cannot reassign department head. Please choose another doctor.")
                cursor.close()
                return

            appointment_check_query = """
                SELECT COUNT(*) AS count FROM APPOINTMENT
                WHERE doctorID = %s AND dateTime > NOW() AND status = 'Scheduled'
            """
            cursor.execute(appointment_check_query, (doctor_id,))
            appointment_check_result = cursor.fetchone()

            if appointment_check_result and appointment_check_result['count'] > 0:
                count = appointment_check_result['count']
                print(f"Doctor has {count} upcoming appointments. Cannot reassign department.")
                print("Please reschedule or cancel these appointments first.")
                cursor.close()
                return

            update_query = "UPDATE DOCTOR SET departmentID = %s WHERE doctorID = %s"
            cursor.execute(update_query, (department_id, doctor_id))
            self.connection.commit()

            if cursor.rowcount > 0:
                print("Doctor successfully assigned to the new department!")

                confirm_query = """
                    SELECT d.name AS doctor_name, dept.name AS dept_name
                    FROM DOCTOR d JOIN DEPARTMENT dept ON d.departmentID = dept.deptID
                    WHERE d.doctorID = %s
                """
                cursor.execute(confirm_query, (doctor_id,))
                confirm_result = cursor.fetchone()

                if confirm_result:
                    print(f"Dr. {confirm_result['doctor_name']} now assigned to {confirm_result['dept_name']} department.")
            else:
                print("Assignment failed. Please try again.")

            cursor.close()

        except Error as e:
            print(f"Error managing department assignment: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def list_patients(self) -> None:
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT patientID, name, dateOfBirth, CONCAT(city, ', ', state) AS location FROM PATIENT ORDER BY name"
            cursor.execute(query)
            patients = cursor.fetchall()

            if not patients:
                print("No patients found in the database.")
                return

            print("\n===== PATIENTS =====")
            print(f"{'ID':<10} {'Name':<30} {'Date of Birth':<15} {'Age':<5} {'Location':<30}")
            print("-" * 90)

            for patient in patients:
                age = self.calculate_age(str(patient['dateOfBirth']))
                print(f"{patient['patientID']:<10} {patient['name']:<30} {patient['dateOfBirth']!s:<15} {age:<5} {patient['location']:<30}")

            print(f"\nTotal patients: {len(patients)}")
            cursor.close()

        except Error as e:
            print(f"Error listing patients: {e}")

    def list_doctors(self) -> None:
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT d.doctorID, d.name, d.specialization, dept.name AS department
                FROM DOCTOR d
                JOIN DEPARTMENT dept ON d.departmentID = dept.deptID
                ORDER BY d.name
            """
            cursor.execute(query)
            doctors = cursor.fetchall()

            if not doctors:
                print("No doctors found in the database.")
                return

            print("\n===== DOCTORS =====")
            print(f"{'ID':<10} {'Name':<30} {'Specialization':<25} {'Department':<20}")
            print("-" * 85)

            for doctor in doctors:
                print(f"{doctor['doctorID']:<10} {doctor['name']:<30} {doctor['specialization']:<25} {doctor['department']:<20}")

            print(f"\nTotal doctors: {len(doctors)}")
            cursor.close()

        except Error as e:
            print(f"Error listing doctors: {e}")

    def list_departments(self) -> None:
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT d.deptID, d.name, d.location,
                       doc.name AS head_doctor,
                       COUNT(r.roomNumber) AS room_count,
                       COUNT(doc2.doctorID) AS doctor_count
                FROM DEPARTMENT d
                LEFT JOIN DOCTOR doc ON d.headDoctor = doc.doctorID
                LEFT JOIN ROOM r ON d.deptID = r.departmentID
                LEFT JOIN DOCTOR doc2 ON d.deptID = doc2.departmentID
                GROUP BY d.deptID
                ORDER BY d.name
            """
            cursor.execute(query)
            departments = cursor.fetchall()

            if not departments:
                print("No departments found in the database.")
                return

            print("\n===== DEPARTMENTS =====")
            print(f"{'ID':<10} {'Name':<25} {'Location':<25} {'Head Doctor':<25} {'Rooms':<7} {'Doctors':<7}")
            print("-" * 99)

            for dept in departments:
                print(f"{dept['deptID']:<10} {dept['name']:<25} {dept['location']:<25} {dept['head_doctor'] or 'None':<25} {dept['room_count']:<7} {dept['doctor_count']:<7}")

            print(f"\nTotal departments: {len(departments)}")
            cursor.close()

        except Error as e:
            print(f"Error listing departments: {e}")

    def list_rooms(self) -> None:
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT r.roomNumber, r.type, r.capacity, r.status, d.name AS department
                FROM ROOM r
                JOIN DEPARTMENT d ON r.departmentID = d.deptID
                ORDER BY r.roomNumber
            """
            cursor.execute(query)
            rooms = cursor.fetchall()

            if not rooms:
                print("No rooms found in the database.")
                return

            print("\n===== ROOMS =====")
            print(f"{'Room #':<10} {'Type':<20} {'Capacity':<10} {'Status':<15} {'Department':<25}")
            print("-" * 80)

            for room in rooms:
                status_display = room['status']
                if status_display == 'Available':
                    status_display = 'Available'
                elif status_display == 'Occupied':
                    status_display = 'Occupied'
                else:
                    status_display = 'Maintenance'

                print(f"{room['roomNumber']:<10} {room['type']:<20} {room['capacity']:<10} {status_display:<15} {room['department']:<25}")

            print(f"\nTotal rooms: {len(rooms)}")

            cursor.execute("SELECT status, COUNT(*) as count FROM ROOM GROUP BY status")
            status_summary = cursor.fetchall()

            print("\nRoom Status Summary:")
            for status in status_summary:
                print(f"  {status['status']}: {status['count']}")

            cursor.close()

        except Error as e:
            print(f"Error listing rooms: {e}")

    def list_appointments(self) -> None:
        try:
            cursor = self.connection.cursor(dictionary=True)

            print("\n===== APPOINTMENTS =====")
            print("Filter by:")
            print("1. All upcoming appointments")
            print("2. Today's appointments")
            print("3. Appointments for specific doctor")
            print("4. Appointments for specific patient")
            print("5. Back to main menu")

            choice = int(input("Enter your choice: "))

            query = """
                SELECT a.appointmentID, a.dateTime, a.duration, a.status, a.type,
                       p.name AS patient_name, d.name AS doctor_name, a.roomNumber
                FROM APPOINTMENT a
                JOIN PATIENT p ON a.patientID = p.patientID
                JOIN DOCTOR d ON a.doctorID = d.doctorID
                WHERE
            """

            params = []

            if choice == 1:
                query += "a.dateTime >= NOW() AND a.status = 'Scheduled'"
            elif choice == 2:
                query += "DATE(a.dateTime) = CURDATE() AND a.status = 'Scheduled'"
            elif choice == 3:
                doctor_id = input("Enter Doctor ID: ")
                query += "a.doctorID = %s AND a.dateTime >= NOW() AND a.status = 'Scheduled'"
                params.append(doctor_id)
            elif choice == 4:
                patient_id = input("Enter Patient ID: ")
                query += "a.patientID = %s AND a.dateTime >= NOW() AND a.status = 'Scheduled'"
                params.append(patient_id)
            elif choice == 5:
                return
            else:
                print("Invalid choice. Returning to main menu.")
                return

            query += " ORDER BY a.dateTime"

            cursor.execute(query, params)
            appointments = cursor.fetchall()

            if not appointments:
                print("No appointments found matching the criteria.")
                return

            print(f"\n{'ID':<10} {'Date/Time':<20} {'Duration':<10} {'Status':<12} {'Type':<15} {'Patient':<25} {'Doctor':<25} {'Room':<10}")
            print("-" * 127)

            for appt in appointments:
                formatted_date = appt['dateTime'].strftime('%Y-%m-%d %H:%M')
                duration_str = f"{appt['duration']} min"
                print(f"{appt['appointmentID']:<10} {formatted_date:<20} {duration_str:<10} {appt['status']:<12} {appt['type']:<15} {appt['patient_name']:<25} {appt['doctor_name']:<25} {appt['roomNumber']:<10}")

            print(f"\nTotal appointments: {len(appointments)}")
            cursor.close()

        except Error as e:
            print(f"Error listing appointments: {e}")
        except ValueError:
            print("Invalid input. Returning to main menu.")

    def run(self) -> None:
        while True:
            print("\nHOSPITAL MANAGEMENT SYSTEM")
            print("=== Patient Management ===")
            print("1. Schedule Patient Appointment")
            print("2. Generate Patient Medical History")
            print("3. List Patients")
            print("\n=== Staff Management ===")
            print("4. Manage Department Staff Assignment")
            print("5. List Doctors")
            print("\n=== Resource Management ===")
            print("6. List Departments")
            print("7. List Rooms")
            print("\n=== Appointments ===")
            print("8. List Appointments")
            print("\n=== System ===")
            print("9. Exit")
            print("\n")

            try:
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    self.schedule_patient_appointment()
                elif choice == 2:
                    self.generate_patient_medical_history()
                elif choice == 3:
                    self.list_patients()
                elif choice == 4:
                    self.manage_department_staff_assignment()
                elif choice == 5:
                    self.list_doctors()
                elif choice == 6:
                    self.list_departments()
                elif choice == 7:
                    self.list_rooms()
                elif choice == 8:
                    self.list_appointments()
                elif choice == 9:
                    print("Exiting application. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid menu option number.")
            except Exception as e:
                print(f"An error occurred: {e}")

def main():
    print("Hospital Management System")
    print("=========================")

    host = input("Enter database host (default: localhost): ") or "localhost"
    user = input("Enter database user (default: root): ") or "root"
    password = input("Enter database password: ")
    database = input("Enter database name (default: hospital_management): ") or "hospital_management"

    hospital_system = HospitalManagementSystem(host, user, password, database)
    hospital_system.run()


if __name__ == "__main__":
    main()
