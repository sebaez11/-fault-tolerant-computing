# **Node.js Server Status Checker Program**

In this guide, we'll walk you through crafting a Python-built program to monitor the status of a Node.js server. The script checks the server process's activity and initiates it if it's down.

## **Prerequisites:**

Before beginning, ensure you have the following prerequisites:

- Python version 3.6 or higher
- Node.js version 14.17.0 or higher
- A virtual environment
- `psutil` library

## **Steps to Run the Program**

1. **Python Script Creation to Manage the Node.js Server**

   The Node.js server performs web scraping on a mobile phone sales page, checking a list of phones. If any phones are in stock, it opens a browser tab playing a song.

   ![Image](https://github.com/Yuberley/Fault-Tolerant-Computing/blob/main/course/8_services_manager/img/2.png)

2. **Crafting the Python Script to Check and Start the Node.js Server**

   Here, the Python script is responsible for assessing the server process's state. It launches the server if it's found to be inactive.

   ```python
   ...

   def check_nodejs_server(server_name):
       for process in psutil.process_iter(attrs=['cmdline']):
           if process.info.get('cmdline') and server_name in ' '.join(process.info['cmdline']):
               return True
       return False

   ...remaining code
   ```

   To test the script:

   ```bash
   python .\process.py .\index.js
   ```

3. **Download and Install the Non-Sucking Service Manager (NSSM).**

   I will use the Chocolatey package manager for the installation, but you can also grab it from its [official website](https://nssm.cc/download).

   ```bash
   choco install nssm
   ```

4. **Initialize NSSM** with the following command:
   
   ```bash
   nssm install service_checker
   ```

   A configuration window will pop up:

   ![Image](https://github.com/Yuberley/Fault-Tolerant-Computing/blob/main/course/8_services_manager/img/1.png)
   
   Populate the fields as follows:
   - Path: Specify the path to the Python interpreter, such as: C:\Python38\python.exe
   - Startup directory: Point to the directory containing `proclocker.py`, like: C:\custom-services
   - Arguments: For intercepting specific applications like Chrome and Firefox: proclocker.py chrome.exe firefox.exe. Since we've specified the directory containing `proclocker.py` in the Startup directory field, there's no need to include the absolute path of the script as the first argument. Instead, the relative path is used: proclocker.py.

* Once the service is set up, initiate it using the console command:

  ```bash
    nssm start service_checker
  ```

5. **Service Management**

   Manage the service as depicted in the following snapshot:

   ![Image](https://github.com/Yuberley/Fault-Tolerant-Computing/blob/main/course/8_services_manager/img/4.png)
