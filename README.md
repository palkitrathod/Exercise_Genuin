Test Cases that we've performed 

Home page load
"Get App" button visibility
"Become a Creator" button visibility
Login button functionality

Prerequisites
1. Python (version 3.7 or later) is installed on your machine.
2. Install Playwright and its browsers
3. Install Pytest

your-repository/
│
├── config.py            # Configuration file for brands and feature flags
├── test_file.py         # Your test script (contains the test cases)
├── requirements.txt     # List of required dependencies
└── README.md            # This file

To run the file follow the command
- pytet test_brands.py -v -s

To generate the report for the same
1. Intall pytest html -> pip install pytest-html
2. Run the test and generate the report -> pytest --html=report.html
