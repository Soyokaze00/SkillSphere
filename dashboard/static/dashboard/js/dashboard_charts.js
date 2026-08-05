document.addEventListener("DOMContentLoaded", function () {
  if (typeof lucide !== "undefined") {
    lucide.createIcons();
  }

  // Check if dark mode is active
  function isDarkMode() {
    return document.documentElement.classList.contains("dark");
  }

  // Get chart colors based on theme
  function getChartColors() {
    const dark = isDarkMode();
    return {
      textColor: dark ? "#E5E7EB" : "#6B7280",
      gridColor: dark ? "#374151" : "#E5E7EB",
      axisColor: dark ? "#4B5563" : "#D1D5DB",
    };
  }

  const weeklyEl = document.getElementById("weekly-data");
  const projectEl = document.getElementById("project-data");
  const storageElData = document.getElementById("storage-data");

  if (!weeklyEl || !projectEl) return;

  const weeklyData = JSON.parse(weeklyEl.textContent);
  const projectData = JSON.parse(projectEl.textContent);
  const storageData = JSON.parse(storageElData.textContent);

  const categories = weeklyData.map((i) => i.day);

  const chartData = {
    downloads: weeklyData.map((i) => i.downloads),
    views: weeklyData.map((i) => i.views),
    uploads: weeklyData.map((i) => i.uploads),
  };

  // Store chart instances for later updates
  let activityChartInstance = null;
  let storageChartInstance = null;
  let performanceChartInstance = null;

  function updateChartColors() {
    const colors = getChartColors();
    const isDark = isDarkMode();

    // Update activity chart
    if (
      activityChartInstance &&
      typeof activityChartInstance.updateOptions === "function"
    ) {
      activityChartInstance.updateOptions({
        xaxis: {
          labels: { style: { colors: colors.textColor } },
          axisBorder: { color: colors.gridColor },
          axisTicks: { color: colors.gridColor },
        },
        yaxis: {
          title: {
            text: "Downloads",
            style: { color: colors.textColor },
          },
          labels: {
            style: { colors: colors.textColor },
            formatter: (val) => Math.round(val),
          },
          forceNiceScale: false,
          decimalsInFloat: 0,
          tickAmount: 4,
        },
        grid: {
          borderColor: colors.gridColor,
          strokeDashArray: 4,
        },
        tooltip: {
          theme: isDark ? "dark" : "light",
        },
      });
    }

    // Update storage chart
    if (
      storageChartInstance &&
      typeof storageChartInstance.updateOptions === "function"
    ) {
      storageChartInstance.updateOptions({
        plotOptions: {
          pie: {
            donut: {
              labels: {
                value: {
                  color: isDark ? "#E5E7EB" : "#374151",
                },
                total: {
                  color: isDark ? "#E5E7EB" : "#374151",
                },
              },
            },
          },
        },
        tooltip: {
          theme: isDark ? "dark" : "light",
        },
      });
    }

    // Update performance chart
    if (performanceChartInstance) {
      performanceChartInstance.updateOptions({
        xaxis: {
          labels: { style: { colors: colors.textColor } },
          axisBorder: { color: colors.gridColor },
          axisTicks: { color: colors.gridColor },
        },
        yaxis: {
          min: 0,
          max: 10,
          tickAmount: 10,
          forceNiceScale: false,
          decimalsInFloat: 0,
          labels: {
            style: { colors: colors.textColor },
            formatter: (val) => Math.round(val),
          },
        },
        grid: {
          borderColor: colors.gridColor,
          strokeDashArray: 4,
        },
        legend: {
          labels: { colors: colors.textColor },
        },
        tooltip: {
          theme: isDark ? "dark" : "light",
        },
      });
    }

    // Update storage legend
    updateStorageLegend();
  }

  // Function to update storage legend
  function updateStorageLegend() {
    const images = storageData.images;
    const PDFs = storageData.PDFs;
    const docs = storageData.docs;
    const other = storageData.other;
    const total = images + PDFs + docs + other;
    const isDark = isDarkMode();

    const items = [
      { label: "Images", value: images, color: "#4F46E5" },
      { label: "PDFs", value: PDFs, color: "#7C3AED" },
      { label: "Docs", value: docs, color: "#22C55E" },
      { label: "Other", value: other, color: "#F59E0B" },
    ];

    const legend = document.getElementById("storageLegend");
    if (!legend) return;

    legend.innerHTML = items
      .map((item) => {
        const percent = total ? ((item.value / total) * 100).toFixed(1) : 0;
        return `
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span
              class="w-3 h-3 rounded-full"
              style="background:${item.color}">
            </span>
            <span class="${isDark ? "text-gray-300" : "text-gray-600"}">${item.label}</span>
          </div>
          <span class="font-medium ${isDark ? "text-gray-300" : "text-slate-600"}">
            ${percent}%
          </span>
        </div>
      `;
      })
      .join("");
  }

  const activityEl = document.querySelector("#activityChart");

  if (activityEl && window.ApexCharts) {
    const colors = getChartColors();
    activityChartInstance = new ApexCharts(activityEl, {
      series: [{ name: "Downloads", data: chartData.downloads }],
      chart: {
        type: "area",
        height: 220,
        toolbar: { show: false },
        background: "transparent",
        redrawOnParentResize: true,
        redrawOnWindowResize: true,
      },
      stroke: { curve: "smooth", width: 3 },
      dataLabels: { enabled: false },
      fill: { type: "gradient", gradient: { opacityFrom: 0.3, opacityTo: 0 } },
      colors: ["#4F46E5"],
      xaxis: {
        categories,
        labels: { style: { colors: colors.textColor } },
        axisBorder: { color: colors.gridColor },
        axisTicks: { color: colors.gridColor },
      },
      yaxis: {
        title: {
          text: "Downloads",
          style: { color: colors.textColor },
        },
        labels: {
          style: { colors: colors.textColor },
          formatter: (val) => Math.round(val),
        },
        forceNiceScale: false,
        decimalsInFloat: 0,
        tickAmount: 4,
      },
      grid: {
        borderColor: colors.gridColor,
        strokeDashArray: 4,
      },
      tooltip: {
        theme: isDarkMode() ? "dark" : "light",
      },
    });

    activityChartInstance.render();

    window.changeChart = function (type, el) {
      if (!activityChartInstance) return;
      activityChartInstance.updateSeries([
        { name: type, data: chartData[type] },
      ]);

      document.querySelectorAll(".chart-btn").forEach((btn) => {
        btn.classList.remove(
          "bg-white",
          "text-indigo-600",
          "font-semibold",
          "shadow-sm",
          "dark:bg-gray-800",
          "dark:text-indigo-400",
        );
        btn.classList.add("text-slate-500", "dark:text-gray-400");
      });

      if (el) {
        el.classList.add(
          "bg-white",
          "text-indigo-600",
          "font-semibold",
          "shadow-sm",
          "dark:bg-gray-800",
          "dark:text-indigo-400",
        );
        el.classList.remove("text-slate-500", "dark:text-gray-400");
      }
    };
  }

  const images = storageData.images;
  const PDFs = storageData.PDFs;
  const docs = storageData.docs;
  const other = storageData.other;

  const storageEl = document.querySelector("#storageChart");
  if (storageEl && window.ApexCharts) {
    const colors = getChartColors();
    const isDark = isDarkMode();
    storageChartInstance = new ApexCharts(storageEl, {
      series: [images, PDFs, docs, other],
      chart: {
        type: "donut",
        height: 220,
        background: "transparent",
        redrawOnParentResize: true,
         redrawOnWindowResize: true,
      },
      labels: ["Images", "PDFs", "Docs", "Other"],
      colors: ["#4F46E5", "#7C3AED", "#22C55E", "#F59E0B"],
      legend: {
        show: false,
      },
      dataLabels: {
        enabled: false,
      },
      plotOptions: {
        pie: {
          donut: {
            size: "65%",
            labels: {
              show: true,
              value: {
                color: isDark ? "#E5E7EB" : "#374151",
              },
              total: {
                show: true,
                label: "Total Files",
                color: isDark ? "#E5E7EB" : "#374151",
                formatter: function (w) {
                  return w.globals.seriesTotals.reduce((a, b) => a + b, 0);
                },
              },
            },
          },
        },
      },
      tooltip: {
        theme: isDark ? "dark" : "light",
      },
    });

    storageChartInstance.render();

    updateStorageLegend();
  }

  const perfEl = document.querySelector("#performanceChart");
  if (perfEl && window.ApexCharts) {
    const colors = getChartColors();

    const downloadsArr = projectData.map((x) => x.downloads);
    const likesArr = projectData.map((x) => x.likes);
    const maxValue = Math.max(...downloadsArr, ...likesArr, 0);

    const yMax = Math.ceil((maxValue * 1.1) / 5) * 5 || 5;

    performanceChartInstance = new ApexCharts(perfEl, {
      series: [
        { name: "Downloads", data: downloadsArr },
        { name: "Likes", data: likesArr },
      ],
      chart: {
        type: "bar",
        height: 250,
        width: "100%",
        toolbar: { show: false },
        background: "transparent",
      },
      plotOptions: {
        bar: {
          columnWidth: "20%",
          borderRadius: 4,
        },
      },
      colors: ["#4F46E5", "#7C3AED"],
      dataLabels: { enabled: false },
      xaxis: {
        categories: projectData.map((x) => x.name),
        // title: {
        //   text: "Projects",
        //   style: { color: colors.textColor },
        // },
        labels: { style: { colors: colors.textColor } },
        axisBorder: { color: colors.gridColor },
        axisTicks: { color: colors.gridColor },
      },
      yaxis: {
        min: 0,
        max: yMax,
        tickAmount: 5,
        forceNiceScale: false,
        decimalsInFloat: 0,
        title: {
          text: "Number",
          style: { color: colors.textColor },
        },
        labels: {
          style: { colors: colors.textColor },
          formatter: (value) => Math.round(value),
        },
      },
      grid: {
        borderColor: colors.gridColor,
        strokeDashArray: 4,
      },
      legend: {
        labels: { colors: colors.textColor },
      },
      tooltip: {
        theme: isDarkMode() ? "dark" : "light",
      },
    }).render();
  }
  // Watch for theme changes without reloading
  let themeChangeTimeout = null;
  const observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
      if (mutation.attributeName === "class") {
        // Clear previous timeout
        if (themeChangeTimeout) {
          clearTimeout(themeChangeTimeout);
        }
        // Update colors after a small delay
        themeChangeTimeout = setTimeout(function () {
          updateChartColors();
          themeChangeTimeout = null;
        }, 100);
      }
    });
  });

  observer.observe(document.documentElement, { attributes: true });
});
