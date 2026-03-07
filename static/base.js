// 플로트 버튼: 스크롤이 일정 이상 내려갔을 때만 표시
(function () {
  const btn = document.getElementById("floatBtn");
  if (!btn) return;

  // 초기 숨김
  btn.style.opacity = "0";
  btn.style.pointerEvents = "none";
  btn.style.transition = "opacity 0.3s";

  window.addEventListener("scroll", function () {
    if (window.scrollY > 200) {
      btn.style.opacity = "1";
      btn.style.pointerEvents = "auto";
    } else {
      btn.style.opacity = "0";
      btn.style.pointerEvents = "none";
    }
  });
})();