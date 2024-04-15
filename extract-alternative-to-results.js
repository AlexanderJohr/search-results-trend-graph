function addH2ToList() {
    var existingH2Elements = document.querySelectorAll('div[data-testid="app-header"] h2');
    
    var newH2Elements = [];

    existingH2Elements.forEach(function(element) {
        var isInList = false;
        h2List.forEach(function(item) {
            if (item.innerText === element.innerText) {
                isInList = true;
            }
        });

        if (!isInList) {
            newH2Elements.push(element.innerText);
        }
    });

    h2List = h2List.concat(newH2Elements);
}

var h2List = [];
addH2ToList();
JSON.stringify(h2List);
