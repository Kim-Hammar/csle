import React from 'react'
import './FiveGDULowDecodingLatencyChart.css'
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
 * Component containing a plot showing the average decoding latency (us) over time
 */
const FiveGDULowDecodingLatencyChart = React.memo((props) => {
    const margin = {
      top: 10,
      right: 30,
      left: 15,
      bottom: 25
    }

    if (props.stats !== undefined && props.stats !== null && props.stats.length > 0) {
      const data = props.stats.map((five_g_du_low_metrics, index) => {
        return {
          't': (index + 1),
          'Channel estimation latency': parseFloat(five_g_du_low_metrics.ul_ch_est_latency_us),
          'LDPC decoding latency': parseFloat(five_g_du_low_metrics.ul_ldpc_dec_latency_us)
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
                <Label angle={270} value="Processing latency (us)" offset={0} position="insideLeft"
                       className="largeFont"
                       dy={50} />
              </YAxis>
              <Tooltip />
              <Legend verticalAlign="top" wrapperStyle={{ position: 'relative', fontSize: '15px' }}
                      className="largeFont" />
              <Line isAnimationActive={props.animation} animation={props.animation} type="monotone"
                    dataKey="Channel estimation latency"
                    stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                    animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)} />
              <Line animation={props.animation} type="monotone" dataKey="LDPC decoding latency"
                    stroke="#8b0000" animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)}
                    isAnimationActive={props.animation} />
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
FiveGDULowDecodingLatencyChart.displayName = 'FiveGDULowDecodingLatencyChart'
FiveGDULowDecodingLatencyChart.propTypes = {}
FiveGDULowDecodingLatencyChart.defaultProps = {}
export default FiveGDULowDecodingLatencyChart
