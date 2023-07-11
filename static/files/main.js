fetch('/get_token')
      .then(response => response.json())
      .then(data => {
        const token = data.token;
        fetch('/employees', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
          .then(response => response.json())
          .then(data => {
            const tableBody = document.getElementById('tableBody');
            data.forEach(employee => {
              const row = document.createElement('tr');
              row.innerHTML = `
                <td>${employee.name}</td>
                <td>${employee.organization}</td>
                <td>${employee.skill}</td>
              `;
              tableBody.appendChild(row);
            });
          })
          .catch(error => console.error(error));
      })
      .catch(error => console.error(error));