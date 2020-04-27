async function getUserInfo() {
    let accessToken = document.getElementById("access_token").value;
    fetch("https://140.96.170.47:60107/api/userinfo", {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        method: 'GET', 
      }).then(response => response.json())
      .then(data => {
        console.log(data)
        document.getElementById("requestOutput").value = JSON.stringify(data);
      });
    
}

async function checkToken() {
    let accessToken = document.getElementById("access_token").value;
    let data = { accessToken: accessToken };
    console.log(JSON.stringify(data))
    fetch("https://140.96.170.47:60107/checkToken", {
        body : JSON.stringify(data),
        method: 'POST', 
        headers: {
            'content-type': 'application/json'
          },
      }).then(response => response.json())
      .then(data => {
        console.log(data)
        document.getElementById("requestOutput").value = JSON.stringify(data);
      });
}

async function callESPI(api) {
    let accessToken = document.getElementById("access_token").value;
    fetch("http://localhost:9999/espi_tw/1_1/resource/" + api, {
        method: 'GET', 
        headers: {
            "Authorization": "Bearer " + accessToken
          },
      }).then(response => response.text())
      .then(data => {
        console.log(data)
        document.getElementById("requestOutput").value = data;
      });
}

async function downloadMyData(RetailCustomerId) {
  let accessToken = document.getElementById("access_token").value;
  console.log(RetailCustomerId)
  fetch(`http://localhost:9999/RetailCustomer/${RetailCustomerId}/DownloadMyData/UsagePoint` , {
      method: 'GET', 
      headers: {
          "Authorization": "Bearer " + accessToken
        },
    }).then(response => response.text())
    .then(data => {
      console.log(data)
      var file = new Blob([data], {type: "application/atom+xml"});
      saveAs(file, "espi_tw_download.xml");
      document.getElementById("requestOutput").value = data;
    });
}
