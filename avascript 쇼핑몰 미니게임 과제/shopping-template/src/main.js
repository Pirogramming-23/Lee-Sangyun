function loadItems() {
    return fetch('data/data.json')
    .then(response => response.json())
    .then(json => json.items);
}

//main
loadItems()
  .then((items) => {
      displayItems(items);
      setEventListeners(items);
  })
  .catch(console.log);