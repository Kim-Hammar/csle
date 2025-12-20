import React from 'react'
import './FiveGDURLCPDULatencyChart.css'
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
 * Component containing a plot showing the average PDU latency of the DU
 */
const FiveGDURLCPDULatencyChart = React.memo((props) => {
    const margin = {
      top: 10,
      right: 30,
      left: 15,
      bottom: 25
    }

    if (props.stats !== undefined && props.stats.length > 0) {
      const data = props.stats.map((five_g_du_rlc_metrics, index) => {
        const totalLatencyNs = Number(five_g_du_rlc_metrics.tx_sum_pdu_latency_ns) || 0;
        const countPdus = Number(five_g_du_rlc_metrics.rx_num_pdus) || 0;
        const avgLatency = countPdus > 0 ? (totalLatencyNs / countPdus) : 0;
        return {
          't': (index + 1),
          'Protocol Data Unit (PDU)': avgLatency
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
                <Label angle={270} value="Processing latency (ns)" offset={0} position="insideLeft"
                       className="largeFont"
                       dy={50} />
              </YAxis>
              <Tooltip />
              <Legend verticalAlign="top" wrapperStyle={{ position: 'relative', fontSize: '15px' }}
                      className="largeFont" />
              <Line isAnimationActive={props.animation} animation={props.animation} type="monotone"
                    dataKey="Protocol Data Unit (PDU)"
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
FiveGDURLCPDULatencyChart.displayName = 'FiveGDURLCPDULatencyChart'
FiveGDURLCPDULatencyChart.propTypes = {}
FiveGDURLCPDULatencyChart.defaultProps = {}
export default FiveGDURLCPDULatencyChart
