<script>
import { Bar, mixins } from 'vue-chartjs'
export default {
    props: ['options'],
    extends: Bar,
    mixins: [mixins.reactiveProp],
    created() {
        this.renderChart(this.chartData, this.options);
    }
}
</script>
