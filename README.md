# LoanApply Project

## Overview

The **LoanApply** project is a loan application system designed to calculate the eligibility of applicants based on their personal, financial, CIBIL, and bank details. The system collects the user's information through forms, processes it, and calculates whether the applicant qualifies for a loan based on various factors such as CIBIL score, debt-to-income ratio, and income levels.

---

## Table of Contents

- [Overview](#overview)
- [Creating Environment](#creating-environment)
- [Installing Dependencies](#installing-dependencies)
- [Setting Up the Project](#setting-up-the-project)
- [Running the Server](#running-the-server)
- [Eligibility Check Logic](#eligibility-check-logic)
- [Features](#features)
- [Troubleshooting](#troubleshooting)
- [Conclusion](#conclusion)
- [License](#license)

---

## Creating Environment

1. **Create a Virtual Environment**:  
   In your terminal, navigate to the project folder and create a virtual environment using the following command:

   ```bash
   python -m venv venv

2. Activate the Virtual Environment
    Activate the virtual environment based on your operating system:
    
    #### For Windows:
    ```bash
    venv\Scripts\activate

    
    #### For MacOS/Linux:
    ```bash
    venv\Scripts\activate
    source venv/bin/activate

## Installing Dependencies

Once the virtual environment is activated, you need to install all the necessary dependencies.

### Install Project Dependencies:
With the virtual environment activated, run the following command to install all the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt

