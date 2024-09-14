function setContainerHeight() {
  var otherElementsHeight = 0;
  var otherElements = document.querySelectorAll('.dinamic-check');
  
  otherElements.forEach(function(element) {
    var elementStyles = window.getComputedStyle(element);
    var marginTop = parseFloat(elementStyles.marginTop);
    var marginBottom = parseFloat(elementStyles.marginBottom);
    var elementHeight = element.offsetHeight + marginTop + marginBottom;
    
    otherElementsHeight += elementHeight;
  });
  
  var windowHeight = window.innerHeight;
  var containerHeight = windowHeight - otherElementsHeight;
  
  
  document.getElementById('dinamic-height').style.height = containerHeight + 'px';
}

// Вызываем функцию при загрузке страницы и при изменении размера окна
window.addEventListener('load', setContainerHeight);
window.addEventListener('resize', setContainerHeight);