<script>
import { Line, mixins } from 'vue-chartjs'
export default {
    props: ['options'],
    extends: Line,
    mixins: [mixins.reactiveProp],
    created() {
        this.renderChart(this.chartData, this.options);
    }
}
</script>
