const swiper = new Swiper('.swiper', {
    // Optional parameters
    effect: 'cube',
  cubeEffect: {
    slideShadows: false,
  },
    direction: 'horizontal',
    loop: true,
  
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
    },
  
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    }
  });