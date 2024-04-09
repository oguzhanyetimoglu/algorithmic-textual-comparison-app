<template>
	<div>
		<canvas ref="scatterChart"></canvas>
	</div>
</template>

<script>
import { Chart, ScatterController, LinearScale, PointElement, Title, Tooltip } from 'chart.js';

Chart.register(ScatterController, LinearScale, PointElement, Title, Tooltip);

export default {
	props: {
		labels: {
			type: Array,
			required: true,
		},
	},
	data() {
		return {
			chart: null,
		};
	},
	mounted() {
		this.createChart();
	},
	methods: {
		createChart() {
			const datasets = this.labels.map((label) => ({
				label: `Label ${label.label}`,
				data: label.data,
				backgroundColor: this.getRandomColor(),
				pointRadius: 5,
			}));
			if (this.$refs.scatterChart) {
				const ctx = this.$refs.scatterChart.getContext('2d');
				datasets.sort((a, b) => a.label.localeCompare(b.label));
				this.chart = new Chart(ctx, {
					type: 'scatter',
					data: {
						datasets,
					},
					options: {
						scales: {
							x: {
								type: 'linear',
								position: 'bottom',
							},
						},
						plugins: {
							legend: {
								display: true,
							},
							tooltip: {
								callbacks: {
									label: function (context) {
										var label = context.dataset.label || '';

										if (label) {
											label += ': ';
										}
										if (context.parsed.x !== undefined && context.parsed.y !== undefined) {
											label += `(${context.parsed.x.toFixed(2)}, ${context.parsed.y.toFixed(2)})`;
										}
										return label;
									},
									afterLabel: function (context) {
										var label = '';
										if (context.raw.company !== undefined) {
											label += `${context.raw.company}`;
										}
										if (context.raw.year !== undefined) {
											label += ` - ${context.raw.year.substring(0, 4)}`;
										}
										return label;
									}
								}
							}
						}
					},
				});
			}
		},
		getRandomColor() {
			const letters = '0123456789ABCDEF';
			let color = '#';
			for (let i = 0; i < 6; i++) {
				color += letters[Math.floor(Math.random() * 16)];
			}
			return color;
		},
	},
	watch: {
		labels: {
			immediate: true,
			handler() {
				this.$nextTick(() => {
					this.createChart();
				});
			},
		},
	},
};
</script>