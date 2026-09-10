(function () {
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;
  var cursor = document.getElementById('cursorDot');

  if (fine && cursor) {
    window.addEventListener('mousemove', function (e) {
      cursor.style.transform = 'translate(' + e.clientX + 'px,' + e.clientY + 'px) translate(-50%,-50%)';
    });
    document.querySelectorAll('a, .plate').forEach(function (el) {
      el.addEventListener('mouseenter', function () { cursor.classList.add('hover'); });
      el.addEventListener('mouseleave', function () { cursor.classList.remove('hover'); });
    });
  } else if (cursor) {
    cursor.style.display = 'none';
  }

  var reveals = document.querySelectorAll('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('in-view'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    reveals.forEach(function (el) { io.observe(el); });
  }
})();
