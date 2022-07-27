var label = document.querySelectorAll('label'),
    itemDiv = document.querySelectorAll('.box-style');

label.forEach(function(checked) {
  checked.addEventListener("click", function(event) {

    itemDiv.forEach(function(item){
      item.classList.remove('active');
    });

    var targetDiv = document.querySelector(this.getAttribute('data-target'));

    targetDiv.classList.add('active');
  });
});