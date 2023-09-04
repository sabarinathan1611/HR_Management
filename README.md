# Employee Attendance Management System with Biometric Integration (Flask Version)

## Overview

This project is an Employee Attendance Management System built using the Flask web framework in Python. It allows HR personnel to efficiently track and manage employee attendance using biometric data. It offers the flexibility to import data from an Excel file or directly retrieve data from a biometric device.

## Features

- **Biometric Integration**: Seamlessly integrate with biometric devices for real-time attendance tracking. Supported biometric data sources include fingerprint, facial recognition, and more.

- **Excel Import**: Import employee data and attendance records from Excel files for easy setup and management.

- **User-Friendly Interface**: A user-friendly web-based interface for HR personnel to view and manage employee attendance records.

- **Attendance Reports**: Generate comprehensive attendance reports, including daily, weekly, and monthly summaries. Export reports in various formats (PDF, Excel) for further analysis.

- **Notifications**: Set up email or in-app notifications for HR personnel to stay informed about attendance-related events, such as late arrivals or absences.

- **Access Control**: Define user roles and permissions to restrict access to sensitive attendance data.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/sabarinathan1611/HR_Management.git

2. **Navigate to the Project Directory:**

   ```bash
    cd HR_Management

3. **Create a Virtual Environment (Optional but Recommended):**
    ```bash
    python -m venv venv
    
4. **Activate the Virtual Environment:**

    4.1 *On Windows:*

        venv\Scripts\activate
  
    4.2 *On macOS and Linux:*
    ```bash 
    source venv/bin/activate
    
5. **Install the Required Dependencies:**
    ```bash
    pip install -r requirements.txt

6. **Start the Flask Application:**
    ```bash
    flask run 
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
