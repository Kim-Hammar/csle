import React from 'react'
import './FiveGDURLCSDULatencyChart.css'
import {
  CartesianGrid,
  Label,
  Legend, Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'


/**
 * Component containing a plot showing the average SDU latency of the DU
 */
const FiveGDURLCSDULatencyChart = React.memo((props) => {
    const margin = {
      top: 10,
      right: 30,
      left: 15,
      bottom: 25
    }

    if (props.stats !== undefined && props.stats.length > 0) {
      const data = props.stats.map((five_g_du_rlc_metrics, index) => {
        const totalLatencyUs = Number(five_g_du_rlc_metrics.tx_sum_sdu_latency_us) || 0;
        const count = Number(five_g_du_rlc_metrics.rx_num_sdus) || 0;
        return {
          't': (index + 1),
          'Service Data Unit (SDU)': count > 0 ? (totalLatencyUs / count) : 0
        }
      })
      var domain = [0, Math.max(1, data.length)]
      return (
        <div style={{ height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={data}
              margin={margin}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="t" type="number" domain={domain}>
                <Label value="Time-step t" offset={-20} position="insideBottom" className="largeFont" />
              </XAxis>
              <YAxis type="number">
                <Label angle={270} value="Processing latency (ms)" offset={0} position="insideLeft"
                       className="largeFont"
                       dy={50} />
              </YAxis>
              <Tooltip />
              <Legend verticalAlign="top" wrapperStyle={{ position: 'relative', fontSize: '15px' }}
                      className="largeFont" />
              <Line isAnimationActive={props.animation} animation={props.animation} type="monotone"
                    dataKey="Service Data Unit (SDU)"
                    stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                    animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )

    } else {
      return (
        <div></div>
      )
    }
  }
)
FiveGDURLCSDULatencyChart.displayName = 'FiveGDURLCSDULatencyChart'
FiveGDURLCSDULatencyChart.propTypes = {}
FiveGDURLCSDULatencyChart.defaultProps = {}
export default FiveGDURLCSDULatencyChart
