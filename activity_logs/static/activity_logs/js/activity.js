function activityPage() {
  const serverData = JSON.parse(document.getElementById('activity-data').textContent);

  return {
    view: 'timeline',
    typeFilter: 'All',
    activeChartKey: 'project',
    chart: null,

    logs: serverData.logs,
    weekly: serverData.weekly,
    counts: serverData.summary,
    weekRange: serverData.week_range,

    typeConfig: {
      login:   { color: '#7C3AED', bg: '#F5F3FF', label: 'Login',   icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3"/></svg>' },
      project: { color: '#4F46E5', bg: '#EEF2FF', label: 'Project', icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V7z"/></svg>' },
      social:  { color: '#F59E0B', bg: '#FFFBEB', label: 'Social',  icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>' },
      file:    { color: '#059669', bg: '#ECFDF5', label: 'File',    icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-6 4h6m2 5H7a2 2 0 01-2-2V4a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V20a2 2 0 01-2 2z"/></svg>' },
      account: { color: '#0EA5E9', bg: '#F0F9FF', label: 'Account', icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>' },
      other:   { color: '#6B7280', bg: '#F3F4F6', label: 'Other',   icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>' },
    },

    chartKeys: [
      { key: 'login', color: '#7C3AED', label: 'Logins' },
      { key: 'project', color: '#4F46E5', label: 'Projects' },
      { key: 'social', color: '#F59E0B', label: 'Social' },
      { key: 'account', color: '#0EA5E9', label: 'Account' },
    ],

    get summary() {
      return [
        { label: 'Logins', value: this.counts.login, color: '#7C3AED', bg: '#F5F3FF', icon: this.typeConfig.login.icon },
        { label: 'Project Actions', value: this.counts.project, color: '#4F46E5', bg: '#EEF2FF', icon: this.typeConfig.project.icon },
        { label: 'Social Actions', value: this.counts.social, color: '#F59E0B', bg: '#FFFBEB', icon: this.typeConfig.social.icon },
        { label: 'Account Actions', value: this.counts.account, color: '#0EA5E9', bg: '#F0F9FF', icon: this.typeConfig.account.icon },
      ];
    },

    filtered() {
      return this.logs.filter(l => this.typeFilter === 'All' || l.type === this.typeFilter.toLowerCase());
    },

    init() {
      this.$nextTick(() => {
        setTimeout(() => this.renderChart(), 0);
      });
    },

    setActiveChart(key) {
      this.activeChartKey = key;
      if (this.chart) {
        const active = this.chartKeys.find(k => k.key === key);
        this.chart.updateOptions({
          colors: [active.color],
        });
        this.chart.updateSeries([{
          name: active.label,
          data: this.weekly.map(w => w[key]),
        }]);
      } else {
        this.renderChart();
      }
    },

    renderChart() {
      const el = document.getElementById('activityChart');
      if (!el || !el.isConnected || !window.ApexCharts) return;

      if (this.chart) {
        try {
          this.chart.destroy();
        } catch (err) {
          console.warn('Chart destroy failed (ignoring, will rebuild):', err);
        }
        this.chart = null;
      }

      const active = this.chartKeys.find(k => k.key === this.activeChartKey);

      try {
        this.chart = new ApexCharts(el, {
          series: [{
            name: active.label,
            data: this.weekly.map(w => w[this.activeChartKey]),
          }],
          chart: {
            type: 'area',
            height: 220,
            toolbar: { show: false },
          },
          stroke: { curve: 'smooth', width: 3 },
          dataLabels: { enabled: false },
          fill: {
            type: 'gradient',
            gradient: { opacityFrom: 0.3, opacityTo: 0 },
          },
          colors: [active.color],
          xaxis: {
            categories: this.weekly.map(w => w.day),
          },
        });
        this.chart.render();
      } catch (err) {
        console.error('ApexCharts failed to initialize (chart will not render):', err);
        this.chart = null;
      }
    },
  };
}