async function fetchEnvironmentVariables() {
  try {
    const envResponse = await fetch('/get_environment_variables');
    if (!envResponse.ok) {
      throw new Error('Failed to fetch environment variables');
    }
    const envData = await envResponse.json();
    return envData;
  } catch (error) {
    console.error(error);
    return null;
  }
}

async function fetchAndStoreToken() {
  try {
    const envData = await fetchEnvironmentVariables();
    if (!envData) {
      throw new Error('Failed to fetch environment variables');
    }

    const tokenResponse = await fetch('/generate-token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: envData.username,
        password: envData.password
      })
    });

    if (!tokenResponse.ok) {
      throw new Error('Failed to generate token');
    }

    const tokenData = await tokenResponse.json();
    const token = tokenData.token;

    localStorage.setItem('token', token);

    fetchEmployeeData(token);
  } catch (error) {
    console.error(error);
  }
}

async function fetchEmployeeData(token) {
  try {
    const employeesResponse = await fetch('/employees', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!employeesResponse.ok) {
      throw new Error('Failed to fetch employee data');
    }

    const employeesData = await employeesResponse.json();
    const tableBody = document.getElementById('tableBody');

    employeesData.forEach(employee => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${employee.name}</td>
        <td>${employee.organization}</td>
        <td>${employee.role}</td>
      `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    console.error(error);
  }
}

fetchAndStoreToken();