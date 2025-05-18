# NextDoorDeals - Installation Guide

Greetings! 😊

Follow these steps to run **NextDoorDeals** smoothly on **Windows** or **Linux**.

---

## 📋 Prerequisites

Before starting, make sure you have the following installed:

- **Python 3.13.1**  
  Download from the official site:  
  [https://www.python.org/downloads/release/python-3131/](https://www.python.org/downloads/release/python-3131/)

- **GDAL Library (Geospatial Data Abstraction Library)**  
  Required for handling geospatial data in Django.

- **Project api keys**
  Download this [here](https://drive.google.com/file/d/1Aee30O8hpjZgxAftdT--GROXWc7o3fTB/view?usp=sharing):   
### 🔧 GDAL Installation

**Windows**  
- Download binaries from: [https://www.gisinternals.com/release.php](https://www.gisinternals.com/release.php)  
- Choose a release compatible with your Python version (e.g., `release-1930-x64-gdal-3-7-0-mapserver-8-0-0`)  
- Add the `bin` folder from GDAL to your system `PATH`.

**Linux (Debian/Ubuntu)**  
```bash
sudo apt update
sudo apt install gdal-bin libgdal-dev
```

---

## 🚀 Installation Steps

### 1. Download the Project

- Go to the [NextDoorDeals GitHub repository](https://github.com/AmazingJuan/NextDoorDeals).
- Click the green **"Code"** button and select **"Download ZIP"**.
- Extract the contents into a folder (e.g., `NextDoorDeals`).

---

### 2. Set Up the Project Directory

- *(Optional but recommended)* Create a folder named `NDD` on your desktop and move the extracted `NextDoorDeals` folder inside it.
- Navigate to the `NextDoorDeals` folder.
- Copy its full path:

  **Windows**  
  Click the address bar in File Explorer and press `CTRL + C`.

  **Linux**  
  Use `pwd` in the terminal or right-click > **Copy as Path**.

---

### 3. Open the Command Line

Open a terminal and navigate to the project folder:

```bash
cd <PASTED_PATH>
```

Example (Windows):

```bash
cd C:\Users\maria\Desktop\NDD\NextDoorDeals
```

---

### 4. Set Up a Virtual Environment (Recommended)

Create the environment:

```bash
python -m venv venv
```

On Linux:

```bash
python3 -m venv venv
```

Activate the environment:

**Windows**
```bash
.\venv\Scripts\activate
```

**Linux/macOS**
```bash
source venv/bin/activate
```

---

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

If GDAL fails to install, make sure it is correctly installed and added to your system’s PATH.

---

### 6. Configure GDAL and GEOS in Django

In your `settings.py` file, add or update the following variables:

```python
import os

GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH', 'C:/Program Files/GDAL/gdal304.dll')
GEOS_LIBRARY_PATH = os.getenv('GEOS_LIBRARY_PATH', 'C:/Program Files/GDAL/geos_c.dll')
```

**Important (Windows):**  
Locate the folder where you installed or extracted GDAL (e.g., `C:/gdal` or `C:/Program Files/GDAL`). Find the `.dll` files named `gdalXXX.dll` and `geos_c.dll`, and copy their full paths into the variables above.

You can right-click the file, go to **Properties**, and copy the path from there.

For **Linux**:

```python
GDAL_LIBRARY_PATH = '/usr/lib/libgdal.so'
GEOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so'
```

Make sure these paths match the actual locations of `libgdal.so` and `libgeos_c.so` on your system. You can use the `find` command to locate them:

```bash
sudo find /usr -name "libgdal.so"
sudo find /usr -name "libgeos_c.so"
```

Adjust the values in `settings.py` based on the output of these commands.

---
### 7. API keys

Place the `keys.env` file in the root folder of the project.

### 8. Run the Server

```bash
python manage.py runserver
```

On Linux:

```bash
python3 manage.py runserver
```

---

### 9. Open the Web Application

Open your browser and go to:

```
http://localhost:8000/
```

You should now see the **NextDoorDeals** homepage. 🎉

---

## 🧩 Troubleshooting

- Ensure Python 3.13.1 is used in your environment.
- Confirm that GDAL is correctly installed and its path is referenced in both your system and `settings.py`.
- Confirm you placed `keys.env` file in the root folder of the project. 
- Reinstall the virtual environment if dependencies fail to install.

---

Enjoy using **NextDoorDeals**! 🚀
