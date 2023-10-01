# **Tutorial: Real-time Bitcoin Price Tracker with Plotting**

In this tutorial, we will guide you through creating a real-time Bitcoin price tracker in Python. This program fetches Bitcoin prices from Binance, stores them in an SQLite database, and plots a real-time price graph. We'll use the `ccxt` library for cryptocurrency data, `matplotlib` for plotting, and `sqlite3` for database management.

## **Prerequisites:**

Before you get started, make sure you have the following prerequisites:

- Python 3.6 or later
- A virtual environment (optional but recommended)
- `ccxt` library
- `matplotlib` library
- `sqlite3` library
- `python3-tk` for GUI backend support

This tutorial was developed and tested on Ubuntu 20.04, but it should work on other systems as well.

You can create a virtual environment, activate it, and install the required Python libraries using `pip` and the necessary system package with `apt`:

```bash
# Create a virtual environment (optional)
python3 -m venv bitcoin-tracker-env

# Activate the virtual environment
source bitcoin-tracker-env/bin/activate

# Install system package for tkinter
sudo apt-get install python3-tk

# Install system package for sqlite3
sudo apt-get install sqlite3

# Install Python packages from requirements.txt
pip install -r requirements.txt
```

## **Steps for Running the Program**

1. **Starting Prefect Server:**

   Before running the program, make sure to start the Prefect server if you haven't already. Use the following command:

   ```bash
   prefect server start
   ```

2. **Executing the Script:**

   - Create a Python script for your Prefect flow. Save the script as `etl-workflow.py`. This script will contain the tasks and flow definition.

   - Copy and paste the code for the tasks and flow from the tutorial into `etl-workflow.py`. The code defines the tasks for fetching, storing, and plotting Bitcoin prices.

   - Save the script.

3. **Running the Program:**

   Open a terminal and navigate to the directory where `etl-workflow.py` is located. Run the script with the following command:

   ```bash
   python3 etl-workflow.py
   ```

4. **Observing Real-time Data:**

   The program will start fetching real-time Bitcoin prices, storing them in the database, and plotting a real-time graph. You can adjust the `cron` schedule in the `bitcoin_info` task to control how often the data is updated.

![Dashboard Prefect](https://lh3.googleusercontent.com/u/2/drive-viewer/AK7aPaDluZWm453udOh_S7_xD38OcSVvM9iksppu88vXR_JO28GRC1-WathlR2tS9toVpmPHOwi06JCNJnWfV9FGJ-lc_rHD=w1848-h976)
![Logs and plot visualization](https://lh3.googleusercontent.com/u/2/drive-viewer/AK7aPaCmwTs4ptktjMDQW2tLz5cDf2dKRwYqJRqv-iBzoLpDKo3RqtFCCJcl5wH5MN7ftL8M0jxeTOG257QuWg0oxafr_BTX=w1848-h976)

6. **Closing Plot Windows:**

   To ensure that the plot windows close before creating new ones, the script uses `plt.close('all')` in the `plot_bitcoin_prices` task.

That's it! You now have a real-time Bitcoin price tracker with dynamic plotting capabilities.

Feel free to customize the program further to suit your needs, such as adjusting the plotting interval or implementing additional features. Happy coding!
