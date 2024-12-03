let slideIndex = 0;
const slides = document.getElementsByClassName("mySlides");
const dots = document.getElementsByClassName("dot");

function showSlides() {
  // Hide all slides
  for (let i = 0; i < slides.length; i++) {
    slides[i].classList.remove("active");
  }

  // Remove active state from dots
  for (let i = 0; i < dots.length; i++) {
    dots[i].classList.remove("active");
  }

  // Increment the slide index
  slideIndex++;
  if (slideIndex > slides.length) {
    slideIndex = 1;
  }

  // Show the current slide and set active class for the corresponding dot
  slides[slideIndex - 1].classList.add("active");
  dots[slideIndex - 1].classList.add("active");

  // Change slide every 3 seconds
  setTimeout(showSlides, 3000);
}

// Initialize the slideshow
showSlides();
