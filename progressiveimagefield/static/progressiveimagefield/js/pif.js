window.onload = function() {

  let placeholders = document.querySelectorAll('.placeholder');

  for (plh of placeholders) {
    // load small image and show it
  	let small = plh.querySelector('.img-small');
  	let smallImg = new Image();
  	smallImg.src = small.src;
  	smallImg.onload = function () {
  	   small.classList.add('loaded');
  	};

  	// load large image
  	let largeImg = new Image();
  	largeImg.src = plh.dataset.large;
  	largeImg.onload = function () {
  		largeImg.classList.add('loaded');
  	};
  	plh.appendChild(largeImg);
  }

};
