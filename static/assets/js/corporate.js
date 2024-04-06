const showBtn = document.querySelector(".btn-bars"),
  closeBtn = document.querySelector(".btn-close"),
  navMenu = document.querySelector(".navbar-collapse");
showBtn.addEventListener("click", () => {
  navMenu.classList.add("showMenu");
});
closeBtn.addEventListener("click", () => {
  navMenu.classList.remove("showMenu");
});

const faqItems = document.querySelectorAll(".faq-item");

faqItems.forEach((item) => {
  const question = item.querySelector(".faq-question");

  question.addEventListener("click", () => {
    item.classList.toggle("active");
  });
});

// form code
let currentStep = 1;
const totalSteps = 3;

// Show initial step on page load
document.getElementById("step1").style.display = "block";

function nextStep() {
  const currentSection = document.getElementById(`step${currentStep}`);
  if (currentStep < totalSteps) {
    currentSection.style.display = "none";
    currentStep++;
    document.getElementById(`step${currentStep}`).style.display = "block";

    if (currentStep === totalSteps) {
      document.getElementById("submitBtn").style.display = "block";
      document.getElementById("nextBtn").style.display = "none";
    }
  }
}

// slider code

let slideIndex = 0;

function showSlides() {
  const slides = document.querySelectorAll(".slide");
  if (slideIndex >= slides.length) {
    slideIndex = 0;
  } else if (slideIndex < 0) {
    slideIndex = slides.length - 1;
  }

  for (let i = 0; i < slides.length; i++) {
    slides[i].classList.remove("active");
  }

  slides[slideIndex].classList.add("active");
}

function changeSlide(n) {
  slideIndex += n;
  showSlides();
}

setInterval(() => {
  slideIndex++;
  showSlides();
}, 3000);

showSlides();

gsap.from(".navbar", {
  y: -50,
  duration: 1,
  delay: 0.5,
  opacity: 0,
});

gsap.from(".corporate-section, corporate-info", {
  opacity: 0,
  duration: 1,
  delay: 1,
  y: 50,
});

gsap.from(".footer-section, .footer", {
  duration: 1,
  delay: 1,
  scale: 1,
  y: 100,
  overflow: "hidden",
  opacity: 0,
  stagger: 0.5,
  scrollTrigger: {
    trigger: ".footer-section, .footer",
    scroll: "body",
    start: "top 85%",
    end: " bottom 15%",
    scrub: 5,
  },
});