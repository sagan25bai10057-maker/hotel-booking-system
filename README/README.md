# Hotel Booking Management System
## 📝 Overview
The **Hotel Booking Management System** is a lightweight, desktop-based application designed to streamline front-desk operations for small hotels, bed & breakfasts, and guest houses. Built using **Python** and **Tkinter** for the graphical user interface (GUI), it leverages a local **SQLite** database for secure and persistent data storage.
This application replaces outdated manual methods like paper logbooks and spreadsheets, providing a digital solution to manage room inventory, process guest check-ins and check-outs, and calculate billing automatically. Its intuitive design ensures that staff with minimal technical training can use it effectively.
## ✨ Features
* **Automatic Setup:** On first launch, the application automatically creates the necessary `hotel.db` database and populates it with a default inventory of rooms (Single, Double, Deluxe, Suite) so it's ready to use immediately.
* **Smart Booking Form:**
    * Capture guest details (Name, Phone Number).
    * Specify duration of stay.
    * **Dynamic Room Selection:** The dropdown list intelligently displays *only* rooms that are currently available, preventing double-booking errors.
* **Real-Time Occupancy Dashboard:** A clear, tabular view shows all guests currently checked into the hotel, along with their room number and check-in date.
* **One-Click Check-Out & Billing:**
    * Easily select a guest from the dashboard to check them out.
    * The system automatically calculates the total bill based on the room price and length of stay.
    * Upon completion, the room's status is instantly updated back to 'Available'.
* **Data Persistence:** All data is stored locally in a reliable SQLite database, ensuring no information is lost when the application is closed.
## 🛠️ Technologies & Tools Used
* **Programming Language:** Python 3.x
* **GUI Framework:** Tkinter (built-in to Python standard library)
* **Database:** SQLite3 (built-in to Python standard library)
* **Version Control:** Git & GitHub
## ⚙️ Installation & Setup Steps
Follow these simple steps to get the project running on your local machine.
### Prerequisites
* Ensure you have **Python installed** on your computer. You can download it from [python.org](https://www.python.org/downloads/).
### Steps to Run
1.  **Clone the Repository:**
    Open your terminal or command prompt and run the following command to download the project files:
    ```bash
    git clone [https://github.com/YourUsername/hotel-booking-system.git](https://github.com/YourUsername/hotel-booking-system.git)
    ```
    *(**Note:** Replace `YourUsername` and `hotel-booking-system` with your actual GitHub username and repository name.)*
2.  **Navigate to the Project Directory:**
    ```bash
    cd hotel-booking-system
    ```
3.  **Run the Application:**
    Execute the main Python script. The database will be initialized automatically on the first run.
    ```bash
    python hotel_app.py
    ```
    *(**Note:** If your main script has a different name, replace `hotel_app.py` with the correct filename.)*
The application window should now appear, ready for use!
## 🧪 How to Test the Application
1.  **Launch the App:** Start the application as described above. You will see the main window with a list of dummy rooms pre-loaded into the database, all marked as available.
2.  **Make a Booking:**
    * In the "New Booking" form on the left, enter a guest name (e.g., "John Doe") and phone number.
    * Select a room from the "Available Rooms" dropdown.
    * Enter a "Stay Duration" (e.g., 3 days).
    * Click the **"Book Room"** button.
    * *Result:* A success message appears, the guest is added to the "Current Bookings" table on the right, and the selected room is removed from the available list.
3.  **Perform a Check-Out:**
    * Click on the row for "John Doe" in the "Current Bookings" table to select it.
    * Click the **"Check Out Selected Guest"** button.
    * Confirm the action in the pop-up dialog.
    * *Result:* A message appears showing the total calculated bill. The booking is removed from the table, and the room becomes available again in the dropdown list for new bookings.

> **Note to Students:** Before submitting, make sure to:
> 1.  Replace the placeholder screenshot filenames above (`1_empty_dashboard.png`, etc.) with the actual names of your screenshot files stored in the `/screenshots` directory.
> 2.  Update the GitHub clone URL in the "Installation & Setup Steps" section with your own repository's URL.
