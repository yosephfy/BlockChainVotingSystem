# Blockchain Voting System

The Blockchain Voting System is a secure and transparent platform for managing elections using blockchain technology. This project allows administrators to oversee election processes, voters to cast their votes, and all stakeholders to view the election results in real time. By leveraging blockchain, the system ensures that all votes are immutable and verifiable.

---

## **Features**

### **Admin Features**
- **Start and End Election**: Control the election timeline.
- **Generate Random Votes**: Add simulated votes for debugging and testing.
- **View Election Results**: Real-time visualization of election data in a pie chart.
- **Blockchain Audit**: Verify the integrity of the blockchain.
- **Reset Election**: Clear all votes and reset election status.
- **Remove All Voters**: Wipe the voter database for a clean start.

### **Voter Features**
- **Register**: Create a secure account with a unique voter ID.
- **Login**: Authenticate to access the voting platform.
- **Cast Vote**: Securely vote for a candidate.
- **View Results**: Visualize election outcomes in a detailed chart.

---

## **Tech Stack**

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Blockchain**: Custom implementation using Python
- **Charting Library**: Chart.js

---

## **Setup and Installation**

### **Prerequisites**
- Python 3.8 or higher
- Git

### **Steps to Run the Project**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/BlockchainVotingSystem.git
   cd BlockchainVotingSystem
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**:
   ```bash
   flask init-db
   ```

5. **Run the Application**:
   ```bash
   flask run
   ```
   The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## **How to Use**

### **Admin Instructions**
1. Navigate to the admin login page (`/admin-login`).
2. Use default credentials:
   - **Username**: `admin`
   - **Password**: `admin123`
3. Access the admin dashboard to manage elections and view results.

### **Voter Instructions**
1. Register as a voter on the registration page (`/register`).
2. Log in to the voter dashboard (`/login`).
3. Cast your vote for a candidate of your choice.
4. View election results on the results page.

---

## **Project Structure**

```
BlockchainVotingSystem/
├── app.py              # Main application file
├── database.py         # Database models and utility functions
├── voting_system.py    # Core blockchain and voting logic
├── templates/          # HTML templates
├── static/             # Static files (CSS, JavaScript)
│   ├── style.css       # Stylesheet
│   ├── admin_dashboard.js  # Admin dashboard logic
│   ├── voter.js        # Voter dashboard logic
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
```

---

## **Testing**

1. **Generate Random Votes**:
   - Use the admin dashboard to generate random votes for candidates.

2. **Blockchain Integrity**:
   - Verify the blockchain using the audit functionality.

3. **Edge Cases**:
   - Test scenarios like duplicate voter registration and invalid votes.

---

## **Future Improvements**

- Migrate to a more robust database (e.g., PostgreSQL) for scalability.
- Add support for multi-election management.
- Implement Two-Factor Authentication (2FA) for enhanced security.
- Improve the UI for mobile responsiveness.

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.

---

## **Contributors**
- **Yoseph Tezera**

For questions or contributions, feel free to open an issue or pull request on [GitHub](https://github.com/yosephfy/BlockchainVotingSystem).
