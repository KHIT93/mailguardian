<script>
import { Pie, mixins } from 'vue-chartjs'
export default {
    props: ['options'],
    extends: Pie,
    mixins: [mixins.reactiveProp],
    created() {
        this.renderChart(this.chartData, this.options);
    }
}
</script>
