// Aura Estates // Quiet Luxury & Financial Engineering
document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const ambientCanvas = document.getElementById('ambientCanvas');
  const resTabs = document.querySelectorAll('.residence-tabs .tab-btn');
  const resTitle = document.getElementById('resTitle');
  const resPrice = document.getElementById('resPrice');
  const resSqm = document.getElementById('resSqm');
  const resTerrace = document.getElementById('resTerrace');
  const resFloor = document.getElementById('resFloor');
  const resView = document.getElementById('resView');
  const resStatus = document.getElementById('resStatus');
  const hoverRoomName = document.getElementById('hoverRoomName');
  const hoverRoomSqm = document.getElementById('hoverRoomSqm');
  const roomZones = document.querySelectorAll('.room-zone');
  const btnRequestPdf = document.getElementById('btnRequestPdf');

  const viewBtns = document.querySelectorAll('.view-filter-buttons .view-btn');
  const panoramicVisual = document.getElementById('panoramicVisual');
  const viewBadge = document.getElementById('viewBadge');

  const rngPrice = document.getElementById('rngPrice');
  const rngDownPct = document.getElementById('rngDownPct');
  const rngTerm = document.getElementById('rngTerm');
  const rngRate = document.getElementById('rngRate');
  const dispPrice = document.getElementById('dispPrice');
  const dispDownPct = document.getElementById('dispDownPct');
  const dispTerm = document.getElementById('dispTerm');
  const dispRate = document.getElementById('dispRate');
  const outMonthly = document.getElementById('outMonthly');
  const outTotalInterest = document.getElementById('outTotalInterest');
  const outCapRate = document.getElementById('outCapRate');

  const tourModal = document.getElementById('tourModal');
  const btnOpenTourModal = document.getElementById('btnOpenTourModal');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const btnBookFromCalc = document.getElementById('btnBookFromCalc');
  const tourForm = document.getElementById('tourForm');

  // Ambient Canvas Liquid Background
  function initAmbientCanvas() {
    ambientCanvas.width = window.innerWidth;
    ambientCanvas.height = window.innerHeight;
    const ctx = ambientCanvas.getContext('2d');
    let t = 0;

    function renderWaves() {
      t += 0.004;
      ctx.clearRect(0, 0, ambientCanvas.width, ambientCanvas.height);

      const grad = ctx.createRadialGradient(
        ambientCanvas.width * 0.5 + Math.sin(t) * 150,
        ambientCanvas.height * 0.4 + Math.cos(t) * 100,
        100,
        ambientCanvas.width * 0.5,
        ambientCanvas.height * 0.5,
        ambientCanvas.width * 0.8
      );
      grad.addColorStop(0, 'rgba(212, 175, 55, 0.06)');
      grad.addColorStop(0.5, 'rgba(14, 18, 26, 0.4)');
      grad.addColorStop(1, 'rgba(10, 11, 13, 0.95)');

      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, ambientCanvas.width, ambientCanvas.height);
      requestAnimationFrame(renderWaves);
    }
    renderWaves();
  }
  initAmbientCanvas();

  // Residences Database
  const residences = {
    penthouse: {
      title: "Penthouse Sky Villa",
      price: "$12,500,000",
      numericPrice: 12500000,
      sqm: "480 м²",
      terrace: "110 м²",
      floor: "48–49 (Пентхаус)",
      view: "180° Панорама океана",
      status: "Доступно к сделке",
      statusClass: "text-avail"
    },
    horizon: {
      title: "Horizon Residence",
      price: "$7,800,000",
      numericPrice: 7800000,
      sqm: "310 м²",
      terrace: "65 м²",
      floor: "34 (Угловая секция)",
      view: "Закатный скайлайн",
      status: "Забронировано",
      statusClass: "text-muted"
    },
    duplex: {
      title: "Royal Duplex",
      price: "$9,200,000",
      numericPrice: 9200000,
      sqm: "395 м²",
      terrace: "85 м²",
      floor: "22–23 (Двухуровневый)",
      view: "Альпийские горы и залив",
      status: "Доступно к сделке",
      statusClass: "text-avail"
    },
    garden: {
      title: "Garden Suite",
      price: "$5,400,000",
      numericPrice: 5400000,
      sqm: "240 м²",
      terrace: "40 м² частный сад",
      floor: "1 (Собственный патио)",
      view: "Центральный парк",
      status: "Продано",
      statusClass: "text-muted"
    }
  };

  // Residence Tab Switcher
  resTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      resTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const key = tab.getAttribute('data-res');
      const r = residences[key];
      if (!r) return;

      resTitle.textContent = r.title;
      resPrice.textContent = r.price;
      resSqm.textContent = r.sqm;
      resTerrace.textContent = r.terrace;
      resFloor.textContent = r.floor;
      resView.textContent = r.view;
      resStatus.textContent = r.status;
      resStatus.className = r.statusClass;

      // Update Calculator Price
      rngPrice.value = r.numericPrice;
      updateCalculator();
    });
  });

  // Room Zone Hover Detection
  roomZones.forEach(zone => {
    zone.addEventListener('mouseenter', () => {
      hoverRoomName.textContent = zone.getAttribute('data-name');
      hoverRoomSqm.textContent = zone.getAttribute('data-sqm');
    });
    zone.addEventListener('mouseleave', () => {
      hoverRoomName.textContent = 'Наведите на план';
      hoverRoomSqm.textContent = '--';
    });
  });

  // Panoramic Views Switcher
  const viewThemes = {
    ocean: {
      bg: "linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.7)), radial-gradient(circle at 50% 40%, #0369A1, #082F49, #020617)",
      badge: "OCEAN HORIZON VIEW // RESIDENCE 4801"
    },
    skyline: {
      bg: "linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.7)), radial-gradient(circle at 60% 50%, #C2410C, #7C2D12, #0F172A)",
      badge: "SUNSET SKYLINE VIEW // RESIDENCE 3402"
    },
    mountains: {
      bg: "linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.7)), radial-gradient(circle at 40% 30%, #334155, #1E293B, #020617)",
      badge: "ALPINE PEAKS VIEW // RESIDENCE 2201"
    },
    park: {
      bg: "linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.7)), radial-gradient(circle at 50% 50%, #15803D, #14532D, #052E16)",
      badge: "CENTRAL PARK VIEW // RESIDENCE 0104"
    }
  };

  viewBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      viewBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const v = btn.getAttribute('data-view');
      const conf = viewThemes[v];
      if (conf) {
        panoramicVisual.style.background = conf.bg;
        viewBadge.textContent = conf.badge;
      }
    });
  });
  panoramicVisual.style.background = viewThemes.ocean.bg;

  // Mortgage & Financial Calculator
  function formatUSD(num) {
    return '$' + Math.round(num).toLocaleString('en-US');
  }

  function updateCalculator() {
    const price = parseFloat(rngPrice.value);
    const downPct = parseFloat(rngDownPct.value);
    const termYears = parseFloat(rngTerm.value);
    const annualRate = parseFloat(rngRate.value);

    const downPayment = price * (downPct / 100);
    const loanPrincipal = price - downPayment;
    const monthlyRate = (annualRate / 100) / 12;
    const numPayments = termYears * 12;

    // Monthly Amortization
    let monthly = 0;
    if (monthlyRate > 0) {
      monthly = loanPrincipal * (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / (Math.pow(1 + monthlyRate, numPayments) - 1);
    } else {
      monthly = loanPrincipal / numPayments;
    }

    const totalPaid = monthly * numPayments;
    const totalInterest = Math.max(0, totalPaid - loanPrincipal);
    const capRate = 6.8; // 6.8% Prime Real Estate Yield
    const annualRent = price * (capRate / 100);

    dispPrice.textContent = formatUSD(price);
    dispDownPct.textContent = `${downPct}% (${formatUSD(downPayment)})`;
    dispTerm.textContent = `${termYears} лет`;
    dispRate.textContent = `${annualRate.toFixed(2)}%`;

    outMonthly.textContent = `${formatUSD(monthly)} / мес`;
    outTotalInterest.textContent = formatUSD(totalInterest);
    outCapRate.textContent = `${capRate}% годовых (${formatUSD(annualRent)} / год)`;
  }

  [rngPrice, rngDownPct, rngTerm, rngRate].forEach(slider => {
    slider.addEventListener('input', updateCalculator);
  });
  updateCalculator();

  // Booking Modal
  btnOpenTourModal.addEventListener('click', () => tourModal.classList.remove('hidden'));
  btnBookFromCalc.addEventListener('click', () => tourModal.classList.remove('hidden'));
  btnCloseModal.addEventListener('click', () => tourModal.classList.add('hidden'));

  tourForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('custName').value;
    const phone = document.getElementById('custPhone').value;
    const residence = document.getElementById('custRes').value;

    try {
      const resp = await fetch('/api/showing/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, phone, residence })
      });
      if (resp.ok) {
        alert('Благодарим Вас! Персональный консьерж свяжется с Вами в течение 15 минут.');
        tourModal.classList.add('hidden');
        tourForm.reset();
      } else {
        alert('Заявка принята, ожидайте подтверждения консьержа.');
        tourModal.classList.add('hidden');
      }
    } catch {
      alert('Заявка принята! Консьерж свяжется с Вами.');
      tourModal.classList.add('hidden');
    }
  });

  // PDF Brochure Trigger
  btnRequestPdf.addEventListener('click', () => {
    window.open('/api/brochure/download?residence=' + resTitle.textContent, '_blank');
  });
});
