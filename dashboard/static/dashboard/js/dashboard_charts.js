
document.addEventListener("DOMContentLoaded", function () {
 
  if (typeof lucide !== "undefined") {
    lucide.createIcons();
  }

  /* ---------------- CHART.JS ---------------- */

  const lineEl = document.getElementById("lineChart");
  if (lineEl) {
    new Chart(lineEl, {
      type: "line",
      data: {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [
          {
            label: "Downloads",
            data: [18, 24, 31, 42, 38, 29, 35],
            borderColor: "#4F46E5",
            tension: 0.4,
          },
          {
            label: "Views",
            data: [45, 62, 58, 87, 94, 71, 83],
            borderColor: "#7C3AED",
            tension: 0.4,
          },
        ],
      },
    });
  }

  const pieEl = document.getElementById("pieChart");
  if (pieEl) {
    new Chart(pieEl, {
      type: "doughnut",
      data: {
        labels: ["Images", "Videos", "Docs", "Other"],
        datasets: [
          {
            data: [38, 22, 18, 22],
            backgroundColor: ["#4F46E5", "#7C3AED", "#22C55E", "#F59E0B"],
          },
        ],
      },
    });
  }

  // const barEl = document.getElementById("barChart");
  // if (barEl) {
  //   new Chart(barEl, {
  //     type: "bar",
  //     data: {
  //       labels: ["Brand", "UI Lib", "Dashboard", "Icon Pack", "Fonts"],
  //       datasets: [
  //         {
  //           label: "Downloads",
  //           data: [412, 387, 298, 521, 164],
  //           backgroundColor: "#4F46E5",
  //         },
  //         {
  //           label: "Stars",
  //           data: [88, 142, 76, 193, 41],
  //           backgroundColor: "#7C3AED",
  //         },
  //       ],
  //     },
      
      
  //   });
  // }


  /* ---------------- APX ---------------- */

  const weeklyEl = document.getElementById("weekly-data");
  const projectEl = document.getElementById("project-data");

  if (!weeklyEl || !projectEl) return;

  const weeklyData = JSON.parse(weeklyEl.textContent);
  const projectData = JSON.parse(projectEl.textContent);

  const categories = weeklyData.map((i) => i.day);

  const chartData = {
    downloads: weeklyData.map((i) => i.downloads),
    views: weeklyData.map((i) => i.views),
    uploads: weeklyData.map((i) => i.uploads),
  };

  const activityEl = document.querySelector("#activityChart");

  if (activityEl && window.ApexCharts) {
    const chart = new ApexCharts(activityEl, {
      series: [{ name: "Downloads", data: chartData.downloads }],
      chart: { type: "area", height: 220, toolbar: { show: false } },
      stroke: { curve: "smooth", width: 3 },
      dataLabels: { enabled: false },
      fill: { type: "gradient", gradient: { opacityFrom: 0.3, opacityTo: 0 } },
      colors: ["#4F46E5"],
      xaxis: { categories },
    });

    chart.render();

    window.changeChart = function (type, el) {
      chart.updateSeries([
        { name: type, data: chartData[type] },
      ]);

      document.querySelectorAll(".chart-btn").forEach((btn) => {
        btn.classList.remove("bg-white", "text-indigo-600", "font-semibold", "shadow-sm");
        btn.classList.add("text-slate-500");
      });

      if (el) {
        el.classList.add("bg-white", "text-indigo-600", "font-semibold", "shadow-sm");
        el.classList.remove("text-slate-500");
      }
    };
  }

  const storageEl = document.querySelector("#storageChart");
  if (storageEl && window.ApexCharts) {
    new ApexCharts(storageEl, {
      series: [38, 22, 18, 22],
      chart: { type: "donut", height: 220 },
      labels: ["Images", "Videos", "Docs", "Other"],
      colors: ["#4F46E5", "#7C3AED", "#22C55E", "#F59E0B"],
      legend: { position: "bottom" },
      plotOptions: {
        pie: { donut: { size: "65%" } },
      },
    }).render();
  }

  const perfEl = document.querySelector("#performanceChart");
  if (perfEl && window.ApexCharts) {
    new ApexCharts(perfEl, {
      series: [
        { name: "Downloads", data: projectData.map((x) => x.downloads) },
        { name: "Stars", data: projectData.map((x) => x.stars) },
      ],
    chart: {
      type: "bar",
      height: 250,
      width: "100%", 
      toolbar: { show: false },
    },
    plotOptions: {
      bar: {
        columnWidth: "20%",
        borderRadius: 4,
      },
    },
 
    colors: ["#4F46E5", "#7C3AED"],
    dataLabels: { enabled: false },      colors: ["#4F46E5", "#7C3AED"],
      xaxis: { categories: projectData.map((x) => x.name) },
      dataLabels: { enabled: false },
      grid: { borderColor: "#e5e7eb", strokeDashArray: 4 },
    }).render();
  }
});