<template>
    <div>
        <canvas id="pieChart"></canvas>
    </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

export default {
    props: {
        labels: {
            type: Array,
            required: true
        },
        data: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            pieChartData: null
        };
    },
    mounted() {
        const ctx = document.getElementById("pieChart");
        Chart.register(...registerables);
        this.createChart(ctx);
    },
    methods: {
        createChart(ctx) {
            const backgroundColors = this.labels.map(() => this.getRandomColor(0.2));
            const borderColors = backgroundColors.map(color => color.replace('0.2', '1'));

            this.pieChartData = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: this.labels,
                    datasets: [{
                        data: this.data,
                        backgroundColor: backgroundColors,
                        borderColor: borderColors,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        },
        getRandomColor(opacity) {
            const r = Math.floor(Math.random() * 256);
            const g = Math.floor(Math.random() * 256);
            const b = Math.floor(Math.random() * 256);
            return `rgba(${r}, ${g}, ${b}, ${opacity})`;
        },
        updateChartData(labels, data) {
            this.pieChartData.data.labels = labels;
            this.pieChartData.data.datasets[0].data = data;
            this.pieChartData.data.datasets[0].backgroundColor = labels.map(() => this.getRandomColor(0.2));
            this.pieChartData.data.datasets[0].borderColor = this.pieChartData.data.datasets[0].backgroundColor.map(color => color.replace('0.2', '1'));
            this.pieChartData.update();
        }
    }
};
</script>