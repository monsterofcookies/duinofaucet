// STAT_URL for the API
const STAT_URL = 'https://server.duinocoin.com/users/(Faucet Username)';

// Function to fetch data from the API and update the tables
async function fetchDataAndUpdateTables() {
    try {
        const response = await fetch(STAT_URL);
        const data = await response.json();
        const transactions = data.result.transactions;
        const sentTransactions = transactions.filter(tx => tx.sender === "(Faucet Username)").slice(0, 20);
        const receivedTransactions = transactions.filter(tx => tx.recipient === "(Faucet Username)").slice(0, 20);
        updateTable('sentBody', sentTransactions);
        updateTable('receivedBody', receivedTransactions);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to update a table
function updateTable(tableId, transactions) {
    const tableBody = document.getElementById(tableId);
    tableBody.innerHTML = ''; // Clear previous entries

    transactions.forEach(tx => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${tx.amount}</td>
            <td>${tx.datetime}</td>
            <td>${tx.sender}</td>
            <td>${tx.recipient}</td>
            <td>${tx.memo}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Sort table columns
function sortTable(tableId, n) {
    const table = document.getElementById(tableId).parentElement;
    let rows, switching, i, x, y, shouldSwitch, dir, switchCount = 0;
    switching = true;
    dir = 'asc'; // Set the sorting direction to ascending

    while (switching) {
        switching = false;
        rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName('TD')[n];
            y = rows[i + 1].getElementsByTagName('TD')[n];

            if (dir == 'asc') {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == 'desc') {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
        }

        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchCount++;
        } else {
            if (switchCount == 0 && dir == 'asc') {
                dir = 'desc';
                switching = true;
            }
        }
    }
}

// Run the fetchDataAndUpdateTables function when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', fetchDataAndUpdateTables);
