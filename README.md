# NextDoorDeals - Installation Guide

Greetings! 😊

Follow these steps to run **NextDoorDeals** smoothly on **Windows** or **Linux**.

## Prerequisites

Before starting, ensure you have the following installed on your system:

- **Python 3.10 or higher**  
  If not, download and install it from [here](https://www.python.org/downloads/).

## Installation Steps

1. **Download the Project**
   - Go to the [NextDoorDeals GitHub repository](https://github.com/AmazingJuan/NextDoorDeals).
   - Click the green **"Code"** button.
   - Select **"Download ZIP"** and wait for the download to finish.
   - Locate the downloaded `.zip` file in your downloads folder.
   - Extract the contents of the ZIP into a folder (e.g., `NextDoorDeals`).

2. **Set Up the Project Directory**
   - (Optional but recommended) Create an empty folder named `NDD` on your desktop and move the extracted `NextDoorDeals` folder inside it.
   - Navigate to the `NextDoorDeals` folder.
   - Copy the full path of the folder:
     - **Windows**: Click the address bar in File Explorer to highlight the path, then press `CTRL + C` to copy.
     - **Linux**: Right-click inside the folder and select **"Copy as Path"** (or use `pwd` in a terminal inside the folder).

3. **Open the Command Line**
   - Open the terminal:
     - **Windows**: Search for **"CMD"** in the start menu and open it.
     - **Linux**: Open the **Terminal**.
   - Type the following command and paste the copied path:
     ```sh
     cd <PASTED_PATH>
     ```
     Example:
     ```sh
     cd C:\Users\maria\Desktop\NDD\NextDoorDeals
     ```
     Then press **Enter**.

4. **Set Up a Virtual Environment (Recommended)**
   To keep dependencies isolated, create a virtual environment before installing the requirements:
   - Run the following command:
     ```sh
     python -m venv venv
     ```
     (For Linux, use `python3` instead of `python`)
   - Activate the virtual environment:
     - **Windows**:
       ```sh
       .\venv\Scripts\activate
       ```
     - **Linux/macOS**:
       ```sh
       source venv/bin/activate
       ```

5. **Install Dependencies**
   - Run the following command to install the required libraries:
     ```sh
     pip install -r requirements.txt
     ```

6. **Run the Server**
   - Start the Django development server:
     ```sh
     python manage.py runserver
     ```
     (For Linux, use `python3 manage.py runserver`)

7. **Open the Web Application**
   - Open your favorite browser and go to:
     ```
     http://localhost:8000/
     ```
   - If everything went well, you should see the **NextDoorDeals** homepage. Enjoy! 🚀
