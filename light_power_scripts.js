var formdata = new FormData();

var requestOptions = {
  method: 'GET',
  body: formdata,
  redirect: 'follow'
};

fetch('http://10.120.51.145:2630/api/light/state/off', requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));




//---------------------------------For switching light ON---------------------------------

var formdata = new FormData();

var requestOptions = {
  method: 'GET',
  body: formdata,
  redirect: 'follow'
};

fetch('http://10.120.51.145:2630/api/light/state/on', requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
